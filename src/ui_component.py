
import warnings
# Suppress urllib3 NotOpenSSLWarning before any other imports
warnings.filterwarnings("ignore", module='urllib3')

import datetime
from src.decision_logic import get_speed_limit

def run_ui():
    """
    Runs the command-line interface for the SpeedLimit system.
    Allows users to input sensor parameters and get real-time speed limit recommendations.
    """
    print("\n--- SpeedLimit System CLI --- ")
    print("Enter sensor readings to get a speed limit recommendation.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            illuminance_str = input("Enter illuminance (millilux, e.g., 800): ")
            if illuminance_str.lower() == 'exit':
                break
            illuminance = float(illuminance_str)

            water_level_str = input("Enter water level (micrometers, e.g., 500): ")
            if water_level_str.lower() == 'exit':
                break
            water_level = float(water_level_str)

            temperature_str = input("Enter temperature (degrees Celsius, e.g., 15): ")
            if temperature_str.lower() == 'exit':
                break
            temperature = float(temperature_str)

            current_hour = datetime.datetime.now().hour # Use current real-world hour for LLM simulation

            speed_limit, justification = get_speed_limit(illuminance, water_level, temperature, current_hour)

            print(f"\nRecommended Speed Limit: {speed_limit} km/h")
            print(f"Justification: {justification}\n")

        except ValueError:
            print("Invalid input. Please enter numerical values for sensor readings.")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Exiting SpeedLimit System CLI. Goodbye!")

if __name__ == '__main__':
    run_ui()
