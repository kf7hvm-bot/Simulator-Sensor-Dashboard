import reflex as rx
from app.state import SensorState, SENSOR_IDS

SENSOR_COLORS = [
    "#6200EA",
    "#03DAC6",
    "#FF6F00",
    "#FFC107",
    "#2962FF",
    "#D50000",
    "#00BFA5",
    "#651FFF",
    "#C51162",
    "#00C853",
]


def line_chart() -> rx.Component:
    """A line chart to visualize sensor water levels over time."""
    return rx.el.div(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", opacity=0.5),
            rx.recharts.x_axis(
                data_key="name", angle=-30, text_anchor="end", height=70, stroke="#333"
            ),
            rx.recharts.y_axis(
                label={
                    "value": "Water Level (m)",
                    "angle": -90,
                    "position": "insideLeft",
                    "style": {"textAnchor": "middle", "fill": "#333"},
                },
                stroke="#333",
            ),
            rx.recharts.tooltip(
                content_style={
                    "backgroundColor": "#FFFFFF",
                    "border": "1px solid #DDD",
                },
                label_style={"fontWeight": "bold"},
            ),
            rx.recharts.legend(vertical_align="top", height=40),
            rx.foreach(
                SENSOR_IDS,
                lambda sensor_id, index: rx.recharts.line(
                    data_key=sensor_id,
                    stroke=rx.Var.create(SENSOR_COLORS)[index % len(SENSOR_COLORS)],
                    type="monotone",
                    dot=False,
                    stroke_width=2,
                ),
            ),
            data=SensorState.chart_data,
            width="100%",
            height=450,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 30},
        ),
        class_name="w-full h-[450px] bg-white rounded-2xl p-4 shadow-[0px_4px_8px_rgba(0,0,0,0.15)] border border-gray-100",
    )