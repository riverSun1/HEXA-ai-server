import pytest

from app.consult.application.use_case.start_consult_use_case import StartConsultUseCase
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from tests.consult.fixtures.fake_consult_repository import FakeConsultRepository
from tests.consult.fixtures.fake_ai_counselor import FakeAICounselor


@pytest.fixture
def repository():
    """테스트용 Fake Consult 저장소"""
    return FakeConsultRepository()


@pytest.fixture
def ai_counselor():
    """테스트용 Fake AI Counselor"""
    return FakeAICounselor()


@pytest.fixture
def use_case(repository, ai_counselor):
    """StartConsultUseCase"""
    return StartConsultUseCase(repository, ai_counselor)


def test_start_consult_creates_session(use_case, repository):
    """상담을 시작하면 새로운 세션이 생성된다"""
    # Given: 유효한 사용자 정보
    user_id = "user-456"
    mbti = MBTI("INTJ")
    gender = Gender("MALE")

    # When: 상담을 시작하면
    result = use_case.execute(user_id=user_id, mbti=mbti, gender=gender)

    # Then: 세션 ID가 반환되고
    assert "session_id" in result
    session_id = result["session_id"]
    assert session_id is not None

    # 세션이 저장된다
    saved_session = repository.find_by_id(session_id)
    assert saved_session is not None
    assert saved_session.user_id == user_id
    assert saved_session.mbti.value == "INTJ"
    assert saved_session.gender.value == "MALE"


def test_start_consult_generates_unique_session_ids(use_case):
    """상담을 여러 번 시작하면 각각 다른 세션 ID가 생성된다"""
    # Given: 동일한 사용자 정보
    user_id = "user-456"
    mbti = MBTI("INTJ")
    gender = Gender("MALE")

    # When: 상담을 2번 시작하면
    result1 = use_case.execute(user_id=user_id, mbti=mbti, gender=gender)
    result2 = use_case.execute(user_id=user_id, mbti=mbti, gender=gender)

    # Then: 각각 다른 세션 ID가 생성된다
    assert result1["session_id"] != result2["session_id"]


def test_start_consult_returns_ai_greeting(use_case):
    """상담을 시작하면 AI 인사말이 포함된다"""
    # Given: 유효한 사용자 정보
    user_id = "user-789"
    mbti = MBTI("ENFP")
    gender = Gender("FEMALE")

    # When: 상담을 시작하면
    result = use_case.execute(user_id=user_id, mbti=mbti, gender=gender)

    # Then: greeting 필드가 포함되어 있고
    assert "greeting" in result
    assert result["greeting"] is not None
    assert len(result["greeting"]) > 0
