import json
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]


def load_json(path):
    with open(BASE_DIR / path, "r", encoding="utf-8") as file:
        return json.load(file)


learners = load_json("data/learners.json")
workload = load_json("data/workload_signals.json")
semantic_model = load_json("data/certification_semantic_model.json")

learners_df = pd.DataFrame(learners)
workload_df = pd.DataFrame(workload)

merged_df = learners_df.merge(workload_df, on="employee_id", how="left")

st.set_page_config(page_title="CertiFlow IQ", layout="wide")

st.title("CertiFlow IQ")
st.caption("Multi-Agent Certification Readiness System for Enterprise Teams")

st.info("Demo uses synthetic data only. No real employee, customer, or personal data is used.")

tab1, tab2, tab3 = st.tabs(["Manager Insights", "Learner Readiness", "Synthetic Data"])

with tab1:
    st.subheader("Team Certification Readiness")

    total_learners = len(merged_df)
    ready_count = (merged_df["readiness_status"] == "Ready").sum()
    at_risk_count = (merged_df["readiness_status"] == "At Risk").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Learners", total_learners)
    col2.metric("Ready", ready_count)
    col3.metric("At Risk", at_risk_count)

    st.dataframe(merged_df, use_container_width=True)

    st.subheader("Manager Summary")
    st.write(
        "Team A has mixed certification readiness. Learners below the 75% practice score threshold "
        "or below recommended study hours should receive adjusted study plans and additional assessment checkpoints."
    )

with tab2:
    st.subheader("Learner Readiness Review")

    selected_learner = st.selectbox(
        "Select learner",
        merged_df["learner_id"].tolist()
    )

    learner = merged_df[merged_df["learner_id"] == selected_learner].iloc[0]

    st.write("### Learner Profile")
    st.json(learner.to_dict())

    cert_id = learner["certification_target"]
    cert_info = next(
        item for item in semantic_model["certifications"] if item["id"] == cert_id
    )

    score_gap = cert_info["readiness_threshold"] - learner["practice_score_avg"]
    hour_gap = cert_info["recommended_hours"] - learner["hours_studied"]

    st.write("### Agent-style Recommendation")

    if learner["practice_score_avg"] >= cert_info["readiness_threshold"] and learner["hours_studied"] >= cert_info["recommended_hours"]:
        st.success("Assessment Agent: Learner appears ready for certification attempt.")
    else:
        st.warning("Assessment Agent: Learner needs further preparation before exam booking.")

    if learner["meeting_hours_per_week"] > 20:
        st.write("Engagement Agent: High meeting load detected. Recommend lighter weekly study allocation and longer preparation timeline.")
    else:
        st.write("Engagement Agent: Workload is manageable. Recommend regular study blocks during preferred learning slot.")

    st.write(
        f"Study Plan Agent: Focus on {', '.join(cert_info['skills'])}. "
        f"Practice score gap: {max(score_gap, 0)}%. "
        f"Recommended study hour gap: {max(hour_gap, 0)} hours."
    )

with tab3:
    st.subheader("Synthetic Learner Data")
    st.dataframe(learners_df, use_container_width=True)

    st.subheader("Synthetic Workload Signals")
    st.dataframe(workload_df, use_container_width=True)

    st.subheader("Synthetic Certification Semantic Model")
    st.json(semantic_model)
