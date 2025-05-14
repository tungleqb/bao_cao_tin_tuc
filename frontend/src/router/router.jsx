import { createBrowserRouter } from "react-router-dom";
import LoginBranch from "../pages/LoginBranch";
import LoginAdmin from "../pages/LoginAdmin";
import UserDashboard from "../pages/UserDashboard"; // 🆕 Thêm dòng này
import AdminDashboard from "../pages/AdminDashboard"; // 🆕 Thêm dòng này
export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginBranch />,
  },
  {
    path: "/login/branch",
    element: <LoginBranch />,
  },
  {
    path: "/login/admin",
    element: <LoginAdmin />,
  },
  {
    path: "/user/dashboard", // 🆕 Route mới cho chi nhánh sau khi đăng nhập
    element: <UserDashboard />,
  },
  {
    path: "/admin/dashboard", // 🆕 Route mới cho chi nhánh sau khi đăng nhập
    element: <AdminDashboard />,
  },
]);
