import streamlit as st


def initialize_incident_state():
    """Initialize incident response state."""

    if "deployment_version" not in st.session_state:
        st.session_state.deployment_version = "v1.8.3"

    if "rollback_completed" not in st.session_state:
        st.session_state.rollback_completed = False

    if "recovery_verified" not in st.session_state:
        st.session_state.recovery_verified = False

    if "incident_resolved" not in st.session_state:
        st.session_state.incident_resolved = False


def rollback_incident():
    """Simulate rollback to the previous stable deployment."""

    st.session_state.deployment_version = "v1.8.2"

    st.session_state.rollback_completed = True

    st.session_state.recovery_verified = False

    st.session_state.incident_resolved = False


def get_current_metrics(original_metrics):
    """
    Return incident metrics before rollback
    and recovered metrics after rollback.
    """

    if st.session_state.rollback_completed:

        return {
            "error_rate_percent": 1.0,
            "avg_latency_ms": 250,
            "db_connections": 40,
            "cpu_percent": 45,
        }

    return {
        "error_rate_percent": original_metrics["error_rate_percent"],
        "avg_latency_ms": original_metrics["avg_latency_ms"],
        "db_connections": original_metrics["db_connections"],
        "cpu_percent": original_metrics["cpu_percent"],
    }


def verify_recovery():
    """
    Verify that production metrics have returned
    toward the normal baseline.
    """

    if not st.session_state.rollback_completed:
        return False

    st.session_state.recovery_verified = True

    return True


def resolve_incident():
    """Resolve only after rollback and recovery verification."""

    if (
        st.session_state.rollback_completed
        and st.session_state.recovery_verified
    ):
        st.session_state.incident_resolved = True
        return True

    return False