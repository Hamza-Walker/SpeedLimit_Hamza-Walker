Based on the lecture material, here are **comprehensive implementation instructions** for the SpeedLimit Software MVP in Python. This is designed for vibe coding with Gemini CLI and covers both training and operational stages.[1]

***

## Complete Implementation Instructions for SpeedLimit Software

### PHASE 1: PROJECT SETUP

**Folder Structure:**
```
speedlimit_project/
├── data/
│   ├── SensorReadings.csv (training data)
│   ├── accidents.csv (training labels)
│   └── SensorTypes.csv (reference)
├── models/
│   └── neural_network_model.pkl (trained NN)
├── src/
│   ├── data_preprocessor.py (Software 1.0)
│   ├── neural_network_trainer.py (Software 2.0)
│   ├── decision_controller.py (Software 1.0)
│   ├── llm_gateway.py (Software 3.0 - LLM interface)
│   ├── sensor_manager.py (Software 1.0)
│   ├── speed_limit_actuator.py (Software 1.0)
│   └── gui_app.py (Software 1.0 - UI for MVP)
├── tests/
│   └── test_cases.py
└── main.py (entry point)
```

***

### PHASE 2: TRAINING STAGE IMPLEMENTATION

#### Step 1: Data Preprocessor (data_preprocessor.py)

**Purpose**: Software 1.0 component that cleans and transforms training data

**Key Tasks**:
1. **Load CSVs** using pandas:
   - `SensorReadings.csv`: Columns like `datetime`, `illuminance_mlx`, `water_depth_um`, `temperature_c`, `current_speed_limit`, etc.
   - `accidents.csv`: Columns like `datetime`, `near_accident_count`, `event_type` (skidding, proximity, etc.)

2. **Data Cleaning**:
   - Remove rows with missing values in critical columns (illuminance, temperature, water_depth)
   - Handle outliers (e.g., temperature > 60°C or < -50°C → flag as sensor malfunction)
   - Normalize numerical features to 0-1 range for NN training

3. **Feature Engineering** (create input vectors for NN):
   - Extract features: `illuminance`, `water_depth`, `temperature`
   - Create binary target labels:
     - **Label = 1** (reduce speed): If `near_accident_count > 0` AND (darkness OR black ice condition)
     - **Label = 0** (maintain speed): Otherwise
   - Define darkness: `illuminance < 500`
   - Define black ice: `water_depth > 1000 AND temperature < 0`

4. **Output**: Two cleaned datasets:
   - `X_train` (features): shape (n_samples, 3)
   - `y_train` (labels): shape (n_samples,) with values 0 or 1

***

#### Step 2: Neural Network Trainer (neural_network_trainer.py)

**Purpose**: Software 2.0 component that trains the predictive model

**Key Tasks**:
1. **Choose Framework**: Use `scikit-learn` for simplicity (fits MVP scope):
   - `from sklearn.neural_network import MLPClassifier`
   - Or use `tensorflow.keras` if more control needed

2. **Model Architecture**:
   - Input layer: 3 neurons (illuminance, water_depth, temperature)
   - Hidden layers: 1-2 layers with 16-32 neurons each, ReLU activation
   - Output layer: 1 neuron with sigmoid activation (binary classification)
   - Loss function: Binary Cross-Entropy

3. **Training**:
   - Split data: 80% train, 20% validation
   - Epochs: 50-100 (monitor for overfitting)
   - Batch size: 32
   - Early stopping: Stop if validation accuracy plateaus for 10 epochs

4. **Validation & Metrics**:
   - Calculate accuracy, precision, recall on validation set
   - Target: accuracy ≥ 85% (from REQ-NFR-13)
   - Log confusion matrix to identify failure modes

5. **Save Model**:
   - Serialize to `.pkl` file using `pickle` or `joblib`
   - Include metadata: training date, accuracy, feature names

***

### PHASE 3: OPERATIONAL STAGE IMPLEMENTATION

#### Step 3: Sensor Manager (sensor_manager.py)

**Purpose**: Software 1.0 component that collects and normalizes real-time sensor data

**Key Tasks**:
1. **Simulate Sensors** (since no real sensors):
   - Create methods to accept manual input or generate random readings
   - For MVP GUI: accept user input (illuminance, water_depth, temperature)

2. **Data Normalization**:
   - Apply same scaling as training phase (0-1 range)
   - Implement error handling for out-of-range values
   - Return: dictionary `{"illuminance": float, "water_depth": float, "temperature": float}`

3. **Validation**:
   - Check if values are within expected ranges
   - Log warnings for extreme values (potential sensor malfunction)

***

#### Step 4: LLM Gateway (llm_gateway.py)

**Purpose**: Software 3.0 component that calls an LLM for air quality decisions

**Key Tasks**:
1. **External API Call**:
   - Use Gemini API (or OpenAI) to query air quality data
   - Design prompt: `"Given current air quality index {aqi_value} and visibility {visibility_m}, recommend a speed limit reduction in km/h (0-60 range). Respond with ONLY a number."`
   - Parse LLM response to extract integer speed reduction

2. **Error Handling**:
   - If API fails → fallback to default reduction (e.g., 10 km/h if bad air quality, 0 if good)
   - Implement retry logic with exponential backoff

3. **Output Validation**:
   - Ensure returned value is in range  (output guardrail)
   - If outside range → clamp to nearest valid value

4. **Prompt Management** (following lecture material ):[1]
   - Version control: Track prompt changes over time
   - Use structured response format: `{"speed_reduction": int, "reasoning": str}`
   - Implement input guardrails: Validate AQI input before sending to LLM

***

#### Step 5: Decision Controller (decision_controller.py)

**Purpose**: Software 1.0 component that orchestrates logic and calls AI components

**Key Tasks**:
1. **Condition Routing**:
   ```
   if darkness OR black_ice:
       call neural_network.predict() with sensor data
       speed_reduction = get_nn_recommendation()
   elif bad_air_quality:
       speed_reduction = llm_gateway.get_air_quality_decision()
   else:
       speed_reduction = 0  # maintain 80 km/h
   ```

2. **Human Override** (EU AI Act compliance - human-in-the-loop):
   - Accept operator input to manually set speed limit
   - Log all override events for audit trail

3. **Output**: Final speed limit calculation:
   - `final_speed = max(80 - speed_reduction, 40)` (never go below 40 km/h)
   - Log: timestamp, conditions, AI decision, final result

***

#### Step 6: Speed Limit Actuator (speed_limit_actuator.py)

**Purpose**: Software 1.0 component that applies the final decision

**Key Tasks**:
1. **Simulate Highway Signs**:
   - Display current speed limit in GUI
   - Update every time Decision Controller produces new value

2. **Logging & Audit**:
   - Record all speed changes with reasons
   - Store in CSV for later analysis

***

### PHASE 4: GUI FOR MVP

#### Step 7: GUI Application (gui_app.py)

**Purpose**: User interface to simulate sensor input and display decisions

**Technology**: Use `tkinter` (built-in Python) or `PySimpleGUI` for simplicity

**Components**:
1. **Training Tab**:
   - Button: "Load Training Data"
   - Button: "Train Neural Network"
   - Display: Model accuracy, training metrics
   - Status: Show if model is ready for production

2. **Production Tab**:
   - **Input Fields**:
     - Illuminance (millilux): slider 0-1000
     - Water Depth (µm): slider 0-2000
     - Temperature (°C): slider -20 to +40
     - AQI (optional): slider 0-500
   - **Buttons**:
     - "Query Current Speed Limit" (calls Decision Controller)
     - "Override" (manual operator decision)
   - **Display**:
     - Current speed limit (large font)
     - Reasoning: "Speed reduced due to: [darkness/black ice/air quality/none]"
     - Neural Network prediction (if triggered)
     - LLM air quality recommendation (if triggered)
   - **Log Output**:
     - Show recent decisions in scrollable list

***

### PHASE 5: INTEGRATION & TESTING

#### Step 8: Main Entry Point (main.py)

**Purpose**: Initialize system and launch GUI

**Tasks**:
1. Load pre-trained neural network model from disk
2. Initialize all components (SensorManager, DecisionController, etc.)
3. Launch GUI
4. Implement menu: "Training Mode" vs "Operational Mode"

***

#### Step 9: Test Suite (tests/test_cases.py)

**Purpose**: Verify all components work correctly

**Test Categories**:
1. **Data Preprocessor Tests**:
   - TC-DP-01: Verify feature scaling to 0-1 range
   - TC-DP-02: Verify binary labels assigned correctly
   - TC-DP-03: Handle missing values gracefully

2. **Neural Network Tests**:
   - TC-NN-01: Verify accuracy ≥ 85%
   - TC-NN-02: Test boundary inputs (edge cases from earlier exercise)
   - TC-NN-03: Verify model serialization/deserialization

3. **LLM Gateway Tests**:
   - TC-LLM-01: Valid API response parsed correctly
   - TC-LLM-02: Speed reduction in valid range [0-60]
   - TC-LLM-03: Fallback behavior when API fails

4. **Decision Controller Tests**:
   - TC-DC-01: Darkness condition triggers NN
   - TC-DC-02: Air quality condition triggers LLM
   - TC-DC-03: No conditions → default 80 km/h
   - TC-DC-04: Manual override works

5. **End-to-End Tests**:
   - TC-E2E-01: Full workflow: input → decision → display

***

### PHASE 6: VIBE CODING WORKFLOW (Using Gemini CLI)

**Iterative Prompt Strategy**:

1. **Initial Prompts to Gemini**:
   ```
   "Write Python code for a neural network trainer using scikit-learn.
   Input: 3 features (illuminance, water_depth, temperature).
   Output: binary classification (0=maintain speed, 1=reduce speed).
   Accuracy target: 85%. Include save/load model functionality."
   ```

2. **If Tests Fail**:
   ```
   "I have a test failure: [paste test case + error message].
   Please fix the code and explain what was wrong."
   ```

3. **Refinement Loop**:
   - Run test suite
   - Share failing test outputs with Gemini
   - Request code fixes
   - Repeat until all tests pass

***

### PHASE 7: MANAGEMENT PRESENTATION

**Slides to Include** (building on all prior exercises):

1. **Title Slide**: SpeedLimit Project – MVP Demo
2. **Requirements Recap**: System/specification requirements, glossary, decision tables
3. **Architecture Overview**: 9 components diagram, training vs operational phases
4. **Testing Summary**: Test cases for weather router, LLM air quality, component tests, results
5. **Implementation Results**:
   - Neural Network accuracy achieved
   - GUI screenshots showing real-time decisions
   - Sample logs of speed limit adjustments
6. **EU AI Act Compliance**: Human oversight, audit trail, output guardrails
7. **Lessons Learned**:
   - Importance of requirements clarity and stakeholder alignment
   - Testing as early detection of AI model shortcomings
   - LLM statelessness requires careful prompt + context design
   - Need for human-in-the-loop for high-risk decisions
8. **Next Steps**: Production deployment, continuous monitoring, model retraining

***

### KEY IMPLEMENTATION NOTES

- **MVP Scope**: No cloud deployment, no real sensors, no production-grade infrastructure
- **Focus**: Demonstrate end-to-end workflow from data to decision
- **Testability**: All components independently testable (mocks for external APIs)
- **EU AI Act Compliance**: Implement audit logging, human override, explainability
- **Vibe Coding Philosophy**: Use Gemini iteratively; fix errors through refined prompts rather than manual debugging

This structure allows Gemini CLI to generate complete, testable code modules one at a time while you validate and refine via test feedback.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/40254434/b19fce1a-1340-459f-a356-85ddf29ddd99/Day3_Part1_Architecture_of_LLM_Powered_Applications_V707.pdf)
