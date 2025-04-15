
import React, { useEffect, useState } from "react";
import { fetchUsers, createUser, updateUser, deleteUser } from "../services/userService";

function AdminAccounts() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    username: "",
    password: "",
    ten_chi_nhanh: "",
    is_admin: false
  });
  const [editId, setEditId] = useState(null);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const res = await fetchUsers(token);
      setUsers(res.data);
    } catch (err) {
      setError("Không thể tải danh sách người dùng.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await updateUser(editId, form, token);
      } else {
        await createUser(form, token);
      }
      setForm({ username: "", password: "", ten_chi_nhanh: "", is_admin: false });
      setEditId(null);
      loadUsers();
    } catch (err) {
      setError("Lỗi khi lưu tài khoản.");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Xoá tài khoản này?")) {
      await deleteUser(id, token);
      loadUsers();
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Quản lý tài khoản chi nhánh</h2>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="mb-4 space-y-2">
        <input
          value={form.username || ""}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          placeholder="Username"
          className="border px-2 py-1"
          required
        />
        <input
          value={form.password || ""}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          placeholder="Password"
          type="password"
          className="border px-2 py-1"
          required
        />
        <input
          value={form.ten_chi_nhanh || ""}
          onChange={(e) => setForm({ ...form, ten_chi_nhanh: e.target.value })}
          placeholder="Tên chi nhánh"
          className="border px-2 py-1"
        />
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            checked={form.is_admin}
            onChange={(e) => setForm({ ...form, is_admin: e.target.checked })}
            className="mr-1"
          />
          Admin?
        </label>
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">
          {editId ? "Cập nhật" : "Tạo mới"}
        </button>
      </form>
      <table className="w-full table-auto border">
        <thead>
          <tr className="bg-gray-200">
            <th>ID</th><th>Username</th><th>Tên chi nhánh</th><th>Admin</th><th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id} className="text-center border-t">
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.ten_chi_nhanh}</td>
              <td>{user.is_admin ? "✔" : ""}</td>
              <td>
                <button
                  onClick={() => {
                    setForm({
                      username: user.username || "",
                      password: "",
                      ten_chi_nhanh: user.ten_chi_nhanh || "",
                      is_admin: user.is_admin || false
                    });
                    setEditId(user.id);
                  }}
                  className="text-blue-600 mr-2"
                >
                  Sửa
                </button>
                <button
                  onClick={() => handleDelete(user.id)}
                  className="text-red-600"
                >
                  Xoá
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminAccounts;
