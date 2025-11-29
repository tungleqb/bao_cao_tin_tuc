import React, { useEffect, useState } from "react";
import axios from "../services/api";
import * as XLSX from "xlsx";

const ReportTypeManager = () => {
    const [form, setForm] = useState({
        Name: "",
        Period_ID: "DAILY",
        ActiveOffset: 0,
        ActiveOn: 0,
        ActiveAt: "00:00:00",
        DeactiveOffset: 0,
        DeactiveOn: 0,
        DeactiveAt: "23:59:59",
        StartOffset: 0,
        StartOn: 0,
        StartAt: "00:00:00",
        EndOffset: 0,
        EndOn: 0,
        EndAt: "23:59:59",
        FromOffset: 0,
        FromOn: 0,
        From: "00:00:00",
        ToOffset: 0,
        ToOn: 0,
        To: "23:59:59",
        XaActiveOffset: 0,
        XaActiveOn: 0,
        XaActiveAt: "00:00:00",
        XaDeactiveOffset: 0,
        XaDeactiveOn: 0,
        XaDeactiveAt: "23:59:59",
        XaStartOffset: 0,
        XaStartOn: 0,
        XaStartAt: "00:00:00",
        XaEndOffset: 0,
        XaEndOn: 0,
        XaEndAt: "23:59:59",
        XaFromOffset: 0,
        XaFromOn: 0,
        XaFromAt: "00:00:00",
        XaToOffset: 0,
        XaToOn: 0,
        XaToAt: "23:59:59",
        DocExtList: ".doc .docx .pdf .bm2 .jpg .xlsx .xls",
        MaxSize: "100MB"
    });
    const [reportTypes, setReportTypes] = useState([]);
    const [search, setSearch] = useState("");
    const [periodFilter, setPeriodFilter] = useState("");
    const fetchData = async () => {
        try {
            const response = await axios.get("/admin/reporttype");
            setReportTypes(response.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post("/admin/reporttype", form);
            fetchData();
        } catch (error) {
            console.error("Create failed:", error);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm("Bạn có chắc muốn xoá loại báo cáo này?")) {
            try {
                await axios.delete(`/admin/reporttype/${id}`);
                fetchData();
            } catch (error) {
                console.error("Delete failed:", error);
            }
        }
    };

    const handleUpdate = async (e) => {
        e.preventDefault();
        if (!form.ID) return;
        if (!window.confirm("Bạn có chắc muốn cập nhật loại báo cáo này?")) return;
        try {
            await axios.put(`/admin/reporttype/${form.ID}`, form);
            setForm({ ...form, ID: undefined });
            fetchData();
        } catch (error) {
            console.error("Update failed:", error);
        }
    };

    const renderOffsetFields = (prefix) => (
        <div className="grid grid-cols-3 gap-2">
            {["Active", "Deactive", "Start", "End", "From", "To"].map((field) => (
                <div key={field}>
                    <label>{prefix}{field}:</label>
                    <div className="flex gap-1">
                        <input name={`${prefix}${field}Offset`} className="w-1/3" value={form[`${prefix}${field}Offset`]} onChange={handleChange} />
                        <input name={`${prefix}${field}On`} className="w-1/3" value={form[`${prefix}${field}On`]} onChange={handleChange} />
                        <input name={`${prefix}${field}${prefix === "Xa" ? "At" : field === "From" || field === "To" ? "" : "At"}`} className="w-1/3" value={form[`${prefix}${field}${prefix === "Xa" ? "At" : field === "From" || field === "To" ? "" : "At"}`]} onChange={handleChange} />
                    </div>
                </div>
            ))}
        </div>
    );

    const renderFieldCell = (label, value) => (
        <div className="text-xs whitespace-nowrap"><strong>{label}:</strong> {value}</div>
    );

    const [currentPage, setCurrentPage] = useState(1);
    const rowsPerPage = 10;

    const filteredReports = reportTypes.filter(r =>
        r.Name.toLowerCase().includes(search.toLowerCase()) &&
        (periodFilter === "" || r.Period_ID === periodFilter)
    );
    const totalPages = Math.ceil(filteredReports.length / rowsPerPage);
    const paginatedReports = filteredReports.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage);
    const exportToExcel = () => {
        const data = filteredReports.map(({ ID, Name, Period_ID, DateCreated, NextAt }) => ({
            ID, Name, Period_ID,
            DateCreated: new Date(DateCreated).toLocaleString("vi-VN"),
            NextAt: NextAt ? new Date(NextAt).toLocaleString("vi-VN") : ""
        }));
        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "LoaiBaoCao");
        XLSX.writeFile(workbook, "DanhSachLoaiBaoCao.xlsx");
    };
    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Quản lý Loại báo cáo</h1>

            <form onSubmit={form.ID ? handleUpdate : handleSubmit} className="bg-white p-4 shadow rounded mb-6">
                <div className="mb-4">
                    <label className="block">Tên Loại báo cáo</label>
                    <input name="Name" value={form.Name} onChange={handleChange} className="w-full border rounded p-1" />
                </div>
                <div className="mb-4">
                    <label className="block">Định kỳ</label>
                    <select name="Period_ID" value={form.Period_ID} onChange={handleChange} className="w-full border rounded p-1">
                        {['DAILY', 'WEEKLY', 'MONTHLY', 'NONE'].map(p => <option key={p}>{p}</option>)}
                    </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <h2 className="font-semibold">Cấp phòng</h2>
                        {renderOffsetFields("")}
                    </div>
                    <div>
                        <h2 className="font-semibold">Cấp xã</h2>
                        {renderOffsetFields("Xa")}
                    </div>
                </div>
                <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label>Định dạng tệp hỗ trợ</label>
                        <input name="DocExtList" value={form.DocExtList} onChange={handleChange} className="w-full border rounded p-1" />
                    </div>
                    <div>
                        <label>Kích thước tối đa</label>
                        <input name="MaxSize" value={form.MaxSize} onChange={handleChange} className="w-full border rounded p-1" />
                    </div>
                </div>
                <div className="text-center mt-4 space-x-2">
                    <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
                        {form.ID ? "Cập nhật" : "Tạo mới"}
                    </button>
                    {form.ID && (
                        <button type="button" className="bg-gray-400 text-white px-4 py-2 rounded" onClick={() => setForm({
                            Name: "",
                            Period_ID: "DAILY",
                            ActiveOffset: 0,
                            ActiveOn: 0,
                            ActiveAt: "00:00:00",
                            DeactiveOffset: 0,
                            DeactiveOn: 0,
                            DeactiveAt: "23:59:59",
                            StartOffset: 0,
                            StartOn: 0,
                            StartAt: "00:00:00",
                            EndOffset: 0,
                            EndOn: 0,
                            EndAt: "23:59:59",
                            FromOffset: 0,
                            FromOn: 0,
                            From: "00:00:00",
                            ToOffset: 0,
                            ToOn: 0,
                            To: "23:59:59",
                            XaActiveOffset: 0,
                            XaActiveOn: 0,
                            XaActiveAt: "00:00:00",
                            XaDeactiveOffset: 0,
                            XaDeactiveOn: 0,
                            XaDeactiveAt: "23:59:59",
                            XaStartOffset: 0,
                            XaStartOn: 0,
                            XaStartAt: "00:00:00",
                            XaEndOffset: 0,
                            XaEndOn: 0,
                            XaEndAt: "23:59:59",
                            XaFromOffset: 0,
                            XaFromOn: 0,
                            XaFromAt: "00:00:00",
                            XaToOffset: 0,
                            XaToOn: 0,
                            XaToAt: "23:59:59",
                            DocExtList: ".doc .docx .pdf .bm2 .jpg .xlsx .xls",
                            MaxSize: "100MB"
                        })}>
                            Huỷ sửa
                        </button>
                    )}
                </div>
            </form>

            <h2 className="text-lg font-bold mb-2">Danh sách loại báo cáo</h2>
            <div className="flex gap-2 mb-2">
                <input
                    type="text"
                    placeholder="Tìm kiếm theo tên..."
                    className="border rounded p-1 w-full"
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                />
                <select className="border rounded p-1" value={periodFilter} onChange={e => setPeriodFilter(e.target.value)}>
                    <option value="">Tất cả</option>
                    <option value="DAILY">DAILY</option>
                    <option value="WEEKLY">WEEKLY</option>
                    <option value="MONTHLY">MONTHLY</option>
                    <option value="NONE">NONE</option>
                </select>
                <button className="bg-green-600 text-white px-3 rounded" onClick={() => exportToExcel()}>Xuất Excel</button>
            </div>

            <div className="overflow-x-auto">
                <table className="table-auto min-w-full border text-sm">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="border px-2 py-1">Tên</th>
                            <th className="border px-2 py-1">Định kỳ</th>
                            <th className="border px-2 py-1">Ngày tạo</th>
                            <th className="border px-2 py-1">NextAt</th>
                            <th className="border px-2 py-1">Chi tiết</th>
                            <th className="border px-2 py-1">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        {paginatedReports.map((r) => (
                            <tr key={r.ID} className="hover:bg-gray-50 align-top">
                                <td className="border px-2 py-1 whitespace-nowrap align-top">{r.Name}</td>
                                <td className="border px-2 py-1 whitespace-nowrap align-top">{r.Period_ID}</td>
                                <td className="border px-2 py-1 whitespace-nowrap align-top">{new Date(r.DateCreated).toLocaleString("vi-VN")}</td>
                                <td className="border px-2 py-1 whitespace-nowrap align-top">{r.NextAt ? new Date(r.NextAt).toLocaleString("vi-VN") : ""}</td>
                                <td className="border px-2 py-1 text-left">
                                    {renderFieldCell("DocExtList", r.DocExtList)}
                                    {renderFieldCell("MaxSize", r.MaxSize)}

                                    {renderFieldCell("ActiveOffset", r.ActiveOffset)}
                                    {renderFieldCell("ActiveOn", r.ActiveOn)}
                                    {renderFieldCell("ActiveAt", r.ActiveAt)}
                                    {renderFieldCell("DeactiveOffset", r.DeactiveOffset)}
                                    {renderFieldCell("DeactiveOn", r.DeactiveOn)}
                                    {renderFieldCell("DeactiveAt", r.DeactiveAt)}
                                    {renderFieldCell("StartOffset", r.StartOffset)}
                                    {renderFieldCell("StartOn", r.StartOn)}
                                    {renderFieldCell("StartAt", r.StartAt)}
                                    {renderFieldCell("EndOffset", r.EndOffset)}
                                    {renderFieldCell("EndOn", r.EndOn)}
                                    {renderFieldCell("EndAt", r.EndAt)}
                                    {renderFieldCell("FromOffset", r.FromOffset)}
                                    {renderFieldCell("FromOn", r.FromOn)}
                                    {renderFieldCell("From", r.From)}
                                    {renderFieldCell("ToOffset", r.ToOffset)}
                                    {renderFieldCell("ToOn", r.ToOn)}
                                    {renderFieldCell("To", r.To)}

                                    {renderFieldCell("XaActiveOffset", r.XaActiveOffset)}
                                    {renderFieldCell("XaActiveOn", r.XaActiveOn)}
                                    {renderFieldCell("XaActiveAt", r.XaActiveAt)}
                                    {renderFieldCell("XaDeactiveOffset", r.XaDeactiveOffset)}
                                    {renderFieldCell("XaDeactiveOn", r.XaDeactiveOn)}
                                    {renderFieldCell("XaDeactiveAt", r.XaDeactiveAt)}
                                    {renderFieldCell("XaStartOffset", r.XaStartOffset)}
                                    {renderFieldCell("XaStartOn", r.XaStartOn)}
                                    {renderFieldCell("XaStartAt", r.XaStartAt)}
                                    {renderFieldCell("XaEndOffset", r.XaEndOffset)}
                                    {renderFieldCell("XaEndOn", r.XaEndOn)}
                                    {renderFieldCell("XaEndAt", r.XaEndAt)}
                                    {renderFieldCell("XaFromOffset", r.XaFromOffset)}
                                    {renderFieldCell("XaFromOn", r.XaFromOn)}
                                    {renderFieldCell("XaFromAt", r.XaFromAt)}
                                    {renderFieldCell("XaToOffset", r.XaToOffset)}
                                    {renderFieldCell("XaToOn", r.XaToOn)}
                                    {renderFieldCell("XaToAt", r.XaToAt)}
                                </td>
                                <td className="border px-2 py-1 text-center">
                                    <button onClick={() => setForm(r)} className="text-blue-600 hover:underline mr-2">Sửa</button>
                                    <button onClick={() => handleDelete(r.ID)} className="text-red-600 hover:underline">Xoá</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="mt-2 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <button className="px-3 py-1 border rounded hover:bg-gray-200" disabled={currentPage === 1} onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}>Trước</button>
                        <span>Trang:</span>
                        <input type="number" min={1} max={totalPages} value={currentPage} onChange={(e) => setCurrentPage(Math.min(totalPages, Math.max(1, Number(e.target.value))))} className="border px-2 py-1 w-16 rounded" />
                        <button className="px-3 py-1 border rounded hover:bg-gray-200" disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))}>Sau</button>
                        <span className="text-sm text-gray-500 ml-2">Tổng: {totalPages} trang</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default ReportTypeManager;
