from app.models.audit_log import AuditLog

def log_action(db, action: str, entity: str, entity_id: int | None = None):
    log = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id
    )
    db.add(log)
    db.commit()
