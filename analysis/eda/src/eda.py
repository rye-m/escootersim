import marimo

__generated_with = "0.7.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import polars as pl
    import altair as alt
    from pathlib import Path
    from base64 import b64decode
    import struct
    import numpy as np
    return Path, alt, b64decode, mo, np, pl, struct


@app.cell
def __(Path, pl):
    data_path = Path("./src/Data/")
    sample_data = data_path / "Sample_data.csv"
    df_raw = pl.read_csv(sample_data, separator=";")
    return data_path, df_raw, sample_data


@app.cell
def __(mo):
    mo.md("""## Cleanup and add velocity magnitude, and shakiness""")
    return


@app.cell
def __(df_raw, pl, struct):
    df = df_raw.with_columns(
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
                pl.col("A escooter acc_x") ** 2 + pl.col("A escooter acc_y") ** 2 + pl.col("A escooter acc_z") ** 2
            ).sqrt()
        ).alias("accel_magnitude")
    )

    df = df.with_columns(
        (
            (
                pl.col("A escooter rot_x") ** 2 + pl.col("A escooter rot_y") ** 2 + pl.col("A escooter rot_z") ** 2
            ).sqrt()
        ).alias("gyro_magnitude")
    )

    df = df.with_columns(
        (
            (
                pl.col("x_vel") ** 2 + pl.col("y_vel") ** 2 + pl.col("z_vel") ** 2
            ).sqrt()
        ).alias("velocity_magnitude")
    )



    df = df.with_row_index()
    return df,


@app.cell
def __(mo):
    mo.md("""here we display a few rows from out sim data""")
    return


@app.cell
def __():
    # df[['gyro_magnitude', 'accel_magnitude']].plot()
    return


@app.cell
def __(df):

    df.head(4) 
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Visualizations
        ### TODO
        - high pass filter on the imu data
        - use STD or RMS rather than raw magnitude
        """
    )
    return


@app.cell
def __(alt, df):
    base = (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x="x_pos",
            y="z_pos",
        )
    )

    row1 = alt.hconcat(
        base.encode(color=alt.Color(
            "ScenarioTime:Q", scale=alt.Scale(scheme="blues")
                
            )), 
        base.encode(color=alt.Color(
            "velocity_magnitude:Q", scale=alt.Scale(scheme="plasma")
            )),
    ).resolve_scale(color='independent')

    row2 = alt.hconcat(
        base.encode(color=alt.Color(
            "accel_magnitude:Q", scale=alt.Scale(scheme="blues")
            )), 
        base.encode(color=alt.Color(
            "gyro_magnitude:Q", scale=alt.Scale(scheme="blues")
            ))).resolve_scale(color='independent')
    row1 & row2

    return base, row1, row2


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
