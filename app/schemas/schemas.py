from typing import List, Optional
from datetime import time
from pydantic import BaseModel


# ==================================================================== DeviceAttribute Schemas ==============================================================

class DeviceAttributeDto(BaseModel):
    key: str
    value: str

    pass
    class Config:
        orm_mode = True

# ==================================================================== DeviceAttribute Schemas ==============================================================









# ==================================================================== DeviceSetting Schemas ================================================================

class DeviceSettingDto(BaseModel):
    name: str
    device_id: str
    attributes: List[DeviceAttributeDto]


    class Config:
        orm_mode = True
# ==================================================================== DeviceSetting Schemas ================================================================






# ==================================================================== Schedule Schemas =====================================================================

class ScheduleDto(BaseModel):
    id:int
    tenant_id: str
    customer_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    active: bool
    time: time
    building: str
    time_zone: str
    days: List[str]
    device_settings: List[DeviceSettingDto]


class CreateScheduleDto(BaseModel):
    tenant_id: str
    customer_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    active: bool
    time: time
    building: str
    time_zone: str
    days: List[str]
    device_settings: List[DeviceSettingDto]


class UpdateScheduleDto(ScheduleDto):
   

    class Config:
        orm_mode = True
# ==================================================================== Schedule Schemas =====================================================================
