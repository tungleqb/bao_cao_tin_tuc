
import React, { useEffect, useState } from "react";
import axios from "axios";
import CountdownClock from "../components/CountdownClock";
import { getMyReportRequests } from "../services/requestService";

function UploadReport() {
  const [loaiBaoCaos, setLoaiBaoCaos] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [selectedLoai, setSelectedLoai] = useState(null);
  const [hasEvent, setHasEvent] = useState(true);
  const [file, setFile] = useState(null);
  const [statusMsg, setStatusMsg] = useState("");
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getMyReportRequests(token);
        const requestLoaiIds = res.data.map(r => r.loai_baocao_id);
        const allLoai = await axios.get("http://localhost:8000/admin/loaibaocao/public", {
          headers: { Authorization: `Bearer ${token}` }
        });
        const filteredLoai = allLoai.data.filter(l => requestLoaiIds.includes(l.id));
        setLoaiBaoCaos(filteredLoai);
      } catch (err) {
        setStatusMsg("Không thể tải loại báo cáo");
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    const loai = loaiBaoCaos.find((l) => l.id === parseInt(selectedId));
    setSelectedLoai(loai);
  }, [selectedId, loaiBaoCaos]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !selectedId) return setStatusMsg("Vui lòng chọn loại và file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("loai_baocao_id", selectedId);
    formData.append("has_event", hasEvent);

    try {
      await axios.post("http://localhost:8000/report/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      setStatusMsg("Gửi báo cáo thành công");
    } catch (err) {
      setStatusMsg("Gửi báo cáo thất bại");
    }
  };

  const isLate = selectedLoai && new Date() > new Date(selectedLoai.han_gui);
  const deadline = selectedLoai ? new Date(selectedLoai.han_gui) : null;

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Gửi báo cáo</h2>
      {statusMsg && <p className="mb-2 text-center text-blue-600">{statusMsg}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
          className="w-full border px-2 py-2 rounded"
          required
        >
          <option value="">-- Chọn loại báo cáo --</option>
          {loaiBaoCaos.map((l) => (
            <option key={l.id} value={l.id}>
              {l.ten_loai}
            </option>
          ))}
        </select>

        {selectedLoai?.ten_loai.toLowerCase().includes("ngày") && (
          <div className="space-x-4">
            <label>
              <input
                type="radio"
                name="hasEvent"
                checked={hasEvent === true}
                onChange={() => setHasEvent(true)}
              />
              <span className="ml-1">Có sự kiện đáng chú ý</span>
            </label>
            <label>
              <input
                type="radio"
                name="hasEvent"
                checked={hasEvent === false}
                onChange={() => setHasEvent(false)}
              />
              <span className="ml-1">Không có sự kiện đáng chú ý</span>
            </label>
          </div>
        )}

        <input
          type="file"
          accept="*"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full"
        />

        {deadline && (
          <div className={`p-2 rounded text-white ${isLate ? "bg-red-500" : "bg-green-600"}`}>
            Hạn gửi: {deadline.toLocaleString("vi-VN")}
            <CountdownClock deadline={deadline} />
          </div>
        )}

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Gửi báo cáo
        </button>
      </form>
    </div>
  );
}

export default UploadReport;
