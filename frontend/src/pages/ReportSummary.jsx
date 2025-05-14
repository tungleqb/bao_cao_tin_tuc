import React, { useState, useEffect } from "react";
import axios from "../services/api";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";
import { useContext } from "react";
import { DashboardContext } from "./AdminDashboard";


const ReportSummary = () => {
  const [reportTypes, setReportTypes] = useState([]);
  const [selectedType, setSelectedType] = useState("");
  const [periods, setPeriods] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [reports, setReports] = useState([]);
  const [totalReports, setTotalReports] = useState(0);
  const { selectedPeriodId } = useContext(DashboardContext);

  const token = localStorage.getItem("admin_token");

  const [currentPage, setCurrentPage] = useState(1);
    const [filters, setFilters] = useState({
    Sender: "",
    OriFileName: "",
    Comment: "",
    Blake3sum: "",
    });
    const rowsPerPage = 10;

    const filteredReports = reports.filter((r) =>
    Object.entries(filters).every(([key, value]) =>
        r[key]?.toString().toLowerCase().includes(value.toLowerCase())
    )
    );

const paginatedReports = filteredReports.slice(
  (currentPage - 1) * rowsPerPage,
  currentPage * rowsPerPage
);
const totalPages = Math.ceil(filteredReports.length / rowsPerPage);

  const handleExportExcel = () => {
  const data = reports.map((r) => ({
    "Tài khoản": r.Sender,
    "Gửi lúc": new Date(r.SentAt).toLocaleString("vi-VN"),
    "Trễ (giây)": r.LateSeconds,
    "Tên file": r.FileName,
    "Có sự kiện": r.HasEvent ? "✓" : "",
    "Ghi chú": r.Comment || "",
    "Blake3sum": r.Blake3sum,
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Thống kê báo cáo");

  const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
  saveAs(blob, `thong_ke_bao_cao_${new Date().toISOString().slice(0, 10)}.xlsx`);
};

  useEffect(() => {
    axios.get("/admin/loaibaocao", {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then(res => {
    console.log("Loaibaocao response:", res.data);
      if (Array.isArray(res.data)) {
      setReportTypes(res.data);
      if (res.data.length > 0) setSelectedType(res.data[0].ID);
    } else {
      console.warn("Dữ liệu loaibaocao không phải mảng:", res.data);
    }
    });
  }, []);

  useEffect(() => {
  if (!selectedType) return;
  axios.get("/period", {
    headers: { Authorization: `Bearer ${token}` },
  }).then(res => {
    const filtered = res.data
      .filter(p => p.TYPE === selectedType)
      .sort((a, b) => new Date(b.ActiveAt) - new Date(a.ActiveAt))
      .slice(0, 10);
    setPeriods(filtered);
    if (selectedPeriodId) {
  const matchedPeriod = res.data.find(p => p.ID === selectedPeriodId);
  if (matchedPeriod) {
    setSelectedType(matchedPeriod.TYPE); // 🟢 cập nhật loại báo cáo
    setSelectedPeriod(matchedPeriod);
    setPeriods(res.data.filter(p => p.TYPE === matchedPeriod.TYPE));
    return;
  }
}
if (filtered.length > 0) {
  setSelectedPeriod(filtered[0]);
}
  });
}, [selectedType, selectedPeriodId]);

  useEffect(() => {
    if (!selectedPeriod) return;
    axios.get(`/report/admin/${selectedPeriod.ID}`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(res => {
      setReports(res.data);
      setTotalReports(res.data.length);
    });
  }, [selectedPeriod]);

const handleDownloadZip = async () => {
  if (!selectedPeriod) return;
  try {
    const response = await axios.get(`/report/download/${selectedPeriod.ID}`, {
      responseType: "blob",
      headers: { Authorization: `Bearer ${token}` },
    });
    const blob = new Blob([response.data], { type: "application/zip" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${selectedPeriod.ID}.zip`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    alert("Không thể tải file. Bạn có quyền admin không?");
    console.error(error);
  }
};

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-xl font-bold">Tổng hợp kỳ báo cáo</h1>

      {/* Phần I */}
      <div className="bg-white rounded-lg shadow p-4 space-y-4">
        <h2 className="text-lg font-semibold">I. Thông tin kỳ báo cáo</h2>
        <div className="flex space-x-4">
          <div>
            <label className="block font-medium">Loại báo cáo</label>
            <select className="border rounded p-1" value={selectedType} onChange={e => setSelectedType(e.target.value)}>
              {Array.isArray(reportTypes) && reportTypes.map(rt => (
                <option key={rt.ID} value={rt.ID}>{rt.Name}</option>
                ))}
            </select>
          </div>
          <div>
            <label className="block font-medium">Kỳ báo cáo</label>
            <select className="border rounded p-1" value={selectedPeriod?.ID || ""} onChange={e => {
              const period = periods.find(p => p.ID === e.target.value);
              setSelectedPeriod(period);
            }}>
              {periods.map(p => (
                <option key={p.ID} value={p.ID}>{p.Name}</option>
              ))}
            </select>
          </div>
          {selectedPeriod && (<div key={"ID"}><b>{"ID"}:</b> {selectedPeriod?.ID ?? "-"}</div>)}
        </div>
        {selectedPeriod && (
          <div className="grid text-sm">
          <div className="grid grid-cols-2 md:grid-cols-2 gap-2 text-sm">
            <div><b>Cấp phòng:</b>
            <div key={"ActiveAt"}><b>{"Kích hoạt từ"}:</b> {new Date(selectedPeriod["ActiveAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"DeactiveAt"}><b>{"Huỷ kích hoạt"}:</b> {new Date(selectedPeriod["DeactiveAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"StartAt"}><b>{"Hạn nhận từ"}:</b> {new Date(selectedPeriod["StartAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"EndAt"}><b>{"Hết hạn"}:</b> {new Date(selectedPeriod["EndAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"Status"}><b>{"Trạng thái"}:</b> {selectedPeriod["Status"] ?? "-"}</div>
            </div>
            <div><b>Cấp xã:</b>
            <div key={"XaActiveAt"}><b>{"Kích hoạt từ"}:</b> {new Date(selectedPeriod["XaActiveAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"XaDeactiveAt"}><b>{"Huỷ kích hoạt"}:</b> {new Date(selectedPeriod["XaDeactiveAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"XaStartAt"}><b>{"Hạn nhận từ"}:</b> {new Date(selectedPeriod["XaStartAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"XaEndAt"}><b>{"Hết hạn"}:</b> {new Date(selectedPeriod["XaEndAt"]).toLocaleString("vi-VN") ?? "-"}</div>
            <div key={"XaStatus"}><b>{"Trạng thái"}:</b> {selectedPeriod["XaStatus"] ?? "-"}</div>
            </div>
          </div>
            <div><b>Tổng số báo cáo đã gửi:</b> {totalReports}</div>
            <div><b>Tổng số báo cáo đã gửi có sự kiện:</b> {reports.filter(r => r.HasEvent).length}</div>
            <div><b>Tổng số báo cáo đã gửi không có sự kiện:</b> {reports.filter(r => !r.HasEvent).length}</div>
            <div><b>Tổng số báo cáo đã gửi đúng hạn:</b> {reports.filter(r => r.LateSeconds === 0).length}</div>
            <div><b>Tổng số báo cáo đã gửi không đúng hạn:</b> {reports.filter(r => r.LateSeconds < 0).length}</div>
            <div className="flex items-center space-x-2">
            <div key={"FolderPath"}><b>FolderPath:</b> {selectedPeriod["FolderPath"] ?? "-"}</div>
            <button
              className="bg-green-500 hover:bg-green-600 text-white text-sm px-3 py-1 rounded border"
              onClick={handleDownloadZip}
            >
              Tải tất cả báo cáo (.zip)
            </button>
            </div>
          </div>
        )}
      </div>

      {/* Phần II */}
      <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
        <h2 className="text-lg font-semibold mb-2">II. Bảng thống kê báo cáo</h2>
        <table className="min-w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Tài khoản</th>
              <th className="border px-2 py-1">Gửi lúc</th>
              <th className="border px-2 py-1">Trễ (giây)</th>
              <th className="border px-2 py-1">Tên file</th>
              <th className="border px-2 py-1">Có sự kiện</th>
              <th className="border px-2 py-1">Ghi chú</th>
              <th className="border px-2 py-1 max-w-[200px]">Blake3sum</th>
            </tr>
            <tr className="bg-white text-xs">
            <th>
                <input
                className="w-full border px-1 py-0.5 rounded"
                placeholder="Tài khoản"
                value={filters.Sender}
                onChange={(e) => setFilters({ ...filters, Sender: e.target.value })}
                />
            </th>
            <th></th>
            <th></th>
            <th>
                <input
                className="w-full border px-1 py-0.5 rounded"
                placeholder="Tên file"
                value={filters.OriFileName}
                onChange={(e) => setFilters({ ...filters, OriFileName: e.target.value })}
                />
            </th>
            <th></th>
            <th>
                <input
                className="w-full border px-1 py-0.5 rounded"
                placeholder="Ghi chú"
                value={filters.Comment}
                onChange={(e) => setFilters({ ...filters, Comment: e.target.value })}
                />
            </th>
            <th>
                <input
                className="w-full border px-1 py-0.5 rounded"
                placeholder="Blake3sum"
                value={filters.Blake3sum}
                onChange={(e) => setFilters({ ...filters, Blake3sum: e.target.value })}
                />
            </th>
            </tr>

          </thead>
          
          <tbody>
            {paginatedReports.map((r, i) => (
              <tr key={i} className="text-center">
                <td className="border px-2">{r.Sender}</td>
                <td className="border px-2">{new Date(r.SentAt).toLocaleString("vi-VN")}</td>
                <td className="border px-2">{r.LateSeconds ?? 0}</td>
                <td className="border px-2 max-w-[150px] truncate">{r.FileName}</td>
                <td className="border px-2">{r.HasEvent ? "✅" : "❌"}</td>
                <td className="border px-2">{r.Comment ?? ""}</td>
                <td className="border px-2 max-w-[200px] truncate">{r.Blake3sum}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-2 flex flex-wrap justify-between items-center">
        <div className="flex items-center gap-2">
            <button
            className="px-3 py-1 border rounded hover:bg-gray-200"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
            >
            ← Trước
            </button>
            <span>Trang:</span>
            <input
            type="number"
            min={1}
            max={totalPages}
            value={currentPage}
            onChange={(e) =>
                setCurrentPage(Math.min(totalPages, Math.max(1, Number(e.target.value))))
            }
            className="border px-2 py-1 w-16 rounded"
            />
            <button
            className="px-3 py-1 border rounded hover:bg-gray-200"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
            >
            Sau →
            </button>
            <span className="text-sm text-gray-500 ml-2">Tổng: {totalPages} trang</span>
        </div>
        <button
            onClick={handleExportExcel}
            className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
        >
            Xuất Excel
        </button>
        </div>

      </div>
    </div>
  );
};

export default ReportSummary;
