// frontend/src/services/periodService.js

import axios from "./api";

export const getActivePeriods = (token) => {
  return axios.get("/period/active", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
