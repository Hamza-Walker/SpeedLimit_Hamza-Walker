
import datetime
import numpy as np
import joblib
import os
try:
    from tensorflow.keras.models import load_model
except ImportError:
    print("Warning: TensorFlow not installed. NN features will be disabled.")
    load_model = None

from src.llm_integration import get_simulated_aqi, get_llm_speed_reduction_recommendation

# Load model and scaler
MODEL_PATH = 'models/nn_model.keras'
SCALER_PATH = 'models/scaler.pkl'

nn_model = None
scaler = None
mean_values = None

try:
    if load_model:
        if os.path.exists(MODEL_PATH):
            nn_model = load_model(MODEL_PATH)
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}")
            
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        # scaler.mean_ corresponds to features:
        # ['humidity', 'light', 'noise', 'temperature', 'traffic', 'wind direction', 'wind strength', 'water']
        mean_values = scaler.mean_
    else:
        print(f"Warning: Scaler file not found at {SCALER_PATH}")

except Exception as e:
    print(f"Error loading model or scaler: {e}")


def get_weather_speed_reduction(illuminance: float, water_level: float, temperature: float) -> tuple[int, str]:
    """
    Determines speed limit reduction based on weather conditions (REQ1).
    Uses a Neural Network to predict near-accident risk.
    """
    speed_reduction = 0
    reason = []

    is_dark = illuminance < 500  # SPEC1
    is_black_ice_danger = (water_level > 1000 and temperature < 0) # SPEC2

    if is_dark:
        reason.append("Darkness (illuminance < 500 millilux)")
    if is_black_ice_danger:
        reason.append("Danger of black ice (water > 1000 µm & temp < 0°C)")

    # --- Router Component Logic (LLM Enhanced) ---
    # Determine if we should check the NN based on an LLM's assessment of the situation
    check_nn = False
    
    # Try using LLM to route
    import os
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
             genai.configure(api_key=api_key)
             router_model = genai.GenerativeModel('gemini-2.5-flash')
             router_prompt = f"""
             You are an intelligent router for a traffic safety system.
             
             Sensor Data:
             - Illuminance: {illuminance} millilux
             - Water Level: {water_level} micrometers
             - Temperature: {temperature} Celsius
             
             Rules:
             - Darkness is defined as Illuminance < 500.
             - Black Ice Risk is Water > 1000 AND Temperature < 0.
             
             Task:
             Decide if we should run the complex Neural Network (NN) to predict accidents.
             Answer "YES" if either Darkness OR Black Ice Risk is present.
             Answer "NO" otherwise.
             
             Output:
             YES or NO
             """
             response = router_model.generate_content(router_prompt)
             llm_router_decision = response.text.strip().upper()
             if "YES" in llm_router_decision:
                 check_nn = True
                 print(f"(LLM: Weather routing decision: Router said '{llm_router_decision}', so checking NN)")
             else:
                 print(f"(LLM: Weather routing decision: Router said '{llm_router_decision}', so skipping NN check)")
        except Exception:
            # Fallback to hardcoded logic on error
            check_nn = is_dark or is_black_ice_danger
    else:
        # Fallback to hardcoded logic if no key
        check_nn = is_dark or is_black_ice_danger

    if check_nn:
        # REQ1: reduce speed limit so at most one near-accident per hour
        predicted_accidents = 0.0
        
        if nn_model and scaler is not None and mean_values is not None:
            try:
                # Construct feature vector using means for missing values
                # Features: ['humidity', 'light', 'noise', 'temperature', 'traffic', 'wind direction', 'wind strength', 'water']
                features = np.copy(mean_values) 
                features[1] = illuminance # light
                features[3] = temperature # temperature
                features[7] = water_level # water
                
                # Reshape and scale
                features_reshaped = features.reshape(1, -1)
                features_scaled = scaler.transform(features_reshaped)
                
                # Predict
                prediction = nn_model.predict(features_scaled, verbose=0)
                predicted_accidents = float(prediction[0][0])
                
            except Exception as e:
                print(f"Error during NN prediction: {e}")
                # Fallback or keep 0.0
        else:
            # Fallback if model not available: Simulate behavior for safety/testing
             if illuminance < 500 or (water_level > 1000 and temperature < 0):
                predicted_accidents = 1.5 
             else:
                predicted_accidents = 0.2

        if predicted_accidents > 1.0:
            speed_reduction = 20 # Example reduction for exceeding target
            reason.append(f"NN predicts {predicted_accidents:.1f} near-accidents/hr, reducing speed by {speed_reduction} km/h.")
        else:
            speed_reduction = 0 # Within target

    return speed_reduction, "; ".join(reason)

def get_speed_limit(illuminance: float, water_level: float, temperature: float, current_hour: int) -> tuple[int, str]:
    """
    Determines the final speed limit based on all conditions and requirements.
    Returns the speed limit and a justification string.
    """
    base_speed_limit = 80 # REQ3: Default speed limit
    final_speed_limit = base_speed_limit
    justification_parts = [] # Collect all parts of the justification

    # 1. Weather-based decision (REQ1)
    weather_reduction, weather_reasons_str = get_weather_speed_reduction(illuminance, water_level, temperature)
    if weather_reasons_str: # If there are any weather-related reasons
        justification_parts.append(weather_reasons_str)

    # 2. Air Quality-based decision (REQ2)
    aqi = get_simulated_aqi(current_hour)
    aqi_reduction = get_llm_speed_reduction_recommendation(aqi)
    if aqi_reduction > 0:
        justification_parts.append(f"Poor air quality (AQI: {aqi}) leading to {aqi_reduction} km/h reduction by LLM recommendation.")


    # Apply reductions, prioritizing the most severe one
    if weather_reduction > 0:
        final_speed_limit = min(final_speed_limit, base_speed_limit - weather_reduction)

    if aqi_reduction > 0:
        final_speed_limit = min(final_speed_limit, base_speed_limit - aqi_reduction)


    # Construct the final justification
    if not justification_parts and final_speed_limit == base_speed_limit:
        justification = "Default speed limit (80 km/h) due to no detected risks."
    elif justification_parts:
        justification = "; ".join(justification_parts)
        if final_speed_limit == base_speed_limit:
            justification += " (Speed limit maintained at 80 km/h as risk is within acceptable limits for detected conditions)."
    else:
        justification = "Default speed limit (80 km/h) due to no detected risks." # Fallback, should ideally be covered by previous conditions

    # Ensure speed limit does not increase above 80 km/h based on AI component decision alone (NFR-8)
    final_speed_limit = min(final_speed_limit, 80)

    return int(final_speed_limit), justification

if __name__ == '__main__':
    print("Testing Decision Logic Component:")

    # Test Case 1: Default (no risk)
    speed_limit, reason = get_speed_limit(illuminance=1000, water_level=500, temperature=10, current_hour=12)
    print(f"Scenario 1 (No risk): Speed Limit = {speed_limit} km/h, Reason: {reason}")

    # Test Case 2: Darkness only
    speed_limit, reason = get_speed_limit(illuminance=100, water_level=500, temperature=10, current_hour=12)
    print(f"Scenario 2 (Darkness): Speed Limit = {speed_limit} km/h, Reason: {reason}")

    # Test Case 3: Black ice danger only
    speed_limit, reason = get_speed_limit(illuminance=1000, water_level=1500, temperature=-5, current_hour=12)
    print(f"Scenario 3 (Black Ice): Speed Limit = {speed_limit} km/h, Reason: {reason}")

    # Test Case 4: Poor air quality only (simulated high AQI for testing)
    # We need to mock get_simulated_aqi for predictable testing here if not relying on random
    # For this test, let's assume get_simulated_aqi returns a high value for a specific hour
    speed_limit, reason = get_speed_limit(illuminance=1000, water_level=500, temperature=10, current_hour=18) # Hour 18 often has higher AQI
    print(f"Scenario 4 (Poor Air Quality): Speed Limit = {speed_limit} km/h, Reason: {reason}")

    # Test Case 5: Combined (Darkness and Poor Air Quality)
    speed_limit, reason = get_speed_limit(illuminance=100, water_level=500, temperature=10, current_hour=18)
    print(f"Scenario 5 (Darkness + Poor Air Quality): Speed Limit = {speed_limit} km/h, Reason: {reason}")

    # Test Case 6: Black ice and Poor Air Quality
    speed_limit, reason = get_speed_limit(illuminance=1000, water_level=1500, temperature=-5, current_hour=18)
    print(f"Scenario 6 (Black Ice + Poor Air Quality): Speed Limit = {speed_limit} km/h, Reason: {reason}")
