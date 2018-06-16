"""Controls the water pumps"""

from enum import Enum
from time import sleep
from gpiozero import OutputDevice as pump

PUMP_A = pump(7)
PUMP_B = pump(8)

def water(pump, duration):
    """Turns on the water in the duration"""
    return 0

def test_pump():
    PUMP_A.on()
    sleep(1)
    PUMP_A.off()
