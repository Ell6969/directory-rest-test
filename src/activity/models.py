from typing import List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constant import ModelFieldConst
from src.database import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (CheckConstraint("level >= 1 AND level <= 3", name="level_range"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(ModelFieldConst.ACT_NAME), index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
    )
    level: Mapped[int] = mapped_column()

    parent: Mapped[Optional["Activity"]] = relationship("Activity", remote_side=[id], back_populates="children")
    children: Mapped[List["Activity"]] = relationship("Activity", back_populates="parent", cascade="all, delete-orphan")
    organizations: Mapped[List["Organization"]] = relationship(  # noqa: F821
        secondary="organization_activities", back_populates="activities"
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (UniqueConstraint("organization_id", "activity_id", name="uix_org_activity"),)
