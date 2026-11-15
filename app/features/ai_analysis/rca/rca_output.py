
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

def calculate_heuristic_confidence(
    ranked_candidates: pd.DataFrame,
) -> float:
    """
    Calculate a heuristic confidence score between 0 and 1.

    Confidence is based on:
    1. Signal agreement: how many signals rank the top service first.
    2. Candidate separation: score difference between the top
       and second-ranked services.

    This is not a calibrated probability.
    """

    if ranked_candidates.empty:
        raise ValueError("Cannot calculate confidence without candidates.")

    top_candidate = ranked_candidates.iloc[0]

    # Factor 1: Agreement across the four telemetry signals.
    signal_agreement = 0.0

    for column in SIGNAL_COLUMNS:
        top_rank = float(top_candidate[f"{column}_rank"])
        max_rank = float(ranked_candidates[f"{column}_rank"].max())

        if top_rank == max_rank:
            signal_agreement += 1

    signal_agreement /= len(SIGNAL_COLUMNS)

    # Factor 2: Separation between the top two candidates.
    if len(ranked_candidates) >= 2:
        second_score = float(ranked_candidates.iloc[1]["onset_score"])
        top_score = float(top_candidate["onset_score"])

        score_gap = max(0.0, min(1.0, top_score - second_score))
    else:
        # No second candidate means separation cannot be measured.
        score_gap = 0.0

    confidence = (0.5 * signal_agreement) + (0.5 * score_gap)

    return round(max(0.0, min(1.0, confidence)), 4)



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
    if str(ranked_candidates.iloc[0]["service"]) != root_cause_service:
        raise ValueError(
            "Predicted service does not match the highest-ranked candidate."
        )
    confidence = calculate_heuristic_confidence(ranked_candidates)

    candidate_services = [
        {
            "service": str(row["service"]),
            "rank": rank,
            "rca_score": float(row["onset_score"]),
            "score_gap": round(
                top_score - float(row["onset_score"]), 4
            ),
        }
        for rank, (_, row) in enumerate(
            ranked_candidates.iterrows(), start=1
        )
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
    strongest_signal = ranked_signals[0]
    weakest_signal = ranked_signals[-1]

    strongest_label = SIGNAL_LABELS[strongest_signal]
    weakest_label = SIGNAL_LABELS[weakest_signal]

    strongest_rank = float(top_row[f"{strongest_signal}_rank"])
    weakest_rank = float(top_row[f"{weakest_signal}_rank"])

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
        "confidence": confidence,
        "model": "RCAEval-V1-rule-based",
        "rca_score": top_score,
        "candidate_services": candidate_services,
        "evidence": evidence,
    }
