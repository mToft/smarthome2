#!/usr/bin/python3

"""Blink the weather forecast"""

# pylint: disable=C0103

from datetime import datetime, date, time
from smarthome import weather
from smarthome import lights
from smarthome import settings

starttime = time(7, 0, 0)
endtime = time(17, 0, 0)
start = datetime.combine(date.today(), starttime)
end = datetime.combine(date.today(), endtime)

if weather.precipitation_in_interval(start, end):
    lights.blink_group(bridge_ip = settings.HUE_IP, group_names = ['Spisebord', 'Køkken'], hue = 43751, brightness = 190, fade_time = 2, blink_duration = 0.4, only_blink_if_on = False)

if weather.wind_above_threshold_in_interval(start, end, 6):
    lights.blink_group(bridge_ip = settings.HUE_IP, group_names = ['Spisebord', 'Køkken'], hue = 65285, brightness = 254, fade_time = 2, blink_duration = 0.4, only_blink_if_on = False)

