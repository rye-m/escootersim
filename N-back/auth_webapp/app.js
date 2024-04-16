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
var app = express();

// create application/json parser
var jsonParser = bodyParser.json()
// var player = require('play-sound')(opts = {})

app.post('/nback', jsonParser, function(req, res){

  command = req.body.command
  console.log("command: " + command);

  // { timeout: 300 } will be passed to child process
var player = require('play-sound')();
player.play('./audio/' + command + '.mp3', (err) => {
    if (err) console.log(`Could not play sound: ${err}`);
});
  res.sendStatus(200);        

})



console.log('Listening on 8888');
app.listen(8888);
