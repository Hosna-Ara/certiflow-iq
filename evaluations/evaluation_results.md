# Evaluation Results

CertiFlow IQ was evaluated using synthetic test cases covering learner readiness, workload-aware planning, manager insight, and synthetic-data safety.

| Test ID | Scenario | Status | Result |
|---|---|---|---|
| TC-001 | Learner below readiness threshold | Completed | Passed: L-1001 is identified as At Risk because practice score is below 75%. |
| TC-002 | High meeting workload | Completed | Passed: EMP-001 has more than 20 meeting hours and receives a lighter study plan. |
| TC-003 | Ready learner | Completed | Passed: L-1002 is identified as Ready based on score and study progress. |
| TC-004 | Manager team insight | Completed | Passed: Dashboard shows total learners, ready learners, needs review, and at-risk learners. |
| TC-005 | Synthetic data safety | Completed | Passed: Safety / Verifier Agent confirms synthetic identifiers and no real personal data. |

## Evaluation Summary

All planned evaluation cases passed in the local Streamlit prototype.

The evaluation confirms that the system can:

- Detect at-risk learners
- Adjust study recommendations based on workload
- Identify ready learners
- Provide manager-level readiness summary
- Apply synthetic-data safety checks
