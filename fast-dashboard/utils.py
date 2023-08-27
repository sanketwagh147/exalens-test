from datetime import datetime
import json
import pytz

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        for key, value in dct.items():
            if isinstance(value, str):
                try:
                    dct[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
        return dct


async def get_sensor_types(collection):
    return await collection.distinct("sensor_type")


async def format_timestamp(timestamp):
    utc_time = timestamp.replace(tzinfo=pytz.UTC)
    ist_time = utc_time.astimezone(pytz.timezone("Asia/Kolkata"))
    formatted_time = ist_time.strftime("%b %d, %Y %I:%M %p %Z")
    return formatted_time