import json
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

STATE_DIR = DATA_DIR / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

DEPLOYMENT_STATE_FILE = STATE_DIR / "deployment_state.json"


# ============================================================
# INCIDENT
# ============================================================

def get_incident():
    """Load the active incident."""

    incident_path = (
        DATA_DIR
        / "incidents"
        / "incident.json"
    )

    with open(
        incident_path,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# LOG SEARCH
# ============================================================

def search_logs(keyword=None):
    """Search checkout service logs for a keyword."""

    log_path = (
        DATA_DIR
        / "logs"
        / "checkout_api.log"
    )

    with open(
        log_path,
        "r",
        encoding="utf-8",
    ) as file:

        lines = file.readlines()

    if not keyword:

        return [
            line.strip()
            for line in lines
        ]

    keyword = keyword.lower()

    return [
        line.strip()
        for line in lines
        if keyword in line.lower()
    ]


# ============================================================
# DEPLOYMENT STATE
# ============================================================

def get_current_deployment():
    """
    Return the currently active deployment.

    If no runtime state exists, the incident deployment
    v1.8.3 is considered active.
    """

    if not DEPLOYMENT_STATE_FILE.exists():

        return "v1.8.3"

    try:

        with open(
            DEPLOYMENT_STATE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            state = json.load(file)

        return state.get(
            "active_version",
            "v1.8.3",
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):

        return "v1.8.3"


def set_current_deployment(version):
    """Persist the currently active deployment."""

    state = {
        "active_version": version
    }

    with open(
        DEPLOYMENT_STATE_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            state,
            file,
            indent=2,
        )


# ============================================================
# ROLLBACK
# ============================================================

def rollback_deployment(
    target_version="v1.8.2",
):
    """
    Simulate a production rollback.

    In this demo, rollback changes the active deployment
    and causes production metrics to recover.
    """

    set_current_deployment(
        target_version
    )

    return {
        "success": True,
        "previous_version": "v1.8.3",
        "current_version": target_version,
        "message": (
            f"Rollback completed successfully. "
            f"Active deployment is now {target_version}."
        ),
    }


# ============================================================
# METRICS
# ============================================================

def get_metrics():
    """
    Load checkout service metrics.

    If v1.8.3 is active, return incident metrics.

    If rollback has completed to v1.8.2, return recovered
    production metrics.
    """

    metrics_path = (
        DATA_DIR
        / "metrics"
        / "checkout_metrics.json"
    )

    with open(
        metrics_path,
        "r",
        encoding="utf-8",
    ) as file:

        metrics_data = json.load(file)

    current_deployment = (
        get_current_deployment()
    )

    # --------------------------------------------------------
    # INCIDENT STATE
    # --------------------------------------------------------

    if current_deployment == "v1.8.3":

        return metrics_data

    # --------------------------------------------------------
    # RECOVERED STATE
    # --------------------------------------------------------

    if current_deployment == "v1.8.2":

        recovered_metrics = {
            "normal_baseline": {
                "error_rate_percent": 0.0,
                "avg_latency_ms": 0,
                "db_connections": 0,
                "cpu_percent": 45,
            },
            "metrics": [
                {
                    "timestamp": "2026-08-16T10:40:00",
                    "error_rate_percent": 1.0,
                    "avg_latency_ms": 250,
                    "db_connections": 40,
                    "cpu_percent": 45,
                }
            ],
        }

        return recovered_metrics

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return metrics_data


# ============================================================
# DEPLOYMENT HISTORY
# ============================================================

def get_deployments():
    """Load deployment history."""

    deployment_path = (
        DATA_DIR
        / "deployments"
        / "deployment_history.json"
    )

    with open(
        deployment_path,
        "r",
        encoding="utf-8",
    ) as file:

        deployments = json.load(file)

    current_version = (
        get_current_deployment()
    )

    # --------------------------------------------------------
    # Support both list and dictionary formats
    # --------------------------------------------------------

    if isinstance(deployments, list):

        for deployment in deployments:

            if deployment.get(
                "version"
            ) == current_version:

                deployment["status"] = "ACTIVE"

            else:

                if deployment.get(
                    "status"
                ) == "ACTIVE":

                    deployment["status"] = "successful"

        return deployments

    # --------------------------------------------------------
    # Dictionary format
    # --------------------------------------------------------

    if isinstance(deployments, dict):

        if "deployments" in deployments:

            for deployment in deployments[
                "deployments"
            ]:

                if deployment.get(
                    "version"
                ) == current_version:

                    deployment["status"] = "ACTIVE"

                elif deployment.get(
                    "status"
                ) == "ACTIVE":

                    deployment["status"] = "successful"

        return deployments

    return deployments


# ============================================================
# REPOSITORY SEARCH
# ============================================================

def search_repository(keyword):
    """Search repository files for a keyword."""

    repository_path = (
        DATA_DIR
        / "repository"
        / "checkout_service"
    )

    results = []

    for file_path in repository_path.rglob("*"):

        if not file_path.is_file():
            continue

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            continue

        if keyword.lower() in content.lower():

            results.append(
                {
                    "file": str(
                        file_path.relative_to(
                            repository_path
                        )
                    ),
                    "match": keyword,
                }
            )

    return results


# ============================================================
# READ REPOSITORY FILE
# ============================================================

def read_repository_file(file_name):
    """Read a file from the checkout repository."""

    repository_path = (
        DATA_DIR
        / "repository"
        / "checkout_service"
    )

    file_path = (
        repository_path
        / file_name
    )

    if not file_path.exists():

        return {
            "error": f"File not found: {file_name}"
        }

    if not file_path.is_file():

        return {
            "error": f"Not a file: {file_name}"
        }

    return {
        "file": file_name,
        "content": file_path.read_text(
            encoding="utf-8"
        ),
    }