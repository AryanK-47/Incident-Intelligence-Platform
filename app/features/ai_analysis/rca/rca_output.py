
from typing import Any

import pandas as pd


SIGNAL_COLUMNS = [
    "cpu_early_change",
    "mem_early_change",
    "latency-50_early_change",
    "latency-90_early_change",
]

SIGNAL_LABELS = {
    "cpu_early_change": "CPU",
    "mem_early_change": "memory",
    "latency-50_early_change": "p50 latency",
    "latency-90_early_change": "p90 latency",
}


def build_rca_output(
    score_df: pd.DataFrame,
    predictions: pd.DataFrame,
) -> dict[str, Any]:
    """
    Build an API-ready RCA payload from frozen V1 scorer results.

    RCA scores and percentile ranks are ranking signals,
    not calibrated probabilities or confirmed causal evidence.
    """

    if score_df.empty or predictions.empty:
        raise ValueError("Scorer results cannot be empty.")

    required_columns = [
        "case",
        "service",
        "onset_score",
        *SIGNAL_COLUMNS,
        *[f"{column}_rank" for column in SIGNAL_COLUMNS],
    ]

    missing = [
        column for column in required_columns
        if column not in score_df.columns
    ]

    if missing:
        raise ValueError(f"Missing scorer output columns: {missing}")

    if (
        "service" not in predictions.columns
        or "onset_score" not in predictions.columns
    ):
        raise ValueError(
            "Predictions must contain service and onset_score."
        )

    if len(predictions) != 1:
        raise ValueError(
            "Expected exactly one prediction for a single-case RCA."
        )

    top_candidate = predictions.iloc[0]
    root_cause_service = str(top_candidate["service"])
    top_score = float(top_candidate["onset_score"])

    ranked_candidates = score_df.sort_values(
        ["onset_score", "service"],
        ascending=[False, True],
    )

    candidate_services = [
        {
            "service": str(row["service"]),
            "rca_score": float(row["onset_score"]),
        }
        for _, row in ranked_candidates.iterrows()
    ]

    evidence = []

    for _, row in ranked_candidates.iterrows():
        signals = {
            column: {
                "value": float(row[column]),
                "percentile_rank": float(row[f"{column}_rank"]),
            }
            for column in SIGNAL_COLUMNS
        }

        evidence.append({
            "service": str(row["service"]),
            "signals": signals,
        })

    # Explain which signals contributed to the top service's ranking.
    top_rows = ranked_candidates[
        ranked_candidates["service"].astype(str)
        == root_cause_service
    ]

    if top_rows.empty:
        raise ValueError(
            "Predicted service was not found in scorer results."
        )

    top_row = top_rows.iloc[0]

    ranked_signals = sorted(
        SIGNAL_COLUMNS,
        key=lambda column: float(top_row[f"{column}_rank"]),
        reverse=True,
    )

    signal_explanations = [
        (
            f"{SIGNAL_LABELS[column]} early-change signal "
            f"was {float(top_row[column]):.4f}, with a "
            f"within-case percentile rank of "
            f"{float(top_row[f'{column}_rank']):.2f}."
        )
        for column in ranked_signals
    ]

    root_cause_analysis = (
        f"Service '{root_cause_service}' received the highest "
        f"V1 onset ranking score of {top_score:.4f}. "
        + " ".join(signal_explanations)
        + " These are relative signal rankings; they do not "
        "prove that this service caused the incident."
    )

    # Generate investigation recommendations only for signals
    # ranked highest among the supplied services.
    suggested_remediation = []

    for column in SIGNAL_COLUMNS:
        rank = float(top_row[f"{column}_rank"])

        if rank >= 1.0:
            label = SIGNAL_LABELS[column]

            suggested_remediation.append(
                f"Investigate the {label} early-change signal for "
                f"'{root_cause_service}'. Compare the relevant "
                "telemetry with the incident timeline, recent "
                "deployments, and service-level metrics before "
                "choosing a corrective action."
            )

    if not suggested_remediation:
        suggested_remediation.append(
            f"Review the telemetry and incident timeline for "
            f"'{root_cause_service}' to identify which signals "
            "are associated with the incident onset."
        )

    return {
        "analysis_type": "root_cause_analysis",
        "root_cause": [root_cause_service],
        "root_cause_analysis": root_cause_analysis,
        "suggested_remediation": suggested_remediation,
        "impact_analysis": (
            "Impact cannot be determined from the supplied early-change "
            "signals alone. Additional information such as affected "
            "users, error rates, service availability, and incident "
            "duration is required."
        ),
        "confidence": None,
        "model": "RCAEval-V1-rule-based",
        "rca_score": top_score,
        "candidate_services": candidate_services,
        "evidence": evidence,
    }
