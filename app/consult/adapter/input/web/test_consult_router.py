import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.consult.adapter.input.web.consult_router import consult_router, get_consult_use_case
from app.consult.domain.analysis import ConcernAnalysis
from app.consult.domain.consult import ConsultResult


class StubConsultUseCase:
    def __init__(self, result: ConsultResult):
        self.result = result
        self.called_with = None

    async def execute(self, text: str, user_id=None):
        self.called_with = {"text": text, "user_id": user_id}
        return self.result


@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(consult_router)

    sample_analysis = ConcernAnalysis(
        summary="요약",
        category="mental",
        user_role="student",
        counterparty="none",
        emotion=["anxious"],
        urgency=3,
        main_question="무엇을 해야 하나요?",
        constraints=["시간 부족"],
        keywords=["불안", "시험"],
        suicide_risk=False,
    )
    stub = StubConsultUseCase(ConsultResult(analysis=sample_analysis, answer="조언"))

    async def override_use_case():
        return stub

    app.dependency_overrides[get_consult_use_case] = override_use_case

    with TestClient(app) as client:
        yield client, stub


def test_consult_endpoint_returns_analysis_and_answer(test_client):
    client, stub = test_client
    payload = {"text": "시험이 걱정돼요", "user_id": 5}

    response = client.post("/consult", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["analysis"]["summary"] == "요약"
    assert body["answer"] == "조언"
    assert stub.called_with == {"text": "시험이 걱정돼요", "user_id": 5}
