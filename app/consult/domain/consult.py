from datetime import datetime
from typing import Optional

from app.consult.domain.analysis import ConcernAnalysis


class ConsultHistory:
    def __init__(
        self,
        user_id: Optional[int],
        original_text: str,
        analysis: ConcernAnalysis,
        answer: str,
        created_at: Optional[datetime] = None,
    ):
        self.id: Optional[int] = None
        self.user_id = user_id
        self.original_text = original_text
        self.analysis = analysis
        self.answer = answer
        self.created_at = created_at or datetime.utcnow()


class ConsultResult:
    def __init__(self, analysis: ConcernAnalysis, answer: str):
        self.analysis = analysis
        self.answer = answer
