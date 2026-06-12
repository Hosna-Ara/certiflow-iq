# Microsoft Agent Framework-Style Structure

## Purpose
CertiFlow IQ uses a local multi-agent system organised in a Microsoft Agent Framework-style pattern.

## Pattern
The system follows a planner-specialist-verifier workflow.

## Agent Contracts
Each agent has a defined role, input, output, tool responsibility, and reasoning purpose.

## Agents

### 1. Orchestrator Agent
- Purpose: Receives learner or manager requests and coordinates the workflow.
- Inputs: user request, learner data, workload data, certification model.
- Outputs: request type, execution order, agent trace.

### 2. Learning Path Curator Agent
- Purpose: Maps role and certification target to required skills.
- Inputs: learner profile, certification semantic model, synthetic certification guide.
- Outputs: certification, role, skills, recommended hours, reasoning.

### 3. Study Plan Generator Agent
- Purpose: Creates a capacity-aware study plan.
- Inputs: learner progress, recommended hours, workload signals.
- Outputs: remaining hours, weekly study hours, estimated weeks, preferred slot.

### 4. Engagement Agent
- Purpose: Recommends realistic reminder strategy using work context.
- Inputs: meeting hours, focus hours, preferred learning slot.
- Outputs: reminder style, timing recommendation, reasoning.

### 5. Assessment Agent
- Purpose: Evaluates certification readiness.
- Inputs: practice score, study hours, readiness threshold.
- Outputs: Ready, Needs Review, or At Risk.

### 6. Grounded Practice Question Agent
- Purpose: Generates practice questions from approved synthetic documents.
- Inputs: certification target, synthetic certification guide.
- Outputs: questions, answers, source references, grounding notes.

### 7. Manager Insights Agent
- Purpose: Summarises team readiness and risk.
- Inputs: team learner data.
- Outputs: total learners, ready count, needs review count, at-risk count, manager summary.

### 8. Safety / Verifier Agent
- Purpose: Checks synthetic-data safety and privacy.
- Inputs: agent outputs.
- Outputs: safety status, checks, reasoning.

## Tool Pattern
- JSON data loader
- Semantic model lookup
- Workload capacity rule
- Readiness rule engine
- Synthetic document question bank
- Team readiness aggregator
- Privacy and synthetic-data checker

## Microsoft Foundry Readiness
A Microsoft Foundry resource was created successfully. Model deployment is currently blocked by Azure for Students quota, so the current system runs locally while remaining ready for Foundry integration.
