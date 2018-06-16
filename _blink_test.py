#!/usr/bin/python3

"""Blink the weather forecast"""

# pylint: disable=C0103

from smarthome import lights
from smarthome import settings

lights.blink_group(bridge_ip = settings.HUE_IP, group_names = ['Spisebord', 'Køkken'], hue = 43751, brightness = 190, fade_time = 2, blink_duration = 0.4, only_blink_if_on = False)
lights.blink_group(bridge_ip = settings.HUE_IP, group_names = ['Spisebord', 'Køkken'], hue = 65285, brightness = 254, fade_time = 2, blink_duration = 0.4, only_blink_if_on = False)
