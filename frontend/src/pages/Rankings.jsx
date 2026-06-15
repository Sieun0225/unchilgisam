import { useState, useEffect } from "react";
import { getLuckRanking, getViewsRanking } from "../api";
import { Link } from "react-router-dom";
import styles from "./Rankings.module.css";

const MEDALS = ["🥇", "🥈", "🥉"];
const RANK_CLASS = [styles.rank1, styles.rank2, styles.rank3];

export default function Rankings() {
  const [tab, setTab] = useState("luck");
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const fetch = tab === "luck" ? getLuckRanking : getViewsRanking;
    fetch(10).then((r) => setList(r.data)).finally(() => setLoading(false));
  }, [tab]);

  return (
    <div className="container">
      <div className={styles.header}>
        <span className={styles.crown}>👑</span>
        <h2 className={`${styles.title} glitch`} data-text="RANKING">RANKING</h2>
        <p className={styles.titleSub}>운칠기삼 명예의 전당</p>
      </div>

      <div className={styles.tabs}>
        <button data-active={tab === "luck"} onClick={() => setTab("luck")}>
          🍀 LUCK SCORE
        </button>
        <button data-active={tab === "views"} onClick={() => setTab("views")}>
          👀 조회수
        </button>
      </div>

      {loading ? (
        <p className={styles.empty}>불러오는 중...</p>
      ) : (
        <div className={styles.list}>
          {list.map((story, i) => (
            <Link
              to={`/stories/${story.id}`}
              key={story.id}
              className={`${styles.item} ${RANK_CLASS[i] ?? ""}`}
            >
              <div className={styles.rankBar} />
              <div className={styles.itemInner}>
                <div className={styles.rankNum}>
                  {i < 3 ? (
                    <span className={styles.medal}>{MEDALS[i]}</span>
                  ) : (
                    `${i + 1}`
                  )}
                </div>
                <div className={styles.info}>
                  <p className={styles.storyTitle}>{story.title}</p>
                  <span className={styles.categoryTag}>{story.category}</span>
                </div>
                <div className={styles.value}>
                  <span className={styles.valueNum}>
                    {tab === "luck"
                      ? (story.prediction?.luck_score?.toFixed(0) ?? "-")
                      : story.views_count}
                  </span>
                  <span className={styles.valueUnit}>
                    {tab === "luck" ? "pts" : "views"}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
