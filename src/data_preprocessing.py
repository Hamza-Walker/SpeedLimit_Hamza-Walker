
import pandas as pd
import numpy as np

def load_and_preprocess_data():
    """
    Loads, cleans, and preprocesses the SpeedLimit project data.
    """
    # Load the datasets
    try:
        accidents = pd.read_csv('data/Case_Study_Speed_Limit_AccidentsYearN_V100.csv', sep=';', decimal=',')
        sensor_readings = pd.read_csv('data/Case_Study_Speed_Limit_SensorReadingsYearN_V100.csv', sep=';', decimal=',')
        sensors = pd.read_csv('data/Case_Study_Speed_Limit_Sensors_V100.csv', sep=';')
        sensor_types = pd.read_csv('data/Case_Study_Speed_Limit_SensorTypes_V100.csv', sep=';')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Make sure the data files are in the 'data/' directory.")
        return None

    # 1. Create a complete sensor lookup table
    # Strip whitespace from SensorTypeCode to ensure correct merging
    sensors['SensorTypeCode'] = sensors['SensorTypeCode'].str.strip()
    sensor_types['SensorTypeCode'] = sensor_types['SensorTypeCode'].str.strip()
    
    sensor_lookup = pd.merge(sensors, sensor_types, on='SensorTypeCode')

    # 2. Clean and pivot sensor readings
    # Merge readings with the lookup table to get sensor types
    sensor_readings_merged = pd.merge(sensor_readings, sensor_lookup, left_on='Sensor', right_on='SensorID')

    # Create a datetime index for time-series analysis
    sensor_readings_merged['datetime'] = pd.to_datetime(
        sensor_readings_merged[['Month', 'Day', 'Hour', 'Minute', 'Second']].assign(Year=2023)
    )
    sensor_readings_merged = sensor_readings_merged.drop(['Month', 'Day', 'Hour', 'Minute', 'Second', 'Sensor'], axis=1)

    # Pivot the table to have sensor types as columns
    sensor_pivot = sensor_readings_merged.pivot_table(
        index='datetime',
        columns='Type',
        values='Value'
    )
    
    # Resample to hourly frequency and forward-fill missing values
    sensor_hourly = sensor_pivot.resample('h').mean()
    sensor_hourly = sensor_hourly.fillna(method='ffill')
    

    # 3. Process accident data
    # Define a near-accident
    accidents['is_near_accident'] = (
        (accidents['SkidAngle'].notna() & accidents['SkidAngle'] > 0) |
        (accidents['CloseCarCm'].notna() & accidents['CloseCarCm'] > 0) |
        (accidents['CloseGuardrailCm'].notna() & accidents['CloseGuardrailCm'] > 0)
    )
    
    # Create a datetime index for accidents
    accidents['datetime'] = pd.to_datetime(
        accidents[['Month', 'Day', 'Hour', 'Second']].assign(Year=2023)
    )
    accidents = accidents.drop(['Month', 'Day', 'Hour', 'Second', 'LicencePlate', 'Damage', 'Injured', 'CloseCarCm', 'CloseGuardrailCm', 'SkidAngle'], axis=1)
    
    # Aggregate near-accidents by hour
    near_accidents_hourly = accidents[accidents['is_near_accident']].resample('h', on='datetime').count()['is_near_accident'].rename('near_accidents')
    
    # 4. Combine sensor data and near-accident counts
    combined_data = sensor_hourly.merge(near_accidents_hourly, left_index=True, right_index=True, how='left')
    combined_data['near_accidents'] = combined_data['near_accidents'].fillna(0) # Fill hours with no accidents with 0
    
    # 5. Save the processed dataset
    output_path = 'data/processed/processed_data.csv'
    combined_data.to_csv(output_path)
    print(f"Processed data saved to {output_path}")
    
    return combined_data

if __name__ == '__main__':
    load_and_preprocess_data()
