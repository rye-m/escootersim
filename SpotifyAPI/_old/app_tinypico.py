import requests
import json
import base64
import time
import board
import busio
import adafruit_mpr121


i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    time.sleep(0.25)  # Small delay to keep from spamming output messages.


























def currently_playing(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    # header = "'\{'Authorization: Bearer {}}".format(token)
    header = {"Authorization": "Bearer {}".format(token)}
    print('token:', header)
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        data = response.json()
        song_title = data["item"]["name"]
        print(song_title)
        is_success = True

    else:
        print(response.json())
    
    return is_success

def start_playback(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/play'
    # header = "'\{'Authorization: Bearer {}}".format(token)
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


def pause_playback(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/pause'
    header = {"Authorization": "Bearer {}".format(token)}
    response = requests.put(url, headers=header)

    if response.status_code == 204:
        print('Playback paused')
        is_success = True

    else:
        print(response.json())
    
    return is_success

def skip_to_next(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/next'
    header = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(url, headers=header)

    if response.status_code == 204:
        print('Command sent')
        is_success = True

    else:
        print(response.json())
    
    return is_success

def skip_to_previous(token):
    is_success = False
    url = 'https://api.spotify.com/v1/me/player/previous'
    header = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(url, headers=header)

    if response.status_code == 204:
        print('Command sent')
        is_success = True

    else:
        print(response.status_code)
        print(response.json())
    
    return is_success

if __name__ == "__main__":
    
    token = 'BQCfV7zrsNlTg8XFl3rp9Wy9HIyT_P2pWpPs5uO7ZG0oom005txK5uBbCaNFtLI4M5Mi5AE_3WBMDOqJ-m-0l4WZUA-xhuZkL6lSh8zQG0NJQsq8HI-5frt-emcTM6Em0gFUKhzBltp1fZAMPl0mbEKW2P-o2JWSTQ9sQ_z_opyKyaXBlu6hSNVCgyY7x8EEpIY'
    
    
    try:
        # currently_playing(token)
        # start_playback(token)
        # pause_playback(token)
        skip_to_next(token)
        # skip_to_previous(token)
    
    except json.decoder.JSONDecodeError:
        print("error")


# Q: Is there any way to give token manually to TinyPico
# Q: Should the participants join Diveloppers community of Spotify to get client_id?