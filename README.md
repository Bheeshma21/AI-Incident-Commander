# 🚨 AI Incident Commander

An AI-powered production incident investigation and response system that analyzes logs, metrics, deployment history, and source-code changes to identify probable root causes and guide incident remediation.

## 🎯 Problem

Production incidents often require engineers to manually correlate:

- Application logs
- Production metrics
- Deployment history
- Source-code changes
- Customer impact

This process can be slow during high-severity incidents.

AI Incident Commander automates this investigation workflow by collecting production evidence and using an LLM to generate an evidence-driven incident analysis.

## 🚀 Features

- 🔍 Production incident investigation
- 📜 Log evidence analysis
- 📊 Production metrics analysis
- 🚀 Deployment history analysis
- 🔧 Healthy vs incident code comparison
- 🧠 LLM-powered root-cause analysis
- 🎯 Confidence assessment
- ⚠️ Customer impact analysis
- 🔴 Rollback recommendation
- 📈 Post-rollback recovery verification
- 🟢 Incident resolution workflow

## 🏗️ Architecture

```text
Streamlit UI
     |
     v
Incident Controller
     |
     +------------------+------------------+
     |                  |                  |
     v                  v                  v
   Logs              Metrics         Deployments
     |                  |                  |
     +------------------+------------------+
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