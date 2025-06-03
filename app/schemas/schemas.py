from typing import List, Optional
from datetime import time
from pydantic import BaseModel


# ==================================================================== DeviceAttribute Schemas ==============================================================

class DeviceAttributeDto(BaseModel):
    key: str
    value: str

# class DeviceAttributeCreate(DeviceAttributeBase): # pydantic will create here id by it self
#     pass

# class DeviceAttributeRead(DeviceAttributeBase):   # return all column info 
    # id: int
    pass
    class Config:
        orm_mode = True

# ==================================================================== DeviceAttribute Schemas ==============================================================









# ==================================================================== DeviceSetting Schemas ================================================================

class DeviceSettingDto(BaseModel):
    name: str
    device_id: str
    attributes: List[DeviceAttributeDto]

# class DeviceSettingCreate(DeviceSettingBase):
#     attributes: List[DeviceAttributeCreate]

# class DeviceSettingRead(DeviceSettingBase):
#     id: int
#     attributes: List[DeviceAttributeRead]

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

# class ScheduleCreate(ScheduleBase):
#     device_settings: List[DeviceSettingCreate]

# class ScheduleRead(ScheduleBase):
#     device_settings: List[DeviceSettingRead]

    class Config:
        orm_mode = True
# ==================================================================== Schedule Schemas =====================================================================
