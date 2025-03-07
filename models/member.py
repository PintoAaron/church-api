from datetime import date, datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import ForeignKey, UniqueConstraint,insert
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from models import Base


class MemberMapper(Base):
    picture: Mapped[Optional[str]]
    fullname: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    dob: Mapped[Optional[date]]
    occupation: Mapped[Optional[str]]
    emergency_contact_name: Mapped[Optional[str]]
    emergency_contact_phone: Mapped[Optional[str]]
    marital_status: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    number_of_children: Mapped[Optional[int]]
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("department.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    department: Mapped["DepartmentMapper"] = relationship(back_populates="member", passive_deletes="all")
    user: Mapped["UserMapper"] = relationship(back_populates="member")
    contribution: Mapped["ContributionMapper"] = relationship(back_populates="member")
    __table_args__ = (UniqueConstraint("email", "fullname", name="unique_member_email_fullname"),)

    @classmethod
    def get_by_email(cls, email: EmailStr, db: Session):
        return db.query(cls).filter_by(email=email).first()

    @classmethod
    def validate_by_email(cls, email: EmailStr, db: Session):
        user = cls.get_by_email(email, db)
        return True if user else False

    @classmethod
    def create_from_file(cls, session: Session, data: list):
        members = session.execute(insert(cls), data).all()
        session.commit()
        return members
