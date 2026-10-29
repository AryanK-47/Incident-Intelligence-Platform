
from typing import Any

from app.features.ai_analysis.rca.telemetry import build_onset_dataframe
from app.features.ai_analysis.rca.rca_scorer import score_v1_rca
from app.features.ai_analysis.rca.rca_output import build_rca_output
from app.features.ai_analysis.versions.schemas import VersionCreate


def generate_rca(
    telemetry: list[dict[str, Any]],
) -> VersionCreate:
    """
    Generate a structured RCA result from precomputed telemetry signals.

    This function does not fetch telemetry, calculate early-change
    signals, or persist results to the database.
    """

    onset_df = build_onset_dataframe(telemetry)

    score_df, predictions = score_v1_rca(onset_df)

    # The current scorer supports multiple cases, but this output
    # builder currently expects exactly one prediction.
    cases = onset_df["case"].unique()

    if len(cases) != 1:
        raise ValueError(
            "RCA inference currently requires telemetry for exactly one case."
        )

    payload = build_rca_output(score_df, predictions)

    return VersionCreate.model_validate(payload)
