import React, { useEffect, useState } from "react";
import axios from "../services/api";

function AdminYeuCauBaoCao() {
  const [requests, setRequests] = useState([]);
  const [users, setUsers] = useState([]);
  const [loaiBaoCao, setLoaiBaoCao] = useState([]);
  const [form, setForm] = useState({
    loai_baocao_id: "",
    user_ids: [],
    dinh_ky_value: 0,
    dinh_ky_unit: "day",
    is_active: true
  });
  const [editId, setEditId] = useState(null);
  const token = localStorage.getItem("token");

  const loadAll = async () => {
    const [r1, r2, r3] = await Promise.all([
      axios.get("/report/request", { headers: { Authorization: `Bearer ${token}` } }),
      axios.get("/admin/user", { headers: { Authorization: `Bearer ${token}` } }),
      axios.get("/admin/loaibaocao", { headers: { Authorization: `Bearer ${token}` } }),
    ]);
    setRequests(r1.data);
    setUsers(r2.data);
    setLoaiBaoCao(r3.data.filter(l => new Date(l.han_gui) > new Date())); // lọc còn hiệu lực
  };

  useEffect(() => { loadAll(); }, []);

  const handleCheckbox = (id) => {
    const ids = form.user_ids.includes(id) ? form.user_ids.filter(x => x !== id) : [...form.user_ids, id];
    setForm({ ...form, user_ids: ids });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editId) {
      await axios.put(`/report/request/${editId}`, form, { headers: { Authorization: `Bearer ${token}` } });
    } else {
      await axios.post("/report/request", form, { headers: { Authorization: `Bearer ${token}` } });
    }
    setForm({ loai_baocao_id: "", user_ids: [], dinh_ky_value: 0, dinh_ky_unit: "day", is_active: true });
    setEditId(null);
    loadAll();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Bạn có chắc muốn xoá?")) {
      await axios.delete(`/report/request/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      loadAll();
    }
  };

  const toggleActive = async (id, current) => {
    await axios.put(`/report/request/${id}/active`, { is_active: !current }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    loadAll();
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Quản lý yêu cầu báo cáo</h2>
      <form onSubmit={handleSubmit} className="space-y-2 mb-4">
        <select
          value={form.loai_baocao_id}
          onChange={e => setForm({ ...form, loai_baocao_id: parseInt(e.target.value) })}
          className="border px-2 py-1"
          required
        >
          <option value="">-- Chọn loại báo cáo --</option>
          {loaiBaoCao.map(l => <option key={l.id} value={l.id}>{l.ten_loai}</option>)}
        </select>
        <div>
          {users.map(u => (
            <label key={u.id} className="inline-block mr-4">
              <input
                type="checkbox"
                checked={form.user_ids.includes(u.id)}
                onChange={() => handleCheckbox(u.id)}
              />
              <span className="ml-1">{u.ten_chi_nhanh}</span>
            </label>
          ))}
        </div>
        <div className="flex space-x-2">
          <input
            type="number"
            value={form.dinh_ky_value}
            onChange={e => setForm({ ...form, dinh_ky_value: parseInt(e.target.value) })}
            className="border px-2 py-1 w-1/3"
            placeholder="Định kỳ"
          />
          <select
            value={form.dinh_ky_unit}
            onChange={e => setForm({ ...form, dinh_ky_unit: e.target.value })}
            className="border px-2 py-1 w-1/3"
          >
            <option value="hour">Giờ</option>
            <option value="day">Ngày</option>
            <option value="month">Tháng</option>
          </select>
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">
          {editId ? "Cập nhật" : "Tạo yêu cầu"}
        </button>
      </form>

      <table className="table-auto border w-full text-sm">
        <thead>
          <tr className="bg-gray-200 text-center">
            <th>ID</th><th>Loại</th><th>Chi nhánh</th><th>Định kỳ</th><th>Kích hoạt</th><th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {requests.map(r => (
            <tr key={r.id} className="text-center border-t">
              <td>{r.id}</td>
              <td>{loaiBaoCao.find(l => l.id === r.loai_baocao_id)?.ten_loai || r.loai_baocao_id}</td>
              <td>{r.user_ids.map(id => users.find(u => u.id === id)?.ten_chi_nhanh || id).join(", ")}</td>
              <td>{r.dinh_ky_value} {r.dinh_ky_unit}</td>
              <td>{r.is_active ? "✔️" : "❌"}</td>
              <td>
                <button onClick={() => {
                  setForm({
                    loai_baocao_id: r.loai_baocao_id,
                    user_ids: r.user_ids,
                    dinh_ky_value: r.dinh_ky_value,
                    dinh_ky_unit: r.dinh_ky_unit,
                    is_active: r.is_active
                  });
                  setEditId(r.id);
                }} className="text-blue-600 mr-2">Sửa</button>
                <button onClick={() => handleDelete(r.id)} className="text-red-600 mr-2">Xoá</button>
                <button onClick={() => toggleActive(r.id, r.is_active)} className="text-yellow-600">
                  {r.is_active ? "Huỷ kích hoạt" : "Kích hoạt lại"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminYeuCauBaoCao;
