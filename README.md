# 🚨 AI Incident Commander

An AI-powered production incident investigation and response system that analyzes logs, metrics, deployment history, and source-code changes to identify probable root causes and guide incident remediation.

## 🌐 Live Demo

**Streamlit App:**
https://ai-incident-commander-pd2yxdpz8tb9nfcu6yye4c.streamlit.app/

**GitHub Repository:**
https://github.com/Bheeshma21/AI-Incident-Commander

---

## 🎯 Problem

Production incidents often require engineers to manually correlate:

* Application logs
* Production metrics
* Deployment history
* Source-code changes
* Customer impact

This process can be slow during high-severity incidents.

AI Incident Commander automates this investigation workflow by collecting production evidence and using an LLM to generate an evidence-driven incident analysis.

---

## 🚀 Features

* 🔍 Production incident investigation
* 📜 Log evidence analysis
* 📊 Production metrics analysis
* 🚀 Deployment history analysis
* 🔧 Healthy vs incident code comparison
* 🧠 LLM-powered root-cause analysis
* 🎯 Confidence assessment
* ⚠️ Customer impact analysis
* 🔴 Rollback recommendation
* 📈 Post-rollback recovery verification
* 🟢 Incident resolution workflow

---

## 🏗️ Architecture

```text
                         Streamlit UI
                              |
                              v
                    Incident Controller
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
        Logs               Metrics           Deployments
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                    Source Code Analysis
                    Healthy vs Incident
                              |
                              v
                             LLM
                    Root Cause Analysis
                              |
                              v
                    Incident Response
                    Rollback + Recovery
```

---

## 🔄 Incident Investigation Workflow

The application follows an evidence-driven investigation pipeline:

```text
1. Load incident
       ↓
2. Collect production logs
       ↓
3. Analyze production metrics
       ↓
4. Review deployment history
       ↓
5. Compare healthy and incident code
       ↓
6. Send correlated evidence to LLM
       ↓
7. Generate root-cause analysis
       ↓
8. Recommend immediate mitigation
       ↓
9. Roll back deployment
       ↓
10. Verify production recovery
       ↓
11. Resolve incident
```

---

## 🤖 AI Investigation

The LLM receives multiple evidence sources rather than relying on a single signal.

The investigation considers:

* Production log patterns
* Error rates
* Latency
* Database connection usage
* Deployment changes
* Healthy implementation
* Incident implementation
* Customer impact

The generated investigation includes:

* Incident summary
* Probable root cause
* Confidence level
* Supporting evidence
* Code regression analysis
* Customer impact
* Immediate mitigation
* Follow-up investigation actions

The application currently uses the Groq API with:

```text
GROQ_MODEL=openai/gpt-oss-120b
```

---

## 🚨 Example Incident

### Incident #INC-1042

**Service:** Checkout API
**Severity:** SEV-2
**Incident Version:** v1.8.3
**Healthy Version:** v1.8.2

The incident simulates elevated HTTP 500 errors and increased latency following deployment of `v1.8.3`.

### Root Cause

The refactored `process_checkout` implementation does not close the database connection in a `finally` block.

This causes database connections to remain open, eventually exhausting the connection pool.

### Evidence

The AI investigation correlates:

* Database connection pool utilization
* Connection acquisition timeouts
* HTTP 500 errors
* Increased latency
* Deployment history
* Healthy vs incident source-code differences

### Mitigation

The system recommends rolling back to:

```text
v1.8.2
```

After rollback, the application verifies:

* Error rate recovery
* Latency recovery
* Database connection recovery
* Stable deployment

The incident can then be marked as resolved.

---

## 🔴 Incident Response Workflow

The application supports a complete incident lifecycle:

```text
Incident Detected
       ↓
AI Investigation
       ↓
Root Cause Identified
       ↓
Rollback Recommended
       ↓
Rollback Executed
       ↓
Recovery Verified
       ↓
Incident Resolved
```

The rollback mechanism updates the active deployment state and the recovery stage verifies that the expected production state has been restored.

---

## 🛠️ Tech Stack

### Application

* Python
* Streamlit

### AI

* Groq API
* `openai/gpt-oss-120b`
* Evidence-driven LLM prompting

### Data

* JSON
* Production logs
* Deployment history
* Production metrics
* Source-code snapshots

### Testing

* Pytest

---

## 📁 Project Structure

```text
AI-Incident-Commander/
│
├── app/
│   └── main.py
│
├── backend/
│   ├── ai_analysis.py
│   ├── incident_state.py
│   ├── investigator.py
│   ├── llm.py
│   ├── tools.py
│   ├── test_llm.py
│   └── test_tools.py
│
├── data/
│   ├── deployments/
│   ├── incidents/
│   ├── logs/
│   ├── metrics/
│   ├── repository/
│   └── state/
│
├── requirements.txt
├── README.md
├── SUBMISSION.md
└── .gitignore
```

---

## ⚙️ Local Setup

Clone the repository:

```bash
git clone https://github.com/Bheeshma21/AI-Incident-Commander.git
cd AI-Incident-Commander
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

**Never commit the `.env` file or your API key to GitHub.**

The repository ignores `.env` through `.gitignore`.

For Streamlit Cloud, configure the same values through the application's **Secrets** settings.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app/main.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

## 🧪 Run Tests

Run the complete test suite:

```bash
pytest
```

The project includes tests for:

* LLM integration
* Checkout service behavior

The expected result is:

```text
2 passed
```

---

## 📊 Expected Result

After starting the application and running the investigation, the AI should identify the database connection leak as the probable root cause.

The investigation should connect:

```text
v1.8.3 deployment
       ↓
Missing connection.close()
       ↓
Leaked DB connections
       ↓
Connection pool exhaustion
       ↓
HTTP 500 errors + latency increase
       ↓
Rollback to v1.8.2
       ↓
Production recovery
```

---

## 📸 Screenshots

Add screenshots of the deployed application here before final submission.

Recommended screenshots:

1. Incident overview and production metrics
2. AI Investigation Report
3. Code Regression comparison
4. Rollback completed
5. Production recovery
6. Incident resolved

---

## 🎯 Project Goal

AI Incident Commander demonstrates how AI can assist production engineers by correlating multiple operational evidence sources and turning them into an actionable incident investigation.

The goal is not simply to generate an LLM response, but to provide an evidence-driven workflow from:

**Detection → Investigation → Root Cause → Mitigation → Recovery → Resolution**

---

## 👨‍💻 Author

**Bheeshma Reddy**

AI/ML Engineer | Python | Machine Learning | LLM Applications
