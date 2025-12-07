import pytest
from app.auth.domain.session import Session


def test_create_session_with_valid_values():
    """유효한 session_id와 user_id로 Session 객체를 생성할 수 있다"""
    # Given: 유효한 값들
    session_id = "session-abc-123"
    user_id = "user-xyz-456"

    # When: Session 객체를 생성하면
    session = Session(session_id=session_id, user_id=user_id)

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert session.session_id == "session-abc-123"
    assert session.user_id == "user-xyz-456"


def test_reject_empty_session_id():
    """빈 session_id를 거부한다"""
    with pytest.raises(ValueError):
        Session(session_id="", user_id="user-123")


def test_reject_empty_user_id():
    """빈 user_id를 거부한다"""
    with pytest.raises(ValueError):
        Session(session_id="session-123", user_id="")