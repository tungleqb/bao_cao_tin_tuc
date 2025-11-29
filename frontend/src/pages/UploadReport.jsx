import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../services/api";

const UploadReport = ({ period, user, serverTime, fetchedAt, onAfterSend }) => {
  const renderTimeStatusMessage = () => {
    if (!reportData || reportData.Status !== "sent") return "";
    const late = reportData.LateSeconds;
    if (late === 0) return "– Bạn đã gửi đúng hạn";
    if (late < 0) return `– Bạn đã gửi trước hạn ${Math.abs(late)} giây`;
    return `– Bạn đã gửi quá hạn ${late} giây`;
  };
  const [file, setFile] = useState(null);
  const [timeStatus, setTimeStatus] = useState("");
  const [timeLeft, setTimeLeft] = useState("");
  const [buttonLabel, setButtonLabel] = useState("Gửi");
  const [sending, setSending] = useState(false);
  const [sendMessage, setSendMessage] = useState("");
  const [reportData, setReportData] = useState(null);
  const [confirmResend, setConfirmResend] = useState(false);
  const [pendingSend, setPendingSend] = useState(false);
  //const [serverTime, setServerTime] = useState(null);     // server trả về
  //const [fetchedAt, setFetchedAt] = useState(null);       // thời điểm máy client nhận được
  const [eventYes, setEventYes] = useState(false);
  const [eventNo, setEventNo] = useState(false);

  const navigate = useNavigate();

  const fetchReportStatus = async () => {
    try {
      const res = await axios.get(`/report/${period?.ID}`);
      setReportData(res.data);
      setButtonLabel(res.data.Status === "sent" ? "Gửi lại" : "Gửi");
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login/branch");
      }
      console.error("Lỗi khi lấy trạng thái báo cáo:", err);
    }
  };

  const getCurrentServerTime = () => {
    if (!serverTime || !fetchedAt) return new Date();
    const diff = Date.now() - fetchedAt; // mili giây trôi qua từ lúc fetch
    return new Date(serverTime.getTime() + diff);
  };

  const handleSend = async () => {
    if (!file) return alert("Vui lòng chọn file trước khi gửi!");
    if (period?.ID?.toUpperCase().startsWith("DAILY")) {
      if ((eventYes && eventNo) || (!eventYes && !eventNo)) {
        return alert("Vui lòng chọn 1 trong 2: 'Có' hoặc 'Không có tình hình đáng chú ý'.");
      }
    }

    const hasEvent = period?.ID?.toUpperCase().startsWith("DAILY") ? eventYes : false;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("period_id", period?.ID);
    formData.append("has_event", hasEvent);

    const now = getCurrentServerTime();
    const start = new Date(user?.level === "CAPXA" ? period?.XaStartAt : period?.StartAt);
    const end = new Date(user?.level === "CAPXA" ? period?.XaEndAt : period?.EndAt);

    const getStatusText = () => {
      if (now < start) return `trước hạn ${Math.floor((start - now) / 60000)} phút`;
      if (now > end) return `quá hạn ${Math.floor((now - end) / 60000)} phút`;
      return "đúng hạn";
    };

    try {
      setSending(true);
      setSendMessage("");
      await axios.post("/report/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setEventYes(false);
      setEventNo(false);
      const sentTime = now.toLocaleString("vi-VN");
      const timeStatusText = getStatusText();
      setSendMessage(`✅ Đã gửi lúc ${sentTime} – Bạn đã gửi ${timeStatusText}`);
      await fetchReportStatus(); // cập nhật trạng thái từ backend
      if (typeof onAfterSend === "function") onAfterSend();
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem("user");
        navigate("/login/branch");
        return;
      }
      console.error("Lỗi gửi báo cáo:", err);
      setSendMessage("❌ Gửi báo cáo thất bại.");
    } finally {
      setSending(false);
    }
  };

  const onSendClick = () => {
    if (reportData?.Status === "sent") {
      setConfirmResend(true);  // hiển thị popup xác nhận
    } else {
      handleSend();  // gửi ngay nếu chưa gửi lần nào
    }
  };

  const formatDuration = (ms) => {
    const totalSeconds = Math.floor(Math.abs(ms) / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${days} ngày ${hours} giờ ${minutes} phút ${seconds} giây`;
  };

  useEffect(() => {
    if (period?.ID) fetchReportStatus();

    const isXa = user?.level === "CAPXA";
    const rawStart = isXa ? period?.XaStartAt : period?.StartAt;
    const rawEnd = isXa ? period?.XaEndAt : period?.EndAt;

    const startTime = new Date(rawStart);
    const endTime = new Date(rawEnd);

    const updateTime = () => {
      const now = getCurrentServerTime();
      if (!now) return;

      if (now < startTime) {
        setTimeStatus("Chưa đến hạn");
        setTimeLeft(formatDuration(startTime - now));
      } else if (now >= startTime && now <= endTime) {
        setTimeStatus("Đúng hạn");
        setTimeLeft(formatDuration(endTime - now));
      } else {
        setTimeStatus("Quá hạn");
        setTimeLeft(formatDuration(now - endTime));
      }
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, [period, user]);

  useEffect(() => {
    setSendMessage("");
    setFile(null);
    setEventYes(false);
    setEventNo(false);
  }, [period?.ID]);

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-lg font-bold text-center text-gray-800 uppercase mb-4">
        {period?.Name || "BÁO CÁO"}
      </h2>

      <div className="text-sm mb-2">
        <span className="font-semibold">Gửi đến: </span>
        <span className={sendMessage.includes("đúng hạn") ? "text-green-600 font-semibold" : "text-yellow-600 font-semibold"}>
          Trung tâm thông tin chỉ huy - Phòng Tham mưu - Công an tỉnh Quảng Trị
        </span>
      </div>

      <div className="flex items-center gap-4 mb-2">
        <label className="font-semibold text-sm">File báo cáo đính kèm</label>
        <input
          type="file"
          id="upload"
          onChange={(e) => setFile(e.target.files[0])}
          className="hidden"
        />
        <label htmlFor="upload" className="px-4 py-1 bg-orange-500 text-white rounded cursor-pointer">
          Tải lên
        </label>
        <span className="text-sm text-gray-700">{file?.name || "<chưa có file>"}</span>
      </div>

      {period?.ID?.toUpperCase().startsWith("DAILY") && (
        <div className="flex flex-col mb-4 gap-1">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="hasEventYes"
              className="mr-2"
              checked={eventYes}
              onChange={(e) => setEventYes(e.target.checked)}
            />
            <label htmlFor="hasEventYes" className="text-sm">
              <b>Có</b> tình hình đáng chú ý
            </label>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="hasEventNo"
              className="mr-2"
              checked={eventNo}
              onChange={(e) => setEventNo(e.target.checked)}
            />
            <label htmlFor="hasEventNo" className="text-sm">
              <b>Không có</b> tình hình đáng chú ý
            </label>
          </div>
        </div>
      )}

      <div className="text-sm mb-2">
        <span className="font-semibold">Thời gian:</span>{" "}
        <span className={
          timeStatus === "Đúng hạn" ? "text-green-600 font-semibold" :
            "text-red-600 font-semibold"
        }>
          {timeStatus}
        </span>{" "}
        <span className="text-gray-800">{timeLeft}</span>
      </div>

      <div className="text-sm mb-4">
        <span className="font-semibold">Trạng thái:</span>{" "}
        {reportData?.Status === "sent" ? (
          <span className={
            timeStatus === "Đúng hạn" ? "text-green-600 font-semibold" : "text-red-600 font-semibold"
          }>
            Đã gửi lúc {new Date(reportData.SentAt).toLocaleString("vi-VN")} {renderTimeStatusMessage()}
          </span>
        ) : (
          <span className="text-gray-500">Chưa gửi</span>
        )}
      </div>

      {sendMessage && (
        <div className="text-sm text-center mb-2" style={{ color: sendMessage.includes("✅") ? (sendMessage.includes("Đúng hạn") ? "green" : "red") : "red" }}>
          {sendMessage}
        </div>
      )}
      {confirmResend && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl shadow-md w-[400px]">
            <p className="text-gray-800 font-semibold mb-4">
              File báo cáo đã gửi sẽ bị xoá và thời gian gửi tính từ lúc này.
            </p>
            <div className="flex justify-end gap-3">
              <button
                className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500"
                onClick={() => setConfirmResend(false)}
              >
                Huỷ
              </button>
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                onClick={() => {
                  setConfirmResend(false);
                  handleSend();  // gửi lại
                }}
              >
                Tiếp tục gửi
              </button>
            </div>
          </div>
        </div>
      )}
      <div className="text-center mt-4">
        <button
          onClick={onSendClick}
          className="bg-blue-600 text-white font-semibold px-6 py-2 rounded hover:bg-blue-700"
        >
          {sending ? "Đang gửi..." : buttonLabel}
        </button>
      </div>
    </div>
  );
};

export default UploadReport;
