import React, { useEffect, useState } from "react";
import { getActivePeriods } from "../services/periodService";
import { getTokenInfo } from "../utils/auth";
import UploadReport from "./UploadReport";
import { useNavigate } from "react-router-dom";
import logo from "/logo.png";
import iconUser from "/icon_user.png";
import iconBell from "/icon_bell.png";
import DropdownMenu from "../components/DropdownMenu";
import axios from "../services/api"; // bổ sung nếu thiếu
import ReportHistory from "./ReportHistory";
import ChangePassword from "./ChangePassword";
import AccountInfo from "./AccountInfo";

const UserDashboard = () => {
  const [periods, setPeriods] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [reportStatus, setReportStatus] = useState("");
  const [reportTime, setReportTime] = useState("");
  const [reportStatusMap, setReportStatusMap] = useState({});
  const [countdownMap, setCountdownMap] = useState({});
  const [showHistory, setShowHistory] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [showAccountInfo, setShowAccountInfo] = useState(false);


  //const navigate = useNavigate();
  //const user = getTokenInfo();


  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const [serverTime, setServerTime] = useState(null);
  const [fetchedAt, setFetchedAt] = useState(null);

  const fetchServerTime = async () => {
    try {
      const res = await axios.get("/server-time");
      const serverNow = new Date(res.data.now);
      setServerTime(serverNow);
      setFetchedAt(Date.now());
    } catch (err) {
      console.error("Không lấy được thời gian server:", err);
    }
  };

  const getCurrentServerTime = () => {
    if (!serverTime || !fetchedAt) return new Date();
    const diff = Date.now() - fetchedAt;
    return new Date(serverTime.getTime() + diff);
  };

  useEffect(() => {
    axios.get("/auth/me", { withCredentials: true })
      .then(async res => {
        setUser(res.data);
        await fetchServerTime();  // gọi server time trước
        fetchPeriods();
      })
      .catch(() => {
        alert("Phiên đăng nhập hết hạn");
        navigate("/login/branch");
      });
  }, []);

  useEffect(() => {
    const updateCountdowns = () => {
      const updated = {};
      const now = getCurrentServerTime();

      periods.forEach((p) => {
        const isXa = user?.level === "CAPXA";
        const start = new Date(isXa ? p.XaStartAt : p.StartAt);
        const end = new Date(isXa ? p.XaEndAt : p.EndAt);
        const diff = Math.abs(now < start ? start - now : now > end ? now - end : end - now);
        const s = Math.floor(diff / 1000) % 60;
        const m = Math.floor(diff / 60000) % 60;
        const h = Math.floor(diff / 3600000) % 24;
        const d = Math.floor(diff / 86400000);
        const formatted = `${d}:${h}:${m}:${s}`;
        const status = now < start
          ? `   Chưa đến hạn (${formatted})`
          : now > end
            ? `   Quá hạn (${formatted})`
            : `    Đúng hạn (${formatted})`;
        updated[p.ID] = status;
      });

      setCountdownMap(updated);
    };

    updateCountdowns();
    const interval = setInterval(updateCountdowns, 1000);
    return () => clearInterval(interval);
  }, [periods]);


  const fetchAllReportStatuses = async (periodList) => {
    const updatedMap = {};
    for (const p of periodList) {
      try {
        const res = await axios.get(`/report/${p.ID}`);
        updatedMap[p.ID] = res.data;
      } catch (err) {
        updatedMap[p.ID] = { Status: "not_sent" };
      }
    }
    return updatedMap;
  };

  const fetchPeriods = async () => {
    try {
      const res = await getActivePeriods();
      setPeriods(res.data);
      console.log("📌 Đã gọi setPeriods với:", res.data);
      if (res.data.length > 0) {
        setSelectedPeriod(res.data[0]);
        fetchAllReportStatuses(res.data); // ✅ gọi tại đây
      }
    } catch (err) {
      console.error("Lỗi tải kỳ báo cáo:", err);
    }
  };
  return (
    <div className="bg-[#eef4fb] min-h-screen flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center px-6 py-3 bg-[#eaf7f5] shadow">
        <div className="flex items-center space-x-3">
          <img src={logo} alt="logo" className="w-8 h-8" />
          <h1 className="text-[#0d2d52] font-bold text-lg">
            Hệ thống báo cáo Công an tỉnh Quảng Trị
          </h1>
        </div>
        <div className="flex items-center space-x-4">
          <img src={iconBell} alt="bell" className="w-5 h-5" />
          <div className="text-right text-sm text-[#0d2d52]">
            <div className="font-semibold">{user?.name || "Tên đơn vị"}</div>
            <div className="text-xs">{user?.username}</div>
          </div>
          <DropdownMenu
            onLogout={async () => {
              try {
                await axios.post("/auth/logout", {}, { withCredentials: true });
              } catch (err) {
                console.error("Logout error:", err);
              } finally {
                // Chuyển hướng sang trang login sau khi xoá cookie

                localStorage.removeItem("remember_branch");
                localStorage.removeItem("user");
                navigate("/login/branch");  // hoặc "/login/admin" tuỳ loại tài khoản
              }
            }}
            onChangePassword={() => {
              setShowChangePassword(true);
              setShowHistory(false);
              setShowAccountInfo(false);
            }}
            onShowAccountInfo={() => {
              setShowAccountInfo(true);
              setShowChangePassword(false);
              setShowHistory(false);
            }}
          />
        </div>
      </div>

      <div className="flex flex-1">
        {/* Sidebar */}
        <div className="w-[280px] bg-white p-3 shadow-inner border-r overflow-y-auto">
          {periods.map((p) => (
            <div
              key={p.ID}
              onClick={() => {
                setSelectedPeriod(p);
                setShowHistory(false);  // ✅ Ẩn trang lịch sử nếu đang hiển thị
                setShowChangePassword(false);
                setShowAccountInfo(false);  // ✅ bổ sung dòng này
              }}
              className={`p-3 rounded-lg mb-3 cursor-pointer ${selectedPeriod?.ID === p.ID
                ? "bg-blue-100 border border-blue-400"
                : "bg-gray-100 hover:bg-gray-200"
                }`}
            >
              <div className="font-semibold text-blue-800 text-sm">{p.Name}</div>
              <div className="text-xs text-gray-600">
                🕓{new Date(user?.level === "CAPXA" ? p.XaStartAt : p.StartAt).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" })} – {new Date(user?.level === "CAPXA" ? p.XaEndAt : p.EndAt).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" })}
                <br />
                <span className="font-semibold text-xs">
                  {countdownMap[p.ID]}
                </span>
              </div>

              {reportStatusMap[p.ID] && (
                <div className={
                  reportStatusMap[p.ID]?.LateSeconds === 0
                    ? "text-green-600 text-xs mt-1 font-medium"
                    : reportStatusMap[p.ID]?.LateSeconds > 0
                      ? "text-red-600 text-xs mt-1 font-medium"
                      : reportStatusMap[p.ID]?.LateSeconds < 0
                        ? "text-red-600 text-xs mt-1 font-medium"
                        : "text-gray-600 text-xs mt-1 font-medium"
                }>
                  📤 {
                    reportStatusMap[p.ID]?.Status === "sent" ? (
                      <>
                        Đã gửi lúc {new Date(reportStatusMap[p.ID]?.SentAt).toLocaleString("vi-VN", {
                          day: "2-digit", month: "2-digit", year: "numeric",
                          hour: "2-digit", minute: "2-digit", second: "2-digit"
                        })}
                        <br />
                        {
                          typeof reportStatusMap[p.ID]?.LateSeconds === "number"
                            ? reportStatusMap[p.ID].LateSeconds === 0
                              ? "  Đúng hạn"
                              : reportStatusMap[p.ID].LateSeconds < 0
                                ? `  Trước hạn ${Math.abs(reportStatusMap[p.ID].LateSeconds)} giây`
                                : `  Quá hạn ${reportStatusMap[p.ID].LateSeconds} giây`
                            : ""
                        }
                      </>
                    ) : "Chưa gửi"
                  }
                </div>
              )}
            </div>
          ))}
          <div
            onClick={() => setShowHistory(true)}
            className="p-2 rounded bg-gray-300 text-sm font-semibold text-center cursor-pointer hover:bg-gray-400"
          >
            Lịch sử báo cáo
          </div>
        </div>

        {/* Nội dung chính */}
        <div className="flex-1 p-6 mb-20">
          <h2 className="text-lg font-bold text-[#0d2d52] mb-4">
            {user?.name || "Tên đơn vị"}
          </h2>
          {showAccountInfo ? (
            <AccountInfo />
          ) : showChangePassword ? (
            <ChangePassword />
          ) : showHistory ? (
            <ReportHistory user={user} />
          ) : selectedPeriod ? (
            <UploadReport
              period={selectedPeriod}
              reportStatus={reportStatus}
              reportTime={reportTime}
              user={user}
              serverTime={serverTime}
              fetchedAt={fetchedAt}
              onAfterSend={async () => {
                const updated = await fetchAllReportStatuses(periods);
                setReportStatusMap(updated);  // ép re-render với object mới
              }}
            />
          ) : (
            <div className="text-center text-gray-500">Không có kỳ báo cáo nào đang kích hoạt.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
