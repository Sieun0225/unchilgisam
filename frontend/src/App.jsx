import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Feed from "./pages/Feed";
import StoryDetail from "./pages/StoryDetail";
import Rankings from "./pages/Rankings";
import Write from "./pages/Write";
import CursorGlow from "./components/CursorGlow";

export default function App() {
  return (
    <BrowserRouter>
      <CursorGlow />
      <Navbar />
      <Routes>
        <Route path="/" element={<Feed />} />
        <Route path="/stories/:id" element={<StoryDetail />} />
        <Route path="/rankings" element={<Rankings />} />
        <Route path="/write" element={<Write />} />
      </Routes>
    </BrowserRouter>
  );
}
