from ..models.audit_log import AuditLog

async def log_action(db, user_id: int, action: str, model: str, model_id: int | None = None, details: str = ""):
    log = AuditLog(
        user_id=user_id,
        action=action,
        model=model,
        model_id=model_id,
        details=details
    )
    db.add(log)
    await db.commit()
