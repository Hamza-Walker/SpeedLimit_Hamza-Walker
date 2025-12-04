# SpeedLimit_Hamza-Walker

## Project Overview

The SpeedLimit software is a **hybrid AI system** designed for dynamic highway speed limit control. Its primary goal is to enhance road safety and optimize traffic flow by leveraging both traditional Machine Learning (Neural Networks) and modern Generative AI (Large Language Models). The system dynamically adjusts speed limits based on real-time environmental conditions, ensuring compliance with safety regulations and providing human oversight.

## Key Features

*   **Dynamic Speed Limit Adjustment:** Automatically adapts highway speed limits based on:
    *   **Weather Conditions:** Darkness (illuminance below 500 millilux) and danger of black ice (water > 1000 µm & temperature < 0°C).
    *   **Air Quality:** Adjustments based on the Air Quality Index (AQI) as recommended by an AI Agent.
*   **Neural Network (NN) for Risk Prediction:** A TensorFlow/Keras model predicts the expected number of near-accidents based on various sensor data.
*   **Generative AI (Google Gemini API) Integration:**
    *   **Intelligent Router:** A Gemini-powered "AI Router" analyzes weather data to decide whether a detailed Neural Network risk assessment is necessary.
    *   **AQI Decision Agent:** A Gemini AI Agent interprets Air Quality Index (AQI) values to recommend appropriate speed limit reductions.
*   **Robust Fallback Mechanisms:** The system is designed with fallbacks to rule-based logic if API keys are missing or AI services are unreachable, ensuring continuous operation.
*   **Human Oversight:** Provides human operators the ability to override automatic speed limit decisions.
*   **Comprehensive Logging:** All system decisions, conditions, and justifications are logged for auditability and compliance.
*   **Command-Line Interface (CLI):** An interactive interface for inputting simulated sensor data and observing real-time speed limit recommendations.

## Architectural Design

The SpeedLimit software follows a modular architecture, separating concerns into distinct components for data handling, model training, AI integration, and decision-making.

### Components

1.  **Data Processing Pipeline (`src/data_preprocessing.py`)**
    *   **Role:** Extract-Transform-Load (ETL) module.
    *   **Description:** Ingests raw CSV logs (accidents, sensor readings, sensor metadata), performs cleaning (e.g., stripping whitespace from sensor types, handling comma-based decimals), aligns time-series data to hourly intervals, aggregates "near-accident" events based on specific sensor thresholds (skidding, close-car, close-guardrail metrics), and outputs a unified `processed_data.csv` dataset.

2.  **Neural Network Training Module (`src/nn_training.py`)**
    *   **Role:** Model Factory.
    *   **Description:** Loads the `processed_data.csv`, splits it into training and testing sets, and applies `StandardScaler` for feature normalization. It constructs and trains a Feedforward Deep Neural Network (Dense layers: 64 -> 32 -> 1) using TensorFlow/Keras. The model regresses various weather and road conditions against the predicted number of near-accidents per hour.
    *   **Artifacts:** Saves the trained model (`models/nn_model.keras`) and the fitted `StandardScaler` (`models/scaler.pkl`) for consistent inference in the operational phase.

3.  **Generative AI Integration (`src/llm_integration.py`)**
    *   **Role:** Intelligent Agent Interface for Air Quality.
    *   **Description:** Connects to the **Google Gemini API** to act as a specialized "Traffic Safety Agent." This agent evaluates the simulated Air Quality Index (AQI) (based on the time of day) and dynamically outputs an integer speed reduction based on defined health safety guidelines. It includes a robust fallback to rule-based logic if the API key is missing or the API service is unreachable.

4.  **Decision Logic Engine (`src/decision_logic.py`)**
    *   **Role:** Operational Core / Controller.
    *   **Description:** This is the central orchestrator during the operational phase.
        *   **Input Handling:** Accepts real-time sensor inputs (illuminance, water level, temperature).
        *   **AI Router:** Uses a Gemini-powered "Router" prompt to analyze weather conditions and decide ("YES" or "NO") whether the expensive Neural Network inference is required.
        *   **Inference:** If routed, loads the NN model/scaler and predicts accident risk.
        *   **Aggregation:** Combines NN risk predictions, AI Agent AQI recommendations, and safety constraints (Minimization logic) to calculate the final speed limit.
        *   **Output:** Returns the integer speed limit and a human-readable justification string.

5.  **User Interface (`src/ui_component.py`)**
    *   **Role:** Interaction Layer.
    *   **Description:** Provides a Command-Line Interface (CLI) that continuously prompts the user for simulated sensor inputs (illuminance, water level, temperature). It then invokes the Decision Logic Engine and displays the real-time speed limit recommendation along with its detailed justification.

### Component Cooperation (Operational Phase)

1.  **Sensor Input:** The `UI Component` receives simulated sensor readings.
2.  **Weather-based Prediction (AI Router + NN):**
    *   The `Decision Logic Component` first queries the **Gemini AI Router** with the current sensor data to assess the immediate need for a detailed risk evaluation.
    *   If the Router's response is "YES" (indicating potential Darkness or Black Ice risk), the `Decision Logic Component` then utilizes the `Trained Neural Network` to predict the number of near-accidents.
    *   Based on this prediction, a weather-based speed reduction is determined.
3.  **Air Quality Assessment (LLM Agent):** Concurrently, the `Decision Logic Component` queries the `LLM Integration Component`. The **Gemini AI Agent** analyzes the current AQI and provides a specific speed reduction recommendation.
4.  **Final Speed Limit Determination:** The `Decision Logic Component` aggregates all inputs. It calculates the final speed limit by applying the most severe reduction (minimum speed) derived from either the weather/NN assessment or the air quality/LLM recommendation, adhering to a default of 80 km/h in safe conditions.
5.  **Output to UI:** The determined speed limit and its comprehensive rationale are displayed on the `UI Component`.

## Setup and Running the Project

### Prerequisites

*   Python 3.9 (or compatible)
*   `pip` (Python package installer)
*   Git

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:Hamza-Walker/SpeedLimit_Hamza-Walker.git
    cd SpeedLimit_Hamza-Walker
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    .venv/bin/pip install pandas scikit-learn tensorflow google-generativeai
    ```
4.  **Download Data:** Ensure your `data/` directory contains the required CSV files.

### Running the Components

1.  **Data Preprocessing:**
    ```bash
    .venv/bin/python src/data_preprocessing.py
    ```
2.  **NN Training:**
    ```bash
    .venv/bin/python src/nn_training.py
    ```
3.  **Run User Interface (CLI):**
    *   **Important:** To enable live Gemini LLM calls, you need a `GEMINI_API_KEY`. Obtain one from [Google AI Studio](https://aistudio.google.com/) and set it as an environment variable:
        ```bash
        export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
        export PYTHONPATH=. # Ensures Python finds your modules
        .venv/bin/python src/ui_component.py
        ```
        (If `GEMINI_API_KEY` is not set, the system will fall back to rule-based logic for AI components.)

### Running Tests

```bash
export PYTHONPATH=. # Ensures Python finds your modules
.venv/bin/python -m unittest tests/test_components.py
```

## Test Coverage

The project currently has **82% overall test coverage**. Core functional logic, including AI component integration and fallback mechanisms, is thoroughly tested. Uncovered lines primarily include manual execution blocks (`if __name__ == '__main__':`) and certain defensive error-handling paths that are challenging to trigger in unit tests.

## Lessons Learned

*   **Environment Management:** Crucial for avoiding development blockers, especially with complex AI dependencies like TensorFlow.
*   **Modularity:** Simplifies development, testing, and adaptation to new requirements.
*   **Hybrid AI Approach:** Combining deterministic rules (fallbacks), probabilistic models (NN), and generative reasoning (LLM) creates a robust and flexible system.
*   **Iterative Testing:** Continuous unit testing and immediate bug fixing are essential for maintaining code quality.
*   **Documentation as a Living Artifact:** Maintaining comprehensive and up-to-date documentation is vital for clarity and communication in complex AI systems.

---