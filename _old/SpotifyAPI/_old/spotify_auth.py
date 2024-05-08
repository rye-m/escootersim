from flask import Flask, request, redirect, jsonify
import requests
import random
import string
import urllib.parse

app = Flask(__name__)

CLIENT_ID = '978e25ba8b0442adaeca418801d80593'
CLIENT_SECRET = 'f9d9bc4ddd8640a5bf3cd8bed05a9db7'
REDIRECT_URI = 'http://localhost:8888/callback'

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

state_key = 'spotify_auth_state'

@app.route('/login')
def login():
    state = generate_random_string(16)
    response = redirect('https://accounts.spotify.com/authorize?' +
        urllib.parse.urlencode({
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'scope': 'user-modify-playback-state user-read-private user-read-email user-read-currently-playing',
            'redirect_uri': REDIRECT_URI,
            'state': state
        }))
    response.set_cookie(state_key, state)
    return response

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = request.cookies.get(state_key)

    if state is None or state != stored_state:
        return redirect('/#' + urllib.parse.urlencode({'error': 'state_mismatch'}))
    else:
        response = requests.post('https://accounts.spotify.com/api/token', data={
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
            'scope': 'user-read-currently-playing user-read-playback-state'
        }, headers={
            'Authorization': 'Basic ' + (CLIENT_ID + ':' + CLIENT_SECRET).encode('utf-8').b64encode().decode('utf-8')
        })

        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            refresh_token = data['refresh_token']

            user_info = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + access_token})
            print(user_info.json())

            return redirect('/#' + urllib.parse.urlencode({
                'access_token': access_token,
                'refresh_token': refresh_token
            }))
        else:
            return redirect('/#' + urllib.parse.urlencode({'error': 'invalid_token'}))

@app.route('/refresh_token')
def refresh_token():
    refresh_token = request.args.get('refresh_token')
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }, headers={
        'Authorization': 'Basic ' + (CLIENT_ID + ':' + CLIENT_SECRET).encode('utf-8').b64encode().decode('utf-8')
    })

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

if __name__ == "__main__":
    app.run(port=8888)
