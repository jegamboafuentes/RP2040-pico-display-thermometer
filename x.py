import time
import urequests

# The function now accepts the 'pens' dictionary
def show_weather_forecast(display, pens):
    # REMOVED: All create_pen calls are gone from here

    display.set_pen(pens["BLACK"])
    display.clear()
    display.set_pen(pens["WHITE"])
    display.set_font("bitmap8")
    display.text("Fetching Forecast...", 15, 50, scale=2)
    display.update()

    URL = "http://wttr.in/Boston?format=j1"

    try:
        response = urequests.get(URL)
        data = response.json()

        current = data['current_condition'][0]
        current_desc = current['weatherDesc'][0]['value']
        current_temp_c = current['temp_C']

        now_hour = int(time.localtime()[3])
        hourly_forecasts = data['weather'][0]['hourly']
        start_index = now_hour // 3

        forecast1 = hourly_forecasts[start_index + 1]
        forecast2 = hourly_forecasts[start_index + 2]

        def format_time(t):
            return f"{int(t) // 100}:00"

        display.set_pen(pens["BLACK"])
        display.clear()

        display.set_pen(pens["ORANGE"]) # Use pen from dictionary
        display.text(f"Now: {current_temp_c}C", 10, 10, scale=2)
        display.text(f"{current_desc}", 10, 30, scale=2)

        display.set_pen(pens["YELLOW"]) # Use pen from dictionary
        time1 = format_time(forecast1['time'])
        temp1 = forecast1['tempC']
        desc1 = forecast1['weatherDesc'][0]['value'].strip()
        display.text(f"{time1}: {temp1}C, {desc1}", 10, 70, scale=2)

        time2 = format_time(forecast2['time'])
        temp2 = forecast2['tempC']
        desc2 = forecast2['weatherDesc'][0]['value'].strip()
        display.text(f"{time2}: {temp2}C, {desc2}", 10, 100, scale=2)

    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(pens["RED"])
        display.text("API Error!", 15, 80, scale=3)

    display.update()
    time.sleep(10)
