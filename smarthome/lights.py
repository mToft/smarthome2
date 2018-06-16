"""Blink hue"""

import time as sleeptimer
from phue import Bridge

def blink_group(bridge_ip, group_names, hue, brightness = 254, fade_time = 2, blink_duration = 0.4,
          only_blink_if_on = False):
    """Blinks all lamps in the specified group in specified color"""

    bridge = Bridge(bridge_ip)

    groups_to_blink = []

    groups = bridge.get_group()
    for group in groups:
        for target_group in group_names:
            if groups[group]['name'] == target_group:
                groups_to_blink.append(groups[group]['lights'])

    lights_to_blink = [val for sublist in groups_to_blink for val in sublist]
    lights_to_blink_on = []

    for light in lights_to_blink:
        if only_blink_if_on:
            if bridge.get_light(int(light), 'on'):
                lights_to_blink_on.append(int(light))
        else:
            lights_to_blink_on.append(int(light))

    if len(lights_to_blink_on) > 0:
        # Store lamp states, before changing them
        old_states = []
        for light in lights_to_blink_on:
            old_states.append(bridge.get_light(light)['state'])

        # Now set lights to the blink color
        command = {'on' : True, 'transitiontime' : fade_time, 'bri' : brightness, 'hue' : hue}
        bridge.set_light(lights_to_blink_on, command)

        # Sleep some time
        sleeptimer.sleep(blink_duration)

        def restore(lights, oldstates):
            """Restores light to old state"""
            i = 0
            for light in lights:
                colormode = oldstates[i]['colormode']
                if colormode == "hs":
                    colormode = "hue"
                command = {}
                if oldstates[i]['on']:
                    command = {'transitiontime' : fade_time,
                               'bri' : oldstates[i]['bri'],
                               oldstates[i]['colormode'] : oldstates[i][colormode],
                               'on' : oldstates[i]['on']}
                else:
                    command = {'transitiontime' : fade_time,
                               'on' : oldstates[i]['on']}
                bridge.set_light(light, command)
                i = i+1

        restore(lights_to_blink_on, old_states)
        sleeptimer.sleep(blink_duration)
        # Make sure that the command went through:
        restore(lights_to_blink_on, old_states)

