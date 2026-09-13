"""
Tests for the per-role user counts on the Configuration page
(app/config/routes.py index()).

Regression: the page used a private role-label map without STUDENT and
INSTRUCTOR, so any tenant with a student or instructor got a 500
(KeyError) on /config/.
"""

import pw_hash as _pw_hash  # pyright: ignore[reportMissingImports]
from models import (  # pyright: ignore[reportMissingImports]
    Role,
    Tenant,
    TenantUser,
    User,
    db,
)


def _add_user(tid, email, role, is_active=True):
    user = User(email=email, password_hash=_pw_hash.hash("pw"), is_active=is_active)
    db.session.add(user)
    db.session.flush()
    db.session.add(TenantUser(user_id=user.id, tenant_id=tid, role=role))
    return user.id


def test_config_page_counts_every_role(app, client, captured_templates):
    with app.app_context():
        tenant = Tenant(name="Flight School")
        db.session.add(tenant)
        db.session.flush()
        admin_id = _add_user(tenant.id, "admin@school.test", Role.ADMIN)
        _add_user(tenant.id, "ip1@school.test", Role.INSTRUCTOR)
        _add_user(tenant.id, "ip2@school.test", Role.INSTRUCTOR)
        _add_user(tenant.id, "student@school.test", Role.STUDENT)
        _add_user(tenant.id, "pilot@school.test", Role.PILOT)
        _add_user(tenant.id, "gone@school.test", Role.STUDENT, is_active=False)
        db.session.commit()

    with client.session_transaction() as sess:
        sess["user_id"] = admin_id
    resp = client.get("/config/")

    assert resp.status_code == 200
    ctx = next(c for t, c in captured_templates if t.name == "config/settings.html")
    assert ctx["user_counts"] == [
        ("Admin", 1),
        ("Pilot / Renter", 1),
        ("Student", 1),
        ("Instructor", 2),
    ]
