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
    data = {"grant_type": "client_credentials"}
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
        data = json.loads(response)
        song_title = data["item"]["TrackObject"]["name"]
        print(song_title)
        is_success = True

    else:
        print(response.json())
    
    return is_success



if __name__ == "__main__":
    
    token = get_token()
    currently_playing(token)