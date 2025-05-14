import React, { useState } from 'react';
import axios from '../services/api'; // dùng cấu hình axios có sẵn
//import api from "../utils/api";

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState(null);
  const [messageType, setMessageType] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setMessage('Mật khẩu mới và xác nhận không khớp');
      setMessageType('error');
      return;
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        '/auth/changepassword',
        {
          old_password: oldPassword,
          new_password: newPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage('Đổi mật khẩu thành công');
      setMessageType('success');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      const msg =
        error.response?.data?.detail || 'Lỗi khi đổi mật khẩu';
      setMessage(msg);
      setMessageType('error');
    }
  };

  return (
    <div className="bg-gray-50 p-8 max-w-2xl mx-auto rounded-xl shadow-sm">
      <h2 className="text-xl font-bold mb-6">Đổi mật khẩu</h2>

      {message && (
        <div
          className={`mb-4 px-4 py-2 rounded text-sm ${
            messageType === 'success'
              ? 'bg-green-100 text-green-700'
              : 'bg-red-100 text-red-700'
          }`}
        >
          {message}
        </div>
      )}

      <form className="space-y-5" onSubmit={handleSubmit}>
        <div>
          <label className="block mb-1 font-medium text-gray-700">Mật khẩu cũ</label>
          <input
            type="password"
            className="w-full border rounded px-4 py-2"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block mb-1 font-medium text-gray-700">Mật khẩu mới</label>
          <input
            type="password"
            className="w-full border rounded px-4 py-2"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block mb-1 font-medium text-gray-700">Xác nhận mật khẩu</label>
          <input
            type="password"
            className="w-full border rounded px-4 py-2"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <div className="flex space-x-4 pt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700"
          >
            Xác nhận
          </button>
          <button
            type="button"
            onClick={() => {
              setOldPassword('');
              setNewPassword('');
              setConfirmPassword('');
              setMessage(null);
            }}
            className="bg-gray-200 text-black px-5 py-2 rounded hover:bg-gray-300"
          >
            Đóng
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChangePassword;
