
import axios from "./api";

export const getMyReportRequests = (token) =>
  axios.get("/report/request/my", {
    headers: { Authorization: `Bearer ${token}` }
  });
