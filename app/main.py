import asyncio
import platform
import logging
from datetime import datetime
from fastapi import FastAPI        
from sqlalchemy.ext.declarative import declarative_base      
from sqlalchemy.orm import DeclarativeMeta   
from app.routers import schedule
from app.db.database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from app.services.executor_service import ExecutorService
from app.models import models
import httpx
import pytz

app = FastAPI()
Base: DeclarativeMeta = declarative_base()


def get_egypt_now():
    
    """Return current time in Egypt with OS-compatible timezone handling."""
    if platform.system() == "Windows":
        tz = pytz.timezone("Egypt")  # Make sure this is installed in pytz
    else:
        tz = pytz.timezone("Africa/Cairo")
    return datetime.now(tz)


async def background_executor_task():
    logger = logging.getLogger("executor")
    logging.basicConfig(level=logging.INFO)

    async with httpx.AsyncClient() as http_client:
        executor = ExecutorService(http_client=http_client, logger=logger)
        logger.info("Schedule Execution Service started.")

        while True:
            try:
                db: Session = SessionLocal()
                now = get_egypt_now()
                current_day = now.strftime("%A")

                logger.info(f"Current Egypt time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

                schedules = db.query(models.Schedule).all()
                logger.info(f"Loaded {len(schedules)} schedules from database.")

                for schedule in schedules:
                    if not schedule.active:
                        logger.info(f"⏭ Skipping inactive schedule: {schedule.name}")
                        continue

                    schedule_time = schedule.time
                    schedule_days = schedule.days or []
                    logger.info(f"Checking schedule: {schedule.name} for day {current_day} at {schedule_time.hour:02}:{schedule_time.minute:02}")

                    if current_day.lower() not in [d.lower().strip() for d in schedule_days]:
                        logger.info(f"Schedule '{schedule.name}' not valid for today ({current_day})")
                        continue

                    if now.hour == schedule_time.hour and now.minute == schedule_time.minute:
                        logger.info(f" Executing schedule: {schedule.name}")
                        await executor.execute_schedule(schedule)
                    else:
                        logger.info(f"Not yet time for schedule '{schedule.name}' (Now: {now:%H:%M}, Scheduled: {schedule_time.hour:02}:{schedule_time.minute:02})")

            except Exception as e:
                logger.error("An error occurred in ScheduleExecutionService loop.", exc_info=e)

            finally:
                db.close()

            await asyncio.sleep(30)

# Startup event
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(background_executor_task())

app.include_router(schedule.router)
