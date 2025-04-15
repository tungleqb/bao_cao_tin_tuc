import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8000", // hoặc URL thật khi deploy
  headers: {
    "Content-Type": "application/json",
  },
});

export default instance;