import React, { useEffect, useState, createContext } from "react";
export const DashboardContext = createContext();
import logo from "/logo.png";
import iconBell from "/icon_bell.png";
import iconUser from "/icon_user.png";
import { useNavigate } from "react-router-dom";
import DropdownMenu from "../components/DropdownMenu";
import ReportSummary from "./ReportSummary";
import AccountManager from "./AccountManager";
import PeriodManager from "./PeriodManager";
import ReportTypeManager from "./ReportTypeManager";
import AuditLog from "./AuditLog";
import ChangePassword from "./ChangePassword";
import AccountInfo from "./AccountInfo";
import axios from "../services/api"; // bổ sung nếu thiếu

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState("summary");
  const [selectedPeriodId, setSelectedPeriodId] = useState(null);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const handleLogout = async () => {
    try {
      await axios.post("/auth/logout", {}, { withCredentials: true });
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      // Chuyển hướng sang trang login sau khi xoá cookie
      setUser("");
      navigate("/login/admin");  // hoặc "/login/admin" tuỳ loại tài khoản
    }
  };
  useEffect(() => {
    axios.get("/auth/me", { withCredentials: true })
      .then(res => setUser(res.data))
      .catch(() => {
        alert("Phiên đăng nhập đã hết hạn");
        navigate("/login/admin");
      });
  }, []);
  const renderContent = () => {
    switch (activeTab) {
      case "summary":
        return <ReportSummary />;
      case "account":
        return <AccountManager />;
      case "period":
        return <PeriodManager />;
      case "reportType":
        return <ReportTypeManager />;
      case "audit":
        return <AuditLog />;
      case "changepw":
        return <ChangePassword />;
      case "accountInfo":
        return <AccountInfo />;
      default:
        return null;
    }
  };

  return (
    <DashboardContext.Provider value={{ activeTab, setActiveTab, selectedPeriodId, setSelectedPeriodId }}>
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
              <div className="font-semibold">{user?.name || "Quản trị viên"}</div>
              <div className="text-xs">{user?.username}</div>
            </div>
            <DropdownMenu
              onLogout={handleLogout}
              onChangePassword={() => setActiveTab("changepw")}
              onShowAccountInfo={() => setActiveTab("accountInfo")}
            />
          </div>
        </div>

        <div className="flex flex-1">
          {/* Sidebar */}
          <div className="w-[280px] bg-white p-4 border-r">
            <SidebarItem label="Tổng hợp báo cáo" tab="summary" activeTab={activeTab} onClick={setActiveTab} />
            <SidebarItem label="Quản lý tài khoản" tab="account" activeTab={activeTab} onClick={setActiveTab} />
            <SidebarItem label="Quản lý Kỳ báo cáo" tab="period" activeTab={activeTab} onClick={setActiveTab} />
            <SidebarItem label="Quản lý loại báo cáo" tab="reportType" activeTab={activeTab} onClick={setActiveTab} />
            <SidebarItem label="Nhật ký thao tác" tab="audit" activeTab={activeTab} onClick={setActiveTab} />
          </div>

          {/* Main Content */}
          <div className="flex-1 p-6">{renderContent()}</div>
        </div>
      </div>
    </DashboardContext.Provider>
  );
};

const SidebarItem = ({ label, tab, activeTab, onClick }) => (
  <div
    onClick={() => onClick(tab)}
    className={`p-3 rounded-lg mb-2 cursor-pointer font-medium text-sm ${activeTab === tab
      ? "bg-blue-100 border border-blue-400 text-blue-800"
      : "bg-gray-100 hover:bg-gray-200 text-gray-700"
      }`}
  >
    {label}
  </div>
);

export default AdminDashboard;
