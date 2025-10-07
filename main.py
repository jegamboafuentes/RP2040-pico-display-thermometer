# This is main.py - with "Room Temperature" label added

import machine
import time
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import a

# --- User Settings ---
LED_BRIGHTNESS = 0.01
HOT_THRESHOLD_C = 25.0

# --- Hardware Setup ---
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)
sensor_temp = machine.ADC(4)
led = RGBLED(6, 7, 8)
button_a = Button(12)

display.set_backlight(0.5)
WIDTH, HEIGHT = display.get_bounds()
display.set_font("bitmap8")

# --- Pen (Color) Setup ---
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
GREY = display.create_pen(120, 120, 120)
LIQUID_COLOUR = display.create_pen(0, 0, 255)

# --- Thermometer Constants ---
TEMP_MIN = 15.0
TEMP_MAX = 30.0
T_X = WIDTH - 40
T_Y = 25
T_WIDTH = 25
T_HEIGHT = HEIGHT - 55
T_BULB_RADIUS = 12

OUTSIDE_TEMP_C = 15.5

# --- Helper Functions ---
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def temperature_to_color_rgb(temp):
    if temp >= HOT_THRESHOLD_C:
        return 255, 0, 0
    p = map_value(temp, TEMP_MIN, HOT_THRESHOLD_C, 0.0, 1.0)
    p = max(0.0, min(1.0, p))
    r = 0
    g = int(map_value(p, 0.0, 1.0, 0, 255))
    b = int(map_value(p, 0.0, 1.0, 255, 0))
    return r, g, b

# --- Main Loop ---
while True:
    if button_a.read():
        outside_f = celsius_to_fahrenheit(OUTSIDE_TEMP_C)
        a.show_outside_temp(display, OUTSIDE_TEMP_C, outside_f)
    else:
        reading = sensor_temp.read_u16() * (3.3 / 65535)
        temp_c = 27 - (reading - 0.706) / 0.001721
        temp_f = celsius_to_fahrenheit(temp_c)
        
        display.set_pen(BLACK)
        display.clear()

        r, g, b = temperature_to_color_rgb(temp_c)
        display.update_pen(LIQUID_COLOUR, r, g, b)
        led.set_rgb(int(r * LED_BRIGHTNESS), int(g * LED_BRIGHTNESS), int(b * LED_BRIGHTNESS))

        liquid_y_end = T_Y + T_HEIGHT
        liquid_y_start = map_value(temp_c, TEMP_MIN, TEMP_MAX, liquid_y_end, T_Y)
        liquid_y_start = max(T_Y, min(liquid_y_start, liquid_y_end))

        display.set_pen(GREY)
        display.circle(T_X + T_WIDTH // 2, T_Y + T_HEIGHT, T_BULB_RADIUS)
        display.rectangle(T_X, T_Y, T_WIDTH, T_HEIGHT)

        display.set_pen(LIQUID_COLOUR)
        display.circle(T_X + T_WIDTH // 2, T_Y + T_HEIGHT, T_BULB_RADIUS - 3)
        if liquid_y_start < (T_Y + T_HEIGHT):
          display.rectangle(T_X + 3, int(liquid_y_start), T_WIDTH - 6, int(T_Y + T_HEIGHT - liquid_y_start))
        
        display.set_pen(WHITE)
        celsius_text = f"{temp_c:.1f}°C"
        display.text(celsius_text, 15, 25, scale=4)
        
        display.set_pen(GREY)
        fahrenheit_text = f"{temp_f:.1f}°F"
        display.text(fahrenheit_text, 15, 65, scale=4)
        
        # --- NEW LINE ADDED HERE ---
        display.text("Room Temp", 15, 105, scale=2)
        
        display.update()

    time.sleep(0.1)
