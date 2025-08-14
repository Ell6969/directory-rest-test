from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.activity.models import Activity, OrganizationActivity
from src.building.models import Building
from src.constant import ModelFieldConst
from src.database import Base
from src.enums import ContactTypeEnum


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(ModelFieldConst.ORG_NAME), index=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    building: Mapped["Building"] = relationship(back_populates="organizations")  # noqa: F821
    contacts: Mapped[List["OrganizationContact"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    activities: Mapped[List["Activity"]] = relationship(  # noqa: F821
        secondary=OrganizationActivity.__table__, back_populates="organizations"
    )

    __table_args__ = (
        Index("ix_organization_name_trgm", "name", postgresql_using="gin", postgresql_ops={"name": "gin_trgm_ops"}),
    )


class OrganizationContact(Base):
    __tablename__ = "organization_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    contact_type: Mapped[ContactTypeEnum] = mapped_column(ENUM(ContactTypeEnum, name="contact_type_enum"))
    value: Mapped[str] = mapped_column(String(ModelFieldConst.CONTACT_VAL))
    description: Mapped[Optional[str]] = mapped_column()

    organization: Mapped["Organization"] = relationship(back_populates="contacts")
