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
│   ├── .env
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
│   │   │   ├── admin_report_type.py
│   │   │   ├── admin_user.py
│   │   │   ├── auth.py
│   │   │   ├── period.py
│   │   │   └── report.py
│   │   ├── scheduler.py
│   │   ├── schemas
│   │   │   ├── audit_log.py
│   │   │   ├── period.py
│   │   │   ├── report.py
│   │   │   ├── report_type.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   └── auth.py
│   │   ├── static
│   │   │   └── reports
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
├── congnghe.txt
├── dinhdang_logic.txt
├── docker-compose.yml
├── env-config.js
├── frontend
│   ├── .env
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
│   │   ├── assets
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
│   │   │   ├── ChangePassword.jsx
│   │   │   ├── LoginAdmin.jsx
│   │   │   ├── LoginBranch.jsx
│   │   │   ├── PeriodManager.jsx
│   │   │   ├── ReportHistory.jsx
│   │   │   ├── ReportSummary.jsx
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
├── project_dump.txt
├── promts.txt
├── requirements.txt
├── roadmap_admin.md
├── roadmap_auth.md
├── roadmap_baocao.md
├── roadmap_deploy.md
├── roadmap_export_excel.md
├── roadmap_frontend.md
├── roadmap_scheduler.md
├── roadmap_tongthe.md
├── spec_loaibaocao.txt
├── tree.md
└── uploaded_reports
    ├── DAILY_191A57B4_20250509003000
    │   └── has_event
    │       └── cahoanlao.baocao_DAILY_191A57B4_20250509003000_20250509_045827.docx
    ├── DAILY_191A57B4_20250510003000
    ├── DAILY_191A57B4_20250511003000
    ├── DAILY_191A57B4_20250512003000
    ├── DAILY_191A57B4_20250513003000
    ├── DAILY_191A57B4_20250514003000
    ├── DAILY_3A6ACB4B_20250510003000
    │   └── no_event
    │       └── px01.baocao_DAILY_3A6ACB4B_20250510003000_20250510_101001.docx
    ├── DAILY_3A6ACB4B_20250511003000
    ├── DAILY_3A6ACB4B_20250512003000
    ├── DAILY_3A6ACB4B_20250513003000
    ├── DAILY_3A6ACB4B_20250514003000
    ├── DAILY_48605862_20250507003000
    ├── DAILY_48605862_20250508003000
    ├── DAILY_48605862_20250509003000
    ├── DAILY_82CAE57B_20250507003000
    ├── DAILY_82CAE57B_20250508003000
    ├── DAILY_82CAE57B_20250509003000
    ├── DAILY_82CAE57B_20250510003000
    │   ├── has_event
    │   └── no_event
    │       └── px01.baocao_DAILY_82CAE57B_20250510003000_20250510_074350.docx
    ├── DAILY_82CAE57B_20250511003000
    ├── DAILY_82CAE57B_20250512003000
    │   ├── has_event
    │   │   └── ph10.baocao_DAILY_82CAE57B_20250512003000_20250512_014938.docx
    │   └── no_event
    │       └── admin_DAILY_82CAE57B_20250512003000_20250512_050856.docx
    ├── DAILY_82CAE57B_20250513003000
    ├── DAILY_82CAE57B_20250514003000
    ├── DAILY_C7F05D90_20250510003000
    │   └── no_event
    │       └── px01.baocao_DAILY_C7F05D90_20250510003000_20250510_083550.docx
    ├── DAILY_C7F05D90_20250511003000
    ├── DAILY_C7F05D90_20250512003000
    ├── DAILY_C7F05D90_20250513003000
    ├── DAILY_C7F05D90_20250514003000
    ├── DAILY_C98B00B2_20250509003000
    │   └── no_event
    │       └── cahoanlao.baocao_DAILY_C98B00B2_20250509003000_20250509_051141.docx
    ├── DAILY_C98B00B2_20250510003000
    ├── DAILY_C98B00B2_20250511003000
    ├── DAILY_C98B00B2_20250512003000
    ├── DAILY_C98B00B2_20250513003000
    ├── DAILY_C98B00B2_20250514003000
    ├── DAILY_D8702E96_20250507003000
    │   ├── has_event
    │   └── no_event
    │       └── px01.baocao_DAILY_D8702E96_20250507003000_20250507_100448.docx
    ├── DAILY_D8702E96_20250508003000
    ├── DAILY_D8702E96_20250509003000
    └── MONTHLY_F695F951_20250510003000
        └── px01.baocao_MONTHLY_F695F951_20250510003000_20250510_161235.docx