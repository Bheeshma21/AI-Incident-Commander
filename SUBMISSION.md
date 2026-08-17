\# 🚨 AI Incident Commander



\## Assignment Submission



\*\*Live Demo:\*\*

https://ai-incident-commander-pd2yxdpz8tb9nfcu6yye4c.streamlit.app/



\*\*GitHub Repository:\*\*

https://github.com/Bheeshma21/AI-Incident-Commander



\---



\# 1. Project Overview



AI Incident Commander is an AI-powered production incident investigation and response system.



The system helps engineers investigate production incidents by correlating:



\* Application logs

\* Production metrics

\* Deployment history

\* Source-code changes

\* Customer impact

\* Recovery status



It uses an LLM to analyze the collected evidence and produce an evidence-driven incident investigation report.



The system also supports incident mitigation through rollback, verifies production recovery, and allows the incident to be resolved only after recovery checks pass.



\---



\# 2. Problem Statement



Production incidents often require engineers to manually investigate multiple sources of information.



During a high-severity incident, engineers may need to correlate:



1\. Application logs

2\. Database and service metrics

3\. Recent deployments

4\. Source-code changes

5\. Customer impact

6\. Recovery status



This investigation can be slow and error-prone.



AI Incident Commander provides a centralized investigation workflow that collects the available evidence and uses AI to identify the most likely root cause.



\---



\# 3. System Architecture



```text

&#x20;                    ┌─────────────────────┐

&#x20;                    │    Streamlit UI     │

&#x20;                    │  Incident Console   │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;                               ▼

&#x20;                    ┌─────────────────────┐

&#x20;                    │ Incident Controller │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;              ┌────────────────┼────────────────┐

&#x20;              ▼                ▼                ▼

&#x20;        ┌──────────┐     ┌──────────┐     ┌─────────────┐

&#x20;        │   Logs   │     │ Metrics  │     │ Deployments │

&#x20;        └──────────┘     └──────────┘     └─────────────┘

&#x20;              │                │                │

&#x20;              └────────────────┼────────────────┘

&#x20;                               ▼

&#x20;                    ┌─────────────────────┐

&#x20;                    │ Source Code Analysis│

&#x20;                    │ Healthy vs Incident │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;                               ▼

&#x20;                    ┌─────────────────────┐

&#x20;                    │        LLM          │

&#x20;                    │ Root Cause Analysis │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;                               ▼

&#x20;                    ┌─────────────────────┐

&#x20;                    │ Incident Response   │

&#x20;                    │ Rollback + Recovery │

&#x20;                    └─────────────────────┘

```



\---



\# 4. Incident Investigation Workflow



The system follows an evidence-first workflow.



\## Step 1 — Load Incident



The system loads the active incident from the incident data source.



Example:



\* Incident: `INC-1042`

\* Service: `checkout-service`

\* Severity: `SEV-2`

\* Problem: Checkout API elevated 500 errors



\---



\## Step 2 — Collect Log Evidence



The system searches production logs for relevant keywords.



For this incident, the investigation searches for database connection evidence.



The logs show:



\* Connection pool usage increased from 78% to 93%

\* Database connection acquisition timed out

\* Checkout processing failed because the connection pool was exhausted



These are direct observations from the supplied production evidence.



\---



\## Step 3 — Analyze Metrics



The system compares production metrics against the available baseline.



The incident evidence shows:



\* Increased database connections

\* Elevated error rate

\* Increased latency



The metrics support the connection-pool exhaustion hypothesis.



\---



\## Step 4 — Analyze Deployment History



The system checks recent deployments.



The incident occurred after:



\*\*v1.8.3\*\*



The deployment included changes related to:



\* Database connection handling

\* Checkout database performance



This makes `v1.8.3` a relevant investigation target.



\---



\## Step 5 — Compare Source Code



The system compares the healthy implementation with the incident implementation.



The healthy version contains:



```python

finally:

&#x20;   connection.close()

```



The incident implementation does not contain the connection cleanup.



This is a direct source-code regression.



\---



\## Step 6 — Determine Root Cause



The evidence forms a consistent chain:



```text

v1.8.3 deployment

&#x20;      ↓

Database connection cleanup removed

&#x20;      ↓

Connections remain open

&#x20;      ↓

Connection pool usage increases

&#x20;      ↓

Connection acquisition timeouts

&#x20;      ↓

Checkout requests fail

&#x20;      ↓

500 errors + increased latency

```



The most likely root cause is therefore:



\*\*Database connection leakage caused by missing connection cleanup in v1.8.3.\*\*



The confidence level is \*\*HIGH\*\* because the source-code regression directly demonstrates the missing cleanup and the production logs show connection pool exhaustion.



\---



\# 5. AI Investigation



The LLM receives structured evidence containing:



\* Incident details

\* Logs

\* Metrics

\* Deployment history

\* Healthy source code

\* Incident source code



The AI is explicitly instructed to:



\* Use only supplied evidence

\* Avoid inventing facts

\* Distinguish observations from inference and hypotheses

\* Compare healthy and incident implementations

\* Identify source-code regressions

\* Use HIGH, MEDIUM, or LOW confidence

\* Return structured JSON



The current AI integration uses the \*\*Groq API\*\* with:



```text

Model: openai/gpt-oss-120b

```



This makes the AI analysis evidence-driven and auditable rather than relying only on a general-purpose LLM response.



\---



\# 6. Product Strategy A — Incident Investigation Copilot



\## Strategy



The first product strategy is to position AI Incident Commander as an \*\*Incident Investigation Copilot\*\*.



The system does not replace the production engineer.



Instead, it reduces the amount of manual investigation required during an incident.



\## Target Users



\* SRE engineers

\* DevOps engineers

\* Backend engineers

\* Platform engineering teams

\* Engineering managers



\## Core Value



The product reduces the time required to correlate production evidence.



Instead of manually opening multiple systems, an engineer can use a centralized incident console.



\## Key Capabilities



\* Evidence collection

\* Log analysis

\* Metrics analysis

\* Deployment correlation

\* Source-code comparison

\* AI root-cause analysis

\* Confidence assessment

\* Incident timeline



\## Product Advantage



The important differentiator is not simply using an LLM.



The system grounds the LLM in actual incident evidence before generating the analysis.



This reduces unsupported AI conclusions and makes the investigation easier to review.



\---



\# 7. Product Strategy B — Automated Incident Response Platform



\## Strategy



The second product strategy is to evolve the system from an investigation copilot into an \*\*automated incident response platform\*\*.



The investigation system can become the decision layer for controlled remediation workflows.



\## Potential Capabilities



\* Automated incident detection

\* Evidence collection

\* Root-cause investigation

\* Rollback recommendation

\* Approval-based rollback

\* Recovery verification

\* Incident resolution

\* Post-incident report generation

\* Audit trail



\## Safety Model



Production-changing actions should not initially be fully autonomous.



A safer progression is:



```text

AI detects incident

&#x20;      ↓

AI collects evidence

&#x20;      ↓

AI recommends action

&#x20;      ↓

Engineer approves

&#x20;      ↓

System performs rollback

&#x20;      ↓

System verifies recovery

&#x20;      ↓

Incident resolved

```



This provides automation while keeping humans in control of high-impact production actions.



\## Long-Term Opportunity



The platform could integrate with:



\* CI/CD systems

\* Kubernetes

\* Cloud monitoring

\* Application logs

\* Databases

\* Alerting systems

\* Incident-management platforms



This would allow the product to move from a demonstration system toward a production-grade incident response platform.



\---



\# 8. Decision-Making Explanation



The system follows an evidence-driven decision process.



\## Decision 1 — Identify the Incident Signal



The first signal is elevated Checkout API failures.



The system does not immediately assume a root cause.



It collects additional evidence.



\---



\## Decision 2 — Correlate Logs and Metrics



The logs show database connection pool exhaustion.



The metrics show increased database connections and elevated error rate.



Together, these observations make database connection handling a strong investigation target.



\---



\## Decision 3 — Correlate With Deployment



The deployment timeline shows that `v1.8.3` was deployed before the incident.



The deployment specifically changed database connection handling.



Therefore, `v1.8.3` becomes the primary regression candidate.



\---



\## Decision 4 — Validate Against Source Code



The healthy implementation closes the connection in a `finally` block.



The incident implementation does not.



This directly demonstrates the code regression.



Therefore, the root-cause confidence is \*\*HIGH\*\*.



\---



\## Decision 5 — Select Mitigation



The safest immediate mitigation is to roll back to the previous stable version, `v1.8.2`.



The system does not recommend making an unvalidated code change during an active SEV-2 incident.



Rollback provides a controlled way to restore the previously stable implementation.



\---



\## Decision 6 — Verify Recovery



Rollback alone is not considered sufficient.



The system checks recovery indicators:



\* Error rate

\* Latency

\* Database connections

\* Active deployment



Only after recovery checks pass can the incident be resolved.



This creates the following safety condition:



```text

Rollback

&#x20;  ↓

Recovery verification

&#x20;  ↓

All checks pass

&#x20;  ↓

Incident can be resolved

```



\---



\# 9. Incident Response Lifecycle



The complete lifecycle is:



```text

Incident Detected

&#x20;      ↓

Evidence Collection

&#x20;      ↓

AI Investigation

&#x20;      ↓

Root Cause Identification

&#x20;      ↓

Mitigation Recommendation

&#x20;      ↓

Rollback

&#x20;      ↓

Recovery Verification

&#x20;      ↓

Incident Resolution

```



The application prevents incident resolution when rollback or recovery verification has not been completed.



\---



\# 10. Reliability Considerations



The LLM layer includes retry handling for transient failures.



The application also validates the returned AI response as JSON before using the analysis.



If the LLM returns invalid JSON, the application raises an explicit error instead of silently accepting malformed data.



This is important because AI output should not be treated as reliable structured data without validation.



The application also checks for required configuration such as the Groq API key before attempting AI analysis.



\---



\# 11. Testing



The project includes automated tests using `pytest`.



The current test suite covers:



\* LLM integration

\* Checkout service behavior



Latest test result:



```text

=============================================

2 passed in 2.60s

=============================================

```



The LLM integration test verifies that the configured Groq model can successfully generate a response.



The checkout service test verifies that the checkout implementation behaves as expected.



Python compilation checks were also performed on the relevant Python modules.



\---



\# 12. Technology Stack



\## Frontend



\* Streamlit



\## Backend



\* Python



\## AI



\* Groq API

\* `openai/gpt-oss-120b`



\## Configuration



\* python-dotenv



\## Testing



\* pytest



\## Version Control



\* Git

\* GitHub



\---



\# 13. Project Structure



```text

AI-Incident-Commander/

│

├── app/

│   └── main.py

│

├── backend/

│   ├── \_\_init\_\_.py

│   ├── ai\_analysis.py

│   ├── incident\_state.py

│   ├── investigator.py

│   ├── llm.py

│   ├── tools.py

│   ├── test\_llm.py

│   └── test\_tools.py

│

├── data/

│   ├── incidents/

│   ├── logs/

│   ├── metrics/

│   ├── deployments/

│   ├── repository/

│   └── state/

│

├── requirements.txt

├── README.md

├── SUBMISSION.md

└── .gitignore

```



\---



\# 14. Incident Demonstration — INC-1042



The demonstration incident is:



\*\*Incident:\*\* `INC-1042`



\*\*Service:\*\* Checkout API



\*\*Severity:\*\* SEV-2



\*\*Initial deployment:\*\* `v1.8.3`



\*\*Stable deployment:\*\* `v1.8.2`



\## Observed Symptoms



\* Elevated HTTP 500 errors

\* Increased API latency

\* Increased database connection usage

\* Database connection pool exhaustion

\* Connection acquisition timeouts



\## Root Cause



\*\*Missing `connection.close()` in the refactored `process\_checkout` implementation introduced in `v1.8.3`.\*\*



The missing cleanup caused database connections to remain open, eventually exhausting the connection pool.



\## Confidence



\*\*HIGH\*\*



The conclusion is supported by:



\* Production logs

\* Production metrics

\* Deployment history

\* Healthy source implementation

\* Incident source implementation



\## Immediate Mitigation



Rollback to:



```text

v1.8.2

```



\## Recovery Verification



After rollback, the application verifies:



\* Error rate recovery

\* Latency recovery

\* Database connection recovery

\* Stable deployment



\## Final State



```text

INCIDENT RESOLVED

```



The incident is resolved only after the recovery checks pass.



\---



\# 15. Evidence-Based Technical Decision



The system does not identify the root cause from a single signal.



Instead, it correlates multiple independent evidence sources.



```text

Logs

&#x20; +

Metrics

&#x20; +

Deployment History

&#x20; +

Source-Code Difference

&#x20; =

High-Confidence Root Cause

```



For INC-1042:



```text

Logs

→ Connection pool exhaustion



Metrics

→ Increased DB connections + increased errors + increased latency



Deployment

→ v1.8.3 changed database connection handling



Code comparison

→ connection.close() removed



Conclusion

→ Database connection leak

```



This evidence chain is the core design principle of AI Incident Commander.



\---



\# 16. Future Improvements



A production-ready version could add:



1\. Real-time monitoring integrations

2\. Kubernetes deployment inspection

3\. Prometheus/Grafana metrics

4\. GitHub/GitLab commit analysis

5\. Automated incident timelines

6\. Human approval workflows

7\. Persistent incident history

8\. LLM evaluation and regression testing

9\. Audit logging

10\. Role-based access control

11\. Automated postmortem generation

12\. Integration with PagerDuty or similar incident-management platforms



\---



\# 17. Final Outcome



AI Incident Commander successfully demonstrates an evidence-driven production incident workflow.



For Incident `INC-1042`, the system identifies:



\*\*Root Cause:\*\*

Database connection leak caused by missing connection cleanup in `v1.8.3`.



\*\*Confidence:\*\*

HIGH



\*\*Mitigation:\*\*

Rollback to `v1.8.2`.



\*\*Recovery:\*\*

Production recovery is verified using error rate, latency, database connections, and deployment state.



\*\*Resolution:\*\*

The incident can be resolved only after recovery checks pass.



The project demonstrates how an AI system can assist engineers with production incident investigation while keeping remediation decisions controlled and evidence-based.



\---



\# 18. Submission Summary



The project demonstrates:



\* Production incident investigation

\* Evidence collection

\* Log analysis

\* Metrics analysis

\* Deployment analysis

\* Source-code regression detection

\* LLM-powered root-cause analysis

\* Confidence assessment

\* Customer-impact analysis

\* Rollback workflow

\* Recovery verification

\* Controlled incident resolution

\* LLM integration testing

\* Automated testing

\* Streamlit deployment

\* Documentation

\* Product strategy

\* Evidence-based technical decision making



\---



\# 19. Demo Links



\*\*Live Streamlit Application\*\*



https://ai-incident-commander-pd2yxdpz8tb9nfcu6yye4c.streamlit.app/



\*\*GitHub Repository\*\*



https://github.com/Bheeshma21/AI-Incident-Commander



\---



\# 20. Conclusion



AI Incident Commander demonstrates a practical approach to using AI for production incident investigation.



Instead of asking an LLM to guess the cause of an incident, the system first collects and correlates operational evidence, including logs, metrics, deployments, and source-code differences.



The LLM then analyzes this structured evidence and produces a root-cause assessment with confidence, evidence, customer impact, mitigation, and follow-up recommendations.



The incident-response workflow extends beyond diagnosis by supporting rollback and recovery verification.



For the demonstrated SEV-2 checkout incident, the system successfully identifies the database connection leak introduced in `v1.8.3`, recommends rollback to `v1.8.2`, verifies recovery, and reaches a controlled incident resolution state.



The project therefore demonstrates both the technical implementation and the product direction of an evidence-driven AI incident response system.



