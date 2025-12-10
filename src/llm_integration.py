
import random
import os
import google.generativeai as genai

# --- SIMULATION (DATA SOURCE) ---
def get_simulated_aqi(hour_of_day: int) -> int:
    """
    Simulates querying an external Air Quality API to get an AQI value.
    The AQI is randomly generated for demonstration purposes.
    """
    # Simulate different AQI levels based on time of day or just random
    if 6 <= hour_of_day < 10:  # Morning rush hour
        return random.randint(70, 120)
    elif 16 <= hour_of_day < 20: # Evening rush hour
        return random.randint(80, 150)
    else:
        return random.randint(30, 90)

# --- HARDCODED LOGIC (FALLBACK) ---
def _fallback_rule_based_logic(aqi: int) -> int:
    """Fallback logic if the AI Agent is unavailable."""
    if aqi > 150: return 30
    elif aqi > 100: return 20
    elif aqi > 50: return 10
    return 0

# --- AI AGENT INTERACTION ---
def get_llm_speed_reduction_recommendation(aqi: int) -> int:
    """
    The 'Agent' function. It attempts to consult a real LLM.
    If no API key is found or the API fails, it falls back to rules.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return _fallback_rule_based_logic(aqi)

    try:
        # 1. Configure the Agent
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 2. Define the Agent's Persona and Task via Prompt Engineering
        prompt = f"""
        You are an AI Traffic Safety Agent responsible for public health.
        
        Context:
        - The current Air Quality Index (AQI) is {aqi}.
        - The base speed limit is 80 km/h.
        - High speeds stir up dust and pollutants, worsening local air quality.
        
        Task:
        Determine the necessary speed limit reduction (in km/h) to mitigate health risks.
        
        Guidelines:
        - If AQI < 50 (Good), reduction is 0.
        - If AQI is Moderate (50-100), consider a small reduction (e.g., 10).
        - If AQI is Unhealthy (100-150), consider a moderate reduction (e.g., 20).
        - If AQI is Hazardous (>150), consider a significant reduction (e.g., 30).
        
        Output:
        Return ONLY the integer number of the reduction (e.g., 10). Do not write any other text.
        """

        # 3. Get the decision
        response = model.generate_content(prompt)
        
        # 4. Parse the result
        reduction_str = response.text.strip()
        reduction_val = int(reduction_str)
        print(f"(LLM: AQI reduction decision -> -{reduction_val} km/h)")
        return reduction_val

    except Exception as e:
        print(f"AI Agent Error (using fallback): {e}")
        return _fallback_rule_based_logic(aqi)

if __name__ == '__main__':
    print("Simulating LLM Integration Component:")
    # Test cases...
    test_hour = 8
    test_aqi = get_simulated_aqi(test_hour)
    test_reduction = get_llm_speed_reduction_recommendation(test_aqi)
    print(f"At hour {test_hour}: Simulated AQI = {test_aqi}, Recommended Speed Reduction = {test_reduction} km/h")

    test_hour = 18
    test_aqi = get_simulated_aqi(test_hour)
    test_reduction = get_llm_speed_reduction_recommendation(test_aqi)
    print(f"At hour {test_hour}: Simulated AQI = {test_aqi}, Recommended Speed Reduction = {test_reduction} km/h")

    test_aqi_high = 180 # Directly test a high AQI
    test_reduction_high = get_llm_speed_reduction_recommendation(test_aqi_high)
    print(f"Directly testing high AQI ({test_aqi_high}): Recommended Speed Reduction = {test_reduction_high} km/h")
