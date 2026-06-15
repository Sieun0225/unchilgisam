import { useEffect, useRef } from "react";
import styles from "./CursorGlow.module.css";

export default function CursorGlow() {
  const outerRef = useRef(null);
  const innerRef = useRef(null);
  const pos = useRef({ x: -999, y: -999 });
  const cur = useRef({ x: -999, y: -999 });
  const rafRef = useRef(null);

  useEffect(() => {
    const onMove = (e) => {
      pos.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener("mousemove", onMove);

    const loop = () => {
      // 외부 글로우는 부드럽게 따라옴
      cur.current.x += (pos.current.x - cur.current.x) * 0.08;
      cur.current.y += (pos.current.y - cur.current.y) * 0.08;

      if (outerRef.current) {
        outerRef.current.style.transform = `translate(${cur.current.x}px, ${cur.current.y}px)`;
      }
      // 내부 점은 즉시 따라옴
      if (innerRef.current) {
        innerRef.current.style.transform = `translate(${pos.current.x}px, ${pos.current.y}px)`;
      }
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <>
      <div ref={outerRef} className={styles.outer} />
      <div ref={innerRef} className={styles.inner} />
    </>
  );
}
