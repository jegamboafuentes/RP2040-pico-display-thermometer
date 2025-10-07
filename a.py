import time
import urequests

# The function now accepts the 'pens' dictionary
def show_outside_temp(display, pens):
    # REMOVED: All create_pen calls are gone from here

    # --- Show "Fetching..." message ---
    display.set_pen(pens["BLACK"])
    display.clear()
    display.set_pen(pens["WHITE"])
    display.set_font("bitmap8")
    display.text("Fetching Weather...", 15, 50, scale=2)
    display.update()

    URL = "http://wttr.in/Boston?format=j1"
    
    try:
        response = urequests.request("GET", URL)
        data = response.json()
        
        temp_c = float(data['current_condition'][0]['temp_C'])
        temp_f = float(data['current_condition'][0]['temp_F'])
        city = data['nearest_area'][0]['areaName'][0]['value']
        
        display.set_pen(pens["BLACK"])
        display.clear()
        
        display.set_pen(pens["CYAN"]) # Use pen from dictionary
        display.text(f"Outside ({city})", 15, 25, scale=2)
        
        display.set_pen(pens["WHITE"])
        celsius_text = f"{temp_c:.1f}°C"
        display.text(celsius_text, 15, 60, scale=4)
        
        fahrenheit_text = f"{temp_f:.1f}°F"
        display.text(fahrenheit_text, 15, 95, scale=4)

    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(pens["RED"])
        display.text("API Error!", 15, 80, scale=3)

    display.update()
    time.sleep(5)
