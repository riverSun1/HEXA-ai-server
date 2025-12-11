"""OpenAI 기반 메시지 변환 어댑터"""

import json
from openai import OpenAI

from app.converter.application.port.message_converter_port import MessageConverterPort
from app.converter.domain.tone_message import ToneMessage
from app.shared.vo.mbti import MBTI


class OpenAIMessageConverter(MessageConverterPort):
    """OpenAI API를 사용한 메시지 변환 구현체"""

    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI()

    def convert(
        self,
        original_message: str,
        sender_mbti: MBTI,
        receiver_mbti: MBTI,
        tone: str,
    ) -> ToneMessage:
        """메시지를 특정 톤으로 변환

        Args:
            original_message: 원본 메시지
            sender_mbti: 발신자 MBTI
            receiver_mbti: 수신자 MBTI
            tone: 변환할 톤

        Returns:
            ToneMessage: 변환된 메시지
        """
        prompt = self._build_prompt(original_message, sender_mbti, receiver_mbti, tone)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 MBTI 기반 커뮤니케이션 전문가입니다. 메시지를 지정된 톤으로 변환하고 JSON 형식으로 응답하세요.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        # JSON 응답 파싱
        content = response.choices[0].message.content
        result = json.loads(content)

        return ToneMessage(
            tone=tone, content=result["content"], explanation=result["explanation"]
        )

    def _build_prompt(
        self, original_message: str, sender_mbti: MBTI, receiver_mbti: MBTI, tone: str
    ) -> str:
        """프롬프트 생성

        Args:
            original_message: 원본 메시지
            sender_mbti: 발신자 MBTI
            receiver_mbti: 수신자 MBTI
            tone: 변환할 톤

        Returns:
            str: 생성된 프롬프트
        """
        # MBTI 차원별 특성 추출
        receiver_characteristics = self._get_mbti_characteristics(receiver_mbti)

        # 톤별 가이드라인 정의
        tone_guidelines = self._get_tone_guidelines(tone)

        return f"""다음 메시지를 '{tone}' 톤으로 변환해주세요.

발신자 MBTI: {sender_mbti.value}
수신자 MBTI: {receiver_mbti.value}

수신자의 MBTI 특성:
{receiver_characteristics}

원본 메시지: {original_message}

[{tone} 톤 변환 가이드라인]
{tone_guidelines}

위 가이드라인을 정확히 따라 메시지를 변환하고,
수신자의 MBTI 특성과 선택한 톤을 고려하여 왜 이 표현이 {receiver_mbti.value} 유형에게 효과적인지 설명해주세요.

JSON 형식으로 응답:
{{
    "content": "변환된 메시지",
    "explanation": "왜 이 표현이 효과적인지 설명 (2-3줄)"
}}"""

    def _get_tone_guidelines(self, tone: str) -> str:
        """톤별 변환 가이드라인을 반환

        Args:
            tone: 톤 ("공손한", "캐주얼한", "간결한")

        Returns:
            str: 톤별 구체적인 가이드라인
        """
        guidelines = {
            "공손한": """
• 존댓말 사용 (요체, 합니다체)
• 정중한 표현과 겸손한 어조 유지
• "~해주실 수 있을까요?", "~드립니다", "감사합니다" 등의 표현 사용
• 격식 있는 문장 구조
• 예시: "안녕하세요. 다음 주 회의 일정을 조율하고자 연락드렸습니다. 가능하신 시간을 알려주시면 감사하겠습니다."
            """,
            "캐주얼한": """
• 반말 또는 편한 말투 사용
• 친근하고 부담 없는 어조
• 이모지나 구어체 표현 활용 가능
• 자연스럽고 편안한 문장 구조
• 예시: "안녕! 다음 주 회의 시간 어때? 네가 편한 시간 알려줘~"
            """,
            "간결한": """
• 핵심 내용만 짧고 명확하게 전달
• 불필요한 수식어나 부연 설명 제거
• 명사형 종결이나 짧은 문장 사용
• 최소한의 단어로 의미 전달
• 예시: "다음 주 회의 시간 조율 필요. 가능한 시간대 공유 부탁드림."
            """,
        }

        return guidelines.get(
            tone,
            "• 메시지의 의미를 유지하면서 자연스럽게 변환해주세요.",
        )

    def _get_mbti_characteristics(self, mbti: MBTI) -> str:
        """MBTI 차원별 특성을 문자열로 반환

        Args:
            mbti: MBTI 값 객체

        Returns:
            str: MBTI 차원별 특성 설명
        """
        characteristics = []

        # E/I 차원
        if mbti.energy == "E":
            characteristics.append("- 외향적 (Extrovert): 활발하고 직접적인 소통 선호")
        else:
            characteristics.append("- 내향적 (Introvert): 신중하고 깊이 있는 소통 선호")

        # S/N 차원
        if mbti.information == "S":
            characteristics.append("- 감각적 (Sensing): 구체적이고 실용적인 정보 선호")
        else:
            characteristics.append("- 직관적 (Intuition): 추상적이고 가능성 있는 아이디어 선호")

        # T/F 차원
        if mbti.decision == "T":
            characteristics.append("- 사고형 (Thinking): 논리적이고 객관적인 접근 선호")
        else:
            characteristics.append("- 감정형 (Feeling): 감정적이고 공감적인 접근 선호")

        # J/P 차원
        if mbti.lifestyle == "J":
            characteristics.append("- 판단형 (Judging): 체계적이고 계획적인 방식 선호")
        else:
            characteristics.append("- 인식형 (Perceiving): 유연하고 즉흥적인 방식 선호")

        return "\n".join(characteristics)
