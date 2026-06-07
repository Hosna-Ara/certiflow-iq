# Orchestration Flow

## Main Workflow

1. User submits a learner or manager request.
2. Orchestrator Agent classifies the request type.
3. Learning Path Curator Agent maps role and certification target to required skills.
4. Study Plan Generator Agent checks recommended hours, current progress, and workload capacity.
5. Engagement Agent adjusts study timing using synthetic work signals.
6. Assessment Agent evaluates readiness using score, study hours, and threshold rules.
7. Manager Insights Agent summarises team-level progress, risks, and actions.
8. Safety / Verifier Agent checks that outputs are safe, synthetic-data based, and suitable for demo use.

## Example Manager Request

"Show certification readiness for Team A and identify learners at risk."

## Example Learner Request

"Create a study plan for learner L-1001 preparing for AZ-204."

## Reasoning Pattern

CertiFlow IQ uses a planner-specialist-verifier pattern:

- Planner: Orchestrator Agent
- Specialists: Learning Path, Study Plan, Engagement, Assessment, Manager Insights Agents
- Verifier: Safety / Verifier Agent

This structure separates responsibilities and makes the reasoning process easier to inspect, test, and improve.
