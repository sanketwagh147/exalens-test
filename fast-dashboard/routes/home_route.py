from fastapi import APIRouter, Request
from config import readings_collection
from fastapi.templating import Jinja2Templates
from utils import format_timestamp, get_sensor_types


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    readings_per_page = 50
    query = {}
    page = 1

    total_readings = await readings_collection.count_documents(query)
    print(total_readings, "total reading")
    total_pages = int(total_readings / readings_per_page)
    skip_count = (page - 1) * readings_per_page
    temperature_readings = (
        await readings_collection.find(query)
        .sort("_id", -1)
        .skip(skip_count)
        .limit(readings_per_page)
        .to_list(None)
    )
    distinct_sensor_ids = await readings_collection.distinct("sensor_id")

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
            "sensor_type": "All sensor types",
            "sensor_types": await get_sensor_types(readings_collection),
            "sensor_ids": distinct_sensor_ids,
            "current_page": page,
        },
    )
