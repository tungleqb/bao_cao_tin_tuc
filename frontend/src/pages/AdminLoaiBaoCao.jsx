import React, { useEffect, useState } from "react";
import axios from "../services/api";

function AdminLoaiBaoCao() {
  const [list, setList] = useState([]);
  const [form, setForm] = useState({ ten_loai: "", thoi_gian_bat_dau: "", han_gui: "", dinh_ky: 0 });
  const [editId, setEditId] = useState(null);
  const token = localStorage.getItem("token");

  const load = async () => {
    const res = await axios.get("/admin/loaibaocao", { headers: { Authorization: `Bearer ${token}` } });
    setList(res.data);
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ...form };
    if (editId) {
      await axios.put(`/admin/loaibaocao/${editId}`, payload, { headers: { Authorization: `Bearer ${token}` } });
    } else {
      await axios.post("/admin/loaibaocao", payload, { headers: { Authorization: `Bearer ${token}` } });
    }
    setForm({ ten_loai: "", thoi_gian_bat_dau: "", han_gui: "", dinh_ky: 0 });
    setEditId(null);
    load();
  };

  const handleDelete = async (id) => {
    if (window.confirm("Xoá?")) {
      await axios.delete(`/admin/loaibaocao/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      load();
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Quản lý loại báo cáo</h2>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input value={form.ten_loai} onChange={e => setForm({ ...form, ten_loai: e.target.value })} placeholder="Tên loại" className="border px-2 py-1" required />
        <input type="datetime-local" value={form.thoi_gian_bat_dau} onChange={e => setForm({ ...form, thoi_gian_bat_dau: e.target.value })} className="border px-2 py-1" required />
        <input type="datetime-local" value={form.han_gui} onChange={e => setForm({ ...form, han_gui: e.target.value })} className="border px-2 py-1" required />
        <input type="number" value={form.dinh_ky} onChange={e => setForm({ ...form, dinh_ky: parseInt(e.target.value) })} placeholder="Định kỳ" className="border px-2 py-1" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">{editId ? "Cập nhật" : "Tạo mới"}</button>
      </form>
      <table className="w-full mt-4 border">
        <thead><tr><th>Tên</th><th>Bắt đầu</th><th>Hạn</th><th>Định kỳ</th><th>Hành động</th></tr></thead>
        <tbody>
          {list.map(item => (
            <tr key={item.id} className="text-center border-t">
              <td>{item.ten_loai}</td>
              <td>{new Date(item.thoi_gian_bat_dau).toLocaleString()}</td>
              <td>{new Date(item.han_gui).toLocaleString()}</td>
              <td>{item.dinh_ky}</td>
              <td>
                <button onClick={() => { setEditId(item.id); setForm(item); }} className="text-blue-600 mr-2">Sửa</button>
                <button onClick={() => handleDelete(item.id)} className="text-red-600">Xoá</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminLoaiBaoCao;
