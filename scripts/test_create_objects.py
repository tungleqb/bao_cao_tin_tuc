# backend/test/test_create_objects.py

import asyncio
from datetime import datetime, time

from backend.app.database import Base, engine, SessionLocal
from backend.app.models.user import User
from backend.app.models.report_type import ReportType
from backend.app.models.period import Period
from backend.app.models.report import Report
from backend.app.models.audit_log import AuditLog

async def test_create_objects():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        # Test User
        user = User(
            username="testuser",
            hashed_password="hashedpassword",
            name="Test Chi Nhanh",
            time_created=datetime.now(),
            avatar="avatar.png",
            level="CAPPHONG",
            is_admin=False
        )
        session.add(user)

        # Test ReportType
        report_type = ReportType(
            ID="BCNGAY",
            DateCreated=datetime.now(),
            Name="Báo cáo ngày",
            Period_ID="DAILY",
            ActiveAt=time(0, 0, 0),
            DeactiveAt=time(23, 59, 59),
            StartAt=time(12, 0, 0),
            EndAt=time(14, 0, 0),
            From=time(0, 0, 0),
            To=time(23, 59, 59)
        )
        session.add(report_type)

        # Test Period
        period = Period(
            TYPE="BCNGAY",
            ID="BCNGAY_20250427",
            Name="Báo cáo ngày 27/4/2025",
            ActiveAt=datetime.now(),
            DeactiveAt=datetime.now(),
            StartAt=datetime.now(),
            EndAt=datetime.now(),
            FromAt=datetime.now(),
            ToAt=datetime.now(),
            Killer="Auto",
            Status="Active",
            FolderPath="/static/reports/BCNGAY_20250427"
        )
        session.add(period)

        # Test Report
        report = Report(
            ID="testuser_BCNGAY_20250427_120000",
            Sender="testuser",
            SendID=1,
            PeriodID="BCNGAY_20250427",
            ReportTypeID="BCNGAY",
            ReportPeriodName="Báo cáo ngày 27/4/2025",
            Blake3sum="dummychecksum",
            FilePath="/static/reports/file1.pdf",
            FileName="testchinhanh_BCNGAY",
            OriFileName="file1.pdf",
            FileSize=1024,
            SentAt=datetime.now(),
            Comment="No comment",
            HasEvent=False,
            LateSeconds=0
        )
        session.add(report)

        # Test AuditLog
        audit_log = AuditLog(
            user_id=1,
            action="CREATE",
            model="Report",
            model_id=1,
            details="Created report",
            timestamp=datetime.now()
        )
        session.add(audit_log)

        await session.commit()
        print("✅ Successfully created all test objects.")

if __name__ == "__main__":
    asyncio.run(test_create_objects())
