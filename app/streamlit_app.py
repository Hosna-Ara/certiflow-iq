import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from agents.local_agents import OrchestratorAgent


def load_json(path):
    with open(BASE_DIR / path, "r", encoding="utf-8") as file:
        return json.load(file)


learners = load_json("data/learners.json")
workload = load_json("data/workload_signals.json")
semantic_model = load_json("data/certification_semantic_model.json")

learners_df = pd.DataFrame(learners)
workload_df = pd.DataFrame(workload)
merged_df = learners_df.merge(workload_df, on="employee_id", how="left")

orchestrator = OrchestratorAgent()

st.set_page_config(page_title="CertiFlow IQ", layout="wide")

st.title("CertiFlow IQ")
st.caption("Multi-Agent Certification Readiness System for Enterprise Teams")

st.info("Demo uses synthetic data only. No real employee, customer, or personal data is used.")

with st.expander("Project Status and Microsoft Foundry Setup", expanded=False):
    st.write("**Foundry resource:** certiflowAI")
    st.write("**Foundry project:** proj-default")
    st.write("**Region:** Southeast Asia")
    st.write("**Status:** Foundry resource created successfully")
    st.warning("Model deployment is currently blocked by Azure for Students quota, so this demo runs locally with a Foundry-ready architecture.")
    st.write("**IQ mapping:** Foundry IQ-ready synthetic knowledge documents, Fabric IQ-inspired semantic model, and Work IQ-inspired workload context.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Manager Insights",
    "Learner Readiness",
    "Agent Trace",
    "Synthetic Data"
])

with tab1:
    st.subheader("Team Certification Readiness")

    manager_result = orchestrator.run_manager_review()
    manager_agent = manager_result["agent_trace"][0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Learners", manager_agent["total_learners"])
    col2.metric("Ready", manager_agent["ready"])
    col3.metric("Needs Review", manager_agent["needs_review"])
    col4.metric("At Risk", manager_agent["at_risk"])

    st.dataframe(merged_df, use_container_width=True)

    st.subheader("Manager Summary")
    st.write(manager_agent["manager_summary"])
    st.caption(manager_agent["reasoning"])

with tab2:
    st.subheader("Learner Readiness Review")

    selected_learner = st.selectbox(
        "Select learner",
        merged_df["learner_id"].tolist()
    )

    learner_result = orchestrator.run_learner_review(selected_learner)
    trace = learner_result["agent_trace"]

    learning_path = trace[0]
    study_plan = trace[1]
    engagement = trace[2]
    assessment = trace[3]
    practice_questions = trace[4]
    safety = trace[5]

    st.write("### Readiness Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Certification", learning_path["certification"])
    col2.metric("Practice Score", f"{assessment['practice_score']}%")
    col3.metric("Readiness", assessment["readiness"])

    if assessment["readiness"] == "Ready":
        st.success(assessment["recommendation"])
    elif assessment["readiness"] == "Needs Review":
        st.warning(assessment["recommendation"])
    else:
        st.error(assessment["recommendation"])

    st.write("### Learning Path")
    st.write(f"**Role:** {learning_path['role']}")
    st.write(f"**Recommended skills:** {', '.join(learning_path['recommended_skills'])}")
    st.caption(learning_path["reasoning"])

    st.write("### Capacity-Aware Study Plan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Remaining Hours", study_plan["remaining_study_hours"])
    col2.metric("Weekly Study Hours", study_plan["suggested_weekly_hours"])
    col3.metric("Estimated Weeks", study_plan["estimated_plan_weeks"])

    st.write(f"**Preferred learning slot:** {study_plan['preferred_slot']}")
    st.caption(study_plan["reasoning"])

    st.write("### Engagement Recommendation")
    st.write(engagement["reminder_style"])
    st.caption(engagement["reasoning"])

    st.write("### Grounded Practice Questions")
    for index, item in enumerate(practice_questions["questions"], start=1):
        st.write(f"**Q{index}. {item['question']}**")
        st.write(f"Answer: {item['answer']}")
        st.caption(f"Source: {item['source']} | Grounding: {item['grounding']}")

    st.write("### Safety Check")
    st.success(f"Verifier status: {safety['status']}")
    st.write(", ".join(safety["checks"]))

    st.write("### How the Agents Worked")

    st.markdown(f"""
    1. **Learning Path Curator Agent** mapped the learner's role to the certification target and selected the relevant skills.
    2. **Study Plan Generator Agent** compared completed study hours against recommended hours and created a workload-aware plan.
    3. **Engagement Agent** checked meeting load, focus hours, and preferred study slot to recommend realistic reminders.
    4. **Assessment Agent** compared practice score and study hours against the readiness threshold.
    5. **Grounded Practice Question Agent** generated practice questions from the approved synthetic certification guide.
    6. **Safety / Verifier Agent** checked that the output uses synthetic data and avoids sensitive personal information.
    """)

    st.write("### Technical Agent Trace")
    st.caption("This section shows the raw agent outputs for transparency and debugging.")
    for agent_output in trace:
        with st.expander(agent_output["agent"], expanded=False):
            st.json(agent_output)

with tab3:
    st.subheader("Multi-Agent Reasoning Trace")

    trace_mode = st.radio(
        "Select trace type",
        ["Manager Review", "Learner Review"],
        horizontal=True
    )

    if trace_mode == "Manager Review":
        result = orchestrator.run_manager_review()
    else:
        selected_trace_learner = st.selectbox(
            "Select learner for trace",
            merged_df["learner_id"].tolist(),
            key="trace_learner"
        )
        result = orchestrator.run_learner_review(selected_trace_learner)

    st.write("### Request Type")
    st.write(result["request_type"])

    st.write("### Agent Execution Order")
    for index, step in enumerate(result["agent_trace"], start=1):
        st.write(f"{index}. {step['agent']}")

    st.write("### Full Trace")
    st.json(result)

with tab4:
    st.subheader("Synthetic Learner Data")
    st.dataframe(learners_df, use_container_width=True)

    st.subheader("Synthetic Workload Signals")
    st.dataframe(workload_df, use_container_width=True)

    st.subheader("Synthetic Certification Semantic Model")
    st.json(semantic_model)
