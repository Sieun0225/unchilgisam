import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000/api" });

export const getStories = (params) => api.get("/stories/", { params });
export const getStory = (id) => api.get(`/stories/${id}`);
export const createStory = (userId, data) =>
  api.post(`/stories/?user_id=${userId}`, data);
export const deleteStory = (id) => api.delete(`/stories/${id}`);

export const createVote = (data) => api.post("/votes/", data);
export const getVoteSummary = (storyId) => api.get(`/votes/${storyId}/summary`);

export const getLuckRanking = (limit = 10) =>
  api.get("/rankings/luck", { params: { limit } });
export const getViewsRanking = (limit = 10) =>
  api.get("/rankings/views", { params: { limit } });
