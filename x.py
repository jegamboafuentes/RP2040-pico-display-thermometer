# This is x.py - for fetching a weather forecast

import time
import urequests

def show_weather_forecast(display):
    # --- Define colors (respecting your custom colors) ---
    BLACK = display.create_pen(0, 0, 0)
    WHITE = display.create_pen(255, 255, 254)
    RED = display.create_pen(255, 0, 0)
    ORANGE = display.create_pen(255, 165, 0)
    YELLOW = display.create_pen(255, 255, 0)

    # --- Show "Fetching..." message ---
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.set_font("bitmap8")
    display.text("Fetching Forecast...", 15, 50, scale=2)
    display.update()

    # The URL for the wttr.in API
    URL = "http://wttr.in/Boston?format=j1"

    try:
        # Make the request to the API
        response = urequests.get(URL)
        data = response.json()

        # --- Get Current Conditions ---
        current = data['current_condition'][0]
        current_desc = current['weatherDesc'][0]['value']
        current_temp_c = current['temp_C']

        # --- Get Hourly Forecast ---
        # Find the current hour to align the forecast
        now_hour = int(time.localtime()[3])
        
        # We need to find the forecast chunk that is closest to our current time
        hourly_forecasts = data['weather'][0]['hourly']
        start_index = now_hour // 3 # The API gives data in 3-hour chunks

        # Get the next two 3-hour forecast periods (total 6 hours)
        forecast1 = hourly_forecasts[start_index + 1]
        forecast2 = hourly_forecasts[start_index + 2]

        def format_time(t):
            return f"{int(t) // 100}:00"

        # --- Display the Forecast ---
        display.set_pen(BLACK)
        display.clear()

        # Display Current Conditions
        display.set_pen(ORANGE)
        display.text(f"Now: {current_temp_c}C", 10, 10, scale=2)
        display.text(f"{current_desc}", 10, 30, scale=2)

        # Display 3-Hour Forecast
        display.set_pen(YELLOW)
        time1 = format_time(forecast1['time'])
        temp1 = forecast1['tempC']
        desc1 = forecast1['weatherDesc'][0]['value'].strip()
        display.text(f"{time1}: {temp1}C, {desc1}", 10, 70, scale=2)

        # Display 6-Hour Forecast
        time2 = format_time(forecast2['time'])
        temp2 = forecast2['tempC']
        desc2 = forecast2['weatherDesc'][0]['value'].strip()
        display.text(f"{time2}: {temp2}C, {desc2}", 10, 100, scale=2)


    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(RED)
        display.text("API Error!", 15, 80, scale=3)

    # Update the display and wait 10 seconds before returning
    display.update()
    time.sleep(10)
