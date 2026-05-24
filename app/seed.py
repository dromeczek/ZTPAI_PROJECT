from sqlalchemy.orm import Session

from app.models.user_model import User
from app.core.security import hash_password


def seed_admin(db: Session):
    admin_email = "admin@test.com"

    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if existing_admin:
        return

    admin = User(
        email=admin_email,
        hashed_password=hash_password("admin123"),
        role="ADMIN"
    )

    db.add(admin)
    db.commit()