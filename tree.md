D:\dev\bao_cao_tin_tuc
├── .dockerignore
├── .env.example
├── .gitignore
├── Cautruc_logic.txt
├── QuanlyBaocao.fig
├── README.md
├── README.txt
├── README_migrate.md
├── backend
│   ├── Dockerfile
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── templates
│   │   │   └── script.py.mako
│   │   └── versions
│   │       ├── 20250429_update_period_table.py
│   │       ├── 27e1d0e0c28c_init_database_schema.py
│   │       └── 63ddd3d48607_create_audit_logs_table_with_model_id_.py
│   ├── alembic.ini
│   ├── app
│   │   ├── config.py
│   │   ├── crud
│   │   │   ├── audit_log.py
│   │   │   ├── period.py
│   │   │   ├── period_create.py
│   │   │   ├── report.py
│   │   │   ├── report_type.py
│   │   │   └── user.py
│   │   ├── database.py
│   │   ├── dependencies
│   │   │   └── auth.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── audit_log.py
│   │   │   ├── period.py
│   │   │   ├── report.py
│   │   │   ├── report_type.py
│   │   │   └── user.py
│   │   ├── routers
│   │   │   ├── admin_audit_log.py
│   │   │   ├── admin_period.py
│   │   │   ├── admin_report.py
│   │   │   ├── admin_reporttype.py
│   │   │   ├── admin_user.py
│   │   │   ├── auth.py
│   │   │   ├── period.py
│   │   │   ├── report.py
│   │   │   └── utils.py
│   │   ├── scheduler.py
│   │   ├── schemas
│   │   │   ├── audit_log.py
│   │   │   ├── period.py
│   │   │   ├── report.py
│   │   │   ├── report_type.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   └── auth.py
│   │   └── utils
│   │       └── period_utils.py
│   ├── cert
│   │   ├── ca.crt
│   │   ├── ca.key
│   │   ├── ca.srl
│   │   ├── openssl.cnf
│   │   ├── server.crt
│   │   ├── server.csr
│   │   └── server.key
│   ├── requirements.txt
│   ├── start.sh
│   └── test
│       ├── test_create_objects.py
│       ├── test_datameta.py
│       ├── test_period.py
│       ├── test_report_api.py
│       ├── test_report_type_api.py
│       └── test_user_api.py
├── cert
├── congnghe.txt
├── dinhdang_logic.txt
├── docker-compose.yml
├── env-config.js
├── frontend
│   ├── Dockerfile
│   ├── cert
│   │   ├── ca.crt
│   │   ├── ca.key
│   │   ├── ca.srl
│   │   ├── openssl.cnf
│   │   ├── server.crt
│   │   ├── server.csr
│   │   └── server.key
│   ├── env-config.js
│   ├── index.html
│   ├── nginx.conf
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── public
│   │   ├── icon_bell.png
│   │   ├── icon_info.png
│   │   ├── icon_logout.png
│   │   ├── icon_password.png
│   │   ├── icon_user.png
│   │   └── logo.png
│   ├── src
│   │   ├── App.jsx
│   │   ├── components
│   │   │   ├── DeleteUserModal.jsx
│   │   │   ├── DropdownMenu.jsx
│   │   │   ├── RenameModal.jsx
│   │   │   ├── ReportForm.jsx
│   │   │   ├── ResetPasswordModal.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   ├── pages
│   │   │   ├── AccountInfo.jsx
│   │   │   ├── AccountManager.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AuditLog.jsx
│   │   │   ├── ChangePassword.jsx
│   │   │   ├── LoginAdmin.jsx
│   │   │   ├── LoginBranch.jsx
│   │   │   ├── PeriodManager.jsx
│   │   │   ├── ReportHistory.jsx
│   │   │   ├── ReportSummary.jsx
│   │   │   ├── ReportTypeManager.jsx
│   │   │   ├── UploadReport.jsx
│   │   │   └── UserDashboard.jsx
│   │   ├── router
│   │   │   └── router.jsx
│   │   ├── services
│   │   │   ├── api.js
│   │   │   ├── periodService.js
│   │   │   ├── requestService.js
│   │   │   └── userService.js
│   │   └── utils
│   │       ├── auth.js
│   │       └── unapi.js
│   ├── tailwind.config.js
│   └── vite.config.js