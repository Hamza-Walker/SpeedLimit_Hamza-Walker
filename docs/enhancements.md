# Prompt for Project Enhancement with TensorFlow Integration

## Objective

Your task is to enhance the existing SpeedLimit software project by replacing the simulated Neural Network (NN) components with a functional TensorFlow/Keras model. You will then update the corresponding unit tests and perform a general review and improvement of the entire codebase. Assume that `tensorflow` and `scikit-learn` are installed and available in the environment.

---

### Phase 1: Integrate a Functional TensorFlow Model

**Goal:** Modify the project to train, save, load, and use a real TensorFlow model for weather-based speed limit decisions.

**1. Update the NN Training Component (`src/nn_training.py`):**
   - **Activate TensorFlow Code:** Uncomment all lines related to `tensorflow.keras` imports, model definition (`Sequential`), compilation, training (`model.fit`), evaluation, and saving (`model.save`).
   - **Remove Placeholders:** Delete the `print` statements that indicate training is being skipped.
   - **Run the Script:** Execute the script to train the model and save the `models/nn_model.h5` file.

**2. Update the Decision Logic Component (`src/decision_logic.py`):**
   - **Load the Model:** At the beginning of the script, load the trained Keras model (`models/nn_model.h5`). You will need to import `tensorflow.keras.models.load_model`.
   - **Load the Scaler:** The `StandardScaler` used during training is crucial for making predictions on new data. Modify `src/nn_training.py` to save the scaler object (e.g., using `joblib` or `pickle`). Then, load this scaler in `src/decision_logic.py`.
   - **Replace Simulation with Real Prediction:**
     - Remove the `_simulate_nn_prediction` function.
     - In the `get_weather_speed_reduction` function, when conditions for darkness or black ice are met, you must:
       1.  Create a NumPy array from the input sensor data (`illuminance`, `water_level`, `temperature`, etc., matching the training features).
       2.  Scale this data using the loaded `StandardScaler`.
       3.  Use the loaded Keras model's `.predict()` method to get the near-accident prediction.
       4.  Use this prediction to determine the speed reduction. You may need to refine the logic that decides the reduction amount based on the prediction (e.g., a simple `if prediction > 1.0` might be too basic).

---

### Phase 2: Update Unit Tests

**Goal:** Adapt the tests to reflect the new TensorFlow model integration.

**1. Modify `tests/test_components.py`:**
   - **Patch the Model, Not the Simulation:** The tests for `TestDecisionLogic` currently mock the old `_simulate_nn_prediction` function or `get_simulated_aqi`. You need to change this approach for the NN.
   - **Mock `load_model` and `predict`:** The best practice is to avoid loading the actual model in unit tests. Use `unittest.mock.patch` to:
     1.  Patch `tensorflow.keras.models.load_model` to return a mock model object.
     2.  Configure the `predict` method of that mock model to return specific values for each test case. For example, in `test_darkness_reduction`, make the mock model's `predict` method return `[1.5]` (a high value), and in `test_default_speed_limit`, make it return `[0.2]` (a low value).
     3.  You will also need to mock the loading and usage of the `StandardScaler`.

---

### Phase 3: General Code Review and Improvement

**Goal:** Leverage your advanced capabilities to refactor and improve the overall quality of the codebase.

**1. Review All Python Files in `src/`:**
   - **Code Quality & Style:** Ensure the code adheres strictly to PEP 8 standards. Improve variable naming, clarity, and remove any redundant code.
   - **Refactoring Opportunities:**
     - Analyze `get_speed_limit` in `src/decision_logic.py`. Can it be broken down into smaller, more focused functions for better readability?
     - Examine the `data_preprocessing.py` script for potential optimizations using pandas/NumPy.
   - **Error Handling:** Enhance exception handling. For instance, what happens if `models/nn_model.h5` is not found in `decision_logic.py`? Add robust checks and informative error messages.
   - **Docstrings and Comments:** Improve all docstrings to be more descriptive and follow a consistent format (e.g., Google Style). Add inline comments to explain any complex or non-obvious logic, especially regarding the NN prediction interpretation.
   - **Final Report:** Briefly summarize the key improvements you made in a new section in the `docs/report.md` file.
