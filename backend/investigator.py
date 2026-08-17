from backend.tools import (
    get_incident,
    search_logs,
    get_metrics,
    get_deployments,
    search_repository,
    read_repository_file,
)


def investigate_incident():
    """Run an evidence-based incident investigation."""

    incident = get_incident()

    print("\n==============================")
    print("AI INCIDENT INVESTIGATION")
    print("==============================")

    # -----------------------------
    # Incident
    # -----------------------------

    print(f"\nIncident: {incident['incident_id']}")
    print(f"Service: {incident['service']}")
    print(f"Severity: {incident['severity']}")
    print(f"Title: {incident['title']}")

    # -----------------------------
    # 1. Log Evidence
    # -----------------------------

    print("\n[1] LOG EVIDENCE")

    log_results = search_logs("connection")

    for log in log_results[:5]:
        print("-", log)

    # -----------------------------
    # 2. Metrics Evidence
    # -----------------------------

    print("\n[2] METRIC EVIDENCE")

    metrics = get_metrics()

    baseline = metrics["normal_baseline"]
    latest = metrics["metrics"][-1]

    print(
        f"DB connections: "
        f"{baseline['db_connections']} -> "
        f"{latest['db_connections']}"
    )

    print(
        f"Error rate: "
        f"{baseline['error_rate_percent']}% -> "
        f"{latest['error_rate_percent']}%"
    )

    print(
        f"Latency: "
        f"{baseline['avg_latency_ms']}ms -> "
        f"{latest['avg_latency_ms']}ms"
    )

    # -----------------------------
    # 3. Deployment Evidence
    # -----------------------------

    print("\n[3] DEPLOYMENT EVIDENCE")

    deployments = get_deployments()

    latest_deployment = deployments[-1]

    print(
        f"Latest deployment: "
        f"{latest_deployment['version']}"
    )

    print(
        f"Deployed at: "
        f"{latest_deployment['deployed_at']}"
    )

    print("Changes:")

    for change in latest_deployment["changes"]:
        print("-", change)

    # -----------------------------
    # 4. Repository Evidence
    # -----------------------------

    print("\n[4] REPOSITORY EVIDENCE")

    repository_results = search_repository("close")

    for result in repository_results:
        print("-", result["file"])

    # -----------------------------
    # 5. Compare Code Versions
    # -----------------------------

    print("\n[5] CODE COMPARISON")

    healthy_code = read_repository_file(
        "app/checkout.py"
    )

    incident_code = read_repository_file(
        "app/checkout_v1.8.3.py"
    )

    print("\n--- Healthy implementation ---")

    if "error" in healthy_code:
        print(healthy_code["error"])
    else:
        print(healthy_code["content"])

    print("\n--- v1.8.3 implementation ---")

    if "error" in incident_code:
        print(incident_code["error"])
    else:
        print(incident_code["content"])

    # -----------------------------
    # 6. Connection Cleanup Analysis
    # -----------------------------

    print("\n[6] CONNECTION CLEANUP ANALYSIS")

    if "error" not in healthy_code and "error" not in incident_code:

        healthy_has_cleanup = (
            "connection.close()" in healthy_code["content"]
        )

        incident_has_cleanup = (
            "connection.close()" in incident_code["content"]
        )

        print(
            "Healthy version closes connection:",
            healthy_has_cleanup
        )

        print(
            "v1.8.3 closes connection:",
            incident_has_cleanup
        )

    else:
        healthy_has_cleanup = False
        incident_has_cleanup = False

    # -----------------------------
    # 7. Root Cause Hypothesis
    # -----------------------------

    print("\n==============================")
    print("ROOT-CAUSE HYPOTHESIS")
    print("==============================")

    if healthy_has_cleanup and not incident_has_cleanup:

        print(
            "v1.8.3 removed database connection cleanup "
            "from the checkout flow."
        )

        print(
            "This can cause database connections to remain "
            "open and eventually exhaust the connection pool."
        )

        print(
            "This is consistent with the observed increase "
            "in database connections and checkout 500 errors."
        )

        print(
            "\nConfidence: HIGH"
        )

    else:

        print(
            "The available evidence does not yet establish "
            "a clear connection cleanup regression."
        )

        print(
            "\nConfidence: LOW"
        )


if __name__ == "__main__":
    investigate_incident()
