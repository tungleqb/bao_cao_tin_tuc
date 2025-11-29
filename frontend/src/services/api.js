import axios from "axios";
const API = window.__ENV__?.VITE_API_BASE_URL || "https://localhost:8000";


const instance = axios.create({
  baseURL: `${API}`, // hoặc URL thật khi deploy
  //headers: {
  //  "Content-Type": "application/json",
  //},
  withCredentials: true,
});

export default instance;