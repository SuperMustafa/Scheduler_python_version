from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, Table
from sqlalchemy.orm import relationship,Mapped
from sqlalchemy.types import JSON
from app.db.database import Base
from typing import List
from datetime import time




#======================================================================Schedule entity==========================================================================

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    thingsboard_url = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    tenant_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    time = Column(Time, nullable=False)
    building = Column(String, nullable=False)
    time_zone = Column(String, nullable=False)

    days = Column(JSON, nullable=False, default=[])

    device_settings:Mapped[List["DeviceSetting"]] = relationship("DeviceSetting", back_populates="schedule", cascade="all, delete-orphan")

#======================================================================Schedule entity==========================================================================











#======================================================================DeviceSetting entity==========================================================================

class DeviceSetting(Base):
    __tablename__ = "device_settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    device_id = Column(String, nullable=False)

    schedule_id = Column(Integer, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    schedule = relationship("Schedule", back_populates="device_settings")

    attributes: Mapped[List["DeviceAttribute"]]  = relationship("DeviceAttribute", back_populates="device_setting", cascade="all, delete-orphan")

#======================================================================DeviceSetting entity==========================================================================









#======================================================================DeviceAttributes entity==========================================================================
class DeviceAttribute(Base):
    __tablename__ = "device_attributes"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    device_setting_id = Column(Integer, ForeignKey("device_settings.id", ondelete="CASCADE"), nullable=False)
    device_setting: Mapped["DeviceSetting"] = relationship("DeviceSetting", back_populates="attributes")


#======================================================================DeviceAttributes entity==========================================================================
