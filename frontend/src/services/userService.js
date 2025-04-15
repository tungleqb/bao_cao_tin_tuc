
import axios from "./api";

export const fetchUsers = (token) =>
  axios.get("/admin/user", {
    headers: { Authorization: `Bearer ${token}` }
  });

export const createUser = (data, token) =>
  axios.post("/admin/user", data, {
    headers: { Authorization: `Bearer ${token}` }
  });

export const updateUser = (id, data, token) =>
  axios.put(`/admin/user/${id}`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });

export const deleteUser = (id, token) =>
  axios.delete(`/admin/user/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
