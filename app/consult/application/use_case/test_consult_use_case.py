import pytest
from unittest.mock import AsyncMock, Mock

from app.consult.application.use_case.consult_use_case import ConsultUseCase
from app.consult.application.port.counseling_port import CounselingPort
from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.application.port.nlp_analysis_port import NlpAnalysisPort
from app.consult.domain.analysis import ConcernAnalysis


@pytest.mark.anyio
class TestConsultUseCase:
    @pytest.fixture
    def analysis_port(self):
        return AsyncMock(spec=NlpAnalysisPort)

    @pytest.fixture
    def counseling_port(self):
        return AsyncMock(spec=CounselingPort)

    @pytest.fixture
    def repository(self):
        return Mock(spec=ConsultRepositoryPort)

    @pytest.fixture
    def use_case(self, analysis_port, counseling_port, repository):
        return ConsultUseCase(
            analysis_port=analysis_port,
            counseling_port=counseling_port,
            consult_repository=repository,
        )

    @pytest.fixture
    def sample_analysis(self):
        return ConcernAnalysis(
            summary="한 줄 요약",
            category="relationship",
            user_role="student",
            counterparty="friend",
            emotion=["sad"],
            urgency=2,
            main_question="무엇을 해야 할까요?",
            constraints=["시간 부족"],
            keywords=["학교", "친구"],
            suicide_risk=False,
        )

    async def test_execute_calls_ports_and_repository(
        self, use_case, analysis_port, counseling_port, repository, sample_analysis
    ):
        analysis_port.analyze.return_value = sample_analysis
        counseling_port.generate.return_value = "상담 결과"

        result = await use_case.execute(text="고민이 있어요", user_id=1)

        analysis_port.analyze.assert_awaited_once_with("고민이 있어요")
        counseling_port.generate.assert_awaited_once_with("고민이 있어요", sample_analysis)
        repository.save.assert_called_once()

        assert result.analysis.summary == sample_analysis.summary
        assert result.answer == "상담 결과"
