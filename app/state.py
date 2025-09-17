import reflex as rx
import asyncio
from typing import TypedDict
import random
from datetime import datetime, timezone


class SensorReading(TypedDict):
    timestamp: str
    sensor_id: str
    water_level: float
    flow_rate: float
    temperature: float


INITIAL_SENSORS = 10
SENSOR_IDS = [f"SG-{i:03d}" for i in range(1, INITIAL_SENSORS + 1)]
GLOBAL_SENSOR_DATA: list[SensorReading] = []


def _generate_initial_data_global():
    """Helper to generate initial batch of sensor data for the global store."""
    if GLOBAL_SENSOR_DATA:
        return
    now = datetime.now(timezone.utc)
    initial_data = []
    for sensor_id in SENSOR_IDS:
        water_level = round(random.uniform(5.0, 15.0), 2)
        initial_data.append(
            {
                "timestamp": now.isoformat(),
                "sensor_id": sensor_id,
                "water_level": water_level,
                "flow_rate": round(random.uniform(10.0, 50.0), 2),
                "temperature": round(random.uniform(-5.0, 25.0), 2),
            }
        )
    GLOBAL_SENSOR_DATA.extend(initial_data)


async def periodic_data_generation():
    """A lifespan task that generates sensor data periodically."""
    global GLOBAL_SENSOR_DATA
    _generate_initial_data_global()
    while True:
        await asyncio.sleep(10)
        now = datetime.now(timezone.utc)
        new_readings = []
        last_levels = {
            row["sensor_id"]: row["water_level"]
            for row in GLOBAL_SENSOR_DATA[-INITIAL_SENSORS:]
        }
        for sensor_id in SENSOR_IDS:
            last_level = last_levels.get(sensor_id, random.uniform(5.0, 15.0))
            change = random.uniform(-0.5, 0.5)
            new_level = max(0, round(last_level + change, 2))
            new_reading: SensorReading = {
                "timestamp": now.isoformat(),
                "sensor_id": sensor_id,
                "water_level": new_level,
                "flow_rate": round(random.uniform(10.0, 50.0), 2),
                "temperature": round(random.uniform(-5.0, 25.0), 2),
            }
            new_readings.append(new_reading)
        GLOBAL_SENSOR_DATA = GLOBAL_SENSOR_DATA[-990:] + new_readings


class SensorState(rx.State):
    @rx.var
    def chart_data(self) -> list[dict[str, float | str]]:
        """Prepares data for the line chart, showing the last 10 readings per sensor."""
        if not GLOBAL_SENSOR_DATA:
            return []
        grouped_by_time = {}
        for reading in GLOBAL_SENSOR_DATA:
            ts = reading["timestamp"]
            if ts not in grouped_by_time:
                dt_obj = datetime.fromisoformat(ts).strftime("%H:%M:%S")
                grouped_by_time[ts] = {"name": dt_obj}
            grouped_by_time[ts][reading["sensor_id"]] = reading["water_level"]
        return list(grouped_by_time.values())[-100:]

    @rx.var
    def latest_readings(self) -> list[SensorReading]:
        """Returns the most recent reading for each sensor."""
        if not GLOBAL_SENSOR_DATA:
            return []
        return GLOBAL_SENSOR_DATA[-INITIAL_SENSORS:]