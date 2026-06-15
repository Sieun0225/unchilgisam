"""
모델 학습 스크립트
실행: python -m app.ml.train
"""
import numpy as np
import pickle
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from app.ml.preprocess import StoryFeatures, extract_features, CATEGORY_MAP

MODEL_PATH = Path(__file__).parent / "luck_model.pkl"


def generate_synthetic_data(n: int = 500) -> tuple[np.ndarray, np.ndarray]:
    """
    실제 데이터가 없을 때 사용하는 합성 학습 데이터 생성

    Luck Score 규칙:
    - control_score 낮을수록 운의 영향 큼 → luck_score 높음
    - satisfaction_score 높을수록 → luck_score 높음
    - stress_score 높을수록 → luck_score 낮음
    """
    rng = np.random.default_rng(42)
    categories = list(CATEGORY_MAP.keys())

    X, y = [], []
    for _ in range(n):
        ctrl = rng.integers(1, 6)
        stress = rng.integers(1, 6)
        satis = rng.integers(1, 6)
        cat = rng.choice(categories)

        features = StoryFeatures(
            control_score=int(ctrl),
            stress_score=int(stress),
            satisfaction_score=int(satis),
            category=cat,
        )
        luck = (
            (6 - ctrl) * 18        # 통제 불가능할수록 운빨
            + satis * 14           # 만족도 높을수록 운 좋음
            - stress * 8           # 스트레스 높을수록 운 나쁨
            + rng.normal(0, 5)     # 노이즈
        )
        luck = float(np.clip(luck, 0, 100))
        X.append(extract_features(features))
        y.append(luck)

    return np.array(X), np.array(y)


def train_and_save():
    X, y = generate_synthetic_data(500)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"MAE : {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"R²  : {r2_score(y_test, y_pred):.4f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"모델 저장 완료 → {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save()
