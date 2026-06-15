import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createStory } from "../api";
import styles from "./Write.module.css";

const CATEGORIES = ["시험운", "발표운", "급식운", "자리운", "날씨운", "기타"];
const USER_ID = 1; // 임시 고정값

export default function Write() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: "", content: "", category: "시험운",
    control_score: 3, stress_score: 3, satisfaction_score: 3,
  });
  const [loading, setLoading] = useState(false);

  const set = (key, val) => setForm((f) => ({ ...f, [key]: val }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim() || !form.content.trim()) return;
    setLoading(true);
    try {
      const r = await createStory(USER_ID, form);
      navigate(`/stories/${r.data.id}`);
    } catch {
      alert("등록에 실패했어요. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2 className={styles.title}>사연 쓰기 ✍️</h2>

      <div className={styles.formWrap}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.field}>
          <label>카테고리</label>
          <select value={form.category} onChange={(e) => set("category", e.target.value)}>
            {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
          </select>
        </div>

        <div className={styles.field}>
          <label>제목</label>
          <input
            placeholder="한 줄로 요약해주세요"
            value={form.title}
            maxLength={100}
            onChange={(e) => set("title", e.target.value)}
          />
        </div>

        <div className={styles.field}>
          <label>내용</label>
          <textarea
            placeholder="어떤 일이 있었나요? 자세히 써주세요"
            value={form.content}
            rows={6}
            onChange={(e) => set("content", e.target.value)}
          />
        </div>

        <div className={styles.sliders}>
          <ScoreSlider
            label="통제 가능성"
            hint="낮을수록 완전 운빨"
            value={form.control_score}
            onChange={(v) => set("control_score", v)}
          />
          <ScoreSlider
            label="스트레스 수준"
            hint="높을수록 스트레스 심함"
            value={form.stress_score}
            onChange={(v) => set("stress_score", v)}
          />
          <ScoreSlider
            label="만족도"
            hint="높을수록 결과 만족"
            value={form.satisfaction_score}
            onChange={(v) => set("satisfaction_score", v)}
          />
        </div>

        <button type="submit" className={styles.submit} disabled={loading}>
          {loading ? "분석 중... 🍀" : "사연 등록하기"}
        </button>
      </form>
      </div>
    </div>
  );
}

function ScoreSlider({ label, hint, value, onChange }) {
  return (
    <div className={styles.slider}>
      <div className={styles.sliderTop}>
        <span className={styles.sliderLabel}>{label}</span>
        <span className={styles.sliderVal}>{value} / 5</span>
      </div>
      <p className={styles.sliderHint}>{hint}</p>
      <input
        type="range" min={1} max={5} step={1}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className={styles.range}
      />
    </div>
  );
}
