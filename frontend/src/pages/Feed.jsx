import { useState, useEffect } from "react";
import { getStories } from "../api";
import StoryCard from "../components/StoryCard";
import styles from "./Feed.module.css";

const CATEGORIES = ["전체", "시험운", "발표운", "급식운", "자리운", "날씨운", "기타"];

export default function Feed() {
  const [stories, setStories] = useState([]);
  const [category, setCategory] = useState("전체");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = category !== "전체" ? { category } : {};
    getStories(params)
      .then((r) => setStories(r.data))
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <div className="container">
      <div className={styles.header}>
        <span className={styles.clover}>🍀</span>
        <h1 className={`${styles.title} glitch`} data-text="운칠기삼">운칠기삼</h1>
        <p className={styles.sub}>학교생활 속 운빨 사연을 공유해요</p>
      </div>

      <div className={styles.filters}>
        {CATEGORIES.map((c) => (
          <button
            key={c}
            className={styles.filterBtn}
            data-active={category === c}
            onClick={() => setCategory(c)}
          >
            {c}
          </button>
        ))}
      </div>

      {loading ? (
        <p className={styles.empty}>불러오는 중...</p>
      ) : stories.length === 0 ? (
        <p className={styles.empty}>아직 사연이 없어요. 첫 번째로 올려보세요!</p>
      ) : (
        <div className={styles.list}>
          {stories.map((s) => <StoryCard key={s.id} story={s} />)}
        </div>
      )}
    </div>
  );
}
