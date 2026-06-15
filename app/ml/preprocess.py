import numpy as np
from dataclasses import dataclass

CATEGORY_MAP = {
    "시험운": 0,
    "발표운": 1,
    "급식운": 2,
    "자리운": 3,
    "날씨운": 4,
    "기타": 5,
}

CATEGORY_COUNT = len(CATEGORY_MAP)


@dataclass
class StoryFeatures:
    control_score: int      # 1~5: 통제 가능성 (낮을수록 운의 영향 큼)
    stress_score: int       # 1~5: 스트레스 수준
    satisfaction_score: int # 1~5: 만족도
    category: str


def encode_category(category: str) -> list[int]:
    """카테고리를 원-핫 인코딩으로 변환"""
    one_hot = [0] * CATEGORY_COUNT
    idx = CATEGORY_MAP.get(category, CATEGORY_MAP["기타"])
    one_hot[idx] = 1
    return one_hot


def extract_features(features: StoryFeatures) -> np.ndarray:
    """
    모델 입력 벡터 생성
    [control_score, stress_score, satisfaction_score, ...category_one_hot]
    총 3 + CATEGORY_COUNT 차원
    """
    numeric = [
        features.control_score / 5.0,
        features.stress_score / 5.0,
        features.satisfaction_score / 5.0,
    ]
    category_enc = encode_category(features.category)
    return np.array(numeric + category_enc, dtype=np.float32)


def features_from_story(story) -> StoryFeatures:
    """ORM LuckStory 객체 → StoryFeatures"""
    return StoryFeatures(
        control_score=story.control_score,
        stress_score=story.stress_score,
        satisfaction_score=story.satisfaction_score,
        category=story.category,
    )
