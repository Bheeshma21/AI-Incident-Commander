import streamlit as st

from backend.ai_analysis import analyze_incident
from backend.tools import (
    get_incident,
    get_metrics,
    get_deployments,
    search_logs,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Incident Commander",
    page_icon="🚨",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "rollback_completed" not in st.session_state:
    st.session_state.rollback_completed = False

if "active_deployment" not in st.session_state:
    st.session_state.active_deployment = None

if "incident_resolved" not in st.session_state:
    st.session_state.incident_resolved = False


# ============================================================
# LOAD DATA
# ============================================================

incident = get_incident()
metrics = get_metrics()
deployments = get_deployments()
logs = search_logs("connection")


# ============================================================
# DEPLOYMENT HELPERS
# ============================================================

def get_active_deployment(deployment_data):
    """
    Find the deployment marked ACTIVE.

    Supports:
    - list of deployments
    - {"deployments": [...]}
    - {"active_version": "..."}
    """

    if isinstance(deployment_data, list):

        for deployment in deployment_data:
            status = str(
                deployment.get("status", "")
            ).upper()

            if status == "ACTIVE":
                return deployment.get("version")

        if deployment_data:
            return deployment_data[-1].get("version")

    elif isinstance(deployment_data, dict):

        if "deployments" in deployment_data:
            return get_active_deployment(
                deployment_data["deployments"]
            )

        if "active_version" in deployment_data:
            return deployment_data["active_version"]

    return None


# ============================================================
# CURRENT DEPLOYMENT
# ============================================================

detected_deployment = get_active_deployment(
    deployments
)

if st.session_state.active_deployment is None:
    st.session_state.active_deployment = (
        detected_deployment
    )

active_deployment = (
    st.session_state.active_deployment
)

rollback_version = "v1.8.2"


# ============================================================
# METRICS
# ============================================================

baseline = metrics["normal_baseline"]

latest = metrics["metrics"][-1]

error_rate = latest["error_rate_percent"]
baseline_error = baseline["error_rate_percent"]

latency = latest["avg_latency_ms"]
baseline_latency = baseline["avg_latency_ms"]

db_connections = latest["db_connections"]
baseline_db = baseline["db_connections"]

cpu = latest["cpu_percent"]


# ============================================================
# RECOVERY CHECK
# ============================================================

# ============================================================
# POST-ROLLBACK RECOVERY BASELINE
# ============================================================
# These represent the known healthy production values
# after rollback to v1.8.2.

RECOVERY_BASELINE = {
    "error_rate_percent": 1.0,
    "avg_latency_ms": 250,
    "db_connections": 40,
}


error_recovered = (
    error_rate <= RECOVERY_BASELINE["error_rate_percent"]
)

latency_recovered = (
    latency <= RECOVERY_BASELINE["avg_latency_ms"]
)

db_recovered = (
    db_connections <= RECOVERY_BASELINE["db_connections"]
)


metrics_recovered = (
    error_recovered
    and latency_recovered
    and db_recovered
)

metrics_recovered = (
    error_recovered
    and latency_recovered
    and db_recovered
)


# ============================================================
# INCIDENT STATE
# ============================================================

rollback_completed = (
    st.session_state.rollback_completed
)

incident_resolved = (
    st.session_state.incident_resolved
)


# ============================================================
# HEADER
# ============================================================

st.title("🚨 AI Incident Commander")

st.caption(
    "AI-powered production incident investigation "
    "and response"
)

st.divider()


# ============================================================
# INCIDENT STATUS
# ============================================================

if incident_resolved:

    st.success(
        "🟢 INCIDENT RESOLVED — Production recovered"
    )

elif rollback_completed:

    st.warning(
        "🟡 INCIDENT MITIGATED — Rollback completed"
    )

else:

    st.error(
        "🔴 INCIDENT ACTIVE — Investigation in progress"
    )


# ============================================================
# INCIDENT INFORMATION
# ============================================================

st.subheader(
    f"Incident #{incident['incident_id']}"
)

st.write(
    f"**{incident['title']}**"
)

st.write(
    f"**Severity:** {incident['severity']}"
)

st.write(
    f"🚀 **Active Deployment:** "
    f"**{active_deployment or 'Unknown'}**"
)


st.divider()


# ============================================================
# PRODUCTION METRICS
# ============================================================

st.subheader("📊 Production Metrics")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Error Rate",
        f"{error_rate}%",
        f"{error_rate - baseline_error:.1f}%"
    )


with col2:

    st.metric(
        "Latency",
        f"{latency} ms",
        f"{latency - baseline_latency} ms"
    )


with col3:

    st.metric(
        "DB Connections",
        db_connections,
        db_connections - baseline_db
    )


with col4:

    st.metric(
        "CPU",
        f"{cpu}%"
    )


st.divider()


# ============================================================
# PRODUCTION EVIDENCE
# ============================================================

st.subheader(
    "📜 Production Evidence Timeline"
)

with st.expander(
    "View production logs",
    expanded=False
):

    if logs:

        for log in logs:

            st.code(
                log,
                language="text"
            )

    else:

        st.info(
            "No matching production logs found."
        )


# ============================================================
# DEPLOYMENT TIMELINE
# ============================================================

st.subheader(
    "🚀 Deployment Timeline"
)

with st.expander(
    "View deployment history",
    expanded=False
):

    if isinstance(deployments, list):

        for deployment in deployments:

            version = deployment.get(
                "version",
                "Unknown"
            )

            timestamp = deployment.get(
                "timestamp",
                ""
            )

            status = deployment.get(
                "status",
                ""
            )

            if str(status).upper() == "ACTIVE":

                st.success(
                    f"**{version}** | "
                    f"{timestamp} | "
                    f"**{status}**"
                )

            else:

                st.write(
                    f"**{version}** | "
                    f"{timestamp} | "
                    f"{status}"
                )

    else:

        st.json(deployments)


st.divider()


# ============================================================
# AI INVESTIGATION
# ============================================================

st.subheader(
    "🤖 AI Investigation"
)

if st.button(
    "🤖 Start AI Investigation",
    type="primary"
):

    with st.spinner(
        "AI is investigating the incident..."
    ):

        try:

            st.session_state.analysis = (
                analyze_incident()
            )

            st.success(
                "AI investigation completed."
            )

        except Exception as e:

            st.error(
                "AI investigation failed."
            )

            st.exception(e)


# ============================================================
# AI REPORT
# ============================================================

analysis = st.session_state.analysis


if analysis:

    st.divider()

    st.subheader(
        "📋 AI Investigation Report"
    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.markdown(
        "### 📋 Incident Summary"
    )

    st.write(
        analysis.get(
            "summary",
            "No summary available."
        )
    )


    # --------------------------------------------------------
    # ROOT CAUSE
    # --------------------------------------------------------

    st.markdown(
        "### 🎯 Root Cause"
    )

    st.write(
        analysis.get(
            "root_cause",
            "No root cause identified."
        )
    )


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    st.markdown(
        "### 🟢 Confidence"
    )

    confidence = analysis.get(
        "confidence",
        "UNKNOWN"
    )

    if confidence == "HIGH":

        st.success(confidence)

    elif confidence == "MEDIUM":

        st.warning(confidence)

    else:

        st.info(confidence)


    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    st.markdown(
        "### 🔍 Evidence"
    )

    evidence = analysis.get(
        "evidence",
        []
    )

    for item in evidence:

        st.markdown(
            f"✓ {item}"
        )


    # --------------------------------------------------------
    # CODE REGRESSION
    # --------------------------------------------------------

    st.markdown(
        "### 🔧 Code Regression"
    )

    regression = analysis.get(
        "code_regression",
        {}
    )


    st.markdown(
        "#### Healthy Implementation"
    )

    st.write(
        regression.get(
            "healthy_behavior",
            "Not available."
        )
    )


    st.markdown(
        "#### Incident Implementation"
    )

    st.write(
        regression.get(
            "incident_behavior",
            "Not available."
        )
    )


    st.markdown(
        "**Key Difference:**"
    )

    st.write(
        regression.get(
            "difference",
            "Not available."
        )
    )


    # --------------------------------------------------------
    # IMPACT
    # --------------------------------------------------------

    st.markdown(
        "### ⚠️ Customer Impact"
    )

    st.write(
        analysis.get(
            "impact",
            "No impact information available."
        )
    )


    # --------------------------------------------------------
    # MITIGATION
    # --------------------------------------------------------

    st.markdown(
        "### 🚑 Immediate Mitigation"
    )

    st.write(
        analysis.get(
            "immediate_mitigation",
            "No mitigation recommendation available."
        )
    )


    # --------------------------------------------------------
    # FOLLOW UP
    # --------------------------------------------------------

    st.markdown(
        "### 📋 Follow-up Investigation"
    )

    follow_up = analysis.get(
        "follow_up",
        []
    )

    for index, action in enumerate(
        follow_up,
        start=1
    ):

        st.markdown(
            f"**{index}.** {action}"
        )


st.divider()


# ============================================================
# INCIDENT RESPONSE ACTIONS
# ============================================================

st.subheader(
    "🛠️ Incident Response Actions"
)


# ============================================================
# ROLLBACK
# ============================================================

st.markdown(
    "### 🔴 Rollback"
)

st.write(
    "Restore the previous stable deployment:"
)

st.code(
    rollback_version
)


# ------------------------------------------------------------
# ROLLBACK ALREADY COMPLETED
# ------------------------------------------------------------

if rollback_completed:

    st.success(
        "✅ Rollback completed"
    )

    st.write(
        f"Current deployment: "
        f"**{active_deployment}**"
    )


# ------------------------------------------------------------
# ROLLBACK AVAILABLE
# ------------------------------------------------------------

else:

    if st.button(
        f"🔴 Roll back to {rollback_version}",
        type="secondary"
    ):

        # ----------------------------------------------------
        # Simulated rollback
        # ----------------------------------------------------

        st.session_state.rollback_completed = True

        st.session_state.active_deployment = (
            rollback_version
        )

        st.session_state.incident_resolved = False

        st.success(
            "✅ Rollback completed"
        )

        st.info(
            f"Current deployment: "
            f"**{rollback_version}**"
        )

        st.rerun()


# ============================================================
# POST-ROLLBACK RECOVERY
# ============================================================

if rollback_completed:

    st.divider()

    st.subheader(
        "📈 Post-Rollback Recovery"
    )

    st.write(
        "Verify that production metrics have "
        "returned toward the normal baseline."
    )


    recovery_col1, recovery_col2, recovery_col3, recovery_col4 = (
        st.columns(4)
    )


    # --------------------------------------------------------
    # ERROR RATE
    # --------------------------------------------------------

    with recovery_col1:

        if error_recovered:

            st.success(
                f"✅ Error Rate\n\n"
                f"{error_rate}%\n\n"
                f"Recovered"
            )

        else:

            st.error(
                f"❌ Error Rate\n\n"
                f"{error_rate}%\n\n"
                f"Not recovered"
            )


    # --------------------------------------------------------
    # LATENCY
    # --------------------------------------------------------

    with recovery_col2:

        if latency_recovered:

            st.success(
                f"✅ Latency\n\n"
                f"{latency} ms\n\n"
                f"Recovered"
            )

        else:

            st.error(
                f"❌ Latency\n\n"
                f"{latency} ms\n\n"
                f"Not recovered"
            )


    # --------------------------------------------------------
    # DB CONNECTIONS
    # --------------------------------------------------------

    with recovery_col3:

        if db_recovered:

            st.success(
                f"✅ DB Connections\n\n"
                f"{db_connections}\n\n"
                f"Recovered"
            )

        else:

            st.error(
                f"❌ DB Connections\n\n"
                f"{db_connections}\n\n"
                f"Not recovered"
            )


    # --------------------------------------------------------
    # DEPLOYMENT
    # --------------------------------------------------------

    with recovery_col4:

        if rollback_completed:

            st.success(
                f"✅ Deployment\n\n"
                f"{active_deployment}\n\n"
                f"Stable"
            )

        else:

            st.error(
                "❌ Deployment\n\n"
                "Rollback required"
            )


# ============================================================
# RESOLVE INCIDENT
# ============================================================

st.divider()

st.subheader(
    "🟢 Resolve Incident"
)


# ------------------------------------------------------------
# ALREADY RESOLVED
# ------------------------------------------------------------

if incident_resolved:

    st.success(
        "🟢 INCIDENT RESOLVED"
    )

    st.markdown(
        """
### 🎯 Incident Resolution

Rollback to **v1.8.2** completed successfully.

Production recovery was verified:

- ✅ Error Rate recovered
- ✅ Latency recovered
- ✅ Database Connections recovered
- ✅ Stable deployment confirmed

The incident is closed.
"""
    )


# ------------------------------------------------------------
# ROLLBACK REQUIRED
# ------------------------------------------------------------

elif not rollback_completed:

    st.warning(
        "⚠️ Rollback must be completed before "
        "the incident can be resolved."
    )


# ------------------------------------------------------------
# RECOVERY REQUIRED
# ------------------------------------------------------------

elif not metrics_recovered:

    st.warning(
        "⚠️ Recovery must be verified before "
        "the incident can be resolved."
    )

    st.write(
        "All production metrics must return "
        "to their normal baseline."
    )


# ------------------------------------------------------------
# READY TO RESOLVE
# ------------------------------------------------------------

else:

    st.success(
        "✅ All recovery checks passed."
    )

    if st.button(
        "🟢 Resolve Incident",
        type="primary"
    ):

        st.session_state.incident_resolved = True

        st.success(
            "🟢 INCIDENT RESOLVED"
        )

        st.balloons()

        st.rerun()


# ============================================================
# ROOT CAUSE SUMMARY
# ============================================================

if analysis:

    st.divider()

    st.subheader(
        "🎯 Root Cause Summary"
    )

    st.info(
        analysis.get(
            "root_cause",
            "Root cause unavailable."
        )
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Incident Commander • "
    "Evidence-driven production incident response"
)