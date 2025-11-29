import React, { useEffect, useState } from "react";
import axios from "../services/api";

const AuditLog = () => {
    const [logs, setLogs] = useState([]);
    const [error, setError] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const rowsPerPage = 20;

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await axios.get("/admin/auditlogs");
                const sorted = response.data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                setLogs(sorted);
            } catch (err) {
                setError("Không thể tải nhật ký.");
            }
        };
        fetchLogs();
    }, []);

    const totalPages = Math.ceil(logs.length / rowsPerPage);
    const paginatedLogs = logs.slice(
        (currentPage - 1) * rowsPerPage,
        currentPage * rowsPerPage
    );

    return (
        <div className="p-4 h-full overflow-hidden flex flex-col">
            <h2 className="text-2xl font-bold mb-4 text-center">NHẬT KÝ TÁC ĐỘNG</h2>
            {error && <div className="text-red-500">{error}</div>}
            <div className="flex-1 overflow-auto border rounded bg-white">
                <table className="table-auto w-full text-sm text-left border-collapse">
                    <thead className="bg-gray-100 text-sm font-semibold">
                        <tr>
                            <th className="px-2 py-1">#</th>
                            <th className="px-2 py-1">Thời gian</th>
                            <th className="px-2 py-1">User</th>
                            <th className="px-2 py-1">Hành động</th>
                            <th className="px-2 py-1">Đối tượng</th>
                            <th className="px-2 py-1">Chi tiết</th>
                        </tr>
                    </thead>
                    <tbody>
                        {paginatedLogs.map((log, index) => (
                            <tr key={log.id} className="border-t hover:bg-gray-50">
                                <td className="px-2 py-1 text-center">
                                    {(currentPage - 1) * rowsPerPage + index + 1}
                                </td>
                                <td className="px-2 py-1">
                                    {new Date(log.timestamp).toLocaleString("vi-VN")}
                                </td>
                                <td className="px-2 py-1 text-center">{log.user_id}</td>
                                <td className="px-2 py-1 text-center">{log.action}</td>
                                <td className="px-2 py-1 text-center">
                                    {log.model} #{log.model_id}
                                </td>
                                <td className="px-2 py-1">{log.details}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-2 flex justify-center items-center gap-4">
                <button
                    className="px-3 py-1 border rounded hover:bg-gray-200"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
                >
                    ← Trước
                </button>
                <span>
                    Trang {currentPage} / {totalPages}
                </span>
                <button
                    className="px-3 py-1 border rounded hover:bg-gray-200"
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
                >
                    Sau →
                </button>
            </div>
        </div>
    );
};

export default AuditLog;
