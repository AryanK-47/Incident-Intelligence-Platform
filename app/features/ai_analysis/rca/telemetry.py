
from typing import Any

import pandas as pd


REQUIRED_SIGNAL_COLUMNS = [
    "cpu_early_change",
    "mem_early_change",
    "latency-50_early_change",
    "latency-90_early_change",
]


def build_onset_dataframe(
    telemetry: list[dict[str, Any]],
) -> pd.DataFrame:
    """
    Validate telemetry records and convert them into
    the DataFrame format expected by score_v1_rca().

    Each record must contain:
    - case
    - service
    - cpu_early_change
    - mem_early_change
    - latency-50_early_change
    - latency-90_early_change

    This function does not collect telemetry or calculate
    the early-change signals.
    """
    if not telemetry:
        raise ValueError("Telemetry input cannot be empty.")

    onset_df = pd.DataFrame(telemetry)

    required_columns = ["case", "service"] + REQUIRED_SIGNAL_COLUMNS

    missing_columns = [
        column
        for column in required_columns
        if column not in onset_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required telemetry columns: {missing_columns}"
        )

    if onset_df[required_columns].isnull().any().any():
        raise ValueError(
            "Telemetry contains missing values in required columns."
        )

    if onset_df["service"].astype(str).str.strip().eq("").any():
        raise ValueError("Service names cannot be empty.")

    signal_values = onset_df[REQUIRED_SIGNAL_COLUMNS].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if signal_values.isnull().any().any():
        raise ValueError(
            "Telemetry signal values must be numeric."
        )

    onset_df[REQUIRED_SIGNAL_COLUMNS] = signal_values

    return onset_df
