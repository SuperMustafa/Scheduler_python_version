# app/main.py
from fastapi import FastAPI
# import asyncio
# import logging
# from services.schedule_executor import execute_schedules_periodically
from app.routers import schedule
from app.db.database import engine, Base

app = FastAPI()

# logging.basicConfig(level=logging.INFO)



# @app.on_event("startup")
# async def start_background_tasks():
#     asyncio.create_task(execute_schedules_periodically())

# app.include_router(schedule.router)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

       # Start background schedule executor
    # asyncio.create_task(execute_schedules_periodically())


app.include_router(schedule.router)


# @app.get("/")
# def root():
#     return {"message": "MyScheduler Python version running!"}
