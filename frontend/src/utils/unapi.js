import axios from "axios";
const API = import.meta.env.VITE_API_BASE_URL;

const token = localStorage.getItem("token");

const api = axios.create({
  baseURL: `${API}:8000`,  // chỉnh theo backend
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

export default api;
