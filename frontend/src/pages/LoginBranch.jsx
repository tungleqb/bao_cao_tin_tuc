import React, { useState, useEffect } from 'react';
import axios from '../services/api';
import { useNavigate } from 'react-router-dom';

const LoginBranch = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState('');
  const [autoTried, setAutoTried] = useState(false);
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    localStorage.removeItem("user");
  }, []);

  // ✅ Auto điền username nếu có nhớ đăng nhập (không tự động login)
  useEffect(() => {
    if (!autoTried) {
      const saved = localStorage.getItem('remember_branch');
      if (saved) {
        try {
          const { username } = JSON.parse(atob(saved));
          setUsername(username);
          setRemember(true);
        } catch (e) {
          console.error("Lỗi giải mã remember_branch:", e);
          localStorage.removeItem("remember_branch");
        }
      }
      setAutoTried(true);
    }
  }, [autoTried]);

  // ✅ Nếu bỏ check ghi nhớ → xoá thông tin
  useEffect(() => {
    if (!remember) {
      localStorage.removeItem("remember_branch");
    }
  }, [remember]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/auth/login', new URLSearchParams({ username, password }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const userRes = await axios.get('/auth/me');
      const userInfo = userRes.data;

      // ✅ Lưu user và ghi nhớ nếu cần (chỉ lưu username)
      localStorage.setItem('user', JSON.stringify(userInfo));
      if (remember) {
        localStorage.setItem("remember_branch", btoa(JSON.stringify({ username })));
      } else {
        localStorage.removeItem("remember_branch");
      }

      navigate("/user/dashboard");
    } catch (err) {
      localStorage.removeItem("remember_branch");
      const msg = err.response?.data?.detail || err.message || "Đăng nhập thất bại. Vui lòng kiểm tra lại.";
      setError(msg);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form className="bg-white p-6 rounded shadow-md w-100" onSubmit={handleLogin}>
        <h2 className="text-xl font-bold mb-4 text-center">Hệ thống gửi báo cáo Công an tỉnh Quảng Trị</h2>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <label className="block mb-2">Tên tài khoản:</label>
        <input type="text" className="w-full p-2 border rounded mb-4"
          value={username} onChange={(e) => setUsername(e.target.value)} required />
        <label className="block mb-2">Mật khẩu:</label>
        <input type={showPassword ? "text" : "password"} className="w-full p-2 border rounded mb-4"
          value={password} onChange={(e) => setPassword(e.target.value)} required />
        <div className="mt-2">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox h-4 w-4"
              checked={showPassword}
              onChange={() => setShowPassword(!showPassword)}
            />
            <span className="ml-2 text-sm text-gray-700">Hiện mật khẩu</span>
          </label>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Đăng nhập
        </button>
        <div className="flex items-center mb-4 mt-2">
          <input type="checkbox" id="remember" className="mr-2"
            checked={remember} onChange={(e) => setRemember(e.target.checked)} />
          <label htmlFor="remember">Ghi nhớ đăng nhập</label>
        </div>
      </form>
    </div>
  );
};

export default LoginBranch;
