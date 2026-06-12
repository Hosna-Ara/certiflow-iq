import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from agents.local_agents import OrchestratorAgent


# -----------------------------
# Data loading
# -----------------------------
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


# -----------------------------
# Helper functions
# -----------------------------
def readiness_class(status):
    if status == "Ready":
        return "ready"
    if status == "Needs Review":
        return "review"
    return "risk"


def readiness_icon(status):
    if status == "Ready":
        return "●"
    if status == "Needs Review":
        return "●"
    return "●"


def risk_level(row):
    if row["readiness_status"] == "At Risk":
        return "High"
    if row["readiness_status"] == "Needs Review":
        return "Medium"
    return "Low"


def get_cert_info(cert_id):
    return next(item for item in semantic_model["certifications"] if item["id"] == cert_id)


def kpi_card(title, value, subtitle, status="neutral"):
    st.markdown(
        f"""
        <div class="kpi-card {status}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title, body, accent="blue"):
    st.markdown(
        f"""
        <div class="info-card {accent}">
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def agent_card(number, name, role, input_text, output_text, accent="blue"):
    st.markdown(
        f"""
        <div class="agent-card {accent}">
            <div class="agent-number">{number}</div>
            <div class="agent-content">
                <div class="agent-name">{name}</div>
                <div class="agent-role">{role}</div>
                <div class="agent-meta"><b>Input:</b> {input_text}</div>
                <div class="agent-meta"><b>Output:</b> {output_text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def question_card(index, question, answer, source, grounding):
    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">Question {index}</div>
            <div class="question-text">{question}</div>
            <div class="answer-text"><b>Expected answer:</b> {answer}</div>
            <div class="source-pill">Source: {source}</div>
            <div class="grounding-note">{grounding}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


merged_df["risk_level"] = merged_df.apply(risk_level, axis=1)


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="CertiFlow IQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    /* Main layout */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1350px;
    }

    /* Hide default Streamlit menu/footer spacing noise */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title area */
    .hero {
        text-align: center;
        padding: 18px 10px 10px 10px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 50px;
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1.05;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #7c3aed, #38bdf8, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        max-width: 850px;
        margin: 0 auto;
        line-height: 1.5;
    }

    .hero-badges {
        margin-top: 18px;
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .badge {
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(148, 163, 184, 0.35);
        background: rgba(15, 23, 42, 0.75);
        color: #dbeafe;
    }

    /* KPI cards */
    .kpi-card {
        min-height: 142px;
        border-radius: 22px;
        padding: 22px 18px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.25);
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.98), rgba(15, 23, 42, 0.98));
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.28);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 12px;
    }

    .kpi-card.ready {
        border-top: 4px solid #22c55e;
    }

    .kpi-card.review {
        border-top: 4px solid #f59e0b;
    }

    .kpi-card.risk {
        border-top: 4px solid #ef4444;
    }

    .kpi-card.neutral {
        border-top: 4px solid #38bdf8;
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 800;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 44px;
        line-height: 1;
        font-weight: 900;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    .kpi-subtitle {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.35;
    }

    /* General cards */
    .info-card {
        border-radius: 20px;
        padding: 20px 22px;
        min-height: 135px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        background: rgba(15, 23, 42, 0.88);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
        margin-bottom: 16px;
    }

    .info-card.blue {
        border-left: 5px solid #38bdf8;
    }

    .info-card.green {
        border-left: 5px solid #22c55e;
    }

    .info-card.amber {
        border-left: 5px solid #f59e0b;
    }

    .info-card.red {
        border-left: 5px solid #ef4444;
    }

    .info-card.purple {
        border-left: 5px solid #8b5cf6;
    }

    .card-title {
        font-size: 18px;
        font-weight: 850;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    .card-body {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.55;
    }

    /* Status pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 850;
        font-size: 14px;
    }

    .status-pill.ready {
        color: #bbf7d0;
        background: rgba(34, 197, 94, 0.18);
        border: 1px solid rgba(34, 197, 94, 0.45);
    }

    .status-pill.review {
        color: #fde68a;
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.45);
    }

    .status-pill.risk {
        color: #fecaca;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid rgba(239, 68, 68, 0.45);
    }

    /* Skill chips */
    .chip-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .skill-chip {
        padding: 7px 11px;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.15);
        color: #bae6fd;
        border: 1px solid rgba(56, 189, 248, 0.35);
        font-size: 13px;
        font-weight: 700;
    }

    /* Readiness bar */
    .meter-shell {
        height: 16px;
        background: rgba(148, 163, 184, 0.22);
        border-radius: 999px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .meter-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #38bdf8, #22c55e);
    }

    .meter-labels {
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 13px;
    }

    /* Agent workflow */
    .agent-card {
        border-radius: 18px;
        padding: 16px 18px;
        display: flex;
        gap: 15px;
        align-items: flex-start;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.22);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.20);
        margin-bottom: 12px;
    }

    .agent-card.blue { border-left: 5px solid #38bdf8; }
    .agent-card.purple { border-left: 5px solid #8b5cf6; }
    .agent-card.green { border-left: 5px solid #22c55e; }
    .agent-card.amber { border-left: 5px solid #f59e0b; }
    .agent-card.red { border-left: 5px solid #ef4444; }

    .agent-number {
        height: 36px;
        width: 36px;
        min-width: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #38bdf8);
        color: white;
        font-weight: 900;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2px;
    }

    .agent-name {
        font-size: 17px;
        font-weight: 850;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .agent-role {
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 8px;
        line-height: 1.45;
    }

    .agent-meta {
        font-size: 13px;
        color: #94a3b8;
        line-height: 1.45;
        margin-top: 3px;
    }

    /* Question cards */
    .question-card {
        border-radius: 18px;
        padding: 20px 22px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-left: 5px solid #38bdf8;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.22);
        margin-bottom: 14px;
    }

    .question-label {
        color: #38bdf8;
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .question-text {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 12px;
        line-height: 1.45;
    }

    .answer-text {
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .source-pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(139, 92, 246, 0.16);
        color: #ddd6fe;
        border: 1px solid rgba(139, 92, 246, 0.4);
        font-size: 12px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .grounding-note {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.4;
    }

    /* Section title */
    .section-heading {
        font-size: 26px;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 16px;
        color: #f8fafc;
    }

    .subtle-text {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #1f2937);
    }

    /* Streamlit tabs */
    button[data-baseweb="tab"] {
        font-weight: 800;
    }

    /* Dataframe polishing */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.markdown("## Control Panel")

    selected_learner = st.selectbox(
        "Learner profile",
        merged_df["learner_id"].tolist(),
        index=0,
    )

    selected_team = st.selectbox(
        "Team",
        sorted(merged_df["team_id"].unique().tolist()),
    )

    readiness_filter = st.multiselect(
        "Risk board filter",
        ["Ready", "Needs Review", "At Risk"],
        default=["Ready", "Needs Review", "At Risk"],
    )

    show_trace = st.toggle("Show technical trace", value=False)

    st.divider()

    st.markdown("### Microsoft Foundry")
    st.caption("Resource: certiflowAI")
    st.caption("Project: proj-default")
    st.caption("Region: Southeast Asia")
    st.warning("Model quota is blocked under Azure for Students. Demo runs locally with a Foundry-ready structure.")

    st.divider()

    st.markdown("### IQ Alignment")
    st.caption("Foundry IQ-ready knowledge docs")
    st.caption("Fabric IQ-inspired semantic model")
    st.caption("Work IQ-inspired workload signals")


# -----------------------------
# Hero
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">CertiFlow IQ</div>
        <div class="hero-subtitle">
            A multi-agent certification readiness system that helps enterprise teams plan, assess,
            and monitor role-based certification progress with workload-aware reasoning.
        </div>
        <div class="hero-badges">
            <span class="badge">Multi-Agent Reasoning</span>
            <span class="badge">Microsoft Foundry-Ready</span>
            <span class="badge">Synthetic Data Only</span>
            <span class="badge">Grounded Practice Questions</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("This demo uses synthetic data only. No real employee, customer, credential, or personal data is used.")


# -----------------------------
# Filtered data
# -----------------------------
filtered_df = merged_df[
    (merged_df["team_id"] == selected_team)
    & (merged_df["readiness_status"].isin(readiness_filter))
].copy()


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Executive Command Centre",
        "Learner 360",
        "Grounded Assessment",
        "Agent Reasoning",
        "Data & Microsoft Setup",
    ]
)


# -----------------------------
# Tab 1: Executive Command Centre
# -----------------------------
with tab1:
    st.markdown('<div class="section-heading">Executive Command Centre</div>', unsafe_allow_html=True)

    manager_result = orchestrator.run_manager_review()
    manager_agent = manager_result["agent_trace"][0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card("Total Learners", manager_agent["total_learners"], "Team members in certification plan", "neutral")
    with col2:
        kpi_card("Ready", manager_agent["ready"], "Can proceed toward exam readiness", "ready")
    with col3:
        kpi_card("Needs Review", manager_agent["needs_review"], "Close but requires checkpoint", "review")
    with col4:
        kpi_card("At Risk", manager_agent["at_risk"], "Needs immediate learning support", "risk")

    st.divider()

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("### Team Readiness Snapshot")

        total = len(merged_df)
        ready = int((merged_df["readiness_status"] == "Ready").sum())
        review = int((merged_df["readiness_status"] == "Needs Review").sum())
        risk = int((merged_df["readiness_status"] == "At Risk").sum())

        ready_pct = round((ready / total) * 100)
        review_pct = round((review / total) * 100)
        risk_pct = round((risk / total) * 100)

        st.markdown(
            f"""
            <div class="info-card blue">
                <div class="card-title">Readiness Distribution</div>
                <div class="card-body">
                    <b>Ready:</b> {ready_pct}% &nbsp; | &nbsp;
                    <b>Needs Review:</b> {review_pct}% &nbsp; | &nbsp;
                    <b>At Risk:</b> {risk_pct}%
                    <br><br>
                    <div class="meter-shell">
                        <div class="meter-fill" style="width:{ready_pct}%; background:#22c55e;"></div>
                    </div>
                    <div class="meter-shell">
                        <div class="meter-fill" style="width:{review_pct}%; background:#f59e0b;"></div>
                    </div>
                    <div class="meter-shell">
                        <div class="meter-fill" style="width:{risk_pct}%; background:#ef4444;"></div>
                    </div>
                    <div class="subtle-text">
                        Green = ready, amber = needs review, red = at risk.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        at_risk_rows = merged_df[merged_df["readiness_status"] == "At Risk"]

        if not at_risk_rows.empty:
            priority = at_risk_rows.iloc[0]
            action_text = (
                f"Prioritise learner <b>{priority['learner_id']}</b>. "
                f"They have a practice score of <b>{priority['practice_score_avg']}%</b>, "
                f"only <b>{priority['hours_studied']}</b> study hours, and "
                f"<b>{priority['meeting_hours_per_week']}</b> meeting hours per week."
            )
            info_card("Recommended Manager Action", action_text, "red")
        else:
            info_card("Recommended Manager Action", "No high-risk learners detected in the current team view.", "green")

        info_card(
            "Manager Summary",
            manager_agent["manager_summary"],
            "purple",
        )

    st.markdown("### Priority Risk Board")

    risk_board = filtered_df[
        [
            "learner_id",
            "role",
            "certification_target",
            "practice_score_avg",
            "hours_studied",
            "meeting_hours_per_week",
            "focus_hours_per_week",
            "readiness_status",
            "risk_level",
        ]
    ].copy()

    risk_board = risk_board.sort_values(
        by=["risk_level", "practice_score_avg"],
        ascending=[True, True],
    )

    st.dataframe(
        risk_board,
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------
# Tab 2: Learner 360
# -----------------------------
with tab2:
    st.markdown('<div class="section-heading">Learner 360</div>', unsafe_allow_html=True)

    learner_result = orchestrator.run_learner_review(selected_learner)
    trace = learner_result["agent_trace"]

    learning_path = trace[0]
    study_plan = trace[1]
    engagement = trace[2]
    assessment = trace[3]
    practice_questions = trace[4]
    safety = trace[5]

    learner_row = merged_df[merged_df["learner_id"] == selected_learner].iloc[0]
    cert_info = get_cert_info(learner_row["certification_target"])

    top_left, top_right = st.columns([1, 1])

    with top_left:
        status = assessment["readiness"]
        status_cls = readiness_class(status)

        st.markdown(
            f"""
            <div class="info-card blue">
                <div class="card-title">Learner Profile</div>
                <div class="card-body">
                    <b>Learner:</b> {learner_row["learner_id"]}<br>
                    <b>Role:</b> {learner_row["role"]}<br>
                    <b>Certification target:</b> {learner_row["certification_target"]}<br>
                    <b>Preferred learning slot:</b> {learner_row["preferred_learning_slot"]}<br>
                    <b>Meeting load:</b> {learner_row["meeting_hours_per_week"]} hrs/week<br>
                    <b>Focus time:</b> {learner_row["focus_hours_per_week"]} hrs/week
                    <br><br>
                    <span class="status-pill {status_cls}">
                        {readiness_icon(status)} {status}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        score = assessment["practice_score"]
        threshold = assessment["readiness_threshold"]

        st.markdown(
            f"""
            <div class="info-card {readiness_class(status)}">
                <div class="card-title">Readiness Decision</div>
                <div class="card-body">
                    {assessment["recommendation"]}
                    <br><br>
                    <b>Practice score:</b> {score}%<br>
                    <b>Readiness threshold:</b> {threshold}%
                    <div class="meter-shell">
                        <div class="meter-fill" style="width:{min(score, 100)}%;"></div>
                    </div>
                    <div class="meter-labels">
                        <span>0%</span>
                        <span>Target: {threshold}%</span>
                        <span>100%</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Capacity-Aware Study Plan")

    plan1, plan2, plan3 = st.columns(3)

    with plan1:
        kpi_card("Remaining Hours", study_plan["remaining_study_hours"], "Study hours still needed", "neutral")
    with plan2:
        kpi_card("Weekly Load", study_plan["suggested_weekly_hours"], "Recommended hours/week", "review")
    with plan3:
        kpi_card("Plan Length", f"{study_plan['estimated_plan_weeks']}", "Estimated week(s)", "ready")

    st.markdown("### Recommended Skill Focus")

    chips = "".join([f'<span class="skill-chip">{skill}</span>' for skill in learning_path["recommended_skills"]])

    st.markdown(
        f"""
        <div class="info-card purple">
            <div class="card-title">Learning Path</div>
            <div class="card-body">
                {learning_path["reasoning"]}
                <div class="chip-wrap">{chips}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Agent Recommendations")

    rec_col1, rec_col2 = st.columns(2)

    with rec_col1:
        info_card("Study Plan Agent", study_plan["reasoning"], "blue")

    with rec_col2:
        info_card("Engagement Agent", engagement["reminder_style"] + " " + engagement["reasoning"], "green")


# -----------------------------
# Tab 3: Grounded Assessment
# -----------------------------
with tab3:
    st.markdown('<div class="section-heading">Grounded Assessment</div>', unsafe_allow_html=True)

    learner_result = orchestrator.run_learner_review(selected_learner)
    practice_questions = learner_result["agent_trace"][4]
    learner_row = merged_df[merged_df["learner_id"] == selected_learner].iloc[0]

    top_a, top_b = st.columns([1, 1])

    with top_a:
        info_card(
            "Assessment Context",
            f"Learner <b>{selected_learner}</b> is preparing for <b>{learner_row['certification_target']}</b>. "
            "The questions below are generated from approved synthetic certification guidance.",
            "blue",
        )

    with top_b:
        info_card(
            "Grounding Rule",
            "Every practice question includes a source reference and a grounding note, so the assessment is not presented as unsupported free text.",
            "green",
        )

    for index, item in enumerate(practice_questions["questions"], start=1):
        question_card(
            index,
            item["question"],
            item["answer"],
            item["source"],
            item["grounding"],
        )


# -----------------------------
# Tab 4: Agent Reasoning
# -----------------------------
with tab4:
    st.markdown('<div class="section-heading">Agent Reasoning</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-card blue">
            <div class="card-title">How to read this page</div>
            <div class="card-body">
                This page shows the multi-agent reasoning flow in plain language.
                Each agent receives a specific input, makes a narrow decision, and passes its output to the next step.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    agent_card(
        "1",
        "Orchestrator Agent",
        "Chooses whether the request is a manager review or learner review.",
        "User request and selected learner/team context",
        "Routes the workflow to the required specialist agents",
        "purple",
    )

    agent_card(
        "2",
        "Learning Path Curator Agent",
        "Maps the learner role and certification target to relevant skills.",
        "Learner role, certification target, semantic model",
        "Recommended skills and study-hour expectation",
        "blue",
    )

    agent_card(
        "3",
        "Study Plan Generator Agent",
        "Creates a realistic study plan based on progress and workload.",
        "Completed hours, recommended hours, meeting load, focus time",
        "Remaining hours, weekly load, estimated plan length",
        "green",
    )

    agent_card(
        "4",
        "Engagement Agent",
        "Adjusts learner support based on work rhythm.",
        "Meeting hours, focus hours, preferred learning slot",
        "Reminder strategy that avoids unrealistic pressure",
        "amber",
    )

    agent_card(
        "5",
        "Assessment Agent",
        "Classifies readiness using score and study threshold rules.",
        "Practice score, study hours, readiness threshold",
        "Ready, Needs Review, or At Risk decision",
        "red",
    )

    agent_card(
        "6",
        "Grounded Practice Question Agent",
        "Creates assessment questions from approved synthetic knowledge.",
        "Certification target and synthetic certification guide",
        "Questions, answers, source references, and grounding notes",
        "blue",
    )

    agent_card(
        "7",
        "Safety / Verifier Agent",
        "Checks privacy, synthetic-data safety, and advisory wording.",
        "Agent outputs",
        "Safety status and guardrail checks",
        "green",
    )

    if show_trace:
        st.markdown("### Technical Trace")

        trace_type = st.radio(
            "Trace type",
            ["Learner Review", "Manager Review"],
            horizontal=True,
        )

        if trace_type == "Learner Review":
            result = orchestrator.run_learner_review(selected_learner)
        else:
            result = orchestrator.run_manager_review()

        for index, step in enumerate(result["agent_trace"], start=1):
            with st.expander(f"{index}. {step['agent']}", expanded=False):
                st.json(step)
    else:
        st.caption("Technical JSON trace is hidden. Enable it from the sidebar if needed.")


# -----------------------------
# Tab 5: Data & Microsoft Setup
# -----------------------------
with tab5:
    st.markdown('<div class="section-heading">Data & Microsoft Setup</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        info_card(
            "Microsoft Foundry Setup",
            "A Microsoft Foundry resource named <b>certiflowAI</b> was created successfully in <b>Southeast Asia</b> under the Azure for Students subscription. "
            "Model deployment is currently blocked by quota, so the prototype runs locally while preserving a Foundry-ready architecture.",
            "purple",
        )

        info_card(
            "Microsoft IQ Mapping",
            "<b>Foundry IQ-ready:</b> synthetic knowledge documents prepared for grounding.<br><br>"
            "<b>Fabric IQ-inspired:</b> semantic model connecting roles, certifications, skills, hours, and thresholds.<br><br>"
            "<b>Work IQ-inspired:</b> workload context using meeting hours, focus hours, and preferred study slots.",
            "blue",
        )

    with right:
        learner_result = orchestrator.run_learner_review(selected_learner)
        safety = learner_result["agent_trace"][5]

        checks = "<br>".join([f"✓ {check}" for check in safety["checks"]])

        info_card(
            "Safety Verification",
            f"<b>Status:</b> {safety['status']}<br><br>{checks}<br><br>{safety['reasoning']}",
            "green",
        )

    st.markdown("### Data Explorer")

    data_choice = st.radio(
        "Select data source",
        ["Learners", "Workload Signals", "Certification Semantic Model"],
        horizontal=True,
    )

    if data_choice == "Learners":
        st.dataframe(learners_df, use_container_width=True, hide_index=True)
    elif data_choice == "Workload Signals":
        st.dataframe(workload_df, use_container_width=True, hide_index=True)
    else:
        st.json(semantic_model)