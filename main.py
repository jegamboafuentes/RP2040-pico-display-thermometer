# This is main.py - Now with Wi-Fi and all features

import machine
import time
import network
import secrets
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import a
import b
import y
import x

# --- User Settings ---
LED_BRIGHTNESS = 0.01
HOT_THRESHOLD_C = 25.0

# --- Hardware Setup ---
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)
sensor_temp = machine.ADC(4)
led = RGBLED(6, 7, 8)
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

display.set_backlight(0.7)
WIDTH, HEIGHT = display.get_bounds()
display.set_font("bitmap8")

# --- Pen (Color) Setup - ALL PENS CREATED HERE ---
pens = {}
pens["WHITE"] = display.create_pen(255, 255, 254)
pens["BLACK"] = display.create_pen(0, 0, 0)
pens["GREY"] = display.create_pen(120, 120, 120)
pens["RED"] = display.create_pen(255, 0, 0)
pens["GREEN"] = display.create_pen(0, 255, 0)
pens["BLUE"] = display.create_pen(0, 0, 255)
pens["CYAN"] = display.create_pen(0, 255, 254)
pens["MAGENTA"] = display.create_pen(255, 0, 255)
pens["YELLOW"] = display.create_pen(255, 255, 0)
pens["ORANGE"] = display.create_pen(255, 165, 0)

# --- Thermometer Constants ---
TEMP_MIN = 15.0
TEMP_MAX = 30.0
T_X = WIDTH - 40
T_Y = 25
T_WIDTH = 25
T_HEIGHT = HEIGHT - 55
T_BULB_RADIUS = 12

# --- Wi-Fi Connection at Startup ---
display.set_pen(pens["BLACK"])
display.clear()
display.set_pen(pens["WHITE"])
display.text("Connecting to Wi-Fi...", 10, 10, scale=2)
display.update()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    # --- LOG ADDED BACK ---
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    display.set_pen(pens["RED"])
    display.text("Wi-Fi Failed!", 10, 40, scale=3)
    display.update()
    time.sleep(5)
else:
    # --- LOGS ADDED BACK ---
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
    display.set_pen(pens["GREEN"])
    display.text("Connected!", 10, 40, scale=3)
    display.update()
    time.sleep(2)


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
    red, green, blue = 0, int(map_value(p, 0.0, 1.0, 0, 255)), int(map_value(p, 0.0, 1.0, 255, 0))
    return red, green, blue


# --- Main Loop ---
while True:
    if button_a.read():
        a.show_outside_temp(display, pens)
    elif button_b.read():
        b.show_eth_price(display, pens)
    elif button_x.read():
        x.show_weather_forecast(display, pens)
    elif button_y.read():
        y.show_sol_price(display, pens)
    else:
        reading = sensor_temp.read_u16() * (3.3 / 65535)
        temp_c = 27 - (reading - 0.706) / 0.001721
        temp_f = celsius_to_fahrenheit(temp_c)
        
        display.set_pen(pens["BLACK"])
        display.clear()

        red_val, green_val, blue_val = temperature_to_color_rgb(temp_c)
        display.update_pen(pens["BLUE"], red_val, green_val, blue_val)
        led.set_rgb(int(red_val * LED_BRIGHTNESS), int(green_val * LED_BRIGHTNESS), int(blue_val * LED_BRIGHTNESS))

        liquid_y_end = T_Y + T_HEIGHT
        liquid_y_start = map_value(temp_c, TEMP_MIN, TEMP_MAX, liquid_y_end, T_Y)
        liquid_y_start = max(T_Y, min(liquid_y_start, liquid_y_end))

        display.set_pen(pens["GREY"])
        display.circle(T_X + T_WIDTH // 2, T_Y + T_HEIGHT, T_BULB_RADIUS)
        display.rectangle(T_X, T_Y, T_WIDTH, T_HEIGHT)

        display.set_pen(pens["BLUE"])
        display.circle(T_X + T_WIDTH // 2, T_Y + T_HEIGHT, T_BULB_RADIUS - 3)
        if liquid_y_start < (T_Y + T_HEIGHT):
            display.rectangle(T_X + 3, int(liquid_y_start), T_WIDTH - 6, int(T_Y + T_HEIGHT - liquid_y_start))
        
        display.set_pen(pens["WHITE"])
        celsius_text = f"{temp_c:.1f}°C"
        display.text(celsius_text, 15, 25, scale=4)
        
        display.set_pen(pens["WHITE"])
        fahrenheit_text = f"{temp_f:.1f}°F"
        display.text(fahrenheit_text, 15, 65, scale=4)
        
        display.text("Room Temp", 15, 105, scale=2)
        
        display.update()

    time.sleep(0.1)
