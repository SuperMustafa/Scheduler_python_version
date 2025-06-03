from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/schedules", tags=["Schedules"])


# ───── CREATE ─────
@router.post("/", response_model=schemas.ScheduleDto) # here we control the shape of returnd json of schedule
def create_schedule(schedule: schemas.CreateScheduleDto, db: Session = Depends(get_db)): # here we control the shape of json we send to database at the request
    db_schedule = models.Schedule(
        tenant_id=schedule.tenant_id,
        customer_id=schedule.customer_id,
        name=schedule.name,
        description=schedule.description,
        active=schedule.active,
        time=schedule.time,
        building=schedule.building,
        time_zone=schedule.time_zone,
        days=schedule.days
    )

    for ds in schedule.device_settings:
        device_setting = models.DeviceSetting(
            name=ds.name,
            device_id=ds.device_id
        )
        for attr in ds.attributes:
            device_setting.attributes.append(models.DeviceAttribute(key=attr.key, value=attr.value))
        db_schedule.device_settings.append(device_setting)

    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule ## here FastAPI will convert it into JSON using the ScheduleDto response model you defined.




# ───── GET ALL ─────
@router.get("/", response_model=List[schemas.ScheduleDto])
def get_all_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()


# ───── GET BY ID ─────
@router.get("/{schedule_id}", response_model=schemas.ScheduleDto)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


# ───── DELETE ─────
@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(schedule)
    db.commit()
    return {"detail": "Schedule deleted successfully"}


# ───── FILTER BY TENANT ─────
@router.get("/by-tenant/{tenant_id}", response_model=List[schemas.ScheduleDto])
def get_schedules_by_tenant(tenant_id: str, db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).filter(models.Schedule.tenant_id == tenant_id).all()
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found for this tenant")
    return schedules


# ───── FILTER BY CUSTOMER ─────
@router.get("/by-customer/{customer_id}", response_model=List[schemas.ScheduleDto])
def get_schedules_by_customer(customer_id: str, db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).filter(models.Schedule.customer_id == customer_id).all()
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found for this customer")
    return schedules
