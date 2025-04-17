import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import LoginPage from "../pages/LoginPage";
import AdminAccounts from "../pages/AdminAccounts";
import UploadReport from "../pages/UploadReport";
import AdminLoaiBaoCao from "../pages/AdminLoaiBaoCao";
import AdminYeuCauBaoCao from "../pages/AdminYeuCauBaoCao";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />,
  },
  {
    path: "/dashboard",
    element: <App />,
  },
  {
    path: "/admin/accounts",
    element: <AdminAccounts />,
  },
  {
    path: "/admin/loaibaocao",
    element: <AdminLoaiBaoCao />,
  },
  {
    path: "/admin/yeucau",
    element: <AdminYeuCauBaoCao />,
  },
  {
    path: "/upload-report",
    element: <UploadReport />,
  }
]);