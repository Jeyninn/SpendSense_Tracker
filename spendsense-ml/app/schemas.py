
from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)

    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)

    reference_amount: float = Field(gt=0)
    has_personal_history: bool = True


class AnomalyResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    severity: str
    explanation: str
    model_version: str
