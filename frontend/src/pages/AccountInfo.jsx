// frontend/src/pages/AccountInfo.jsx
import React, { useEffect, useState } from "react";
import axios from "../services/api";
//import api from "../utils/api";
import iconUser from "/icon_user.png";
import iconInfo from "/icon_info.png";

const AccountInfo = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchMe = async () => {
      try {
        const res = await axios.get("/auth/me");
        setUser(res.data);
      } catch (err) {
        console.error("❌ Lỗi khi lấy thông tin tài khoản:", err);
      }
    };
    fetchMe();
  }, []);

  if (!user) return <div className="p-4 text-gray-600">Đang tải thông tin...</div>;

  return (
    <div className="bg-gray-50 p-8 max-w-2xl mx-auto rounded-xl shadow-sm">
      <h2 className="text-xl font-bold mb-6 flex items-center">
        <img src={iconInfo} alt="icon" className="w-6 h-6 mr-2" />
        Thông tin tài khoản
      </h2>

      <div className="flex items-center mb-6">
        <img
          src={user.avatar || iconUser}
          alt="Avatar"
          className="w-20 h-20 rounded-full border mr-4"
        />
        <div>
          <p className="text-lg font-semibold">{user.name}</p>
          <p className="text-gray-600">Tên đăng nhập: {user.username}</p>
          <p className="text-gray-600">Cấp tài khoản: {user.level}</p>
        </div>
      </div>

      <div className="bg-gray-100 p-4 rounded">
        <p className="text-sm text-gray-600">
          Ngày tạo:{" "}
          {user.time_created
            ? new Date(user.time_created).toLocaleString("vi-VN")
            : "Không rõ"}
        </p>
      </div>
    </div>
  );
};

export default AccountInfo;
