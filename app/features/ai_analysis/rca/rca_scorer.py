
import pandas as pd


def score_v1_rca(
    onset_df,
    signal_cols=None,
    case_col="case",
    service_col="service"
):
    """
    Frozen V1 RCA scorer.

    Uses within-case percentile ranks of:
    - CPU early change
    - Memory early change
    - Latency-50 early change
    - Latency-90 early change

    The mean of these ranks is the onset score.

    The service with the highest onset score is selected
    as the predicted root-cause service.

    This is a deterministic rule-based scorer.
    No model training is performed.
    """

    if signal_cols is None:
        signal_cols = [
            "cpu_early_change",
            "mem_early_change",
            "latency-50_early_change",
            "latency-90_early_change"
        ]

    required_cols = [case_col, service_col] + signal_cols

    missing_cols = [
        col for col in required_cols
        if col not in onset_df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}"
        )

    score_df = onset_df.copy()

    rank_cols = []

    for col in signal_cols:
        rank_col = f"{col}_rank"

        score_df[rank_col] = (
            score_df
            .groupby(case_col)[col]
            .rank(method="average", pct=True)
        )

        rank_cols.append(rank_col)

    score_df["onset_score"] = (
        score_df[rank_cols]
        .mean(axis=1)
    )

    predictions = (
        score_df
        .sort_values(
            [case_col, "onset_score", service_col],
            ascending=[True, False, True]
        )
        .groupby(case_col, as_index=False)
        .first()
    )

    return score_df, predictions
