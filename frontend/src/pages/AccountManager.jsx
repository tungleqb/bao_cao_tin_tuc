
import React, { useEffect, useRef, useState } from "react";
//import api from "../utils/api";
import axios from "../services/api";
import RenameModal from "../components/RenameModal";
import ResetPasswordModal from "../components/ResetPasswordModal";
import DeleteUserModal from "../components/DeleteUserModal";


const AccountManager = () => {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    username: "",
    name: "",
    level: "CAPPHONG",
    is_admin: false,
    password: "",
  });
  const [filters, setFilters] = useState({
    username: "",
    name: "",
    level: "",
    is_admin: "",
  });

  const [currentPage, setCurrentPage] = useState(1);
  const [menuOpen, setMenuOpen] = useState(null);
  const menuRef = useRef(null);
  const rowsPerPage = 10;

  const fetchUsers = async () => {
    try {
      //const token = localStorage.getItem("admin_token");
      const res = await axios.get("/admin/user");
      setUsers(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Failed to fetch users", err);
      setUsers([]);
    }
  };

  const [selectedUser, setSelectedUser] = useState(null);
  const [showRenameModal, setShowRenameModal] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);


  const handleRename = async (user, newName) => {
    try {
      await axios.put(`/admin/user/${user.id}`, {
        name: newName,
        level: user.level,
        password: user.password || "placeholder",  // hoặc để backend bỏ qua password
        is_admin: user.is_admin,
      });
      fetchUsers();
      alert("✅ Đổi tên thành công");
    } catch (err) {
      alert("❌ Lỗi khi đổi tên: " + err.response?.data?.detail || err.message);
    }
  };

  const handleResetPassword = async (user, newPassword) => {
    try {
      await axios.put(`/admin/user/${user.id}`, {
        name: user.name,
        level: user.level,
        password: newPassword,
        is_admin: user.is_admin,
      });
      alert("✅ Đổi mật khẩu thành công");
    } catch (err) {
      alert("❌ Lỗi khi đổi mật khẩu: " + (err.response?.data?.detail || err.message));
    }
  };
  const handleDeleteUser = async (user) => {
    try {
      await axios.delete(`/admin/user/${user.id}`);
      fetchUsers();
      alert("✅ Đã xoá tài khoản");
    } catch (err) {
      alert("❌ Lỗi khi xoá: " + (err.response?.data?.detail || err.message));
    }
  };
  const createUser = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/admin/user", form);
      alert("✅ Tạo tài khoản thành công");
      fetchUsers();
      setForm({
        username: "",
        name: "",
        level: "CAPPHONG",
        is_admin: false,
        password: "",
      });
    } catch (err) {
      alert("❌ Lỗi tạo tài khoản: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleToggleLock = async (user) => {
    try {
      await axios.put(`/admin/user/${user.id}`, {
        is_locked: !user.is_locked,
        name: user.name,
        level: user.level,
        is_admin: user.is_admin,
      });
      fetchUsers();
      alert(`✅ Đã ${user.is_locked ? "Mở khoá" : "Khoá"} tài khoản ${user.username}`);
    } catch (err) {
      alert("❌ Lỗi khi cập nhật trạng thái tài khoản: " + (err.response?.data?.detail || err.message));
    }
  };


  const handleAction = async (action, user) => {
    setMenuOpen(null);
    if (action === "rename") {
      setSelectedUser(user);
      setShowRenameModal(true);
    }

    if (action === "changepass") {
      setSelectedUser(user);
      setShowResetModal(true);
    }

    if (action === "delete") {
      setSelectedUser(user);
      setShowDeleteModal(true);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredUsers = users.filter((u) =>
    Object.entries(filters).every(([key, value]) =>
      u[key]?.toString().toLowerCase().includes(value.toLowerCase())
    )
  );

  const totalPages = Math.ceil(filteredUsers.length / rowsPerPage);
  const paginatedUsers = filteredUsers.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  return (
    <div className="p-4 space-y-6">
      <h2 className="text-xl font-bold">Tạo tài khoản mới</h2>
      <form onSubmit={createUser} className="space-y-2 bg-white p-4 rounded shadow w-full md:w-1/2">
        <input className="w-full border p-2" placeholder="Username" required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <input className="w-full border p-2" placeholder="Tên chi nhánh" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <select className="w-full border p-2" value={form.level} onChange={(e) => setForm({ ...form, level: e.target.value })}>
          <option value="CAPPHONG">Cấp phòng</option>
          <option value="CAPXA">Cấp xã</option>
        </select>
        <input className="w-full border p-2" type="password" placeholder="Mật khẩu" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <label className="flex items-center space-x-2">
          <input type="checkbox" checked={form.is_admin} onChange={(e) => setForm({ ...form, is_admin: e.target.checked })} />
          <span>Là tài khoản quản trị</span>
        </label>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Tạo tài khoản</button>
      </form>

      <h2 className="text-xl font-bold mt-10">Danh sách tài khoản</h2>
      <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">ID</th>
              <th className="border px-2 py-1">Username</th>
              <th className="border px-2 py-1">Tên</th>
              <th className="border px-2 py-1">Cấp</th>
              <th className="border px-2 py-1">Admin</th>
              <th className="border px-2 py-1">Ngày tạo</th>
              <th className="border px-2 py-1">Trạng thái</th>
              <th className="border px-2 py-1">Thao tác</th>
            </tr>
            <tr className="text-xs bg-white">
              <th></th>
              <th><input className="w-full border px-1 py-0.5 rounded" placeholder="Lọc Username" value={filters.username} onChange={(e) => setFilters({ ...filters, username: e.target.value })} /></th>
              <th><input className="w-full border px-1 py-0.5 rounded" placeholder="Lọc Tên" value={filters.name} onChange={(e) => setFilters({ ...filters, name: e.target.value })} /></th>
              <th><input className="w-full border px-1 py-0.5 rounded" placeholder="Lọc Cấp" value={filters.level} onChange={(e) => setFilters({ ...filters, level: e.target.value })} /></th>
              <th></th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {paginatedUsers.map((u, idx) => (
              <tr key={u.id}>
                <td className="border px-2 py-1">{u.id}</td>
                <td className="border px-2 py-1">{u.username}</td>
                <td className="border px-2 py-1">{u.name}</td>
                <td className="border px-2 py-1">{u.level}</td>
                <td className="border px-2 py-1">{u.is_admin ? "✔" : ""}</td>
                <td className="border px-2 py-1">{u.time_created?.slice(0, 10)}</td>
                <td className="border px-2 py-1">
                  {u.is_locked ? (
                    <span className="text-red-600 font-semibold">Đã khoá</span>
                  ) : (
                    <span className="text-green-600">Hoạt động</span>
                  )}
                </td>
                <td className="border px-2 py-1 relative" ref={menuOpen === idx ? menuRef : null}>
                  <button onClick={() => setMenuOpen(menuOpen === idx ? null : idx)} className="bg-gray-200 px-2 py-1 rounded">⋮</button>
                  {menuOpen === idx && (
                    <div className="absolute right-0 mt-1 bg-white border rounded shadow z-10">
                      <button onClick={() => handleAction("rename", u)} className="block w-full text-left px-4 py-2 hover:bg-gray-100">Đổi tên</button>
                      <button onClick={() => handleAction("changepass", u)} className="block w-full text-left px-4 py-2 hover:bg-gray-100">Đổi mật khẩu</button>
                      <button
                        onClick={() => handleToggleLock(u)}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-blue-600"
                      >
                        {u.is_locked ? "Mở khoá" : "Khoá"}
                      </button>
                      <button onClick={() => handleAction("delete", u)} className="block w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100">Xoá</button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-2 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <button className="px-3 py-1 border rounded hover:bg-gray-200" disabled={currentPage === 1} onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}>← Trước</button>
            <span>Trang:</span>
            <input type="number" min={1} max={totalPages} value={currentPage} onChange={(e) => setCurrentPage(Math.min(totalPages, Math.max(1, Number(e.target.value))))} className="border px-2 py-1 w-16 rounded" />
            <button className="px-3 py-1 border rounded hover:bg-gray-200" disabled={currentPage === totalPages} onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}>Sau →</button>
            <span className="text-sm text-gray-500 ml-2">Tổng: {totalPages} trang</span>
          </div>
        </div>
      </div>
      {showRenameModal && selectedUser && (
        <RenameModal
          user={selectedUser}
          onClose={() => setShowRenameModal(false)}
          onRename={handleRename}
        />
      )}
      {showResetModal && selectedUser && (
        <ResetPasswordModal
          user={selectedUser}
          onClose={() => setShowResetModal(false)}
          onReset={handleResetPassword}
        />
      )}
      {showDeleteModal && selectedUser && (
        <DeleteUserModal
          user={selectedUser}
          onClose={() => setShowDeleteModal(false)}
          onDelete={handleDeleteUser}
        />
      )}
    </div>
  );
};

export default AccountManager;