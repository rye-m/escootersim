var express = require('express');
var app = express();
var ws = require('ws')
var tinyws= require('tinyws').tinyws
// import {tinyws} from tinyws;

// var expressWs = require('express-ws')(app);

app.use('/hmr', tinyws(), async (req, res) => {
  if (req.ws) {
    const ws = await req.ws()

    return ws.send('hello from express@4')
  } else {
    res.send('Hello from HTTP!')
  }
})

// app.get('/', function(req, res, next){
//   console.log('get route', req.testing);
//   res.end();
// });

// app.ws('/', function(ws, req) {
//   ws.on('message', function(msg) {
//     console.log(msg);
//   });
//   console.log('socket', req.testing);
// });

// app.ws('/echo', function(ws, req) {
//     ws.on('message', function(msg) {
//       ws.send(msg);
//     });
//   });

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`);
});