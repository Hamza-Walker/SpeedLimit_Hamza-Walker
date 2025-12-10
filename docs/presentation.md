# SpeedLimit Software Project: Management Presentation

## Slide 1: Introduction & Project Overview

*   **Project Goal:** To implement a dynamic speed limit system for highways to enhance road safety and optimize traffic flow, utilizing AI (Neural Networks and LLMs).
*   **Key Features:** Automated speed limit adjustments based on weather (darkness, black ice), air quality, and a default safe speed. Human override capability for emergencies.
*   **Current Status:** MVP implemented with core logic, simulated AI components, and a command-line interface.

## Slide 2: Day 1 - Requirements Elicitation

*   **Stakeholders:** Highway Operator Company, Drivers/Road Users, Regulatory Bodies, System Developers/Data Scientists, External Data Providers (Air Quality API).
*   **EU AI Act Compliance:**
    *   **High-Risk AI:** The Speed Limit System falls under this category due to its role in critical infrastructure management.
    *   **Compliance Measures:** Requires robust Risk Management, Data Governance, Technical Documentation, Human Oversight, and high standards for Accuracy, Robustness, and Cybersecurity.
*   **Facial Recognition Scenario:** **NON-COMPLIANT.** This would violate prohibitions against unacceptable risks (untargeted scraping, biometric categorization, social scoring) under the EU AI Act.
*   **Lessons Learned:** Clear stakeholder analysis, regulation-aware requirements from the start, and early filtering of prohibited AI applications are crucial.

## Slide 3: Day 1 - Requirements Structuring

*   **System Requirements:** Automatically adapt highway speed limits based on darkness/black ice risk, air quality, and a default of 80 km/h.
*   **Requirements Specifications:** Defined precise thresholds (e.g., darkness < 500 millilux; black-ice risk if water > 1000 µm & temperature < 0°C) and how NN/LLM use them.
*   **Assumptions & Rationales:** Assumed accurate sensors and external APIs; justified dynamic speed limits reduce near-accidents while maintaining traffic flow.
*   **Non-Functional Requirements:** Ensured high reliability (99.8% uptime), low latency (5 seconds), safety fallbacks, auditability, and EU AI Act–compliant logging and human override. Performance (NN model size < 50MB, inference cost < €0.01), Accuracy (NN prediction >= 85%), Security (Data Confidentiality, Integrity, Audit Trail), Maintainability, Scalability, Usability, and Transparency are also covered.

## Slide 4: Day 1 - Requirements Documentation

*   **Glossary:** Key terms (e.g., “near-accident”, “black ice”, “illuminance”, “neural network”, “LLM”) defined for common understanding.
*   **Natural Language Quality:** Requirements rewritten for clarity, unambiguousness, and active voice, avoiding vague words.
*   **Helpful Tables:** Decision tables used to structure complex logic (e.g., conditions vs. resulting speed limit) to reduce misunderstandings.

## Slide 5: Day 2 - Architectural Design

*   **Modular Architecture:** Designed with distinct components for Data Processing, NN Training, LLM Integration, Decision Logic, and a User Interface.
*   **Component Cooperation:** Explained how sensor inputs are processed, fed to NN and LLM components, and then integrated by the Decision Logic to determine the final speed limit.
*   **Change Request Adaptations:** Showcased adaptability to changes like Fahrenheit temperature sensors, refined near-accident definitions, and electric car exemptions, demonstrating architectural flexibility.
    *   **Fahrenheit Sensors:** Adapt Data Processing and Decision Logic for unit conversion.
    *   **Skidding Only:** Modify Data Processing component's `is_near_accident` definition.
    *   **EV Exemption:** Adapt Decision Logic to consider vehicle type, potentially impacting LLM input.

## Slide 6: Day 2 - The Importance of Testing

*   **Purpose:** To identify software defects and ensure components meet requirements.
*   **Router Component (Weather-based Decision):**
    *   **Input:** Illuminance, water level, temperature.
    *   **Expected Output:** Binary (yes/no reduction).
    *   **Test Cases (Examples):** Clear day (no reduction), dark (reduction), black ice (reduction), dark and black ice (reduction).
*   **Air Quality Component (LLM-based Decision):**
    *   **Input:** Air Quality Index (AQI).
    *   **Expected Output:** Speed reduction amount (e.g., 0, 10, 20, 30 km/h).
    *   **Golden Answer:** Derived from predefined AQI thresholds and corresponding reduction rules.
    *   **Test Cases (Examples):** Good AQI (0 reduction), Moderate AQI (10 reduction), Unhealthy for Sensitive Groups (20 reduction), Unhealthy for All (30 reduction).
*   **Implemented Tests:** Unit tests successfully verified `llm_integration` and `decision_logic` components, including initial bug fixes.

## Slide 7: Day 3 - Full Implementation (MVP)

*   **Data Processing Component:** Implemented in `src/data_preprocessing.py`. Successfully loads, cleans, merges, and transforms raw CSV data into a clean, hourly-aggregated dataset (`processed_data.csv`). **Fix Applied:** Resolved sensor mapping issues to ensure all data is utilized.
*   **Neural Network (NN) Training Component:** Implemented in `src/nn_training.py`. Fully functional TensorFlow/Keras implementation that trains a model on historical data and saves both the model (`nn_model.keras`) and scaler (`scaler.pkl`).
*   **LLM Integration Component:** Implemented in `src/llm_integration.py`. Replaced simulation with **Google Gemini API** integration. An AI Agent now dynamically determines speed reductions based on Air Quality Index (AQI).
*   **Decision Logic Component:** Implemented in `src/decision_logic.py`. Features an **"AI Router" (using Gemini)** to intelligently route weather checks to the Neural Network. Combines real-time NN risk predictions with LLM air quality recommendations.
*   **User Interface (UI) Component:** Implemented as a Command-Line Interface (CLI) in `src/ui_component.py`. Allows interactive input of sensor parameters and displays real-time speed limit recommendations.

## Slide 8: Lessons Learned

*   **Environment Management:** Early and thorough environment setup (virtual environments, dependency installation) is critical to avoid development blockers.
*   **Modularity:** A modular architecture greatly simplifies development, testing, and adaptation to new requirements.
*   **Hybrid AI Approach:** Combining deterministic rules (fallbacks), probabilistic models (NN), and generative reasoning (LLM) creates a robust and flexible system.
*   **Iterative Testing:** Continuous unit testing and immediate bug fixing (as demonstrated by the justification logic fix) are essential for maintaining code quality.
*   **Documentation as a Living Artifact:** Maintaining comprehensive documentation (e.g., `report.md`, `architecture.md`) throughout the project is crucial for clarity and communication, especially in complex AI systems.

## Slide 9: Next Steps

*   Deploy to a production environment with GPU support for faster NN inference (if scaling up).
*   Implement secure API key management (Secrets Manager) for production deployment.
*   Enhance UI to a graphical interface for better user experience.
*   Implement audit logging as per NFR-11.
*   Further refine and optimize the NN model and LLM prompts.



here is something from machinelearning script summary from cluely 
## Action Items

- Read **AI Act Article 5** (prohibited AI practices) and **Article 3** (definitions).
- Review the **GDPR** data‑minimization principle; note which personal features are disallowed.
- Explore online law programs (e.g., “Yodka Ulins” master’s) if interested in a legal career.
- Run a small Python demo comparing **squared‑error** vs **absolute‑error** linear regression (measure fit time).
- Contact the Austrian bridge‑monitoring agency to arrange a guest speaker on real‑world ML use.
- Practice implementing **gradient descent** and **stochastic gradient descent** on a toy dataset.
- Try a **k‑fold cross‑validation** routine to see how validation splits affect error estimates.

---

## Core ML Components

- Machine learning = **data**, **model**, **loss**.
- Data points have **features (X)** and **labels (Y)**.
- Choice of what counts as a data point (pixel, whole image, bridge) is a design decision.

## Features, Labels & Design Choices

- Images → RGB values per pixel (features); pixel class (foreground/background) as label.
- Whole image → million‑pixel RGB vector (features); “dog vs. cat” as label.
- Bridge example: dimensions, vibrations, crack photos as features; safety in 2 years as label.
- Feature selection must balance measurability, stability, and relevance to the prediction.

## Legal & Ethical Constraints

- **AI Act** bans AI that manipulates user behavior (e.g., targeted radicalizing videos).
- Labels that aim to drive purchases, opinions, or votes may be prohibited.
- GDPR limits use of personal identifiers (gender, race, ID numbers) unless strictly needed.
- Data‑minimization: only collect features essential for the target label.

## Model Fundamentals

- Model = collection of **hypotheses** (parameterized functions).
- Linear models: weighted sum of features (parameter vector w).
- Neural nets, decision trees, and polynomial expansions are specific hypothesis families.

## Loss Functions & Their Impact

- **Squared‑error** (L2) – smooth, easy gradient, sensitive to outliers.
- **Absolute‑error** (L1) – robust to outliers, non‑smooth, slower optimization.
- **Logistic loss** – for categorical labels (e.g., binary classification).
- Choice of loss influences training speed, robustness, and final model performance.

## Optimization & Gradient Descent

- Empirical Risk Minimization = minimize average loss over training set.
- **Batch gradient descent** uses all data each step; **SGD** approximates with random mini‑batches.
- Learning rate (α) must be neither too large (overshoot) nor too small (slow).
- Theoretical bound: α ≤ 1/β where β limits how fast the gradient can change.

## Ensemble & Model‑Combining Techniques

- **Bagging**, **Boosting**, **Stacking** combine multiple base models.
- Modern practice often favors a single large neural network, but ensembles still useful for niche tasks.

## Training, Validation & Over/Under‑fitting

- Compare **training loss** vs **validation loss** to detect overfitting (low train, high val) or underfitting (high both).
- Large training error + low validation error may indicate data leakage or an unlucky split.

## Cross‑Validation

- **k‑fold**: split data into k subsets, rotate each as validation set, average errors.
- Reduces variance from a single train/val split; helps assess model generalization.

## Learning‑Rate & Hyperparameter Tuning

- Learning rate is a hyperparameter; can be tuned via grid search, Bayesian optimization, or meta‑learning.
- Meta‑learning: train a model to predict optimal step size from local loss landscape features.

## Quantum Computing Speculation

- Open question: whether quantum algorithms could replace gradient‑based optimization for ML.
- Current research explores quantum speed‑ups for certain optimization problems, but practical impact remains uncertain. 
