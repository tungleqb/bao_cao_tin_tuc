import React, { useEffect, useState } from "react";
import axios from "../services/api";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

const ReportHistory = () => {
  const [reports, setReports] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;
  
  const [filters, setFilters] = useState({
  Sender: "",
  ReportPeriodName: "",
  Blake3sum: "",
  OriFileName: "",
  SentAt: "",
  Comment: "",
});
  const filteredReports = reports.filter((r) =>
    Object.entries(filters).every(([key, value]) =>
      r[key]?.toString().toLowerCase().includes(value.toLowerCase())
    )
  );
  const totalPages = Math.ceil(filteredReports.length / rowsPerPage);
  const paginatedReports = filteredReports.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      axios
        .get("/report/reports", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => setReports(res.data))
        .catch((err) => console.error("Lỗi tải lịch sử báo cáo:", err));
    }
  }, []);
  const handleExportExcel = () => {
  const data = reports.map((r) => ({
    "Tên đơn vị": r.Sender,
    "Tên kỳ báo cáo": r.ReportPeriodName,
    "Blake3sum": r.Blake3sum,
    "Tên file": r.OriFileName,
    "Thời gian gửi": new Date(r.SentAt).toLocaleString("vi-VN"),
    "Ghi chú": r.Comment || "",
    "Có sự kiện": r.HasEvent ? "✓" : "",
    "Thời hạn": r.LateSeconds === 0
      ? "Đúng hạn"
      : r.LateSeconds < 0
        ? `Trước hạn ${Math.abs(r.LateSeconds)} giây`
        : `Quá hạn ${r.LateSeconds} giây`
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Lịch sử báo cáo");

  const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
  saveAs(blob, `lich_su_bao_cao_${new Date().toISOString().slice(0, 10)}.xlsx`);
};

  return (
  <div className="p-4 h-full overflow-hidden flex flex-col">
    <h2 className="text-2xl font-bold mb-4 text-center">LỊCH SỬ BÁO CÁO</h2>
    
    <div className="flex-1 overflow-auto border rounded bg-white">
      <table className="table-auto w-full text-sm text-left border-collapse">
        <thead>
          <tr className="bg-gray-100 text-sm font-semibold">
            <th className="px-2 py-1">Tên đơn vị</th>
            <th className="px-2 py-1">Tên kỳ báo cáo</th>
            <th className="px-2 py-1">Blake3sum</th>
            <th className="px-2 py-1">Tên file</th>
            <th className="px-2 py-1">Thời gian gửi</th>
            <th className="px-2 py-1">Ghi chú</th>
            <th className="px-2 py-1">Sự kiện</th>
            <th className="px-2 py-1">Thời hạn</th>
          </tr>
          <tr className="bg-white text-xs">
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.Sender}
                onChange={(e) => setFilters({ ...filters, Sender: e.target.value })}
              />
            </th>
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.ReportPeriodName}
                onChange={(e) => setFilters({ ...filters, ReportPeriodName: e.target.value })}
              />
            </th>
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.Blake3sum}
                onChange={(e) => setFilters({ ...filters, Blake3sum: e.target.value })}
              />
            </th>
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.OriFileName}
                onChange={(e) => setFilters({ ...filters, OriFileName: e.target.value })}
              />
            </th>
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.SentAt}
                onChange={(e) => setFilters({ ...filters, SentAt: e.target.value })}
              />
            </th>
            <th>
              <input
                className="w-full border px-1 py-0.5 rounded"
                value={filters.Comment}
                onChange={(e) => setFilters({ ...filters, Comment: e.target.value })}
              />
            </th>
            <th></th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {paginatedReports.map((r) => (
            <tr key={r.ID} className="border-t">
              <td className="px-2 py-1 truncate">{r.Sender}</td>
              <td className="px-2 py-1 break-words">{r.ReportPeriodName}</td>
              <td className="px-2 py-1 break-all max-w-[150px]">
                {r.Blake3sum}
              </td>
              <td className="px-2 py-1 break-words">{r.OriFileName}</td>
              <td className="px-2 py-1">{new Date(r.SentAt).toLocaleString("vi-VN")}</td>
              <td className="px-2 py-1 break-words">{r.Comment || ""}</td>
              <td className="px-2 py-1 text-center">{r.HasEvent ? "✓" : ""}</td>
              <td className="px-2 py-1">
                {typeof r.LateSeconds === "number"
                  ? r.LateSeconds === 0
                    ? "Đúng hạn"
                    : r.LateSeconds < 0
                      ? `Trước hạn ${Math.abs(r.LateSeconds)} giây`
                      : `Quá hạn ${r.LateSeconds} giây`
                  : ""}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    <div className="mt-1 flex flex-wrap justify-center gap-5 mb-1">
      <div className="flex flex-wrap items-center gap-3">
        <button
          className="px-3 py-1 border rounded hover:bg-gray-200"
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
        >
          ← Trước
        </button>
        <div className="flex items-center gap-2">
          Trang:
          <input
            type="number"
            value={currentPage}
            min={1}
            max={totalPages}
            onChange={(e) =>
              setCurrentPage(Math.min(totalPages, Math.max(1, Number(e.target.value))))
            }
            className="border px-2 py-1 w-16 rounded"
          />
          <button
            className="px-3 py-1 border rounded hover:bg-gray-200"
            onClick={() => setCurrentPage(currentPage)}
          >
            Go
          </button>
        </div>
        <button
          className="px-3 py-1 border rounded hover:bg-gray-200"
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
        >
          Sau →
        </button>

        <span className="text-sm text-gray-500 ml-4">
          Tổng số trang: {totalPages}
        </span>
      </div>
      <button 
      onClick={handleExportExcel}
      className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700 mt-1 right-0">
        Xuất Excel
      </button>
    </div>
  </div>
);

};

export default ReportHistory;
