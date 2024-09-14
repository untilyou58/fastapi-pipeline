from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import List
import random
from datetime import datetime, timedelta

app = FastAPI()


class WeatherForecast(BaseModel):
    date: str
    temperature: float
    condition: str


class TrafficInfo(BaseModel):
    date: str
    congestion_level: str
    delay_minutes: int


@app.get("/api/weather", response_model=List[WeatherForecast])
async def get_weather_forecast():
    conditions = ["晴れ", "曇り", "雨", "雪"]
    forecasts = []
    for i in range(7):  # One-week weather forecast
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        forecasts.append(
            WeatherForecast(
                date=date,
                temperature=round(random.uniform(0, 35), 1),
                condition=random.choice(conditions),
            )
        )
    return forecasts


@app.get("/api/traffic", response_model=List[TrafficInfo])
async def get_traffic_info():
    congestion_levels = ["低", "中", "高"]
    traffic_info = []
    for i in range(7):  # Traffic information for one week
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        traffic_info.append(
            TrafficInfo(
                date=date,
                congestion_level=random.choice(congestion_levels),
                delay_minutes=random.randint(0, 60),
            )
        )
    return traffic_info


class EventInfo(BaseModel):
    date: str
    event_name: str
    location: str


@app.get("/api/events", response_model=List[EventInfo])
async def get_event_info():
    events = []
    for i in range(7):  # Events for the week
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        events.append(
            EventInfo(date=date, event_name=f"イベント{i+1}", location=f"場所{i+1}")
        )
    return events


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
