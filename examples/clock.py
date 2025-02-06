import time
from rpi_ws281x_disk.rpi_ws281x_disk import PixelDisk


# LED strip configuration:
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # 0 or 1. pin 18 is on channel 0.



def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

HOUR_COLOR = (0,45,109)
MINUTE_COLOR = (100, 10, 24)
SECOND_COLOR = hex_to_rgb("#8F00FF")
BACKGROUND = (0,1,5)



def clock(disk):
    print("Starting Clock")
    disk.fill(BACKGROUND)
    sec_pix = []
    min_pix = []
    hour_pix = []

    while True:
        disk.set_pixels(sec_pix, BACKGROUND)
        disk.set_pixels(min_pix, BACKGROUND)
        disk.set_pixels(hour_pix, BACKGROUND)

        current_time = time.localtime()

        #adj = gyro.get_angle(self.gyro) + 45
        #adj = 5 * round(adj/5)
        adj = 0
        sec_angle = current_time.tm_sec * 6
        min_angle = current_time.tm_min * 6
        hour_angle = (current_time.tm_hour % 12) * 30

        sec_pix = disk.get_chain("8", sec_angle, 5, adj)
        min_pix = disk.get_chain("5", min_angle, 3, adj)
        hour_pix = disk.get_chain("3", hour_angle, 1, adj)

        disk.set_pixels(sec_pix, SECOND_COLOR)
        disk.set_pixels(min_pix, MINUTE_COLOR)
        disk.set_pixels(hour_pix, HOUR_COLOR)

        disk.show()
        time.sleep(.2)

disk = PixelDisk(LED_PIN, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL)

clock(disk)
