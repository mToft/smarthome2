#!/usr/bin/python3

"""Blink if temperature dips to or below 1 at night"""

# pylint: disable=C0103

from datetime import datetime, date, time, timedelta
from smarthome import weather
from smarthome import lights
from smarthome import settings

starttime = time(21, 0, 0)
endtime = time(8, 0, 0)
start = datetime.combine(date.today(), starttime)
end = datetime.combine(date.today()+timedelta(days=1), endtime)

# Blink if temperature goes <= 1 degrees C
if weather.temperature_below_threshold_in_interval(start, end, 1):
    lights.blink_groups(settings.HUE_IP, ['Spisebord', 'Køkken'], 43751, 190, 2, 0.4, False)
