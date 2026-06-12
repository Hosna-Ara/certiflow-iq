# CertiFlow IQ

## Multi-Agent Certification Readiness System for Enterprise Teams

CertiFlow IQ is a multi-agent reasoning system built for the Reasoning Agents with Microsoft Foundry challenge. It helps organisations manage internal certification programmes by creating role-based study plans, assessing learner readiness, generating grounded practice questions, and giving managers team-level readiness insights.

## Core Users

- Learners preparing for role-based certifications
- Managers monitoring team certification readiness and risk

## Key Features

- Role-to-certification mapping
- Capacity-aware study planning
- Workload-based engagement recommendations
- Readiness assessment using score and study-hour thresholds
- Grounded practice questions from synthetic documents
- Manager-level team readiness insights
- Safety verifier for synthetic-data and privacy checks
- Streamlit dashboard for demo and visualisation
- Microsoft Foundry-ready architecture

## Multi-Agent System

1. Orchestrator Agent
2. Learning Path Curator Agent
3. Study Plan Generator Agent
4. Engagement Agent
5. Assessment Agent
6. Grounded Practice Question Agent
7. Manager Insights Agent
8. Safety / Verifier Agent

## Microsoft Foundry Setup

A Microsoft Foundry resource was successfully created.

- Resource name: certiflowAI
- Project: proj-default
- Resource group: rg-habegum-3396
- Region: Southeast Asia
- Subscription: Azure for Students

Model deployment was attempted, but the Azure for Students subscription showed insufficient quota for available chat model deployments. The current implementation runs locally while remaining ready for Foundry model integration once quota becomes available.

## Microsoft IQ Layer Mapping

### Foundry IQ
Synthetic certification documents are prepared as approved knowledge sources for grounded learning recommendations and cited practice questions.

### Fabric IQ
The semantic model represents relationships between learners, roles, certifications, skills, recommended study hours, and readiness thresholds.

### Work IQ
Synthetic workload signals represent organisational work context, including meeting hours, focus hours, and preferred learning slots.

## Data Notice

All data used in this project is synthetic and for demonstration only. No real employee data, customer data, credentials, or personally identifiable information are used.

## How to Run Locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py

## Demo Flow

1. Open the Streamlit dashboard.
2. View manager-level readiness summary.
3. Select a learner.
4. Review role-based learning path.
5. Review capacity-aware study plan.
6. Review grounded practice questions.
7. Review safety checks.
8. Inspect technical agent trace.

## Current Status

- Local multi-agent prototype: complete
- Streamlit dashboard: complete
- Synthetic data and documents: complete
- Foundry resource creation: complete
- Model deployment: blocked by Azure for Students quota
- Foundry-ready integration path: documented
