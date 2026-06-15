import pickle
import numpy as np
from pathlib import Path
from app.ml.preprocess import extract_features, features_from_story

MODEL_PATH = Path(__file__).parent / "luck_model.pkl"
MODEL_VERSION = "v1.0"

_model = None


def _load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"학습된 모델 파일이 없습니다. 먼저 'python -m app.ml.train'을 실행하세요."
            )
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict_luck(story) -> dict:
    """
    LuckStory ORM 객체를 받아 luck_score와 confidence를 반환

    Returns:
        {"luck_score": float, "confidence": float, "model_version": str}
    """
    model = _load_model()
    features = features_from_story(story)
    X = extract_features(features).reshape(1, -1)

    luck_score = float(np.clip(model.predict(X)[0], 0, 100))

    # GradientBoosting은 predict_proba가 없으므로 잔차 분산으로 confidence 추정
    # staged_predict로 개별 트리 예측 수집 후 표준편차 기반 신뢰도 계산
    staged = np.array([p[0] for p in model.staged_predict(X)])
    std = float(np.std(staged))
    confidence = float(np.clip(1.0 - std / 50.0, 0.0, 1.0))

    return {
        "luck_score": round(luck_score, 2),
        "confidence": round(confidence, 4),
        "model_version": MODEL_VERSION,
    }


def predict_luck_batch(stories: list) -> list[dict]:
    """여러 사연을 한 번에 예측"""
    return [predict_luck(story) for story in stories]
