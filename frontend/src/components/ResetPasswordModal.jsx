import React, { useState } from "react";

const ResetPasswordModal = ({ user, onClose, onReset }) => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = () => {
    if (!password.trim() || !confirmPassword.trim()) {
      alert("Vui lòng nhập đầy đủ thông tin");
      return;
    }
    if (password !== confirmPassword) {
      alert("❌ Mật khẩu không khớp");
      return;
    }
    onReset(user, password);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-white rounded shadow p-6 w-96 border border-blue-500 bg-blue-50">
        <h2 className="text-blue-600 font-bold text-lg mb-2">
          Đặt lại mật khẩu cho tài khoản <span className="text-black">{user.username}</span>
        </h2>
        <input
          type="password"
          placeholder="Mật khẩu mới"
          className="w-full border p-2 rounded mb-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Xác nhận mật khẩu"
          className="w-full border p-2 rounded mb-4"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <div className="flex justify-end gap-2">
          <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-1 rounded">
            Đặt lại
          </button>
          <button onClick={onClose} className="bg-gray-200 text-black px-4 py-1 rounded">
            Huỷ
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordModal;