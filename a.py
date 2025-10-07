# This is file a.py

import time

def show_outside_temp(display, temp_c, temp_f):
    # Define colors needed for this screen
    BLACK = display.create_pen(0, 0, 0)
    CYAN = display.create_pen(0, 255, 255)
    WHITE = display.create_pen(255, 255, 255)

    # Clear the screen
    display.set_pen(BLACK)
    display.clear()
    
    # Display the "Outside Temperature" screen
    display.set_pen(CYAN)
    display.set_font("bitmap8") # Use the same font as the main screen
    display.text("Outside Temp (Revere, MA)", 15, 25, scale=2)
    
    display.set_pen(WHITE)
    celsius_text = f"{temp_c}°C"
    display.text(celsius_text, 15, 60, scale=4)
    
    fahrenheit_text = f"{temp_f}°F"
    display.text(fahrenheit_text, 15, 95, scale=4)
    
    display.update()
    time.sleep(5)  # Wait for 5 seconds
