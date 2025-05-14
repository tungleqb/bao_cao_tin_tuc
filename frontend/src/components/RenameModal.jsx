import React, { useState } from "react";

const RenameModal = ({ user, onClose, onRename }) => {
  const [newName, setNewName] = useState("");

  const handleSubmit = () => {
    if (!newName.trim()) return alert("Vui lòng nhập tên mới");
    onRename(user, newName.trim());
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-white rounded shadow p-6 w-96 border border-blue-500">
        <h2 className="text-blue-600 font-bold text-lg mb-2">ĐỔI TÊN CHI NHÁNH</h2>
        <p className="mb-2">Tên chi nhánh cũ: <b>{user.name}</b></p>
        <input
          type="text"
          placeholder="Tên chi nhánh mới"
          className="w-full border p-2 rounded mb-4"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <div className="flex justify-end gap-2">
          <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-1 rounded">Đổi tên</button>
          <button onClick={onClose} className="bg-gray-200 text-black px-4 py-1 rounded">Huỷ</button>
        </div>
      </div>
    </div>
  );
};

export default RenameModal;