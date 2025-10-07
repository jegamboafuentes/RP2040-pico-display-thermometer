# This is y.py - for fetching the Solana price

import time
import urequests

def show_sol_price(display):
    # --- Define colors ---
    BLACK = display.create_pen(0, 0, 0)
    MAGENTA = display.create_pen(0, 255, 0)
    WHITE = display.create_pen(255, 255, 254)
    RED = display.create_pen(255, 0, 0)

    # --- Show "Fetching..." message ---
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.set_font("bitmap8")
    display.text("Fetching SOL Price...", 15, 50, scale=2)
    display.update()

    # The URL for the CoinGecko API, now for Solana
    URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    
    try:
        # Make the request to the API
        response = urequests.get(URL)
        data = response.json()
        
        # Get the price from the data
        sol_price = data['solana']['usd']
        
        # --- Display the Live Price ---
        display.set_pen(BLACK)
        display.clear()
        
        display.set_pen(MAGENTA)
        display.text("Solana Price (USD)", 15, 25, scale=2)
        
        display.set_pen(WHITE)
        price_text = f"${sol_price:,.2f}"
        display.text(price_text, 15, 60, scale=4)

    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(RED)
        display.text("API Error!", 15, 80, scale=3)

    # Update the display and wait 5 seconds before returning
    display.update()
    time.sleep(5)
