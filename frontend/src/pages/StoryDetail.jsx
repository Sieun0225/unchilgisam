import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getStory, createVote, getVoteSummary } from "../api";
import styles from "./StoryDetail.module.css";

const USER_ID = 1; // 임시 고정값

export default function StoryDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [story, setStory] = useState(null);
  const [votes, setVotes] = useState(null);
  const [voted, setVoted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getStory(id), getVoteSummary(id)])
      .then(([s, v]) => { setStory(s.data); setVotes(v.data); })
      .finally(() => setLoading(false));
  }, [id]);

  const handleVote = async (type) => {
    try {
      await createVote({ story_id: Number(id), user_id: USER_ID, vote_type: type });
      const r = await getVoteSummary(id);
      setVotes(r.data);
      setVoted(true);
    } catch (e) {
      if (e.response?.status === 409) alert("이미 투표했어요!");
    }
  };

  if (loading) return <p className={styles.empty}>불러오는 중...</p>;
  if (!story) return <p className={styles.empty}>사연을 찾을 수 없어요.</p>;

  const score = story.prediction?.luck_score;
  const confidence = story.prediction?.confidence;

  return (
    <div className="container">
      <button className={styles.back} onClick={() => navigate(-1)}>← 돌아가기</button>

      <div className={styles.card}>
      <div className={styles.cardInner}>
        <div className={styles.top}>
          <span className={styles.category}>{story.category}</span>
          <span className={styles.date}>
            {new Date(story.created_at).toLocaleDateString("ko-KR")}
          </span>
        </div>

        <h2 className={styles.title}>{story.title}</h2>
        <p className={styles.content}>{story.content}</p>

        <div className={styles.scores}>
          <div className={styles.scoreItem}>
            <span className={styles.label}>통제 가능성</span>
            <Dots value={story.control_score} />
          </div>
          <div className={styles.scoreItem}>
            <span className={styles.label}>스트레스</span>
            <Dots value={story.stress_score} />
          </div>
          <div className={styles.scoreItem}>
            <span className={styles.label}>만족도</span>
            <Dots value={story.satisfaction_score} />
          </div>
        </div>

        {score != null && (
          <div className={styles.luck}>
            <div className={styles.luckLabel}>🍀 Luck Score</div>
            <div className={styles.luckScore}>{score.toFixed(1)}점</div>
            <div className={styles.luckBar}>
              <div className={styles.luckFill} style={{ width: `${score}%` }} />
            </div>
            <div className={styles.luckConf}>
              신뢰도 {((confidence ?? 0) * 100).toFixed(0)}%
            </div>
          </div>
        )}
      </div>
      </div>

      {votes && (
        <div className={styles.voteBox}>
        <div className={styles.voteInner}>
          <p className={styles.voteTitle}>이 사연, 진짜 운빨이야?</p>
          <div className={styles.voteBtns}>
            <button
              className={styles.voteUp}
              onClick={() => handleVote("+")}
              disabled={voted}
            >
              👍 운빨 맞아 {votes.plus_count}
            </button>
            <button
              className={styles.voteDown}
              onClick={() => handleVote("-")}
              disabled={voted}
            >
              👎 노력이지 {votes.minus_count}
            </button>
          </div>
          {voted && <p className={styles.voted}>투표 완료!</p>}
        </div>
        </div>
      )}
    </div>
  );
}

function Dots({ value }) {
  return (
    <div style={{ display: "flex", gap: 5 }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <span
          key={i}
          style={{
            width: 10, height: 10, borderRadius: "2px",
            background: i <= value ? "var(--neon)" : "rgba(255,255,255,0.06)",
            border: i <= value ? "1px solid rgba(0,255,136,0.6)" : "1px solid rgba(255,255,255,0.08)",
            boxShadow: i <= value ? "0 0 6px var(--neon)" : "none",
            transition: "all 0.2s",
          }}
        />
      ))}
    </div>
  );
}
