const playSound = require('play-sound')();
const path = require('path');

const audioFilePath = path.join(__dirname, 'audio/Buzz.wav'); // Adjust the path to your audio file

function benchmarkAudioPlayback() {
  const startTime = Date.now();
  console.log(`start: ${startTime} ms`);

  playSound.play(audioFilePath, (err) => {
    console.log(`finish playing`);
    if (err) {
      console.error('Error playing sound:', err);
      return;
    }

    const endTime = Date.now();
    const playbackDuration = endTime - startTime;

    console.log(`Audio playback completed in ${playbackDuration} ms`);
  });
}

benchmarkAudioPlayback();
