# Future To-Dos for SpeedLimit Project

This document outlines potential future enhancements, improvements, and maintenance tasks for the SpeedLimit software project. These items are shelved for future development.

## 1. Core Logic & AI Enhancements

*   **Input Validation & Clamping:** Implement robust input validation and clamping for sensor readings in `src/decision_logic.py` to prevent out-of-distribution values (e.g., extremely high temperatures) from being fed to the Neural Network, which can lead to unstable predictions.
    *   *Example:* Clamp `temperature` to a realistic range (e.g., -50°C to +60°C) and `water_level` to sensor operating limits.
*   **Real-time AQI Data Source:** Replace the `get_simulated_aqi` function in `src/llm_integration.py` with an actual integration to a live Air Quality Index (AQI) API (e.g., OpenAQ, local government APIs). This will make the AQI decisions truly real-time.
*   **LLM Explainability Enhancement:** Modify the LLM prompts in `src/llm_integration.py` and `src/decision_logic.py` to encourage more detailed, structured reasoning (e.g., JSON output with `"reason": "..."`) that can be presented in the UI.
*   **NN Model Optimization:** Explore advanced Neural Network architectures, hyperparameter tuning, or transfer learning to improve prediction accuracy (NFR-13) and potentially reduce model size (NFR-3) and inference cost (NFR-4).
*   **Dynamic Speed Reduction from NN:** Instead of a fixed `20 km/h` reduction, make the NN output influence a more granular speed reduction amount, possibly by mapping its predicted near-accident count to a continuous reduction scale.
*   **Cumulative Speed Reductions (Re-evaluation):** Revisit the decision logic regarding cumulative vs. minimum speed reductions if future requirements dictate that multiple risk factors should lead to a combined, stricter speed limit.

## 2. System Robustness & Compliance

*   **Audit Logging (NFR-11):** Implement a comprehensive audit logging mechanism to record all system decisions, triggering conditions, AI component outputs, justifications, and any human overrides. This is critical for regulatory compliance (EU AI Act Article 10).
*   **Secure API Key Management:** For production deployment, implement a secure method for managing API keys (e.g., using environment variables for local, or a dedicated Secrets Manager service for cloud deployments) rather than hardcoding or relying solely on shell exports.
*   **Error Handling & Fallbacks Refinement:** Enhance existing error handling in `src/decision_logic.py` and `src/llm_integration.py` for API failures, model loading issues, and unexpected LLM responses. Implement more sophisticated fallback strategies (e.g., using cached safe defaults, alerting operators).
*   **Python Version Upgrade:** Address the Python 3.9 deprecation warnings by upgrading the virtual environment and project to Python 3.10 or a later supported version to ensure ongoing library compatibility and security updates.

## 3. User Experience & Deployment

*   **Graphical User Interface (GUI):** Replace the current Command-Line Interface (`src/ui_component.py`) with a more user-friendly graphical interface for better operator interaction and visualization of sensor data and decisions.
*   **Deployment Strategy:** Develop a deployment plan for a high-performance environment, considering containerization (Docker), orchestration (Kubernetes), and potential GPU acceleration for NN inference.
*   **Monitoring & Alerting (NFR-18):** Implement real-time monitoring dashboards to track system performance, sensor health, AI model accuracy, and decision distributions.

## 4. Documentation Updates

*   **Detailed Architectural Diagram:** Update the `docs/architecture.md` diagram with a more detailed visual representation (e.g., Mermaid diagram with subprocesses) of the AI Router and Agent interactions within the Decision Logic.
*   **Requirements Traceability:** Implement a system to trace each requirement (REQ, SPEC, NFR) to its corresponding code implementation and test cases.

---