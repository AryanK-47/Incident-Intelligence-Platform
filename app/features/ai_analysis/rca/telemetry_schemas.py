
from pydantic import BaseModel, ConfigDict, Field


class TelemetrySignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case: str = Field(..., min_length=1)
    service: str = Field(..., min_length=1)

    cpu_early_change: float
    mem_early_change: float

    latency_50_early_change: float = Field(
        alias="latency-50_early_change"
    )
    latency_90_early_change: float = Field(
        alias="latency-90_early_change"
    )


class TelemetryRCARequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    telemetry: list[TelemetrySignal] = Field(..., min_length=1)
