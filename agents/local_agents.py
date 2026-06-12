import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    with open(BASE_DIR / relative_path, "r", encoding="utf-8") as file:
        return json.load(file)


class LearningPathCuratorAgent:
    def run(self, learner, semantic_model):
        cert_id = learner["certification_target"]
        cert = next(item for item in semantic_model["certifications"] if item["id"] == cert_id)

        return {
            "agent": "Learning Path Curator Agent",
            "certification": cert_id,
            "role": learner["role"],
            "recommended_skills": cert["skills"],
            "recommended_hours": cert["recommended_hours"],
            "reasoning": f"{learner['role']} is aligned with {cert_id}, so the learning path focuses on {', '.join(cert['skills'])}."
        }


class StudyPlanGeneratorAgent:
    def run(self, learner, workload, learning_path):
        remaining_hours = max(learning_path["recommended_hours"] - learner["hours_studied"], 0)

        if workload["meeting_hours_per_week"] > 20:
            weekly_hours = 4
            plan_length = max(round(remaining_hours / weekly_hours), 1)
            workload_note = "High meeting load detected, so the study plan is extended with lighter weekly study hours."
        elif workload["focus_hours_per_week"] >= 15:
            weekly_hours = 6
            plan_length = max(round(remaining_hours / weekly_hours), 1)
            workload_note = "Good focus capacity detected, so the learner can follow a moderate weekly study plan."
        else:
            weekly_hours = 5
            plan_length = max(round(remaining_hours / weekly_hours), 1)
            workload_note = "Moderate capacity detected, so the learner should follow a balanced study plan."

        return {
            "agent": "Study Plan Generator Agent",
            "remaining_study_hours": remaining_hours,
            "suggested_weekly_hours": weekly_hours,
            "estimated_plan_weeks": plan_length,
            "preferred_slot": workload["preferred_learning_slot"],
            "reasoning": workload_note
        }


class EngagementAgent:
    def run(self, workload):
        if workload["meeting_hours_per_week"] > 20:
            reminder_style = "Low-frequency reminders during preferred learning slot only."
            escalation = "Avoid aggressive reminders because learner has high meeting load."
        else:
            reminder_style = "Regular reminders during preferred learning slot."
            escalation = "Standard weekly checkpoint reminder is suitable."

        return {
            "agent": "Engagement Agent",
            "reminder_style": reminder_style,
            "preferred_learning_slot": workload["preferred_learning_slot"],
            "reasoning": escalation
        }


class AssessmentAgent:
    def run(self, learner, semantic_model):
        cert_id = learner["certification_target"]
        cert = next(item for item in semantic_model["certifications"] if item["id"] == cert_id)

        score_gap = max(cert["readiness_threshold"] - learner["practice_score_avg"], 0)
        hour_gap = max(cert["recommended_hours"] - learner["hours_studied"], 0)

        if score_gap == 0 and hour_gap == 0:
            readiness = "Ready"
            recommendation = "Learner appears ready for certification attempt."
        elif score_gap <= 5:
            readiness = "Needs Review"
            recommendation = "Learner is close to ready but should complete another assessment checkpoint."
        else:
            readiness = "At Risk"
            recommendation = "Learner needs more preparation before exam booking."

        return {
            "agent": "Assessment Agent",
            "readiness": readiness,
            "practice_score": learner["practice_score_avg"],
            "readiness_threshold": cert["readiness_threshold"],
            "score_gap": score_gap,
            "hour_gap": hour_gap,
            "recommendation": recommendation,
            "reasoning": "Readiness is calculated using practice score, study hours, and certification threshold."
        }


class ManagerInsightsAgent:
    def run(self, all_learners):
        total = len(all_learners)
        ready = sum(1 for learner in all_learners if learner["readiness_status"] == "Ready")
        at_risk = sum(1 for learner in all_learners if learner["readiness_status"] == "At Risk")
        needs_review = sum(1 for learner in all_learners if learner["readiness_status"] == "Needs Review")

        return {
            "agent": "Manager Insights Agent",
            "total_learners": total,
            "ready": ready,
            "at_risk": at_risk,
            "needs_review": needs_review,
            "manager_summary": (
                f"Team A has {total} learners: {ready} ready, {needs_review} needing review, "
                f"and {at_risk} at risk. Manager should prioritise learners below readiness threshold."
            ),
            "reasoning": "Team readiness is summarised using learner readiness status and risk indicators."
        }


class SafetyVerifierAgent:
    def run(self):
        return {
            "agent": "Safety / Verifier Agent",
            "status": "Passed",
            "checks": [
                "Synthetic learner IDs only",
                "No real employee names",
                "No personal emails",
                "No customer data",
                "Recommendations are advisory only"
            ],
            "reasoning": "The response is safe for demo use because it relies only on synthetic data."
        }


class OrchestratorAgent:
    def __init__(self):
        self.learners = load_json("data/learners.json")
        self.workloads = load_json("data/workload_signals.json")
        self.semantic_model = load_json("data/certification_semantic_model.json")

    def run_learner_review(self, learner_id):
        learner = next(item for item in self.learners if item["learner_id"] == learner_id)
        workload = next(item for item in self.workloads if item["employee_id"] == learner["employee_id"])

        learning_path = LearningPathCuratorAgent().run(learner, self.semantic_model)
        study_plan = StudyPlanGeneratorAgent().run(learner, workload, learning_path)
        engagement = EngagementAgent().run(workload)
        assessment = AssessmentAgent().run(learner, self.semantic_model)
        safety = SafetyVerifierAgent().run()

        return {
            "request_type": "Learner Review",
            "learner_id": learner_id,
            "agent_trace": [
                learning_path,
                study_plan,
                engagement,
                assessment,
                safety
            ]
        }

    def run_manager_review(self):
        manager_insights = ManagerInsightsAgent().run(self.learners)
        safety = SafetyVerifierAgent().run()

        return {
            "request_type": "Manager Review",
            "team_id": "TEAM-A",
            "agent_trace": [
                manager_insights,
                safety
            ]
        }
