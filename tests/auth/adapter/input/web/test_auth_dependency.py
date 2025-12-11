import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.auth.adapter.input.web.auth_dependency import (
    get_current_user_id,
    set_session_repository,
)
from app.auth.domain.session import Session
from tests.auth.fixtures.fake_session_repository import FakeSessionRepository


@pytest.fixture
def session_repo():
    """테스트용 세션 저장소"""
    return FakeSessionRepository()


@pytest.fixture
def app(session_repo):
    """테스트용 FastAPI 앱"""
    test_app = FastAPI()

    # 세션 저장소 설정
    set_session_repository(session_repo)

    @test_app.get("/protected")
    def protected_route(user_id: str = Depends(get_current_user_id)):
        return {"user_id": user_id}

    return test_app


@pytest.fixture
def client(app):
    """테스트 클라이언트"""
    return TestClient(app)


class TestAuthDependency:
    """인증 의존성 테스트"""

    def test_유효한_세션으로_user_id_반환(self, client, session_repo):
        """유효한 세션 ID면 user_id를 반환한다"""
        # Given: 유효한 세션
        session = Session(session_id="valid-session-123", user_id="user-456")
        session_repo.save(session)

        # When: Authorization 헤더로 요청
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer valid-session-123"},
        )

        # Then: user_id 반환
        assert response.status_code == 200
        assert response.json()["user_id"] == "user-456"

    def test_세션_없이_요청시_401_에러(self, client):
        """Authorization 헤더 없이 요청하면 401 에러"""
        response = client.get("/protected")

        assert response.status_code == 401
        assert "인증" in response.json()["detail"]

    def test_유효하지_않은_세션으로_요청시_401_에러(self, client, session_repo):
        """존재하지 않는 세션 ID면 401 에러"""
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer invalid-session-999"},
        )

        assert response.status_code == 401
        assert "세션" in response.json()["detail"]

    def test_잘못된_authorization_형식_401_에러(self, client):
        """Bearer 형식이 아니면 401 에러"""
        response = client.get(
            "/protected",
            headers={"Authorization": "Basic some-token"},
        )

        assert response.status_code == 401
