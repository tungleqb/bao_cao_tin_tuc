import React, { useState, useEffect } from 'react';
import axios from '../services/api';
import { useNavigate } from 'react-router-dom';

const LoginBranch = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState('');
  const [autoTried, setAutoTried] = useState(false);  // ✅ chỉ cho phép auto login 1 lần
  const navigate = useNavigate();

  // Auto login nếu có lưu remember
  useEffect(() => {
  if (!autoTried) {
    const saved = localStorage.getItem('remember_branch');
    if (saved) {
      try {
        const { username, password } = JSON.parse(atob(saved));
        setUsername(username);
        setPassword(password);
        setRemember(true);
        autoLogin(username, password);
      } catch (e) {
        console.error("Lỗi giải mã remember_branch:", e);
        localStorage.removeItem("remember_branch");
      }
    }
    setAutoTried(true);
  }
}, [autoTried]);


  const autoLogin = async (username, password) => {
  try {
    const res = await axios.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const token = res.data.access_token;
    localStorage.setItem('access_token', token);

    // ✅ Gọi /auth/me để lấy thông tin người dùng
    const headers = { Authorization: `Bearer ${token}` };
    const userRes = await axios.get('/auth/me', { headers });
    const userInfo = userRes.data;

    localStorage.setItem('user', JSON.stringify(userInfo));
    navigate('/user/dashboard');
  } catch (err) {
    console.warn('Tự động đăng nhập thất bại');
    localStorage.removeItem('remember_branch');
  }
};


  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const loginRes = await axios.post('/auth/login', new URLSearchParams({ username, password }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const token = loginRes.data.access_token;
      const headers = { Authorization: `Bearer ${token}` };

      // Gọi /auth/me để lấy user đầy đủ
      const userRes = await axios.get('/auth/me', { headers });
      const userInfo = userRes.data;

      // Lưu token + user
      localStorage.setItem("access_token", token);
      localStorage.setItem("user", JSON.stringify(userInfo));
      if (remember) {
        localStorage.setItem("remember_branch", btoa(JSON.stringify({ username, password })));
      } else {
        localStorage.removeItem("remember_branch");
      }

      // Chuyển trang
      navigate("/user/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
      setError("Đăng nhập thất bại. Vui lòng kiểm tra lại.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form className="bg-white p-6 rounded shadow-md w-96" onSubmit={handleLogin}>
        <h2 className="text-xl font-bold mb-4 text-center">Hệ thống gửi báo cáo Công an tỉnh Quảng Bình</h2>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <label className="block mb-2">Tên tài khoản:</label>
        <input type="text" className="w-full p-2 border rounded mb-4"
          value={username} onChange={(e) => setUsername(e.target.value)} required />
        <label className="block mb-2">Mật khẩu:</label>
        <input type="password" className="w-full p-2 border rounded mb-4"
          value={password} onChange={(e) => setPassword(e.target.value)} required />
        <div className="flex items-center mb-4">
          <input type="checkbox" id="remember" className="mr-2"
            checked={remember} onChange={(e) => setRemember(e.target.checked)} />
          <label htmlFor="remember">Ghi nhớ đăng nhập</label>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Đăng nhập
        </button>
      </form>
    </div>
  );
};

export default LoginBranch;
