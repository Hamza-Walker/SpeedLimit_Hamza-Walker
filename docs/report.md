# SpeedLimit Project Report

## 1. Data Exploration (Initial)

This section documents the initial exploration of the datasets provided for the SpeedLimit project.

**File-by-File Analysis:**

*   **`Case_Study_Speed_Limit_AccidentsYearN_V100.csv`**: Contains records of near-accidents.
    *   **Format:** Semicolon-separated.
    *   **Columns:** `Month;Day;Hour;Second;LicencePlate;Damage;Injured;CloseCarCm;CloseGuardrailCm;SkidAngle`
    *   **Observations:** The primary indicators for a "near-accident" appear to be `CloseCarCm`, `CloseGuardrailCm`, and `SkidAngle`. The `Damage` and `Injured` columns seem sparse in the preview.

*   **`Case_Study_Speed_Limit_SensorReadingsYearN_V100.csv`**: Contains time-series data from various sensors.
    *   **Format:** Semicolon-separated.
    *   **Columns:** `Month;Day;Hour;Minute;Second;Sensor;Value`
    *   **Observations:** The `Value` column uses a comma (`,`) as a decimal separator, which will require special handling during parsing. The `Sensor` column is an ID that needs to be mapped to a sensor type.

*   **`Case_Study_Speed_Limit_Sensors_V100.csv`**: Maps sensor IDs to sensor type codes.
    *   **Format:** Semicolon-separated.
    *   **Columns:** `SensorID;SensorTypeCode`
    *   **Observations:** This is a crucial link between the sensor readings and their meaning.


## 2. Data Preprocessing

The raw data was successfully cleaned and transformed into a unified, analysis-ready dataset. The following steps were performed:

1.  **Data Loading:** All four CSV files were loaded using pandas, with special handling for semicolon delimiters and comma-based decimals.
2.  **Sensor Metadata Merging:** `Sensors_V100.csv` and `SensorTypes_V100.csv` were merged to create a comprehensive lookup table that maps `SensorID` to sensor types, units, and operating ranges.
3.  **Sensor Readings Transformation:**
    *   The raw sensor readings were merged with the sensor metadata.
    *   A `datetime` index was created from the timestamp columns to facilitate time-series analysis.
    *   The data was pivoted to transform the sensor types into distinct columns.
    *   The pivoted data was resampled to an hourly frequency, and missing values were forward-filled to ensure a continuous dataset.
4.  **Near-Accident Aggregation:**
    *   A "near-accident" event was defined as any record where `SkidAngle`, `CloseCarCm`, or `CloseGuardrailCm` had a non-null value.
    *   The accident data was aggregated to produce a count of near-accidents for each hour.
5.  **Final Dataset Combination:**
    *   The hourly sensor data and the hourly near-accident counts were merged into a single DataFrame.
    *   Hours with no recorded near-accidents were filled with a `0`.
6.  **Output:** The final, processed dataset was saved to `data/processed/processed_data.csv`. This file now serves as the clean input for the neural network training and the operational logic.


## 3. Refactoring and Code Quality Improvements

A comprehensive review and enhancement of the codebase was performed, resulting in the following key improvements:

1.  **TensorFlow Model Integration:** 
    *   The `src/nn_training.py` module was updated to fully implement a TensorFlow/Keras neural network. It now successfully trains on the processed data and saves both the model (`models/nn_model.h5`) and the feature scaler (`models/scaler.pkl`).
    *   The `src/decision_logic.py` module was refactored to load the trained model and scaler. It now uses the actual Neural Network for risk prediction instead of a simulation, significantly increasing the system's realism and capabilities.
    *   Robust error handling was added to gracefully handle cases where the model files are missing or TensorFlow is unavailable.

2.  **Data Preprocessing Fix:**
    *   A bug in `src/data_preprocessing.py` was identified where whitespace in `SensorTypeCode` prevented the correct merging of sensor data (specifically 'water' sensors).
    *   This was fixed by stripping whitespace, ensuring all sensor types are correctly included in the processed dataset.

3.  **Unit Test Updates:**
    *   The `tests/test_components.py` suite was extensively updated to reflect the new TensorFlow integration.
    *   `unittest.mock` is now used to mock the Neural Network model and scaler, allowing for deterministic testing of the decision logic without requiring the heavy TensorFlow dependency or a trained model file during test execution.

4.  **Code Quality:**
    *   PEP 8 standards were enforced across modified files.
    *   Docstrings and comments were improved for better maintainability.
    *   Redundant simulation code was removed.

5.  **Generative AI (Gemini) Integration:**
    *   **Real LLM for Air Quality:** The `src/llm_integration.py` module was upgraded from using hardcoded simulation logic to calling the **Google Gemini API**. An AI Traffic Safety Agent now analyzes the Air Quality Index (AQI) and dynamically determines the appropriate speed reduction.
    *   **Intelligent Routing:** An "AI Router" was implemented in `src/decision_logic.py`. It uses the Gemini API to intelligently analyze sensor data (Illuminance, Water, Temperature) and decide whether the Neural Network needs to be consulted for a risk assessment.
    *   **Robust Fallbacks:** Both integrations include automatic fallback mechanisms. If the API key is missing or the service is unreachable, the system gracefully reverts to the original rule-based logic to ensure continuous operation.