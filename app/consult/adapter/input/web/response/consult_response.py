from pydantic import BaseModel, ConfigDict

from app.consult.domain.analysis import ConcernAnalysis


class ConsultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis: ConcernAnalysis
    answer: str
