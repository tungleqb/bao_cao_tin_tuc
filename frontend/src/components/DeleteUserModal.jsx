import React from "react";

const DeleteUserModal = ({ user, onClose, onDelete }) => {
  const handleConfirm = () => {
    onDelete(user);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-red-50 border border-red-400 text-red-700 rounded shadow p-6 w-96">
        <p className="text-base mb-4">
          Bạn có chắc chắn xoá tài khoản <b>{user.username}</b> không?
        </p>
        <div className="flex justify-end gap-2">
          <button onClick={handleConfirm} className="bg-red-600 text-white px-4 py-1 rounded">
            Xoá
          </button>
          <button onClick={onClose} className="bg-gray-200 text-black px-4 py-1 rounded">
            Không xoá
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteUserModal;