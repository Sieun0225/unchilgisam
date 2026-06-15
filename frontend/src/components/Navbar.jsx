import { Link, useLocation, useNavigate } from "react-router-dom";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  return (
    <nav className={styles.nav}>
      <Link to="/" className={styles.logo}>
        <span className={styles.logoLeaf}>🍀</span>운칠기삼
      </Link>
      <div className={styles.links}>
        <Link to="/" className={pathname === "/" ? styles.active : ""}>피드</Link>
        <Link to="/rankings" className={pathname === "/rankings" ? styles.active : ""}>랭킹</Link>
        <button className={styles.writeBtn} onClick={() => navigate("/write")}>사연 쓰기</button>
      </div>
    </nav>
  );
}
