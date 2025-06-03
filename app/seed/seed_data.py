from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import models

def seed_database():
    db: Session = SessionLocal()

    # Clear existing data (optional, for dev only)
    db.query(models.DeviceAttribute).delete()
    db.query(models.DeviceSetting).delete()
    db.query(models.Schedule).delete()
    db.commit()

    # Sample schedule
    schedule = models.Schedule(
        tenant_id="tenant_001",
        customer_id="customer_001",
        name="Morning AC ON",
        description="Turn on all ACs at 8 AM",
        active=True,
        time="08:00:00",  # time object (HH:MM:SS)
        building="Building A",
        time_zone="Africa/Cairo",
        days=["Monday", "Tuesday", "Wednesday"]
    )

    # Device setting 1
    ds1 = models.DeviceSetting(
        name="AC Room 101",
        device_id="device_001"
    )
    ds1.attributes = [
        models.DeviceAttribute(key="power", value="on"),
        models.DeviceAttribute(key="temperature", value="24")
    ]

    # Device setting 2
    ds2 = models.DeviceSetting(
        name="AC Room 102",
        device_id="device_002"
    )
    ds2.attributes = [
        models.DeviceAttribute(key="power", value="on"),
        models.DeviceAttribute(key="mode", value="cool")
    ]

    schedule.device_settings = [ds1, ds2]

    db.add(schedule)
    db.commit()
    db.close()

    print("✅ Sample data seeded.")
