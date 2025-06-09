from services.config import settings

if settings.USE_GPIO:
    from .gpio_rpi import GPIORpiController as GPIOController
else:
    from .gpio_mock import GPIOMockController as GPIOController

gpio = GPIOController()