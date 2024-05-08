from machine import SPI, Pin
import tinypico as TinyPICO
from dotstar import DotStar
import time, random, micropython
import requests
import json
import base64
import wifi

# """
# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power( True )

# Say hello
print("\nHello from TinyPICO!")
print("--------------------\n")

# Show some info on boot 
print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

# Show available memory
print("Memory Info - micropython.mem_info()")
print("------------------------------------")
micropython.mem_info()

# Create a colour wheel index int
color_index = 0

# Rainbow colours on the Dotstar
while True:
    # Get the R,G,B values of the next colour
    r,g,b = TinyPICO.dotstar_color_wheel( color_index )
    # Set the colour on the dotstar
    dotstar[0] = ( r, g, b, 0.5)
    # Increase the wheel index
    color_index += 1
    # Sleep for 20ms so the colour cycle isn't too fast
    time.sleep_ms(20)
"""
def start_playback(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/play'
    header = {"Authorization": "Bearer {}".format(token),
              "Content-Type": "application/json"}
    datas = {
            }
    print('token:', header)
    response = requests.put(url, headers=header, data=datas)

    if response.status_code == 204:
        print('Playback started')
        is_success = True

    else:
        print(response.json())
    
    return is_success
"""