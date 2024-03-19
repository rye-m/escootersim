import requests
import json
import base64

Client_ID = '978e25ba8b0442adaeca418801d80593'
Client_secret = 'f9d9bc4ddd8640a5bf3cd8bed05a9db7'
# token = 'BQCvxE0gLfxHpBDk8NbL8bCCKkgVlYhBwJd7Vz7PONNjcOpQ3nFDv1yOYUpt5AXZK7P-fA-FuYgqIlYOTdA7kZ9pSzUFxNOzZRnsEj0JDa4FQeRcouE'

def get_token():
    # base64 encording
    client_info_str = '{}:{}'.format(Client_ID, Client_secret)
    client_info_byte = client_info_str.encode("ascii")     # get token
    client_info_base64 = base64.b64encode(client_info_byte) 
    base64_string = client_info_base64.decode("ascii") 
    # send request
    header = {"Authorization": "Basic {}".format(base64_string)}
    data = {"grant_type": "client_credentials",
            "scope": "playlist-modify-private user-library-read user-read-currently-playing user-read-playback-state"}
    response = requests.post(url='https://accounts.spotify.com/api/token', headers=header, data=data)
    token = response.json()["access_token"]
    return token



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