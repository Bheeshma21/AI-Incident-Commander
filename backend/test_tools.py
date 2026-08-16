from backend.tools import (
    get_incident,
    search_logs,
    get_metrics,
    get_deployments,
    search_repository,
    read_repository_file,
)


# -----------------------------
# Incident
# -----------------------------

incident = get_incident()

print("Incident ID:", incident["incident_id"])
print("Title:", incident["title"])
print("Severity:", incident["severity"])


# -----------------------------
# Logs
# -----------------------------

print("\n--- Log Search: connection ---")

results = search_logs("connection")

for result in results:
    print(result)


# -----------------------------
# Metrics
# -----------------------------

print("\n--- Metrics ---")

metrics = get_metrics()

print("Normal baseline:")
print(metrics["normal_baseline"])

print("\nLatest metrics:")
print(metrics["metrics"][-1])


# -----------------------------
# Deployments
# -----------------------------

print("\n--- Deployments ---")

deployments = get_deployments()

for deployment in deployments:
    print(
        deployment["version"],
        "|",
        deployment["deployed_at"],
        "|",
        deployment["status"],
    )


# -----------------------------
# Repository Search
# -----------------------------

print("\n--- Repository Search: connection ---")

repository_results = search_repository("connection")

for result in repository_results:
    print(result)


# -----------------------------
# Read Repository File
# -----------------------------

print("\n--- Read v1.8.3 Checkout Implementation ---")

file_result = read_repository_file(
    "app/checkout_v1.8.3.py"
)

if "error" in file_result:
    print(file_result["error"])
else:
    print(file_result["content"])
