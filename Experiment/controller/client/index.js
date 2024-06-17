/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/documentation/web-api/tutorials/code-flow
 */

var express = require('express');
var request = require('request');
var crypto = require('crypto');
var cors = require('cors');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser')

var client_id = '978e25ba8b0442adaeca418801d80593'; // your clientId
var client_secret = 'f9d9bc4ddd8640a5bf3cd8bed05a9db7'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri

var mode = 'none'; // init app mode

global.ACCESS_TOKEN = ''

const generateRandomString = (length) => {
  return crypto
  .randomBytes(60)
  .toString('hex')
  .slice(0, length);
}

var stateKey = 'spotify_auth_state';

var app = express();
app.use(express.static(__dirname + '/public'))
   .use(cors())
   .use(cookieParser());

// create application/json parser
var jsonParser = bodyParser.json()
var path = require('path');

//Return the index for any other GET request
app.get('/', function (req, res) {
    console.log('Hello, guest!');
    res.sendFile('index.html', {root: path.join(__dirname, 'public')});
});


app.get('/mode_tinypico', jsonParser, function(req, res){

  statuscode = 400;
  switch (mode) {
    case 'Spotify_button':
      console.log('Spotify_button');
      statuscode = 201;
      break;
      case 'Spotify_foot_button':
        console.log('Spotify_foot_button');
        statuscode = 209;
        break;
      case 'Spotify_footpedal':
      console.log('Spotify_footpedal');
      statuscode = 202;
      break;
    case 'Spotify_gearshifter':
      console.log('Spotify_gearshifter');
      statuscode = 203;
      break;
    case 'Spotify_throttle':
      console.log('Spotify_throttle');
      statuscode = 204;
      break;
    case 'Nback_button':
      console.log('Nback_button');
      statuscode = 205;
      break;
      case 'Nback_foot_button':
        console.log('Nback_foot_button');
        statuscode = 210;
        break;
      case 'Nback_footpedal':
      console.log('Nback_footpedal');
      statuscode = 206;
      break;
    case 'Nback_gearshifter':
      console.log('Nback_gearshifter');
      statuscode = 207;
      break;
    case 'Nback_throttle':
      console.log('Nback_throttle');
      statuscode = 208;
      break;
    default:
      console.log(`Sorry, there is no ${mode}.`);
      break;
  }
  
  res.sendStatus(statuscode);        

})


app.get('/mode_server/:mode', jsonParser, function(req, res){

  if (req.params['mode'] != 'mode'){
    mode = req.params['mode']
  }
  console.log('mode: ' + mode);

  if (RegExp("^Spotify").test(mode)){
    res.sendFile('spotify.html', {root: path.join(__dirname, 'public')});
  }
  else{
    res.set('Content-Type', 'text/html');
    res.send(JSON.stringify(mode));  }

})


app.post('/api', jsonParser, function(req, res){

  command = req.body.command

  var authOptions = {
    url: 'https://api.spotify.com/v1/me/player/' + command,
    headers: {
      'content-type': 'application/json',
      'Authorization': 'Bearer ' + global.ACCESS_TOKEN,
    },
    json: true
  };
  console.log("authOptions.url: " + authOptions.url);

  if (command == 'next' || command == 'previous'){
    request.post(authOptions, function(error, response, body) {
      res.json(response.statusCode);
      console.log("response: " + response.statusCode);
    })
  }
  else if (command == 'play' || command == 'pause'){
    request.put(authOptions, function(error, response, body) {
      res.json(response.statusCode);
      console.log("response: " + response.statusCode);
    })
  }
  else if (command == 'currently-playing'){
    request.get(authOptions, function(error, response, body) {
      try {
        if (response.body.is_playing == false) {
          res.sendStatus(201);        
            }
        else if (response.body.is_playing == true) {
          res.sendStatus(202);        
        }
        else { res.sendStatus(500); }
        console.log("statusCode: " + response.statusCode);
        console.log("is_playing: " + response.body.is_playing);
      }
      catch(e) {
        console.log(e);
        console.log("Error: " + e);
    }
    })}
  }
)

app.post('/nback', jsonParser, function(req, res){

  command = req.body.command
  console.log("command: " + command);

var player = require('play-sound')();
player.play('./audio/' + command + '.mp3', (err) => {
    if (err) console.log(`Could not play sound: ${err}`);
});
  res.sendStatus(200);        

})


app.get('/login', function(req, res) {

  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // your application requests authorization
  var scope = 'user-modify-playback-state user-read-private user-read-email user-read-currently-playing';
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});

app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code',
        scope: 'user-read-currently-playing user-read-playback-state'

      },
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        Authorization: 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;
        
        global.ACCESS_TOKEN = body.access_token

        //console.log("ACCESS_TOKEN: "+ ACCESS_TOKEN);
        var options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
          console.log(body);
        });

        // we can also pass the token to the browser to make requests from there
        res.redirect('/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});

app.get('/refresh_token', function(req, res) {

  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 
      'content-type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64')) 
    },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token,
          refresh_token = body.refresh_token;
      res.send({
        'access_token': access_token,
        'refresh_token': refresh_token
      });
    }
  });
});

console.log('Listening on 8888');
app.listen(8888);
