import React, { useEffect, useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";

const LoginAdmin = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [showPassword, setShowPassword] = useState(false);


  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post(
        "/auth/admin",
        new URLSearchParams({ username, password }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      if (remember) {
        localStorage.setItem("admin_username", username);
      }
      navigate("/admin/dashboard");
    } catch (error) {
      alert("Sai tên đăng nhập hoặc mật khẩu.");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-100">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Hệ thống gửi báo cáo Công an tỉnh Quảng Trị
        </h1>
        <h2 className="text-1xl font-bold mb-4 text-center">Đăng nhập Quản trị viên</h2>
        <input
          type="text"
          placeholder="Tên đăng nhập"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleKeyPress}
          className="w-full p-2 mb-4 border border-gray-300 rounded"
        />
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Mật khẩu"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleKeyPress}
          className="w-full p-2 mb-2 border border-gray-300 rounded"
        />
        <div className="flex items-center mb-2">
          <input
            type="checkbox"
            checked={showPassword}
            onChange={() => setShowPassword(!showPassword)}
            className="mr-2"
          />
          <label>Hiện mật khẩu</label>
        </div>
        <button
          onClick={handleLogin}
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Đăng nhập
        </button>
        <div className="flex items-center mb-4">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="mr-2"
          />
          <label>Ghi nhớ đăng nhập</label>
        </div>
      </div>
    </div>
  );
};

export default LoginAdmin;
