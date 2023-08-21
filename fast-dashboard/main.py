from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pytz
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

app = FastAPI()

mongo_uri = "mongodb://localhost:27017/"
client = AsyncIOMotorClient(mongo_uri)
db = client["sensor_data"]
collection = db["readings"]

templates = Jinja2Templates(directory="templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

SENSOR_TYPES = {"temperature": "Temperature", "humidity": "Humidity", "": "All"}

mongo_uri = "mongodb://localhost:27017/"
client = AsyncIOMotorClient(mongo_uri)
db = client["sensor_data"]
collection = db["readings"]

templates = Jinja2Templates(directory="templates")


async def format_timestamp(timestamp):
    utc_time = timestamp.replace(tzinfo=pytz.UTC)
    ist_time = utc_time.astimezone(pytz.timezone("Asia/Kolkata"))
    formatted_time = ist_time.strftime("%b %d, %Y %I:%M %p %Z")
    return formatted_time


@app.get("/")
async def home(request: Request):
    readings_per_page = 50
    query = {}
    page = 1

    total_readings = await collection.count_documents(query)
    print(total_readings, "total reading")
    total_pages = int(total_readings / readings_per_page)
    skip_count = (page - 1) * readings_per_page
    temperature_readings = (
        await collection.find(query)
        .sort("_id", -1)
        .skip(skip_count)
        .limit(readings_per_page)
        .to_list(None)
    )

    readings = [
        {**each, "timestamp": await format_timestamp(each["timestamp"])}
        for each in temperature_readings
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "readings": readings,
            "page": page,
            "total_pages": total_pages,
            "sensor_type": "All sensor reading",
            "sensor_types": SENSOR_TYPES,
        },
    )


@app.get("/filter")
async def filter(
    request: Request,
    sensor_id: str = "",
    page: int = 1,
    sensor_type: str = "",
    start_date: str = "",
    end_date: str = "",
):
    readings_per_page = 50
    query = {}
    print(sensor_id)
    if sensor_id:
        query["sensor_id"] = sensor_id
    if sensor_type:
        query["sensor_type"] = sensor_type
    if start_date:
        start_date_obj = datetime.fromisoformat(start_date)
        start_date_obj = start_date_obj.replace(tzinfo=pytz.UTC)
        print(start_date_obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        query["timestamp"] = {"$gte": start_date_obj}
    if end_date:
        end_date_obj = datetime.fromisoformat(end_date)
        end_date_obj = end_date_obj.replace(tzinfo=pytz.UTC)
        print(end_date_obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if "timestamp" in query:
            query["timestamp"]["$lte"] = end_date_obj
        else:
            query["timestamp"] = {"$lte": end_date_obj}
    print(query)

    total_readings = await collection.count_documents(query)
    print(total_readings, "total reading")
    total_pages = int(total_readings / readings_per_page)
    skip_count = (page - 1) * readings_per_page
    temperature_readings = (
        await collection.find(query)
        .sort("_id", -1)
        .skip(skip_count)
        .limit(readings_per_page)
        .to_list(None)
    )

    readings = [
        {**each, "timestamp": await format_timestamp(each["timestamp"])}
        for each in temperature_readings
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "readings": readings,
            "page": page,
            "total_pages": total_pages,
            "sensor_type": sensor_type or "All sensor reading",
            "sensor_types": SENSOR_TYPES,
            "current_sensor_id": sensor_id,
        },
    )
