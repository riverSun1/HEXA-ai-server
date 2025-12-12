class Analysis:
    """상담 분석 결과 도메인"""

    def __init__(
        self,
        situation: str,
        traits: str,
        solutions: str,
        cautions: str,
        compatibility: str | None = None,
        scripts: str | None = None,
    ):
        self._validate(situation, traits, solutions, cautions)
        self.situation = situation
        self.traits = traits
        self.solutions = solutions
        self.cautions = cautions
        self.compatibility = compatibility  # 상대방 MBTI 궁합 분석 (optional)
        self.scripts = scripts  # 대화 스크립트 제안 (optional)

    def _validate(self, situation: str, traits: str, solutions: str, cautions: str) -> None:
        if not situation or not situation.strip():
            raise ValueError("situation은 비어있을 수 없습니다")
        if not traits or not traits.strip():
            raise ValueError("traits는 비어있을 수 없습니다")
        if not solutions or not solutions.strip():
            raise ValueError("solutions는 비어있을 수 없습니다")
        if not cautions or not cautions.strip():
            raise ValueError("cautions는 비어있을 수 없습니다")

    def to_dict(self) -> dict:
        """Analysis를 dict로 변환한다"""
        result = {
            "situation": self.situation,
            "traits": self.traits,
            "solutions": self.solutions,
            "cautions": self.cautions,
        }
        if self.compatibility:
            result["compatibility"] = self.compatibility
        if self.scripts:
            result["scripts"] = self.scripts
        return result
