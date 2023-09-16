from fastapi import FastAPI
import datetime
from zoneinfo import ZoneInfo
import jpholiday

app = FastAPI()
TIME_ZONE_JST = ZoneInfo("Asia/Tokyo")

FROM_CHITOSE_STATION_WEEKDAYS = ["06:30", "06:50", "07:30", "07:50", "08:20", "08:50", "09:50", "10:20", "10:50", "11:50", "12:20", "12:50", "13:20", "13:50", "14:20", "14:50", "15:20", "15:50", "16:50", "17:30", "17:50", "18:50", "19:50", "21:10", "21:55"]
FROM_CHITOSE_STATION_HOLIDAYS = ["07:10", "07:50", "08:30", "08:50", "09:20", "09:50", "10:50", "11:20", "11:50", "12:50", "14:20", "15:20", "15:50", "16:50", "17:50", "18:50", "19:50", "21:10", "21:55"]
FROM_FUKUZUMI_WEEKDAYS = ["05:45", "06:05", "06:45", "07:00", "07:20", "07:40", "08:25", "08:45", "09:15", "09:45", "10:45", "11:15", "11:45", "12:15", "12:45", "13:15", "13:45", "14:15", "14:45", "15:45", "16:45", "17:45", "19:05", "20:25", "21:05"]
FROM_FUKUZUMI_HOLIDAYS = ["06:25", "07:05", "07:25", "07:45", "08:05", "08:45", "09:15", "09:45", "10:15", "10:45", "11:15", "11:45", "12:15", "13:15", "14:15", "14:45", "15:45", "16:45", "17:45", "19:05", "20:25", "21:05"]

def is_holiday(now: datetime) -> bool:
    return jpholiday.is_holiday(now)

def get_buses(bus_list: list, now: datetime) -> list:
    return_bus_list = []
    now_hour = int(now.hour)
    for bus in bus_list:
        if now_hour <= int(bus[:2]) <= now_hour + 2:
            return_bus_list.append(bus)
    return return_bus_list

@app.get("/fukuzumi")
async def fukuzumi():
    now = datetime.datetime.now(TIME_ZONE_JST)
    if is_holiday(now):
        chitose_bus_list = get_buses(FROM_CHITOSE_STATION_HOLIDAYS, now)
        fukuzumi_bus_list = get_buses(FROM_CHITOSE_STATION_HOLIDAYS, now)
    else:
        chitose_bus_list = get_buses(FROM_CHITOSE_STATION_WEEKDAYS, now)
        fukuzumi_bus_list = get_buses(FROM_FUKUZUMI_WEEKDAYS, now)
    
    return {
        "from_chitose": chitose_bus_list,
        "from_fkuzumi": fukuzumi_bus_list,
    }