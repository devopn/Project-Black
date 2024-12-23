from .command_handler import router as command_router
from .weather_handler import router as weather_router
handlers = [
    command_router,
    weather_router
]