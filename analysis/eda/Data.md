# Data Dictionary

## Data Column Descriptions
| Index | Column | Description |
|-------|--------|-------------|
| 0 | ScenarioTime | Time within the scenario. Each Scenario (Prototype x Task) starts at zero and proceeds until route completion |
| 1 | A escooter accel | E-scooter acceleration from throttle _within the unity simulator_ |
| 2 | A escooter steering | E-scooter steering angle |
| 3 | A escooter acc_x | E-scooter acceleration along X-axis _from the imu mounted on the scooter_ |
| 4 | A escooter acc_y | E-scooter acceleration along Y-axis _from the imu mounted on the scooter_ |
| 5 | A escooter acc_z | E-scooter acceleration along Z-axis _from the imu mounted on the scooter_ |
| 6 | A escooter rot_x | E-scooter rotation around X-axis _from the imu mounted on the scooter_ |
| 7 | A escooter rot_y | E-scooter rotation around Y-axis _from the imu mounted on the scooter_ |
| 8 | A escooter rot_z | E-scooter rotation around Z-axis _from the imu mounted on the scooter_ |
| 9 | Websocket_message_timestamp | Timestamp in unity of websocket message arrival. These account for all prototype interactions (buttons and responses) |
| 10 | Prototype | Prototype identifier (BUTTON, FOOTBUTTON, THROTTLE, PHONE, WATCH, CONTROL) |
| 11 | Task | Task identifier (NBACK, SONG, ScooterStudyenv=Control)  |
| 12 | ws_action | Websocket action, the message type described below |
| 13 | ws_value | Websocket value, the message value, described below  |
| 14 | x_pos | X-coordinate position _within the unity simulator_ |
| 15 | y_pos | Y-coordinate position _within the unity simulator_ |
| 16 | z_pos | Z-coordinate position _within the unity simulator_ |
| 17 | x_vel | Velocity along X-axis _within the unity simulator_ |
| 18 | y_vel | Velocity along Y-axis _within the unity simulator_ |
| 19 | z_vel | Velocity along Z-axis _within the unity simulator_ |
| 20 | vehicle x_Rot | Vehicle rotation around X-axis _within the unity simulator_ |
| 21 | vehicle y_Rot | Vehicle rotation around Y-axis _within the unity simulator_ |
| 22 | vehicle z_Rot | Vehicle rotation around Z-axis _within the unity simulator_ |
| 23 | accel_magnitude | Magnitude of acceleration _from the imu mounted on the scooter_ |
| 24 | gyro_magnitude | Magnitude of gyroscopic force _from the imu mounted on the scooter_ |
| 25 | velocity_magnitude | Magnitude of velocity _within the unity simulator_ |
| 26 | participantID | Unique identifier for participant, maps to the randomID in the qualtrics survey |

## Prototype Action Descriptions
| Value | Description |
|-------|-------------|
| None | No event occured |
| NBACK_CLIENT_ACCURACY | at the completion of an NBACK session, the prototype reports the accuracy it logged. This can also just be calculated from the NBACK in this table itself |
| NBACK_CLIENT_TOTAL | at the completion of an NBACK session, the prototype reports the total number of nback tasks it logged. This can also just be calculated from the NBACK in this table itself  |
| NBACK_START_COMMAND_BY_RESEARCHER | the researcher has initiated the NBACK task on the server |
| NBACK_END_COMMAND_BY_RESEARCHER | the researcher has ended the NBACK task on the server |
| NBACK_MCU_BEGIN | the MCU acknowleges the task has begun |
| NBACK_MCU_END | the MCU acknowleges the task has ended |
| NBACK_DIGIT | the digit that was stated |
| NBACK_CLIENT_RESPONSE | the response from the partipant if the digit repeats the previous number <br>__0=NO 1=YES__ |
| NBACK_SERVER_RESPONSE | the response from the server <br>__0=INCORRECT 1=CORRECT__ |
| SONG_NEXT_PREVIOUS | the participant has initiated skipping to the next or previous song <br>__-1=PREVIOUS SONG 1=NEXT SONG__|
| SONG_OOB | the participant has initiated skipping to the next or previous song but were at the end or beginning of the playlist <br>__-1=PREVIOUS SONG 1=NEXT SONG__|
| SONG_PLAYPAUSE_ACK | the server acknowledging a song has been played or paused, only used for VOICE, PHONE, WATCH <br>__0=PAUSE 1=PLAY__ |
| SONG_RESEARCHER_PLAY_PAUSE | the researcher intitiating a song play or pause, only used for VOICE, PHONE, WATCH <br>__0=PAUSE 1=PLAY__ |
| SONG_USER_PLAY_PAUSE | the participant intitiating a song play or pause, only used for PHONE and WATCH. There may be some accidental touches on watch WATCH we should discuss <br>__0=PAUSE 1=PLAY__|
| SYSTEM_PING | a check to make sure things are working properly, feel free to ignore |