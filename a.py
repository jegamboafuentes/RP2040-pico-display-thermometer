# This is a.py - now simplified to only fetch weather

import time
import urequests

# Helper function can stay here
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def show_outside_temp(display):
    # --- Define colors ---
    BLACK = display.create_pen(0, 0, 0)
    CYAN = display.create_pen(0, 255, 255)
    WHITE = display.create_pen(255, 255, 255)
    RED = display.create_pen(255, 0, 0)

    # --- Show "Fetching..." message ---
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.set_font("bitmap8")
    display.text("Fetching Weather...", 15, 50, scale=2)
    display.update()

    # The URL for the wttr.in API
    URL = "http://wttr.in/Boston?format=j1"
    
    try:
        # Make the request to the API, assuming we are already connected to Wi-Fi
        response = urequests.request("GET", URL)
        data = response.json()
        
        # Get the temperature and city name from the data
        temp_c = float(data['current_condition'][0]['temp_C'])
        temp_f = float(data['current_condition'][0]['temp_F'])
        city = data['nearest_area'][0]['areaName'][0]['value']
        
        # --- Display the Live Weather ---
        display.set_pen(BLACK)
        display.clear()
        
        display.set_pen(CYAN)
        display.text(f"Outside ({city})", 15, 25, scale=2)
        
        display.set_pen(WHITE)
        celsius_text = f"{temp_c:.1f}°C"
        display.text(celsius_text, 15, 60, scale=4)
        
        fahrenheit_text = f"{temp_f:.1f}°F"
        display.text(fahrenheit_text, 15, 95, scale=4)

    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(RED)
        display.text("API Error!", 15, 80, scale=3)

    # Update the display and wait 5 seconds before returning
    display.update()
    time.sleep(5)
