// frontend/src/utils/auth.js

import axios from "../services/api";

export const getTokenInfo = async () => {
  try {
    const res = await axios.get("/auth/me", { withCredentials: true });
    return res.data;
  } catch (err) {
    console.error("Token not valid or expired", err);
    return null;
  }
};
