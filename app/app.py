import reflex as rx
import reflex_enterprise as rxe
from app.state import SensorState, periodic_data_generation
from app.components.data_grid import data_grid
from app.components.line_chart import line_chart


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "waves", class_name="mr-3 text-3xl md:text-4xl text-purple-600"
                    ),
                    rx.el.h1(
                        "Stream Gauge Sensor Dashboard",
                        class_name="text-3xl md:text-4xl font-bold text-gray-800",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.p(
                    "Real-time monitoring of simulated stream gauge data.",
                    class_name="text-base text-gray-500 mt-2",
                ),
                class_name="text-center md:text-left",
            ),
            rx.el.div(line_chart(), class_name="mt-8"),
            rx.el.div(
                rx.el.h2(
                    "Latest Sensor Readings",
                    class_name="text-2xl font-semibold text-gray-700 mb-4",
                ),
                data_grid(),
                class_name="mt-8",
            ),
            class_name="container mx-auto p-4 md:p-8",
        ),
        class_name="w-full min-h-screen bg-gray-50 font-['Inter']",
        on_mount=SensorState.refresh_data,
    )


app = rxe.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
    theme=rx.theme(appearance="light", accent_color="violet"),
)
app.add_page(index, title="Sensor Dashboard")
app.register_lifespan_task(periodic_data_generation)