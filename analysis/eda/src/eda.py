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
    from scipy import signal
    from scipy.fft import fft, fftfreq
    return Path, alt, b64decode, fft, fftfreq, mo, np, pl, signal, struct


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
            (
                pl.col("x_vel") ** 2 + pl.col("y_vel") ** 2 + pl.col("z_vel") ** 2
            ).sqrt()
        ).alias("velocity_magnitude")
    )

    df = df.with_columns(
        rolling_std_accel=pl.col("accel_magnitude").rolling_std(window_size=5),
        rolling_std_gyro=pl.col("gyro_magnitude").rolling_std(window_size=5),
    )

    df = df.with_row_index()
    return df,


@app.cell
def __(mo):
    mo.md("""here we display a few rows from out sim data""")
    return


@app.cell
def __():
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

    brush = alt.selection_interval()

    row1 = alt.hconcat(
        base.encode(
            color=alt.condition(
                brush,
                alt.Color("ScenarioTime:Q", scale=alt.Scale(scheme="blues")),
                alt.value("lightgray"),
            )
        ),
        base.encode(
            color=alt.condition(
                brush,
                alt.Color(
                    "velocity_magnitude:Q", scale=alt.Scale(scheme="plasma")
                ),
                alt.value("lightgray"),
            )
        ),
    ).resolve_scale(color="independent")

    row2 = alt.hconcat(
        base.encode(
            color=alt.condition(
                brush,
                alt.Color("rolling_std_accel:Q", scale=alt.Scale(scheme="blues")),
                alt.value("lightgray"),
            )
        ),
        base.encode(
            color=alt.condition(
                brush,
                alt.Color("rolling_std_gyro:Q", scale=alt.Scale(scheme="blues")),
                alt.value("lightgray"),
            )
        ),
    ).resolve_scale(color="independent")

    timeline = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="ScenarioTime:Q",
            color=alt.Color(
                "ScenarioTime:Q", scale=alt.Scale(scheme="blues"), legend=None
            ),
        )
        .properties(width="container")
        .add_params(brush)
    )

    row1 & row2 & timeline
    return base, brush, row1, row2, timeline


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Frequency Analyis

        fft on logged data isn't so helpful because the sample rate is too low to pick up any interesting peaks.
        """
    )
    return


@app.cell
def __(df, fft, fftfreq, np, pl):
    sample_rate = 1 / df.select(pl.col("ScenarioTime").diff()).mean()[0, 0]
    nyquist_frequency = sample_rate / 2


    fft_accel_x = np.abs(
        fft(df["A escooter acc_x"].drop_nulls().drop_nans().to_numpy())
    )
    fft_accel_y = np.abs(
        fft(df["A escooter acc_y"].drop_nulls().drop_nans().to_numpy())
    )
    fft_accel_z = np.abs(
        fft(df["A escooter acc_z"].drop_nulls().drop_nans().to_numpy())
    )

    fft_gyro_x = np.abs(
        fft(df["A escooter rot_x"].drop_nulls().drop_nans().to_numpy())
    )
    fft_gyro_y = np.abs(
        fft(df["A escooter rot_y"].drop_nulls().drop_nans().to_numpy())
    )
    fft_gyro_z = np.abs(
        fft(df["A escooter rot_z"].drop_nulls().drop_nans().to_numpy())
    )

    freq_accel = fftfreq(
        len(df["A escooter acc_x"].drop_nulls().drop_nans().to_numpy()),
        1 / sample_rate,
    )
    freq_gyro = fftfreq(
        len(df["A escooter rot_x"].drop_nulls().drop_nans().to_numpy()),
        1 / sample_rate,
    )

    accel_data = pl.DataFrame(
        {
            "accel_x": fft_accel_x,
            "accel_y": fft_accel_y,
            "accel_z": fft_accel_z,
            "freq_accel": freq_accel,
        }
    ).unpivot(index=["freq_accel"], on=["accel_y", "accel_x", "accel_z"]).filter(pl.col('value')< 200)
    gyro_data = pl.DataFrame(
        {
            "gyro_x": fft_gyro_x,
            "gyro_y": fft_gyro_y,
            "gyro_z": fft_gyro_z,
            "freq_gyro": freq_gyro,
        }
    ).unpivot(index=["freq_gyro"], on=["gyro_y", "gyro_x", "gyro_z"]).filter(pl.col('value')< 100)
    return (
        accel_data,
        fft_accel_x,
        fft_accel_y,
        fft_accel_z,
        fft_gyro_x,
        fft_gyro_y,
        fft_gyro_z,
        freq_accel,
        freq_gyro,
        gyro_data,
        nyquist_frequency,
        sample_rate,
    )


@app.cell
def __():
    return


@app.cell
def __(accel_data, alt):
    accel_chart = (
        alt.Chart(accel_data)
        .mark_line()
        .encode(x="freq_accel:Q", y="value:Q", color="variable:N")
        .properties(title="Accelerometer FFT")
    )
    accel_chart.show()
    return accel_chart,


@app.cell
def __(alt, gyro_data):
    gyro_chart = (
        alt.Chart(gyro_data)
        .mark_line()
        .encode(x="freq_gyro:Q", y="value:Q", color="variable:N")
        .properties(title="Gyroscope FFT")
    )
    gyro_chart.show()
    return gyro_chart,


@app.cell
def __(mo):
    mo.md("""## Survey Analysis""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Other Analysis

        - Distance from optimal path?
        -
        """
    )
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
