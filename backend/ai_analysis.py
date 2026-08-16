import json

from backend.tools import (
    get_incident,
    search_logs,
    get_metrics,
    get_deployments,
    read_repository_file,
)

from backend.llm import ask_llm


def build_incident_evidence():
    """Collect all relevant evidence for the incident."""

    incident = get_incident()

    logs = search_logs("connection")

    metrics = get_metrics()

    deployments = get_deployments()

    healthy_code = read_repository_file(
        "app/checkout.py"
    )

    incident_code = read_repository_file(
        "app/checkout_v1.8.3.py"
    )

    return {
        "incident": incident,
        "logs": logs,
        "metrics": metrics,
        "deployments": deployments,
        "healthy_code": healthy_code,
        "incident_code": incident_code,
    }


def clean_json_response(result):
    """Clean accidental Markdown code fences from LLM output."""

    result = result.strip()

    if result.startswith("```json"):
        result = result[len("```json"):].strip()

    elif result.startswith("```"):
        result = result[len("```"):].strip()

    if result.endswith("```"):
        result = result[:-3].strip()

    return result


def analyze_incident():
    """Collect evidence and return structured AI analysis."""

    evidence = build_incident_evidence()

    system_prompt = """
You are an expert production incident commander.

Investigate production incidents using ONLY the evidence
provided.

You must distinguish between:

OBSERVATION:
Something directly visible in logs, metrics, deployments,
or source code.

INFERENCE:
A conclusion logically derived from multiple observations.

HYPOTHESIS:
A possible root cause that still requires validation.

Compare the healthy implementation with the incident
implementation whenever both are provided.

Pay special attention to:

- resource cleanup
- connection lifecycle
- configuration changes
- error handling
- concurrency
- performance regressions

Do not invent facts.

Do not assign arbitrary percentage confidence.

Confidence must be exactly one of:

HIGH
MEDIUM
LOW

If the source code directly demonstrates a regression,
explicitly identify it.

Your response MUST be valid JSON.

Do not use Markdown.

Do not wrap the JSON in code fences.

Return exactly this structure:

{
  "summary": "short incident summary",
  "root_cause": "most likely root cause",
  "confidence": "HIGH",
  "evidence": [
    "evidence item 1",
    "evidence item 2",
    "evidence item 3"
  ],
  "code_regression": {
    "healthy_behavior": "what the healthy version does",
    "incident_behavior": "what the incident version does",
    "difference": "important difference"
  },
  "impact": "customer and system impact",
  "immediate_mitigation": "safest immediate action",
  "follow_up": [
    "follow-up action 1",
    "follow-up action 2",
    "follow-up action 3"
  ]
}
"""

    user_prompt = f"""
Investigate production incident
{evidence["incident"]["incident_id"]}.

========================
INCIDENT
========================

{evidence["incident"]}


========================
LOG EVIDENCE
========================

{evidence["logs"]}


========================
METRICS
========================

{evidence["metrics"]}


========================
DEPLOYMENTS
========================

{evidence["deployments"]}


========================
HEALTHY IMPLEMENTATION
========================

{evidence["healthy_code"]}


========================
INCIDENT IMPLEMENTATION
========================

{evidence["incident_code"]}


========================
ANALYSIS REQUIREMENTS
========================

Determine:

1. What is happening?

2. What are the strongest pieces of evidence?

3. What changed between the healthy implementation
   and v1.8.3?

4. How could that code change explain the production
   symptoms?

5. What is the most likely root cause?

6. What is the confidence level?

7. What is the production/customer impact?

8. What should the engineering team do immediately?

9. What should be investigated afterward?

Important:

Do not claim certainty beyond the evidence.

If the code directly demonstrates a regression,
explicitly mention it.
"""

    result = ask_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    result = clean_json_response(result)

    try:
        analysis = json.loads(result)

    except json.JSONDecodeError:
        raise ValueError(
            "Groq returned an invalid JSON response.\n\n"
            f"Raw response:\n{result}"
        )

    return analysis


def ask_incident_copilot(question):
    """
    Answer a user question using the incident evidence.
    """

    evidence = build_incident_evidence()

    system_prompt = """
You are an AI Production Incident Commander.

Answer questions using ONLY the incident evidence provided.

Available evidence includes:

- incident details
- production logs
- metrics
- deployment history
- healthy source code
- incident version source code

Do not invent facts.

If the evidence does not establish an answer, say:

"The available evidence does not establish this."

When explaining a root cause, distinguish between:

OBSERVATION:
Directly visible evidence.

INFERENCE:
A conclusion logically derived from evidence.

HYPOTHESIS:
A possible explanation that still requires validation.

Keep the answer concise, technically precise,
and useful to an engineer investigating the incident.

Do not return JSON.

Return a normal text answer.
"""

    user_prompt = f"""
You are investigating this production incident.

========================
INCIDENT
========================

{evidence["incident"]}


========================
LOG EVIDENCE
========================

{evidence["logs"]}


========================
METRICS
========================

{evidence["metrics"]}


========================
DEPLOYMENTS
========================

{evidence["deployments"]}


========================
HEALTHY IMPLEMENTATION
========================

{evidence["healthy_code"]}


========================
INCIDENT IMPLEMENTATION
========================

{evidence["incident_code"]}


========================
USER QUESTION
========================

{question}

Answer the user's question using only the evidence above.
"""

    return ask_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )


if __name__ == "__main__":

    print("\n==============================")
    print("AI INCIDENT COMMANDER")
    print("==============================")

    analysis = analyze_incident()

    print(
        json.dumps(
            analysis,
            indent=2,
        )
    )