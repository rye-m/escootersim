import polars as pl
from base64 import b64decode
import struct
from pathlib import Path
import re
from datetime import datetime
from enum import Enum


def expand_encoded_data(input_df):
    df = input_df.with_columns(
        [
            pl.col("A escooter Pos")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[0:4])[0], pl.Float64)
            .alias("x_pos"),
            pl.col("A escooter Pos")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[4:8])[0], pl.Float64)
            .alias("y_pos"),
            pl.col("A escooter Pos")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[8:12])[0], pl.Float64)
            .alias("z_pos"),
            pl.col("A escooter velocity")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[0:4])[0], pl.Float64)
            .alias("x_vel"),
            pl.col("A escooter velocity")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[4:8])[0], pl.Float64)
            .alias("y_vel"),
            pl.col("A escooter velocity")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[8:12])[0], pl.Float64)
            .alias("z_vel"),
            pl.col("A escooter Rot")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[0:4])[0], pl.Float64)
            .alias("vehicle x_Rot"),
            pl.col("A escooter velocity")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[4:8])[0], pl.Float64)
            .alias("vehicle y_Rot"),
            pl.col("A escooter velocity")
            .cast(pl.Binary)
            .bin.decode("base64")
            .map_elements(lambda x: struct.unpack("f", x[8:12])[0], pl.Float64)
            .alias("vehicle z_Rot"),
        ]
    )

    df = df.with_columns(
        (
            (
                pl.col("A escooter acc_x") ** 2
                + pl.col("A escooter acc_y") ** 2
                + pl.col("A escooter acc_z") ** 2
            ).sqrt()
        ).alias("accel_magnitude")
    )

    df = df.with_columns(
        (
            (
                pl.col("A escooter rot_x") ** 2
                + pl.col("A escooter rot_y") ** 2
                + pl.col("A escooter rot_z") ** 2
            ).sqrt()
        ).alias("gyro_magnitude")
    )

    df = df.with_columns(
        (
            (pl.col("x_vel") ** 2 + pl.col("y_vel") ** 2 + pl.col("z_vel") ** 2).sqrt()
        ).alias("velocity_magnitude")
    )

    # df = df.with_columns(
    #     rolling_std_accel=pl.col("accel_magnitude").rolling_std(window_size=5),
    #     rolling_std_gyro=pl.col("gyro_magnitude").rolling_std(window_size=5),
    # )
    return df


def get_datetime(path):
    pattern = r"(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})"
    match = re.search(pattern, str(path))
    if match:
        datetime_str = match.group(1)
        return datetime.strptime(datetime_str, "%Y-%m-%d-%H-%M-%S")
    return None


class Task(Enum):
    NBACK = "Nback"
    SONG = "Song"
    PRACTICE = "ScooterStudyenv"


class Prototype(Enum):
    BUTTON = "Button"
    FOOTBUTTON = "Footbutton"
    PHONE = "Phone"
    THROTTLE = "Throttle"
    VOICE = "Voice"
    WATCH = "Watch"
    CONTROL = "Control"


def get_scenario(path):
    path_str = str(path)
    task = next((task for task in Task if task.value in path_str), Task.PRACTICE)
    prototype = next(
        (proto for proto in Prototype if proto.value in path_str), Prototype.CONTROL
    )

    return task, prototype


def process_csv(path):
    df = pl.read_csv(path, separator=";")
    if "]GameTime" in df.columns:
        df = df.drop(["]GameTime"])
    else:
        df = df.drop(["GameTime"])
    task, prototype = get_scenario(path)
    if prototype:
        df = df.with_columns(pl.lit(prototype.value).alias("Prototype"))
    if task:
        df = df.with_columns(pl.lit(task.value).alias("Task"))
        if task == Task.NBACK:
            df = fix_nback_logging(df)
        if task == Task.SONG:
            df = fix_song_logging(df, prototype)
    
    if task == Task.PRACTICE and prototype == Prototype.CONTROL:
        df = df.with_columns(pl.lit(None).cast(pl.String).alias("ws_action"))
        df = df.with_columns(pl.lit(None).cast(pl.Decimal).alias("ws_value"))
    df = df.drop(["Websocket_message_category", "Websocket_message_action"])

    df = expand_encoded_data(df)
    df = df.drop(
        [
            "A escooter Pos",
            "A escooter velocity",
            "A escooter Rot",
            "FrameRate",
            "FrameRate-XRDevice",
            "Frame Number",
        ]
    )
    df = df.filter(pl.col("ScenarioTime").is_not_null())
    df = df.with_columns(pl.col('ws_value').cast(pl.Float64))

    return df

def read_trials(path):
    trial_paths = Path(path).glob("CSV_Scenario-*.csv")
    dataframes = []
    for trial in trial_paths:
        df = process_csv(trial)
        dataframes.append(df)

    combined_df = pl.concat(dataframes)
    return combined_df


def scenario_df(df, task=None, prototype=None):
    if task is None:
        return df.filter(pl.col("Prototype") == prototype.value)
    if prototype is None:
        return df.filter(pl.col("Task") == task.value)
    else:
        return df.filter(
            (pl.col("Task") == task.value) & (pl.col("Prototype") == prototype.value)
        )

nback_ws_map = {
    r"\s[0-9]": (
        "NBACK_DIGIT",
        pl.col("Websocket_message_action").str.strip_chars(),
    ),
    "timedout": ("NBACK_TIMEOUT", 1),
    "yes|no": (
        "NBACK_CLIENT_RESPONSE",
        pl.col("Websocket_message_action")
        .str.strip_chars()
        .replace(["yes", "no"], ["1", "0"]),
    ),  # yes=1, no=0
    "Accuracy=": (
        "NBACK_CLIENT_ACCURACY",
        pl.col("Websocket_message_action").str.extract(
            r"=\s*([0-9]+\.?[0-9]*)", 1
        ),
    ),
    "Total=": (
        "NBACK_CLIENT_TOTAL",
        pl.col("Websocket_message_action").str.extract(
            r"=\s*([0-9]+\.?[0-9]*)", 1
        ),
    ),
    "end": ("NBACK_MCU_END", pl.lit(1)),  # end = 1
    "begin": ("NBACK_MCU_BEGIN", pl.lit(0)),  # start = 0
    "start_nback": (
        "NBACK_START_COMMAND_BY_RESEARCHER",
        pl.lit(0),
    ),  # start = 0
    "finish_nback": ("NBACK_END_COMMAND_BY_RESEARCHER", pl.lit(1)),  # end = 1
    "ping": ("PING", pl.lit(1)),
    "correct|incorrect": (
        "NBACK_SERVER_RESPONSE",
        pl.col("Websocket_message_action")
        .str.strip_chars()
        .replace(["correct", "incorrect"], ["1", "0"]),
    ),
}

def fix_nback_logging(df, mapping=nback_ws_map):
    df = df.with_columns(pl.lit(None).alias("ws_action"))
    df = df.with_columns(pl.lit(None).alias("ws_value"))

    for k, v in mapping.items():
        df = df.with_columns(
            [
                pl.when(pl.col("Websocket_message_action").str.contains(k))
                .then(pl.lit(v[0]))
                .otherwise(pl.col("ws_action"))
                .alias("ws_action"),
                pl.when(pl.col("Websocket_message_action").str.contains(k))
                .then(v[1])
                .otherwise(pl.col("ws_value"))
                .alias("ws_value"),
            ]
        )
    df = df.with_columns(pl.col("ws_value").str.to_decimal())
    return df


def get_remapping(prototype): 
    if prototype == Prototype.VOICE:
        playpause = ("SONG_RESEARCHER_PLAY_PAUSE", None)
    else:
        playpause = ("SONG_USER_PLAY_PAUSE", None)

    if prototype in [Prototype.VOICE, Prototype.WATCH, Prototype.PHONE]:
        play = ("SONG_PLAYPAUSE_ACK", pl.lit(1))

    else:
        play = ("SONG_NEXT_PREVIOUS", pl.lit(1))

    pause = ("SONG_PLAYPAUSE_ACK", pl.lit(0))

    remapped = {
        r"\bnext\b": ("SONG_NEXT_PREVIOUS", pl.lit(1)),
        r"\bprevious\b": ("SONG_NEXT_PREVIOUS", pl.lit(-1)),
        r"next_failed": ("SONG_OOB", pl.lit(1)),
        r"previous_failed": ("SONG_OOB", pl.lit(-1)),
        r"Ping": ("SYSTEM_PING", pl.lit(1)),
        r"next_failed": ("SONG_OOB", pl.lit(1)),
        r"previous_failed": ("SONG_OOB", pl.lit(-1)),
        r"playpause": playpause,
        r"\bplay\b": play,
    }
    return remapped

def fix_song_logging(df, prototype):
    mapping1 = get_remapping(prototype)
    df = df.with_columns(pl.lit(None).alias("ws_action"))
    df = df.with_columns(pl.lit(None).alias("ws_value"))
    for k, v in mapping1.items():
        if prototype in [Prototype.VOICE, Prototype.PHONE, Prototype.WATCH] and k == r"playpause":
            df = df.with_columns(
                [
                    pl.when(pl.col("Websocket_message_action").str.contains(k))
                    .then(pl.lit(v[0]))
                    .otherwise(pl.col("ws_action"))
                    .alias("ws_action"),
                    pl.when(pl.col("Websocket_message_action").str.contains(k))
                    .then(
                        pl.when(
                            pl.col("Websocket_message_action")
                            .eq(k)
                            .cum_count()
                            .over("Websocket_message_action")
                            == 1
                        )
                        .then(pl.lit(1))
                        .when(
                            pl.col("Websocket_message_action")
                            .eq(k)
                            .cum_count()
                            .reverse()
                            .over("Websocket_message_action")
                            == 1
                        )
                        .then(pl.lit(-1))
                        .otherwise(pl.col("ws_value"))
                    )
                    .otherwise(pl.col("ws_value"))
                    .alias("ws_value"),
                ]
        )
        elif k != r"playpause":
            df = df.with_columns(
                [
                    pl.when(pl.col("Websocket_message_action").str.contains(k))
                    .then(pl.lit(v[0]))
                    .otherwise(pl.col("ws_action"))
                    .alias("ws_action"),
                    pl.when(pl.col("Websocket_message_action").str.contains(k))
                    .then(v[1])
                    .otherwise(pl.col("ws_value"))
                    .alias("ws_value"),
                ]
            )
    df = df.with_columns(pl.col("ws_value").cast(pl.Decimal(precision=None, scale=0)))
    return df

def combine_dataset(data_dir, output=None):
    participants = data_dir.glob("P*")
    dfs = []
    for participant in participants:
        # print(participant.name)
        df = read_trials(participant)
        df = df.with_columns(pl.lit(participant.name).alias("participantID"))
        dfs.append(df)
    combined_df = pl.concat(dfs)
    # if output is not None:
        # combined_df.write_csv(output + '.csv')
        # combined_df.write_parquet(output + '.parquet')
         
    return combined_df