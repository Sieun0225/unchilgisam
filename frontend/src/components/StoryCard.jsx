import { Link } from "react-router-dom";
import styles from "./StoryCard.module.css";

const CATEGORY_EMOJI = {
  시험운: "📝", 발표운: "🎤", 급식운: "🍱", 자리운: "💺", 날씨운: "☀️", 기타: "✨",
};

export default function StoryCard({ story }) {
  const score = story.prediction?.luck_score;

  return (
    <Link to={`/stories/${story.id}`} className={styles.card}>
    <div className={styles.inner}>
      <div className={styles.top}>
        <span className={styles.category}>
          {CATEGORY_EMOJI[story.category] ?? "✨"} {story.category}
        </span>
        {score != null && (
          <span className={styles.score} data-high={score >= 70}>
            🍀 {score.toFixed(0)}점
          </span>
        )}
      </div>
      <h3 className={styles.title}>{story.title}</h3>
      <div className={styles.meta}>
        <span>조회 {story.views_count}</span>
        <span>{new Date(story.created_at).toLocaleDateString("ko-KR")}</span>
      </div>
    </div>
    </Link>
  );
}
