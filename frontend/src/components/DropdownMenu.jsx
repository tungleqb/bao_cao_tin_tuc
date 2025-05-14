import React, { useState, useRef, useEffect } from "react";

const DropdownMenu = ({ onLogout, onChangePassword, onShowAccountInfo }) => {
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  const handleClickOutside = (e) => {
    if (menuRef.current && !menuRef.current.contains(e.target)) {
      setOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <img
        src="/icon_user.png"
        alt="user"
        className="w-8 h-8 rounded-full border cursor-pointer"
        onClick={() => setOpen(!open)}
      />
      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-white border rounded shadow-md text-sm z-50">
          <div className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer"
           onClick={() => {
            onShowAccountInfo();
            setOpen(false);
          }}>
            <img src="/icon_info.png" alt="info" className="w-4 h-4 mr-2" />
            Thông tin
          </div>
          <div
            className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer"
            onClick={() => {
              onChangePassword();
              setOpen(false); // đóng menu sau khi nhấn
            }}
          >
            <img src="/icon_password.png" alt="password" className="w-4 h-4 mr-2" />
            Đổi mật khẩu
          </div>
          <div
            className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer text-red-600"
            onClick={onLogout}
          >
            <img src="/icon_logout.png" alt="logout" className="w-4 h-4 mr-2" />
            Đăng xuất
          </div>
        </div>
      )}
    </div>
  );
};

export default DropdownMenu;
