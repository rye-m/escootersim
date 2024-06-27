const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Store all connected clients
const clients = new Set();

// Serve static files from 'public' directory
app.use(express.static('./'));

// Regular HTTP route
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Broadcast function to send a message to all connected clients
function broadcast(message) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
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

  // Handle disconnection
  ws.on('close', () => {
    console.log('WebSocket connection closed');
    // Remove the client from our set
    clients.delete(ws);
  });

  // Send a welcome message to the new client
  ws.send('Welcome to the WebSocket server!');
  
  // Broadcast a message about the new connection
  broadcast('A new client has connected!');
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});