from typing import Optional

from app.consult.application.port.counseling_port import CounselingPort
from app.consult.application.port.nlp_analysis_port import NlpAnalysisPort
from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.domain.consult import ConsultHistory, ConsultResult


class ConsultUseCase:
    def __init__(
        self,
        analysis_port: NlpAnalysisPort,
        counseling_port: CounselingPort,
        consult_repository: ConsultRepositoryPort,
    ):
        self.analysis_port = analysis_port
        self.counseling_port = counseling_port
        self.consult_repository = consult_repository

    async def execute(self, text: str, user_id: Optional[int] = None) -> ConsultResult:
        analysis = await self.analysis_port.analyze(text)
        answer = await self.counseling_port.generate(text, analysis)

        history = ConsultHistory(
            user_id=user_id,
            original_text=text,
            analysis=analysis,
            answer=answer,
        )
        self.consult_repository.save(history)

        return ConsultResult(analysis=analysis, answer=answer)
