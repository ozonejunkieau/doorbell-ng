from time import sleep
from lifxlan import CYAN, PINK, BLUE, COLD_WHITE, RED, GREEN, Light

def blink_light(mac, ip):
    """
    Run a rapid blink on a light to provide a notification.
    """
    light = Light(mac, ip)

    colors = light.get_color()
    power_state = light.get_power()

    repeats = 3
    delay = 0.25
    light.set_power(1)
    for _ in range(repeats):
        
        light.set_color(RED, rapid=True)
        sleep(delay)
        light.set_color(GREEN, rapid=True)
        sleep(delay)
        light.set_color(BLUE, rapid=True)
        sleep(delay)
        if power_state:
            light.set_color(colors)
        else:
            light.set_color(COLD_WHITE)
        sleep(1)
    light.set_color(colors)
    light.set_power(power_state)
