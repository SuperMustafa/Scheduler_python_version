from fastapi import APIRouter, Depends, HTTPException,Path
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
        thingsboard_url=schedule.thingsboard_url,
        username=schedule.username,
        password=schedule.password,
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






@router.put("/{schedule_id}", response_model=schemas.ScheduleDto)
def update_schedule(schedule_id: int,updated_schedule: schemas.CreateScheduleDto,db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    # Update main schedule fields
    db_schedule.name = updated_schedule.name
    db_schedule.description = updated_schedule.description
    db_schedule.active = updated_schedule.active
    db_schedule.time = updated_schedule.time
    db_schedule.building = updated_schedule.building
    db_schedule.time_zone = updated_schedule.time_zone
    db_schedule.days = updated_schedule.days
    db_schedule.tenant_id = updated_schedule.tenant_id
    db_schedule.customer_id = updated_schedule.customer_id
    

    # Clear existing device settings & attributes
    db_schedule.device_settings.clear()

    # Add new device settings and attributes
    for ds in updated_schedule.device_settings:
        device_setting = models.DeviceSetting(
            name=ds.name,
            device_id=ds.device_id,
            schedule_id=schedule_id
        )
        for attr in ds.attributes:
            device_setting.attributes.append(models.DeviceAttribute(key=attr.key, value=attr.value))
        db_schedule.device_settings.append(device_setting)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule









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




