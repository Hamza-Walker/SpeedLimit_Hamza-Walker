## Day1_Part3_Requirements_Elicitation

### What are the stakeholders of the SpeedLimit project?
Based on the project description, the stakeholders are:
*   **The Highway Operator Company**: This entity initiates the project, owns the records (accident history, speed limits, sensor data), and will use the system to manage road safety.[1]
*   **Drivers/Road Users**: These are the people directly affected by the speed limit changes and the primary subjects of safety improvements (reduced near-accidents).[1]
*   **Regulatory Bodies**: Entities responsible for ensuring compliance with laws such as the EU AI Act, especially regarding high-risk AI applications in critical infrastructure.[2]
*   **System Developers/Data Scientists**: The team responsible for building the neural networks, LLM integration, and maintaining the system logic.[1]
*   **External Data Providers**: The API providers for air quality data.[1]

### is the Speed Limit System compliant with the EU AI Act?
☐ No because
________
☐ Yes because
________
**☑ Yes, but only with the following technical and organizational measures:**
The Speed Limit System falls under **High-Risk AI Applications** because it is a safety component in the management of road traffic (critical infrastructure). To be compliant, it must implement strict requirements including:[2]
*   **Risk Management System**: Identifying and analyzing foreseeable risks to health and safety.[2]
*   **Data Governance**: Ensuring training, validation, and testing data are relevant, representative, and free of errors.[2]
*   **Technical Documentation**: Detailed descriptions of the system, its development, and architecture.[2]
*   **Human Oversight**: The system must be designed so it can be effectively overseen by natural persons to minimize risks.[2]
*   **Standards for Accuracy, Robustness, and Cybersecurity**: The system must meet high standards in these areas throughout its lifecycle.

### Imagine the Speed Limit System gets a new requirement:
The faces of the drivers having near-accidents shall be identified using facial
recognition software. The pictures, names and near-accident information shall be
kept in a database. The database and a neural network shall be used to learn to
predict future accidents.
**Would this compliant with the EU AI Act?**
**☑ No because**
This requirement would likely violate the prohibition against **AI Applications with Unacceptable Risks**. Specifically, it involves creating a facial recognition database which can be considered **untargeted scraping of facial images** if not strictly controlled, or **biometric categorization**. More critically, using this data to predict future accidents based on personal traits could be interpreted as **social scoring** or a prohibited risk assessment of natural persons based on profiling, which often leads to unfavorable treatment (e.g., penalties or different rules) unrelated to the immediate context. Furthermore, "real-time" remote biometric identification in public spaces is generally banned for law enforcement except for very specific threats (e.g., terrorism, missing persons), which predicting traffic accidents does not typically qualify for.[2]

# slides : 
lessons learn from Requirments Elicitation: 
- Clear stakeholder analysis is essential: we must identify road users, operators, regulators, and developers early to capture all relevant needs and constraints.
- Regulation-aware requirements: for safety-critical and high-risk AI (EU AI Act), legal and ethical constraints must shape requirements from the start, not as an afterthought.
- Beware of requirement creep into prohibited zones: ideas like facial recognition + profiling can quickly cross into “unacceptable risk” and must be filtered out early.

## Day1_Part4_Requirements_Structuring
Based on the lecture material and project description, here are the answers to your requirements structuring questions for the Speed Limit project:

***

## Complete List of System Requirements
**REQ1:** When it is dark or there is danger of black ice, the speed limit on the highway shall be reduced in such a way that there will be on average at most one near-accident per hour.
**REQ2:** When poor air quality is predicted, the speed limit on the highway shall be reduced in an appropriate way.
**REQ3:** If there is no reason to reduce the speed limit because of REQ1 or REQ2, it is set to 80 km/h.
**REQ4:** The system shall continuously monitor highway sensor data and make speed limit adjustments in real time.
**REQ5:** The system shall provide human operators with the ability to override automatic speed limit decisions in emergency situations.

***

## Complete List of Requirements Specifications
**SPEC1:** It is dark when the illuminance is below 500 millilux.
**SPEC2:** There is danger of black ice if there is more than 1000 micrometers water on the road and the temperature is below zero degrees Celsius.
**SPEC3:** A neural network shall learn from sensor data how weather, current speed limit, and the number of near-accidents are connected.
**SPEC4:** A near-accident is defined as a car skidding or getting too close to another car or the highway guardrail.
**SPEC5:** The LLM shall query an external API to obtain current air quality data (e.g., AQI—Air Quality Index) and determine appropriate speed limit reductions based on this data.
**SPEC6:** The neural network shall be trained using historical sensor data from the SensorReadings.csv files (including illuminance, water on road, temperature) and accidents.csv (near-accident metrics).
**SPEC7:** Speed limit adjustments shall be communicated to highway signs and driver information systems within a maximum latency of 5 seconds from sensor input.
**SPEC8:** The system shall maintain an audit log of all speed limit decisions, including timestamps, triggering conditions, and reasoning (neural network vs. LLM decision).
***
## Assumptions
**AS1:** Highway is equipped with the sensors described in Sensors.csv and SensorTypes.csv (illuminance, temperature, water on road).
**AS2:** Sensor readings are available approximately every hour and are accurate to ±10% for illuminance and ±2°C for temperature.
**AS3:** The external air quality API is available 99.5% of the time with a response latency < 2 seconds.
**AS4:** Historical accident and near-accident data in accidents.csv is accurate and comprehensively recorded.
**AS5:** A speed reduction to the lowest recorded safe speed in similar conditions (dark + rain) is acceptable for REQ1.
**AS6:** The LLM will make reasonable decisions about air quality-based speed reductions without explicit quantitative thresholds.
**AS7:** Highway operators are willing to accept occasional speed limit changes (e.g., multiple changes per hour during variable weather).
**AS8:** All drivers see and respond to updated speed limit signs within 30 seconds.

***

## Rationales

**Rationale for REQ1:** Reducing speed limits during dangerous conditions (darkness, black ice risk) directly minimizes the risk of accidents and near-accidents, protecting lives and infrastructure.
**Rationale for REQ2:** Air quality significantly affects driver visibility and vehicle performance. An LLM can make contextually appropriate decisions where historical ML data is insufficient.
**Rationale for REQ3:** Maintaining a default speed limit of 80 km/h during good conditions ensures traffic flow and predictability when no safety risk is detected.
**Rationale for REQ4:** Real-time monitoring and adjustment ensures the system responds immediately to changing road conditions rather than using outdated information.
**Rationale for REQ5:** Human oversight is required for EU AI Act compliance (high-risk system) and allows operators to handle edge cases or system errors.
***

## Non-Functional Requirements for the Speed Limit System

### Performance & Efficiency
- **REQ-NFR-1 (Latency):** Speed limit adjustment decisions shall be made and communicated within 5 seconds of sensor input change.
- **REQ-NFR-2 (Throughput):** The system shall process sensor readings from at least 100 highway sections simultaneously.
- **REQ-NFR-3 (Model Size):** The neural network model size shall not exceed 50 MB to enable efficient deployment and updates.
- **REQ-NFR-4 (Inference Cost):** The cost per prediction (neural network + LLM decision) shall not exceed €0.01.

### Reliability & Safety
- **REQ-NFR-5 (Availability):** The system shall maintain 99.8% uptime (no more than 1.7 hours downtime per week).
- **REQ-NFR-6 (Fault Tolerance):** If the neural network fails, the system shall fall back to conservative pre-computed speed limits.
- **REQ-NFR-7 (Robustness):** The system shall handle sensor malfunctions, missing data, and API timeouts gracefully without crashing.
- **REQ-NFR-8 (Safety):** The system shall never increase the speed limit above 80 km/h based on an individual AI component's decision alone.

### Security & Compliance
- **REQ-NFR-9 (Data Confidentiality):** Driver identity information shall not be stored or processed by the AI system.
- **REQ-NFR-10 (Integrity):** Speed limit decisions shall be cryptographically signed and logged to prevent tampering.
- **REQ-NFR-11 (Audit Trail):** All system decisions shall be logged with sufficient detail for regulatory compliance (EU AI Act Article 10).
- **REQ-NFR-12 (Explainability):** The system shall provide human-readable justifications for speed limit decisions (e.g., "80→60 km/h due to black ice risk detected").

### Accuracy & Fairness
- **REQ-NFR-13 (Accuracy - Neural Network):** The neural network's accident prediction accuracy shall be ≥85% on validation data.
- **REQ-NFR-14 (Fairness):** Speed limit decisions shall not discriminate based on geographic location, time of day, or other protected attributes beyond objective sensor data.
- **REQ-NFR-15 (Bias):** The training dataset shall represent at least 80% of documented highway conditions (weather, lighting, traffic patterns).

### Maintainability & Scalability
- **REQ-NFR-16 (Modifiability):** The neural network retraining pipeline shall support updates without system downtime.
- **REQ-NFR-17 (Testability):** At least 90% of the system code shall be covered by automated tests.
- **REQ-NFR-18 (Monitoring):** The system shall provide real-time dashboards showing prediction accuracy, sensor health, and decision distributions.
- **REQ-NFR-19 (Scalability):** The system shall support expansion to 1000+ highway sections with linear growth in computational resources.

### Usability & Transparency
- **REQ-NFR-20 (Transparency):** Regulatory authorities shall have access to model architecture, training data documentation, and decision logs.
- **REQ-NFR-21 (Intervenability):** Human operators shall be able to manually override AI decisions and set custom speed limits within <10 seconds.
- **REQ-NFR-22 (Energy Efficiency):** The system's computational infrastructure shall not exceed 50 kW average power consumption.

# slides:
System requirements (1 bullet)
Automatically adapt highway speed limits based on darkness/black ice risk, air quality, and a default of 80 km/h when no risk is detected.

Requirements specifications (1 bullet)
Define precise thresholds and rules (e.g., “dark” = illuminance < 500 millilux; black-ice risk = water > 1000 µm & temperature < 0 °C) and how NN/LLM use them.

Assumptions & rationales (1 bullet)
Assume sensors and external APIs are accurate and available; justify that dynamic speed limits reduce near-accidents while keeping traffic flow acceptable.

Nonfunctional requirements (1 bullet)
Ensure high reliability, low latency (few seconds), safety fallbacks, auditability, and EU AI Act–compliant logging and human override.


## Day1_Part5_Requirements_Documentation
Here’s how we can tackle this part for your SpeedLimit project.

Before I go into details: what’s your current level (Master in SE/AI, right?) and how familiar are you with terms like “glossary” and “natural language errors” in RE?

***

## 1. Glossary (excerpt for your spec)

| Term           | Description                                                                                                   | Synonyms                | Homonyms / Potential Confusion         |
|----------------|---------------------------------------------------------------------------------------------------------------|-------------------------|----------------------------------------|
| Black Ice      | A condition where a transparent layer of ice forms on the road surface. Defined in this project as water depth > 1000 µm combined with air temperature < 0°C. | Glatteis (German)       | "Ice" (generic frozen water)           |
| Darkness       | An environmental condition where illuminance is insufficient for optimal visibility. Defined in this project as illuminance < 500 millilux. | Low light, Nighttime    |                                        |
| Illuminance    | The measure of light falling on a surface, measured in millilux by highway sensors.                           | Brightness, Light Level | Luminance (light emitted/reflected)    |
| Near-Accident  | A traffic event involving a car skidding or coming dangerously close to another vehicle or guardrail without contact. | Close call, Near miss   | Accident (actual collision)            |
| Air Quality    | The condition of the air relative to pollution levels, retrieved via external API. Used as a decision factor for speed reduction (REQ2). | AQI (Air Quality Index) | Weather (rain/wind conditions)         |
| Sensor Reading | A data point generated by highway sensors (typically hourly), including speed limits (sensorID -1), weather, and traffic data. | Telemetry, Measurement  |                                        |
| Speed Limit    | The maximum legal speed allowed on a specific highway section, dynamically adjusted by the system. Default is 80 km/h. | Maximum speed           |                                        |
***

## 2. Remove typical natural language errors

We already avoid:
- **Nominalizations**: we use active verbs (“the system reduces…”, “the neural network learns…”).
- **Incompletely specified processes**: we name the actor (system, neural network, LLM).
- **Missing else**: REQ3 clearly defines what happens when REQ1 and REQ2 do not apply.
- **Universal quantifiers**: we don’t use vague “always”, “any”, “all” without conditions.

Original REQ1: "When it is dark or there is danger of black ice the speed limit on the highway shall be reduced..."
Refined REQ1 (Active Voice & Precise): "The system shall reduce the speed limit when the illuminance sensor detects values below 500 millilux OR when the water depth sensor detects > 1000 µm with temperatures < 0°C."

Original REQ2: "When poor air quality is predicted the speed limit on the highway shall be reduced in an appropriate way."
Refined REQ2 (Removing Vague "Appropriate Way"): "The LLM component shall query the external Air Quality API every 60 minutes. If the Air Quality Index (AQI) exceeds the defined threshold (e.g., AQI > 150), the system shall reduce the speed limit to the value recommended by the LLM's logic."

Original REQ3: "If there is no reason to reduce the speed limit because of REQ1 or REQ2, it is set to 80 km/h."
Refined REQ3 (Complete Condition): "If neither the conditions for REQ1 (darkness/ice) nor REQ2 (poor air quality) are met, the system shall set the speed limit to the default value of 80 km/h."
```md
REQ1: When it is dark or there is danger of black ice, the system shall reduce the speed limit on the highway so that the expected number of near-accidents does not exceed one per hour.
```

***

## 3. Add helpful tables

Example: clarify conditions and resulting speed limits.

```md
### Speed Limit Decision Table

| Condition                          | Applies? | Actor           | Resulting speed limit rule                        |
|------------------------------------|---------|-----------------|---------------------------------------------------|
| Dark OR danger of black ice       | Yes     | Neural network  | System reduces speed limit to meet REQ1.          |
| Poor air quality predicted        | Yes     | LLM             | System reduces speed limit as decided by LLM.     |
| Neither of the above conditions   | No      | Fixed logic     | System sets speed limit to 80 km/h (REQ3).        |
```

example 2. 
This table helps clarify the logic and avoids "missing else" or conflicting condition errors.​
```md
| Rule ID | Darkness (Illuminance < 500 mlx) | Black Ice Risk (Water > 1mm & Temp < 0°C) | Poor Air Quality (API Alert) | System Action                                    | Responsibility  |
| ------- | -------------------------------- | ----------------------------------------- | ---------------------------- | ------------------------------------------------ | --------------- |
| R1      | YES                              | -                                         | -                            | Reduce speed to target near-accident rate ≤ 1/hr | Neural Network  |
| R2      | -                                | YES                                       | -                            | Reduce speed to target near-accident rate ≤ 1/hr | Neural Network  |
| R3      | NO                               | NO                                        | YES                          | Reduce speed based on pollution severity         | LLM             |
| R4      | NO                               | NO                                        | NO                           | Maintain default speed (80 km/h)                 | Hardcoded Logic |
```
***
# slides: 
Glossary: Define key terms (e.g., “near-accident”, “black ice”, “illuminance”, “neural network”, “LLM”) so all stakeholders use the same language.
Natural language quality: Rewrite requirements to be clear, unambiguous, and active (named actor, clear conditions, no vague words like “often”, “quickly”).
Tables: Use decision tables (e.g., conditions vs. resulting speed limit) to structure complex logic and reduce misunderstandings.

## Day2_Part1_The_Importance_of_Testing_V702 
### Question_1:

The SpeedLimit project should have a router component that has three integers as its input parameters:
• illuminance in milllux
• water level on the highway in micrometers
• temperature in degrees Celsius

The component uses this input to decide whether the speed limit
should be reduced because of the weather, which is a binary result
(yes/no). Note that there are also other possible reasons to reduce the
speed limit (air quality), but that is outside the scope of this
component and its test.
Based on the requirements, write four test cases of which you think
they will find as many software defects as possible. The test cases
should be in the form of a table with five columns: test case ID, the
three input parameters, the expected output value. You don‘t need to
do negative testing.

```md
| Test Case ID | Illuminance (millilux) | Water Level (µm) | Temperature (°C) | Expected Output (Reduce Speed?) |
| ------------ | ---------------------- | ---------------- | ---------------- | ------------------------------- |
| TC01         | 499                    | 500              | 5                | Yes                             |
| TC02         | 600                    | 1001             | -1               | Yes                             |
| TC03         | 500                    | 1001             | 1                | No                              |
| TC04         | 600                    | 1000             | -5               | No                              |
```

Rationale for Test Cases:
TC01 (Darkness Boundary): Tests the "Darkness" condition. Illuminance is 499 (just below the 500 threshold), so it counts as "Dark". Even though there is no black ice risk (Temp > 0), the result must be Yes.
TC02 (Black Ice Condition): Tests the "Black Ice" condition. Illuminance is 600 (Not Dark), but Water is 1001 (> 1000) and Temp is -1 (< 0). Both black ice criteria are met, so result must be Yes.
TC03 (No Risk - Temp Boundary): Tests the "No Black Ice" boundary. Water is high (> 1000), but Temp is 1 (Not < 0). Illuminance is 500 (Not < 500, assuming < 500 is strict). Neither condition is met, so result must be No.
TC04 (No Risk - Water Boundary): Tests the "No Black Ice" boundary. Temp is low (-5), but Water is 1000 (Not > 1000, assuming > 1000 is strict). Illuminance is 600 (Not Dark). Neither condition is met, so result must be No.

### Question_2:

The SpeedLimit project should have an air quality component that asks an LLM about by how much to reduce the speed limit because of bad air quality.

Your job is to test this component based on the requirements.

How would you do that?

What would a test case look like?
- What is the input?
- Is there a golden answer?
- If so, where do you get it from?
- Write at least five test cases.

Based on the project requirements, here's how to test the LLM-based air quality component:

---

## Testing Approach for the LLM Air Quality Component

### Test Strategy
Since the LLM makes decisions without historical training data (reason it's used instead of ML), there is **no single "golden answer"** in the traditional sense. However, we can test for:[1]
- **Reasonableness**: The LLM's decision should be proportional to air quality severity
- **Consistency**: Similar inputs should produce similar outputs
- **Safety bounds**: Speed reductions should never be unsafe (e.g., reducing to 0 km/h or increasing speed)
- **Format compliance**: Output must be a valid speed reduction value

### Test Case Structure

| Test Case ID | Input: Air Quality Data (AQI + Context) | Expected Output Characteristics | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **TC-AQ-01** | AQI = 50 (Good), PM2.5 = 12 µg/m³, visibility = normal | **No reduction or minimal (0-5 km/h)** | LLM recommends ≤ 5 km/h reduction; justification mentions "good air quality" |
| **TC-AQ-02** | AQI = 150 (Unhealthy), PM2.5 = 55 µg/m³, visibility = moderate haze | **Moderate reduction (10-20 km/h)** | LLM recommends 10-20 km/h reduction; mentions visibility/health concerns |
| **TC-AQ-03** | AQI = 250 (Very Unhealthy), PM2.5 = 150 µg/m³, visibility = <500m | **Significant reduction (25-40 km/h)** | LLM recommends 25-40 km/h reduction; cites severe visibility impairment |
| **TC-AQ-04** | AQI = 350 (Hazardous), PM2.5 = 250 µg/m³, visibility = <200m, smog alert | **Major reduction (40-60 km/h)** | LLM recommends 40-60 km/h reduction; mentions emergency conditions |
| **TC-AQ-05** | AQI = 150 (repeat of TC-AQ-02) | **Consistent with TC-AQ-02 (±5 km/h)** | LLM produces similar result to TC-AQ-02 (tests consistency) |

### Input Details
- **Input format**: JSON or text prompt containing:
  - Current AQI value (0-500 scale)
  - Pollutant breakdown (PM2.5, PM10, O₃, NO₂, SO₂)
  - Visibility distance
  - Current speed limit (baseline 80 km/h)
  - Weather context if relevant

### Where to Get "Golden Answers"
Since there's no historical data, we establish golden answers through:
1. **Expert judgment**: Domain experts (traffic safety + environmental health) define reasonable ranges for each AQI band
2. **Regulatory guidelines**: Consult existing pollution-response protocols from similar highway systems
3. **LLM output validation**: Run the LLM multiple times and validate outputs fall within expert-defined acceptable ranges
4. **Oracle testing**: Compare LLM decisions against a simple rule-based oracle (e.g., "AQI 150-200 → reduce 15 km/h")

### Additional Test Cases (Boundary & Edge Cases)

| Test Case ID | Input: Air Quality Data | Expected Output Characteristics | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **TC-AQ-06** | AQI = 100 (Moderate, boundary) | **Small reduction (5-10 km/h)** | LLM handles boundary condition appropriately |
| **TC-AQ-07** | AQI = 301 (Hazardous threshold) | **Major reduction (35-50 km/h)** | LLM recognizes hazardous threshold crossing |
| **TC-AQ-08** | API returns error / null data | **Fallback behavior or error handling** | System defaults to no reduction OR alerts operator; does not crash |

This approach uses **metamorphic testing** (consistency across similar inputs) and **oracle approximation** (expert-defined acceptable ranges) since traditional golden answers don't exist for LLM-based reasoning components.



## Day2_Part4_Architectural_Quality_V702 
### Question_1:
## SpeedLimit Software Architecture Design
### Component Descriptions
1.  **Sensor Manager**: Collects raw data from highway sensors (illuminance, water level, temperature) and normalizes it for system use.
2.  **Air Quality Client**: Queries external APIs to retrieve current air quality index (AQI) and pollutant data.
3.  **Historical Data Storage**: A database storing past sensor logs, accident reports, and speed limit history for training purposes.
4.  **Data Preprocessor**: Cleans and formats historical data (e.g., labeling near-accidents) to prepare it for model training.
5.  **Model Trainer**: Uses preprocessed data to train and validate the neural network for accident prediction.
6.  **Trained Neural Network**: The deployable inference model that predicts accident risk based on darkness and weather conditions.
7.  **LLM Gateway**: Interfaces with the Large Language Model to get speed limit recommendations based on air quality data.
8.  **Decision Controller**: The core logic unit that orchestrates data flow, checks conditions (is it dark?), calls the appropriate AI model (NN vs. LLM), and determines the final speed limit.
9.  **Speed Limit Actuator**: Sends the final speed limit command to highway electronic signs and driver information systems.

### Architecture Visualization
### Component Cooperation
In the **Production Phase**, the **Sensor Manager** continuously streams road data to the **Decision Controller**. The Controller first checks if "Darkness" or "Black Ice" conditions are met.
*   If **YES**: It sends data to the **Trained Neural Network**, which predicts risk and suggests a speed limit reduction.
*   If **NO**: It triggers the **Air Quality Client** to check pollution levels. If high, it sends this context to the **LLM Gateway**, which returns a decision.
*   **Result**: The **Decision Controller** aggregates these outputs (prioritizing safety risks) and sends the final command to the **Speed Limit Actuator**.

Meanwhile, in the **Training Phase** (offline), the **Data Preprocessor** pulls logs from **Historical Data Storage** to update the **Model Trainer**, which periodically deploys a new **Trained Neural Network** to the production environment.

***

### Component Test Cases (5 per Component)
#### 1. Sensor Manager
| ID | Input | Expected Output |
| :--- | :--- | :--- |
| SM-01 | Raw illuminance: 400 mlx | Normalized: 400.0 (Valid) |
| SM-02 | Raw temp: -5°C | Normalized: -5.0 (Valid) |
| SM-03 | Connection timeout | Error Flag: "Sensor Offline" |
| SM-04 | Malformed data packet | Log error & discard |
| SM-05 | Max value (temp: 100°C) | Alert: "Sensor Malfunction" |

#### 2. Decision Controller
| ID | Input | Expected Output |
| :--- | :--- | :--- |
| DC-01 | Dark=True, NN_Speed=60 | Final Speed: 60 |
| DC-02 | Dark=False, Air=Bad, LLM_Speed=70 | Final Speed: 70 |
| DC-03 | Dark=True, NN=Fail | Fallback Speed: 60 |
| DC-04 | Dark=False, Air=Good | Final Speed: 80 (Default) |
| DC-05 | Emergency Override=True | Final Speed: Set by Operator |

#### 3. LLM Gateway
| ID | Input | Expected Output |
| :--- | :--- | :--- |
| LG-01 | AQI: 200 (Bad) | Reduction: 20 km/h |
| LG-02 | AQI: 50 (Good) | Reduction: 0 km/h |
| LG-03 | Prompt Injection Attack | Standard Refusal / Safe Default |
| LG-04 | Empty Context | Error: "Insufficient Data" |
| LG-05 | Ambiguous Response | Safe Default (e.g., 10 km/h red.) |

#### 4. Trained Neural Network
| ID | Input Vector | Expected Output |
| :--- | :--- | :--- |
| NN-01 | Dark/Wet/Cold | Risk: High -> Speed: 60 |
| NN-02 | Dark/Dry/Warm | Risk: Medium -> Speed: 70 |
| NN-03 | Boundary (Just Dark) | Risk: Low/Med -> Speed: 70 |
| NN-04 | Extreme Values | Risk: High -> Speed: 50 |
| NN-05 | All Zeros (Null) | Error / Default |

#### 5. Air Quality Client
| ID | Input | Expected Output |
| :--- | :--- | :--- |
| AC-01 | Valid API Key | JSON with AQI data |
| AC-02 | Invalid API Key | Auth Error Log |
| AC-03 | API Timeout | Retry / Cached Data |
| AC-04 | Bad Response Format | Parse Error Exception |
| AC-05 | Rate Limit Hit | Backoff Strategy Active |

***

### Adaptation to Change Requests
#### CR1: Some temperature sensors return Fahrenheit instead of Celsius.
*   **Adapted Component:** **Sensor Manager**
*   **Adaptation:** Add a conversion logic layer (`def normalize_temp(val, unit): if unit=='F' return (val-32)*5/9`). This ensures all downstream components (NN, Controller) still receive Celsius, preserving their logic without changes.

#### CR2: Only skidding counts as a near-accident.
*   **Adapted Component:** **Data Preprocessor**
*   **Adaptation:** Modify the labeling algorithm to filter historical accident logs. It currently flags "skidding OR proximity" as near-accidents; it must now strictly filter for `event_type == 'skidding'` before passing data to the Model Trainer. The **Model Trainer** will then produce a new model based on this stricter definition.

#### CR3: Electric cars are exempt from a speed limit caused by bad air quality.
*   **Adapted Component:** **Speed Limit Actuator** (and potentially digital signage infrastructure)
*   **Adaptation:** This is complex because the current *Speed Limit System* sets a global limit for the road section. To implement this, the **Speed Limit Actuator** must be updated to send "conditional" limits to digital signs (e.g., "80 km/h (EVs), 60 km/h (ICE)").
*   *Alternatively*: If the system communicates directly to cars, the **Decision Controller** would need to output a flagged message `{"speed": 60, "exempt_type": "EV"}`, which the Actuator broadcasts. The primary logic for *calculating* the reduction (LLM Gateway) stays the same, but the *enforcement/display* logic changes.

# slides:
Architecture Overview:
Nine-component system split into Training Phase (offline: data prep → model training) and Production Phase (real-time: sensors → decision → actuator).
Decision Controller orchestrates logic: if dark/ice → call Neural Network; else if bad air quality → call LLM Gateway; else → default 80 km/h.
Component Testing:
Test each component in isolation (Sensor Manager validates data, LLM Gateway handles edge cases, NN predicts risk, Actuator sends commands).
Focus on boundary conditions, error handling, and fallback behavior for safety-critical components.
Change Request Resilience:
Fahrenheit sensors: Add conversion layer in Sensor Manager (no downstream changes needed).
Skidding-only near-accidents: Retrain Neural Network with stricter data labels in Data Preprocessor.
EV exemptions from air quality limits: Extend Speed Limit Actuator to broadcast conditional speed limits (e.g., "80 km/h for EVs, 60 km/h for others").

## Day2_Part5_Architectural_Development_V702 (optional)
### Using AI to Develop an Architecture – the Embedding Approach
Feed embeddings of the functional SpeedLimit
requirements into a vector database. Have the
database cluster the requirements.
The result is – almost – an architecture
proposal for the architecture of SpeedLimit, as
each component should implement one of
those requirements clusters. Find good names
for the clusters = components.

### copying this is challanging but its basically nodes that are connected 
-> The lion sleeps tonight.
-> The tiger hunts all day.
-> Johann Sebastian Bach
lived from 1685 to 1750.


 ## Day3_Part1_Architecture_of_LLM_Powered_Applications_V707
### Full Implementation 
Implement the SpeedLimit Software in Python. You may try
vibe coding. The implementation should cover both
• the training stage in which you set up a neural network and train it
using the provided data after cleaning it and transforming it suitably
• and the operational stage in which the speed limit is set at a regular
basis. You don‘t need to buy any sensors, instead you create a GUI in
which to enter parameters like the temperature.
As this is a minimum viable product (MVP), you don‘t need deploy your
software to a high-performance environment.
Create a final presentation for management. It should also cover the
results of all other exercises concerning the SpeedLimit project.
Moreover, it should cover lessons learned.
