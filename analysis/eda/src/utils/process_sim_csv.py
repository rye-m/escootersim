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
    task = next((task for task in Task if task.value in path_str), None)
    prototype = next((proto for proto in Prototype if proto.value in path_str), Prototype.CONTROL)

    return task, prototype

def process_csv(path):
    df = pl.read_csv(path, separator=";")
    task, prototype = get_scenario(path)
    if task:
        df = df.with_columns(pl.lit(task.value).alias("Task"))
    if prototype:
        df = df.with_columns(pl.lit(prototype.value).alias("Prototype"))
    return df

def read_trials(path):
    trial_paths = Path(path).glob("CSV_Scenario-*.csv")
    dataframes = []
    for trial in trial_paths:
        df = process_csv(trial)
        dataframes.append(df)
    
    combined_df = pl.concat(dataframes)
    combined_df = expand_encoded_data(combined_df)
    combined_df = combined_df.drop(["A escooter Pos", "A escooter velocity", "A escooter Rot", "]GameTime", "FrameRate", "FrameRate-XRDevice", "Frame Number"])
    combined_df = combined_df.filter(pl.col("ScenarioTime").is_not_null())

    return combined_df