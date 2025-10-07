import time
import urequests

# The function now accepts the 'pens' dictionary
def show_eth_price(display, pens):
    # REMOVED: All create_pen calls are gone from here

    display.set_pen(pens["BLACK"])
    display.clear()
    display.set_pen(pens["WHITE"])
    display.set_font("bitmap8")
    display.text("Fetching ETH Price...", 15, 50, scale=2)
    display.update()

    URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    
    try:
        response = urequests.get(URL)
        data = response.json()
        eth_price = data['ethereum']['usd']
        
        display.set_pen(pens["BLACK"])
        display.clear()
        
        display.set_pen(pens["GREEN"]) # Use pen from dictionary
        display.text("Ethereum Price (USD)", 15, 25, scale=2)
        
        display.set_pen(pens["WHITE"])
        price_text = f"${eth_price:,.2f}"
        display.text(price_text, 15, 60, scale=4)

    except Exception as e:
        print(f"API Error: {e}")
        display.set_pen(pens["RED"])
        display.text("API Error!", 15, 80, scale=3)

    display.update()
    time.sleep(5)
