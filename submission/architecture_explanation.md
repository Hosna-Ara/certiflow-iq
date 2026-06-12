# CertiFlow IQ Architecture

## Overview

CertiFlow IQ is a multi-agent certification readiness system for enterprise teams. It supports learners and managers by combining role-based learning paths, capacity-aware study planning, grounded practice questions, readiness assessment, and manager-level risk insights.

## Architecture Flow

User Request
→ Orchestrator Agent
→ Learning Path Curator Agent
→ Study Plan Generator Agent
→ Engagement Agent
→ Assessment Agent
→ Grounded Practice Question Agent
→ Manager Insights Agent
→ Safety / Verifier Agent
→ Streamlit Dashboard

## Microsoft Foundry Integration

A Microsoft Foundry resource was created successfully:

- Resource name: certiflowAI
- Project: proj-default
- Resource group: rg-habegum-3396
- Region: Southeast Asia
- Subscription: Azure for Students

The project is designed to be Foundry-ready. The current local implementation can later connect to a deployed Foundry model once model quota becomes available.

## Microsoft IQ Layer Mapping

### Foundry IQ
Synthetic certification documents are prepared as approved knowledge sources for grounding learning content and practice questions.

### Fabric IQ
The semantic model represents business relationships between learners, roles, certifications, skills, recommended study hours, and readiness thresholds.

### Work IQ
Synthetic workload signals represent work context such as meeting hours, focus hours, and preferred learning slots. These signals guide study planning and engagement decisions.

## Data Sources

- data/learners.json
- data/workload_signals.json
- data/certification_semantic_model.json
- docs/synthetic_engineering_certification_guide.md
- docs/synthetic_team_learning_report.md
- docs/synthetic_workload_insights_report.md

## Safety

The system uses synthetic data only and does not include real employee data, customer data, credentials, or personally identifiable information.
