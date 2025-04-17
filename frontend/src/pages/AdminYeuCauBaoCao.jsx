import React, { useEffect, useState } from "react";
import axios from "../services/api";

function AdminYeuCauBaoCao() {
  const [requests, setRequests] = useState([]);
  const [users, setUsers] = useState([]);
  const [loaiBaoCao, setLoaiBaoCao] = useState([]);
  const [form, setForm] = useState({ loai_baocao_id: "", user_ids: [], dinh_ky: 0 });
  const [filter, setFilter] = useState({ loai_baocao_id: "", user_id: "" });
  const token = localStorage.getItem("token");

  const loadAll = async () => {
    const [r1, r2, r3] = await Promise.all([
      axios.get("/report/request", { headers: { Authorization: `Bearer ${token}` } }),
      axios.get("/admin/user", { headers: { Authorization: `Bearer ${token}` } }),
      axios.get("/admin/loaibaocao", { headers: { Authorization: `Bearer ${token}` } }),
    ]);
    setRequests(r1.data);
    setUsers(r2.data);
    setLoaiBaoCao(r3.data);
  };

  useEffect(() => { loadAll(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post("/report/request", form, { headers: { Authorization: `Bearer ${token}` } });
    setForm({ loai_baocao_id: "", user_ids: [], dinh_ky: 0 });
    loadAll();
  };

  const handleCheckbox = (id) => {
    const ids = form.user_ids.includes(id) ? form.user_ids.filter(x => x !== id) : [...form.user_ids, id];
    setForm({ ...form, user_ids: ids });
  };

  const filtered = requests.filter(r => {
    return (
      (!filter.loai_baocao_id || r.loai_baocao_id === parseInt(filter.loai_baocao_id)) &&
      (!filter.user_id || r.user_ids.includes(parseInt(filter.user_id)))
    );
  });

  const exportCSV = () => {
    const headers = ["ID", "Loại báo cáo", "Chi nhánh", "Định kỳ"];
    const rows = filtered.map(r => [
      r.id,
      r.loai_baocao_id,
      r.user_ids.join("; "),
      r.dinh_ky
    ]);
    const csvContent = [headers, ...rows].map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "yeu_cau_baocao.csv";
    link.click();
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Tạo yêu cầu báo cáo</h2>
      <form onSubmit={handleSubmit} className="space-y-2">
        <select value={form.loai_baocao_id} onChange={e => setForm({ ...form, loai_baocao_id: parseInt(e.target.value) })} className="border px-2 py-1">
          <option value="">-- Chọn loại báo cáo --</option>
          {loaiBaoCao.map(l => <option key={l.id} value={l.id}>{l.ten_loai}</option>)}
        </select>
        <div>
          {users.map(u => (
            <label key={u.id} className="inline-block mr-4">
              <input type="checkbox" checked={form.user_ids.includes(u.id)} onChange={() => handleCheckbox(u.id)} />
              <span className="ml-1">{u.ten_chi_nhanh}</span>
            </label>
          ))}
        </div>
        <input type="number" value={form.dinh_ky} onChange={e => setForm({ ...form, dinh_ky: parseInt(e.target.value) })} placeholder="Định kỳ" className="border px-2 py-1" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-1 rounded">Gửi yêu cầu</button>
      </form>

      <h3 className="text-lg font-bold mt-6 mb-2">Bộ lọc</h3>
      <div className="space-x-2 mb-2">
        <select value={filter.loai_baocao_id} onChange={e => setFilter({ ...filter, loai_baocao_id: e.target.value })} className="border px-2 py-1">
          <option value="">-- Loại báo cáo --</option>
          {loaiBaoCao.map(l => <option key={l.id} value={l.id}>{l.ten_loai}</option>)}
        </select>
        <select value={filter.user_id} onChange={e => setFilter({ ...filter, user_id: e.target.value })} className="border px-2 py-1">
          <option value="">-- Chi nhánh --</option>
          {users.map(u => <option key={u.id} value={u.id}>{u.ten_chi_nhanh}</option>)}
        </select>
        <button onClick={exportCSV} className="bg-green-600 text-white px-3 py-1 rounded">Export CSV</button>
      </div>

      <h3 className="text-lg font-bold mb-2">Danh sách yêu cầu</h3>
      <table className="table-auto border w-full text-sm">
        <thead><tr className="bg-gray-200"><th>ID</th><th>Loại báo cáo</th><th>Chi nhánh</th><th>Định kỳ</th></tr></thead>
        <tbody>
          {filtered.map(r => (
            <tr key={r.id} className="border-t text-center">
              <td>{r.id}</td>
              <td>{r.loai_baocao_id}</td>
              <td>{r.user_ids.join(", ")}</td>
              <td>{r.dinh_ky}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminYeuCauBaoCao;
