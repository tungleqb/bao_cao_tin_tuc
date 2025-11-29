import React, { useEffect, useState } from "react";
import axios from "../services/api";
import { useContext } from "react";
import { DashboardContext } from "./AdminDashboard";


const PAGE_SIZE = 10;

const PeriodManager = () => {
  const [periods, setPeriods] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const { setActiveTab, setSelectedPeriodId } = useContext(DashboardContext);

  const fetchReportCount = async (periodId) => {
    try {
      const res = await axios.get(`/admin/report/${periodId}`);
      return res.data.length;
    } catch (err) {
      console.error(`Lỗi khi lấy báo cáo cho period ${periodId}:`, err);
      return 0;
    }
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("/admin/period");

      const periodsWithCounts = await Promise.all(
        response.data.map(async (p) => {
          const count = await fetchReportCount(p.ID);
          return { ...p, reportCount: count };
        })
      );

      // Sắp xếp theo mốc thời gian kích hoạt gần nhất (max của min(ActiveAt, XaActiveAt))
      periodsWithCounts.sort((a, b) => {
        const minA = new Date(Math.min(new Date(a.ActiveAt), new Date(a.XaActiveAt || a.ActiveAt)));
        const minB = new Date(Math.min(new Date(b.ActiveAt), new Date(b.XaActiveAt || b.ActiveAt)));
        return minB - minA; // giảm dần: mới nhất ở trên
      });

      setPeriods(periodsWithCounts);
      setFiltered(periodsWithCounts);
    } catch (err) {
      console.error("Lỗi khi lấy dữ liệu kỳ báo cáo:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSearch = (e) => {
    const value = e.target.value.toLowerCase();
    setSearchTerm(value);
    const result = periods.filter(
      (p) =>
        p.ID.toLowerCase().includes(value) ||
        p.Name.toLowerCase().includes(value) ||
        p.TYPE.toLowerCase().includes(value)
    );
    setFiltered(result);
    setCurrentPage(1); // reset page
  };

  const handleDeactivate = async (period) => {
    const confirmed = window.confirm(`Bạn có chắc muốn huỷ kích hoạt kỳ báo cáo "${period.Name}"?`);
    if (!confirmed) return;

    try {
      const res = await axios.put(`/admin/period/${period.ID}`, {
        Name: period.Name,
        Status: "INACTIVE",
        XaStatus: "INACTIVE",
        Killer: "Admin",
      });
      alert("✅ Đã huỷ kích hoạt kỳ báo cáo.");
      fetchData(); // reload lại danh sách
    } catch (err) {
      alert("❌ Lỗi khi huỷ kích hoạt: " + (err.response?.data?.detail || err.message));
    }
  };
  const handleReactivate = async (period) => {
    const confirmed = window.confirm(`Bạn có chắc muốn kích hoạt lại kỳ báo cáo "${period.Name}"?`);
    if (!confirmed) return;

    try {
      const res = await axios.put(`/admin/period/${period.ID}`, {
        Name: period.Name,
        Status: "Active",
        XaStatus: "Active",
        Killer: "Admin",
      });
      alert("✅ Đã kích hoạt lại kỳ báo cáo.");
      fetchData(); // reload lại danh sách
    } catch (err) {
      alert("❌ Lỗi khi kích hoạt lại: " + (err.response?.data?.detail || err.message));
    }
  };
  const formatDateTime = (dateStr) =>
    new Date(dateStr).toLocaleString("vi-VN", { hour12: false });
  const pageCount = Math.ceil(filtered.length / PAGE_SIZE);
  const currentData = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Danh sách kỳ báo cáo</h2>
      <div className="mb-3">
        <input
          type="text"
          placeholder="Tìm kiếm theo ID, Tên hoặc Loại"
          className="border p-2 w-full"
          value={searchTerm}
          onChange={handleSearch}
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100 text-xs">
            <tr>
              <th className="border px-2 py-1 w-20">ID</th>
              <th className="border px-2 py-1 w-40">Tên</th>
              <th className="border px-2 py-1 w-24">Loại</th>
              <th className="border px-2 py-1 w-48">Active → Deactive</th>
              <th className="border px-2 py-1 w-40">Start → End</th>
              <th className="border px-2 py-1 w-40">From → To</th>
              <th className="border px-2 py-1 w-48">XaActive → XaDeactive</th>
              <th className="border px-2 py-1 w-40">XaStart → XaEnd</th>
              <th className="border px-2 py-1 w-40">XaFrom → XaTo</th>
              <th className="border px-2 py-1 w-24">Trạng thái</th>
              <th className="border px-2 py-1 w-16">#BC</th>
              <th className="border px-2 py-1 w-28">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            {currentData.map((p) => (
              <tr
                key={p.ID}
                className="hover:bg-gray-50 text-xs cursor-pointer"
                onDoubleClick={() => {
                  setSelectedPeriodId(p.ID);
                  setActiveTab("summary");
                }}
              >
                <td className="border px-2 py-1">{p.ID}</td>
                <td className="border px-2 py-1">{p.Name}</td>
                <td className="border px-2 py-1">{p.TYPE}</td>
                <td className="border px-2 py-1">{formatDateTime(p.ActiveAt)} → {formatDateTime(p.DeactiveAt)}</td>
                <td className="border px-2 py-1">{formatDateTime(p.StartAt)} → {formatDateTime(p.EndAt)}</td>
                <td className="border px-2 py-1">{formatDateTime(p.FromAt)} → {formatDateTime(p.ToAt)}</td>
                <td className="border px-2 py-1">{formatDateTime(p.XaActiveAt)} → {formatDateTime(p.XaDeactiveAt)}</td>
                <td className="border px-2 py-1">{formatDateTime(p.XaStartAt)} → {formatDateTime(p.XaEndAt)}</td>
                <td className="border px-2 py-1">{formatDateTime(p.XaFromAt)} → {formatDateTime(p.XaToAt)}</td>
                <td className="border px-2 py-1 text-center">{p.Status} / {p.XaStatus}</td>
                <td className="border px-2 py-1 text-center">{p.reportCount}</td>
                <td className="border px-2 py-1 text-center space-x-1">
                  {p.Status === "Active" || p.XaStatus === "Active" ? (
                    <button
                      className="text-red-600 hover:underline text-xs"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeactivate(p);
                      }}
                    >
                      Huỷ kích hoạt
                    </button>
                  ) : (
                    <button
                      className="text-green-600 hover:underline text-xs"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleReactivate(p);
                      }}
                    >
                      Kích hoạt lại
                    </button>
                  )}
                </td>

              </tr>
            ))}
          </tbody>


        </table>
        <div className="mt-2 flex justify-center items-center">
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
              max={pageCount}
              value={currentPage}
              onChange={(e) =>
                setCurrentPage(
                  Math.min(pageCount, Math.max(1, Number(e.target.value)))
                )
              }
              className="border px-2 py-1 w-16 rounded"
            />
            <button
              className="px-3 py-1 border rounded hover:bg-gray-200"
              disabled={currentPage === pageCount}
              onClick={() => setCurrentPage((p) => Math.min(p + 1, pageCount))}
            >
              Sau →
            </button>
            <span className="text-sm text-gray-500 ml-2">Tổng: {pageCount} trang</span>
          </div>
        </div>
        {filtered.length === 0 && (
          <p className="text-center mt-4 text-gray-500">Không tìm thấy kỳ báo cáo nào.</p>
        )}
      </div>
    </div>
  );
};

export default PeriodManager;
