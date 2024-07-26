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
const http = require('http');
const WebSocket = require('ws');

var client_id = '978e25ba8b0442adaeca418801d80593'; // your clientId
var client_secret = 'f9d9bc4ddd8640a5bf3cd8bed05a9db7'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri

var mode = 'None! Please select a mode to play!'; // init app mode
var spotify_count; // counter for Spotify

global.ACCESS_TOKEN = ''

const generateRandomString = (length) => {
  return crypto
  .randomBytes(60)
  .toString('hex')
  .slice(0, length);
}

var stateKey = 'spotify_auth_state';

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Store all connected clients
const clients = new Set();

// Serve static files from 'public' directory
app.use(express.static(__dirname + '/public'))
   .use(cors())
   .use(cookieParser());

// create application/json parser
var jsonParser = bodyParser.json()
var path = require('path');


// Broadcast function to send a message to all connected clients
function broadcast(message) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}


function logger(log_message){
  // time_stamp = Math.floor(+new Date() / 1000)
  // broadcast(`${time_stamp}: ${log_message}`);
  console.log(`${log_message}`)
  broadcast(`${log_message}`);
}


// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('New WebSocket connection');
  
  // Add the new client to our set
  clients.add(ws);

  // Handle incoming messages
  ws.on('message', (message) => {
    console.log('Received:', message);

    // Broadcast the message to all clients
    broadcast(`Client said: ${message}`);
  });

  ws.on('generate_number', (message) => {
    console.log('Received:', message);

    // Broadcast the message to all clients
    broadcast(`Client said: ${message}`);
  });




  // Handle disconnection
  ws.on('close', () => {
    console.log('WebSocket connection closed');
    // Remove the client from our set
    clients.delete(ws);
  });

  // Send a welcome message to the new client
  // ws.send('Welcome to the WebSocket server!');
  
  // Broadcast a message about the new connection
  // broadcast('A new client has connected!');
});


//Return the index for any other GET request
app.get('/', function (req, res) {
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
    case 'Spotify_web':
        console.log('Spotify_web');
        statuscode = 216;
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
    case 'Nback_watch':
      console.log('Nback_watch');
      statuscode = 211;
      break;
      case 'Navi_button':
        console.log('Navi_button');
        statuscode = 212;
      break;
      case 'Navi_foot_button':
        console.log('Navi_foot_button');
        statuscode = 213;
        break;
      case 'Navi_gearshifter':
        console.log('Navi_gearshifter');
        statuscode = 214;
        break;
      case 'Navi_throttle':
        console.log('Navi_throttle');
        statuscode = 215;
        break;
      default:
    console.log(`Sorry, there is no ${mode}.`);
      break;
  }
  logger(`mode: ${mode}`);
  res.sendStatus(statuscode);        

})


app.get('/mode_server/:mode', jsonParser, function(req, res){
  spotify_count = 1; // init counter for Spotify
  console.log("spotify_count: " + spotify_count)

  if (req.params['mode'] != 'mode'){
    mode = req.params['mode']
  }
  logger(`mode: ${mode}`);

  if (mode == "Authentication"){
    res.sendFile('spotify.html', {root: path.join(__dirname, 'public')});
  }
  else if (mode == "Nback_watch") {
    res.sendFile('nback_watch.html', {root: path.join(__dirname, 'public')});
  }
  else if (mode == "web"){
    res.sendFile('spotify_web.html', {root: path.join(__dirname, 'public')});
  }
  else if (RegExp("^Nback").test(mode)){
    res.sendFile('nback.html', {root: path.join(__dirname, 'public')});
  }
  else{
    res.set('Content-Type', 'text/html');
    res.send(JSON.stringify(mode));  }

})


app.get('/api/:command', jsonParser, function(req, res){

  command = req.params['command']
  player_url= 'https://api.spotify.com/v1/me/player/'

  var authOptions = {
    url: player_url + command,
    headers: {
      'content-type': 'application/json',
      'Authorization': 'Bearer ' + global.ACCESS_TOKEN,
    },
    json: true
  };
  console.log("authOptions.url: " + authOptions.url);

    if (command == 'next' || command == 'previous'){      
      if ((command == 'next' && spotify_count == 4) || (command == 'previous' && spotify_count == 1)){
        logger(`Spotify: ${command}_failed`);
        
        var player = require('play-sound')();
        player.play('./audio/Buzz.wav', (err) => {
        if (err) console.log(`Could not play sound: ${err}`);
        });
        res.sendStatus(204)
        return; // Exit the function if there's an error
      }

      request.post(authOptions, function(error, response, body) {
        logger(`Spotify: ${command}`);

        if (response.statusCode >= 200 && response.statusCode < 300){
          if (command == 'next'){spotify_count++;}
          if (command == 'previous'){spotify_count--;}
          console.log("spotify_count(changed): " + spotify_count)

          if (mode = 'web'){ res.sendFile('spotify_web.html', {root: path.join(__dirname, 'public')})}
          else {res.sendStatus(204)}    
          console.log("response???: " + response.statusCode);
        }
        else{
          res.sendStatus(response.statusCode)
        }
      })
    }

    else if (command == 'play' || command == 'pause'){
      logger(`Spotify: ${command}`);

        request.put(authOptions, function(error, response, body) {
        res.json(response.statusCode);
        console.log("response: " + response.statusCode);
      })
    }

    else if (command == 'playpause'){
      logger(`Spotify: ${command}`);
      authOptions.url = player_url + 'currently-playing'

      request.get(authOptions, function(error, response, body) {
        try {
          if (response.body.is_playing == false) {
            authOptions.url = player_url + 'play'
            logger("Spotify: play");
          }
          else if (response.body.is_playing == true) {
            authOptions.url = player_url + 'pause'
            logger("Spotify: pause");
          }
          else { res.sendStatus(500); }
          
          request.put(authOptions, function(error, response, body) {
              console.log("response: " + response.statusCode);
              if (mode = 'web'){ res.sendFile('spotify_web.html', {root: path.join(__dirname, 'public')})}
              else {res.sendStatus(204)}    
          })
        }
        catch(e) {
          console.log(e);
          console.log("Error: " + e);
        }
      })
    }
    // TODO: Need to delete this function after finish modifying the controller code
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


app.get('/gearshifter/:track_no', jsonParser, function(req, res){

  track_no = req.params['track_no']
  logger(`Spotify: ${track_no}`);
  
  var authOptions = {
    url: 'https://api.spotify.com/v1/me/player/play',
    headers: {
      'content-type': 'application/json',
      'Authorization': 'Bearer ' + global.ACCESS_TOKEN,
    },
    json: {
        'context_uri': 'spotify:playlist/6cWthOVBhmDNCYcTREexhK',
        'offset': { 'position' : track_no },
        'position_ms': 0
    }
    // json: true
  };
  
    request.put(authOptions, function(error, response, body) {
      res.json(response.statusCode);
      // console.log("request: " + request.body);
      console.log("Spotify_track_no: " + track_no);
    })
  }
  
)


app.get('/nback_watch_http/:answer', jsonParser, function(req, res){

  answer = req.params['answer']
  console.log("answer: " + answer);
  // logger(`N-back: ${answer}`);

  broadcast(answer);
  res.sendFile('nback_watch.html', {root: path.join(__dirname, 'public')});

})

app.get('/nback_controller/:command', jsonParser, function(req, res){

  command = req.params['command']
  broadcast(command);
  res.sendFile('nback.html', {root: path.join(__dirname, 'public')});
  }
)


app.get('/nback/:command', jsonParser, function(req, res){

  command = req.params['command']
  console.log("command: " + command);

  var player = require('play-sound')();
  player.play('./audio/' + command + '.mp3', (err) => {
      if (err) console.log(`Could not play sound: ${err}`);
  });
  logger(`N-back: ${command}`);

  res.sendStatus(200);        

})


app.get('/navi/:command', jsonParser, function(req, res){

  command = req.params['command']
  console.log("command: " + command);
  broadcast(command);
  logger(`Navi_command: ${command}`);

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


// Start the server
const PORT = process.env.PORT || 8888;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});