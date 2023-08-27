from fastapi import APIRouter, Request
from datetime import datetime
import pytz
from config import redis, readings_collection
from utils import DateTimeDecoder, get_sensor_types, DateTimeEncoder, format_timestamp
import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/filter")
async def filter(
    request: Request,
    sensor_id: str = "",
    page: int = 1,
    sensor_type: str = "",
    start_date: str = "",
    end_date: str = "",
    last: str = "",
):
    readings_per_page = 50
    query = {}
    skip_count = (page - 1) * readings_per_page

    if sensor_id:
        query["sensor_id"] = sensor_id
    if sensor_type:
        query["sensor_type"] = sensor_type
    if start_date:
        start_date_obj = datetime.fromisoformat(start_date)
        start_date_obj = start_date_obj.replace(tzinfo=pytz.UTC)
        query["timestamp"] = {"$gte": start_date_obj}
    if end_date:
        end_date_obj = datetime.fromisoformat(end_date)
        end_date_obj = end_date_obj.replace(tzinfo=pytz.UTC)
        if "timestamp" in query:
            query["timestamp"]["$lte"] = end_date_obj
        else:
            query["timestamp"] = {"$lte": end_date_obj}

    # cache yesterdays result

    #  TODO:  improve this
    if last == "Yesterday":
        print("set cached lst 1 day")

        if redis.get("Yesterday"):
            print("getting cached")

            total_readings = redis.get("Yesterday")
            total_readings = int(total_readings) if total_readings else 0
            sensor_readings = redis.get("Yesterday_readings")

            sensor_readings = json.loads(sensor_readings, cls=DateTimeDecoder) if sensor_readings else []
            
            
        else:
            print("setting cache")
            total_readings = await readings_collection.count_documents(query)
            redis.set("Yesterday", total_readings)
            sensor_readings = (
                await readings_collection.find(query, projection={"_id": 0})
                .sort("_id", -1)
                .skip(skip_count)
                .limit(readings_per_page)
                .to_list(None)
            )
            print(sensor_readings, "Sensor readings")
            redis.set("Yesterday", int(total_readings))
            redis.set(
                "Yesterday_readings", json.dumps(sensor_readings, cls=DateTimeEncoder)
            )
    else:
        sensor_readings = (
            await readings_collection.find(query)
            .sort("_id", -1)
            .skip(skip_count)
            .limit(readings_per_page)
            .to_list(None)
        )
        total_readings = await readings_collection.count_documents(query)

    print(query)

    print(total_readings, "total reading")
    total_pages = int(total_readings / readings_per_page)
    skip_count = (int(page) - 1) * readings_per_page

    if sensor_readings:
        readings = [
            {**each, "timestamp": await format_timestamp(each["timestamp"])}
            for each in sensor_readings
        ]
    else:
        readings = []

    return templates.TemplateResponse(
        "content.html",
        {
            "request": request,
            "readings": readings,
            "page": page,
            "current_page": page,
            "total_pages": total_pages,
            "sensor_type": sensor_type or "All sensor types",
            "sensor_types": await get_sensor_types(readings_collection),
            "current_sensor_id": sensor_id,
        },
    )
