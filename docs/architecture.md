# SpeedLimit Software Architecture

## Overview

The SpeedLimit software is designed with a modular architecture to handle both a training phase for its Neural Network (NN) and a production (operational) phase where real-time decisions are made. The system integrates sensor data, a trained NN, and an LLM for dynamic speed limit adjustments.

## Components

### 1. Data Processing Component
*   **Description:** Handles all data loading, cleaning, and transformation. This component is responsible for taking raw sensor and accident data and preparing it for NN training and operational use.
*   **Inputs:** Raw CSV files (`Accidents`, `SensorReadings`, `Sensors`, `SensorTypes`).
*   **Outputs:** Cleaned, processed time-series data (`processed_data.csv`).

### 2. Neural Network (NN) Training Component
*   **Description:** Develops, trains, and evaluates a neural network model to predict near-accidents based on historical weather and road conditions. It uses TensorFlow/Keras to build a Dense neural network.
*   **Inputs:** Processed data from the Data Processing Component.
*   **Outputs:** A trained NN model (`models/nn_model.keras`) and a feature scaler (`models/scaler.pkl`).

### 3. LLM Integration Component
*   **Description:** Manages interaction with the **Google Gemini API** to interpret air quality data (AQI) and recommend appropriate speed limit reductions. It acts as an AI Traffic Safety Agent.
*   **Inputs:** Simulated Air Quality Index (AQI) based on time of day.
*   **Outputs:** Recommended speed limit reduction (e.g., in km/h) based on AQI.

### 4. Decision Logic Component
*   **Description:** The central orchestrator in the operational phase. It integrates a **Gemini-powered Router** to decide when to consult the Neural Network. It loads the trained NN model and scaler for risk prediction and combines these with LLM-based air quality recommendations to determine the final speed limit.
*   **Inputs:** Real-time sensor readings (illuminance, water level, temperature), NN model output (predicted risk), LLM air quality recommendation.
*   **Outputs:** Final recommended speed limit.

### 5. User Interface (UI) Component
*   **Description:** Provides a simple graphical interface for human operators to input simulated sensor data, observe the system's decisions, and manually override speed limits in emergencies.
*   **Inputs:** User-entered sensor parameters (illuminance, water level, temperature), override commands.
*   **Outputs:** Display of current speed limit, decision rationale, and system status.

## Component Cooperation (Operational Phase)

1.  **Sensor Input:** The UI component receives simulated sensor readings (illuminance, water level, temperature).
2.  **Weather-based Prediction (AI Router + NN):** 
    *   The Decision Logic Component first calls the **Gemini AI Router**, passing the sensor data to ask if a risk assessment is needed.
    *   If the Router answers "YES" (due to Darkness or Black Ice), the component then calls the **Trained Neural Network** to predict the number of near-accidents.
3.  **Air Quality Assessment (LLM Agent):** Concurrently, the Decision Logic Component queries the LLM Integration Component. The **Gemini AI Agent** analyzes the current AQI and outputs a specific speed reduction recommendation (e.g., "Reduce by 20 km/h").
4.  **Final Speed Limit Determination:** The Decision Logic Component calculates the final limit by taking the minimum speed required by either the Weather/NN decision or the Air Quality/LLM decision, ensuring safety.
5.  **Output to UI:** The determined speed limit and its rationale are displayed on the UI.
6.  **Human Override:** The UI allows human operators to override the system's decision, which is then logged by the Decision Logic Component.

## Architecture Diagram

```mermaid
graph TD
    A[Raw Data] --> B(Data Processing Component)
    B --> C{Processed Data (CSV)}

    C --> D[NN Training Component]
    D --> E(Trained NN Model)

    F[External Air Quality API] --> G(LLM Integration Component)

    H[Real-time Sensor Input via UI] --> I(Decision Logic Component)
    E --> I
    G --> I

    I --> J[Final Speed Limit]
    I --> K(Audit Log)
    J --> L[UI Display]
    L --> H
    H -- Human Override --> I
```

## Change Requests Adaptations

### 1. Some temperature sensors return Fahrenheit instead of Celsius.
*   **Component to Adapt:** Data Processing Component (for training phase) and Decision Logic Component (for operational phase).
*   **How:** Introduce a unit conversion module within the Data Processing Component to convert Fahrenheit to Celsius during ingestion. The Decision Logic Component will need to ensure any real-time Fahrenheit inputs from the UI or new sensors are converted before being fed to the NN or decision rules.

### 2. Only skidding counts as a near-accident.
*   **Component to Adapt:** Data Processing Component.
*   **How:** Modify the `is_near_accident` definition in the Data Processing Component to only consider `SkidAngle` (i.e., `accidents['SkidAngle'].notna() & accidents['SkidAngle'] > 0`). This will affect the training data for the NN.

### 3. Electric cars are exempt from a speed limit caused by bad air quality.
*   **Component to Adapt:** Decision Logic Component and potentially LLM Integration Component.
*   **How:**
    *   **Decision Logic Component:** This component would need to receive additional input about the vehicle type (e.g., from a vehicle detection system, or an additional field in the UI for simulation). It would then add a conditional check: if `vehicle_type == 'electric'` AND the speed limit reduction reason is `air_quality`, then the air quality-based reduction should not be applied for that specific vehicle. This would require the system to manage different speed limits for different vehicle types, which adds significant complexity to output communication.
    *   **LLM Integration Component (less likely, but possible):** The LLM could be prompted with the information about electric vehicles to directly factor this into its recommendation. However, it's generally better to keep such specific business rules outside the LLM to maintain control and auditability within the core logic.
