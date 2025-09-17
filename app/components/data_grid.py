import reflex as rx
import reflex_enterprise as rxe
from app.state import SensorState


def data_grid() -> rx.Component:
    """A grid to display the latest sensor readings."""
    return rx.el.div(
        rxe.ag_grid(
            id="sensor_grid",
            row_data=SensorState.latest_readings,
            column_defs=[
                {
                    "field": "sensor_id",
                    "headerName": "Sensor ID",
                    "filter": True,
                    "sortable": True,
                },
                {"field": "timestamp", "headerName": "Timestamp", "sortable": True},
                {"field": "water_level", "headerName": "Water Level (m)"},
                {"field": "flow_rate", "headerName": "Flow Rate (m³/s)"},
                {"field": "temperature", "headerName": "Temperature (°C)"},
            ],
            default_col_def={"flex": 1, "minWidth": 150, "resizable": True},
            row_selection="multiple",
            theme="quartz",
            width="100%",
            height="400px",
        ),
        class_name="w-full h-[400px] bg-white rounded-2xl p-1 shadow-[0px_4px_8px_rgba(0,0,0,0.15)] border border-gray-100",
    )