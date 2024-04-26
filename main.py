import utime
import requests
import network
import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

ssid = ''
password = ''

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mempool_api = "https://www.blockstream.info/api/blocks/tip/height"
rate = "https://api.coinbase.com/v2/exchange-rates?currency=BTC"

def get_price():
    response = requests.get(rate)
    try:
        if response.status_code == 200:
            data = response.json()
            return "$" + data["data"]["rates"]["USD"]
        else:
            print(f"Error: {response.status_code}")
            return ""
    except Exception as e:
        print(e)
        return ""

def get_height():
    response = requests.get(mempool_api)

    if response.status_code == 200:
        data = response.json()
        return str(data)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

def main():
    #Test function for verifying basic functionality
    print("Running test_main")
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
    lcd.putstr("It Works!")
    utime.sleep(2)
    lcd.clear()
    while True:
        lcd.clear()
        height = get_height()
        price = get_price()
        lcd.putstr(price)
        lcd.putstr("\n")
        lcd.putstr(height)
        utime.sleep(60)

#if __name__ == "__main__":
main()
