import marimo

__generated_with = "0.7.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import polars as pl
    import altair as alt
    from pathlib import Path
    from base64 import b64decode, b64encode
    import struct
    import numpy as np
    from scipy.signal import butter, filtfilt
    from scipy.fft import fft, fftfreq
    from PIL import Image
    from io import BytesIO
    return (
        BytesIO,
        Image,
        Path,
        alt,
        b64decode,
        b64encode,
        butter,
        fft,
        fftfreq,
        filtfilt,
        mo,
        np,
        pl,
        struct,
    )


@app.cell
def __(BytesIO, Image, Path, b64encode, pl):
    data_path = Path("./src/Data/")
    sample_data = data_path / "Sample_data.csv"
    df_raw = pl.read_csv(sample_data, separator=";")
    pil_image = Image.open(data_path / 'map.png')
    output = BytesIO()
    pil_image.save(output, format='PNG')
    b64_image = "data:image/png;base64," + b64encode(output.getvalue()).decode()
    return b64_image, data_path, df_raw, output, pil_image, sample_data


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
def __(df):
    df.head(4)
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
                alt.Color("A escooter steering:Q", scale=alt.Scale(scheme="blueorange")),
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

    row1 & timeline
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
            "PSD_x": fft_accel_x**2 / sample_rate,
            "PSD_y": fft_accel_y**2 / sample_rate,
            "PSD_z": fft_accel_z**2 / sample_rate,
            "freq_accel": freq_accel,
            "time": df["ScenarioTime"].drop_nulls(),
        }
    ).unpivot(
        index=["freq_accel", "time"],
        on=["accel_y", "accel_x", "accel_z", "PSD_x", "PSD_y", "PSD_z"],
    )
    # .filter((pl.col('value')< 100) & (pl.col('freq_accel') >0))

    gyro_data = pl.DataFrame(
        {
            "gyro_x": fft_gyro_x,
            "gyro_y": fft_gyro_y,
            "gyro_z": fft_gyro_z,
            "PSD_x": fft_gyro_x**2 / sample_rate,
            "PSD_y": fft_gyro_y**2 / sample_rate,
            "PSD_z": fft_gyro_z**2 / sample_rate,
            "freq_gyro": freq_gyro,
            "time": df["ScenarioTime"].drop_nulls(),
        }
    ).unpivot(
        index=["freq_gyro"],
        on=["gyro_y", "gyro_x", "gyro_z", "PSD_y", "PSD_x", "PSD_z"],
    )
    # .filter((pl.col('value')< 100) & (pl.col('freq_gyro') >0))
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
def __(accel_data, alt, pl):
    accel_chart = (
        alt.Chart(
            accel_data.filter(
                (pl.col("value") < 100)
                & (pl.col("freq_accel") > 0)
                & (pl.col("variable").str.contains("accel"))
            )
        )
        .mark_line()
        .encode(x="freq_accel:Q", y="value:Q", color="variable:N")
        .properties(title="Accelerometer FFT")
    )

    PSD_accel_chart = (
        alt.Chart(
            accel_data.filter(
                (pl.col("value") < 1000)
                & (pl.col("freq_accel") > 0)
                & (pl.col("variable").str.contains("PSD"))
            )
        )
        .mark_line()
        .encode(x="freq_accel:Q", y="value:Q", color="variable:N")
        .properties(title="Accelerometer PSD")
    )

    accel_chart | PSD_accel_chart
    return PSD_accel_chart, accel_chart


@app.cell
def __(alt, gyro_data, pl):
    gyro_chart = (
        alt.Chart(
            gyro_data.filter(
                (pl.col("value") < 100)
                & (pl.col("freq_gyro") > 0)
                & (pl.col("variable").str.contains("gyro"))
            )
        )
        .mark_line()
        .encode(x="freq_gyro:Q", y="value:Q", color="variable:N")
        .properties(title="Gyroscope FFT")
    )

    PSD_gyro_chart = (
        alt.Chart(
            gyro_data.filter(
                (pl.col("value") < 100)
                & (pl.col("freq_gyro") > 0)
                & (pl.col("variable").str.contains("PSD"))
            )
        )
        .mark_line()
        .encode(x="freq_gyro:Q", y="value:Q", color="variable:N")
        .properties(title="Gyroscope PSD")
    )
    gyro_chart | PSD_gyro_chart
    return PSD_gyro_chart, gyro_chart


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
    # df[["A escooter acc_x", "A escooter acc_y", "A escooter acc_z"]].plot()
    return


@app.cell
def __(butter, df, filtfilt, np, pl, sample_rate):
    def butterworth_filter(data, cutoff, fs, order=5, btype="low"):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        y = filtfilt(b, a, data)
        return y


    low_cutoff = 2
    low_x = butterworth_filter(df["A escooter acc_x"].drop_nans().drop_nulls().to_numpy()-9.8, low_cutoff, sample_rate)
    low_y = butterworth_filter(df["A escooter acc_y"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate)
    low_z = butterworth_filter(df["A escooter acc_z"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate)

    high_x = butterworth_filter(df["A escooter acc_x"].drop_nans().drop_nulls().to_numpy()-9.8, low_cutoff, sample_rate, btype="high")
    high_y = butterworth_filter(df["A escooter acc_y"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate, btype="high")
    high_z = butterworth_filter(df["A escooter acc_z"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate, btype="high")

    accel_filter_testing = pl.DataFrame({
        "time": df['ScenarioTime'].drop_nans().drop_nulls(),
        'x_pos': df['x_pos'].drop_nans().drop_nulls(),
        'z_pos': df['z_pos'].drop_nans().drop_nulls(),
        "acc_x": df["A escooter acc_x"].drop_nans().drop_nulls()- 9.8,
        "acc_y": df["A escooter acc_y"].drop_nans().drop_nulls(),
        "acc_z": df["A escooter acc_x"].drop_nans().drop_nulls(),
        "low_x": low_x,
        "low_y": low_y,
        "low_z": low_z,
        "low_mag": np.sqrt(low_x**2 + low_y**2 + low_z**2),
        "high_x": high_x,
        "high_y": high_y,
        "high_z": high_z,
        "high_mag": np.sqrt(high_x**2 + high_y**2 + high_z**2)

    })

    accel_filter_testing = accel_filter_testing.with_columns(
        std_low_mag = pl.col('low_mag').rolling_std(window_size=5).fill_null(0),
        std_high_mag = pl.col('high_mag').rolling_std(window_size=5).fill_null(0),

    )
    return (
        accel_filter_testing,
        butterworth_filter,
        high_x,
        high_y,
        high_z,
        low_cutoff,
        low_x,
        low_y,
        low_z,
    )


@app.cell
def __(mo):
    mo.md("""### Acceleration data split by high and low frequencies""")
    return


@app.cell
def __(accel_filter_testing, alt):
    base2 = (
        alt.Chart(accel_filter_testing)
        .mark_circle()
        .encode(
            x="x_pos",
            y="z_pos",
            color = alt.Color("std_high_mag:Q", scale=alt.Scale(scheme="blues")),
        )
    )
    alt.hconcat(base2, base2.encode(color = alt.Color("std_low_mag:Q", scale=alt.Scale(scheme="blues")))).resolve_scale(color='independent')
    return base2,


@app.cell
def __(
    butterworth_filter,
    df,
    high_x,
    high_y,
    high_z,
    low_cutoff,
    low_x,
    low_y,
    low_z,
    np,
    pl,
    sample_rate,
):
    gyro_low_x = butterworth_filter(df["A escooter rot_x"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate)
    gyro_low_y = butterworth_filter(df["A escooter rot_y"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate)
    gyro_low_z = butterworth_filter(df["A escooter rot_z"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate)

    gyro_high_x = butterworth_filter(df["A escooter rot_x"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate, btype="high")
    gyro_high_y = butterworth_filter(df["A escooter rot_y"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate, btype="high")
    gyro_high_z = butterworth_filter(df["A escooter rot_z"].drop_nans().drop_nulls().to_numpy(), low_cutoff, sample_rate, btype="high")

    gyro_filter_testing = pl.DataFrame({
        "time": df['ScenarioTime'].drop_nans().drop_nulls(),
        'x_pos': df['x_pos'].drop_nans().drop_nulls(),
        'z_pos': df['z_pos'].drop_nans().drop_nulls(),
        "rot_x": df["A escooter rot_x"].drop_nans().drop_nulls(),
        "rot_y": df["A escooter rot_y"].drop_nans().drop_nulls(),
        "rot_z": df["A escooter rot_x"].drop_nans().drop_nulls(),
        "low_x": gyro_low_x,
        "low_y": gyro_low_y,
        "low_z": gyro_low_z,
        "low_mag": np.sqrt(low_x**2 + low_y**2 + low_z**2),
        "high_x": gyro_high_x,
        "high_y": gyro_high_y,
        "high_z": gyro_high_z,
        "high_mag": np.sqrt(high_x**2 + high_y**2 + high_z**2)

    })

    gyro_filter_testing = gyro_filter_testing.with_columns(
        std_low_mag = pl.col('low_mag').rolling_std(window_size=5).fill_null(0),
        std_high_mag = pl.col('high_mag').rolling_std(window_size=5).fill_null(0),

    )
    return (
        gyro_filter_testing,
        gyro_high_x,
        gyro_high_y,
        gyro_high_z,
        gyro_low_x,
        gyro_low_y,
        gyro_low_z,
    )


@app.cell
def __(mo):
    mo.md("""### Gyro data split by high and low frequencies""")
    return


@app.cell
def __(alt, gyro_filter_testing):
    base3 = (
        alt.Chart(gyro_filter_testing)
        .mark_circle()
        .encode(
            x="x_pos",
            y="z_pos",
            color = alt.Color("std_high_mag:Q", scale=alt.Scale(scheme="blues")),
        )
    )
    alt.hconcat(base3, base3.encode(color = alt.Color("std_low_mag:Q", scale=alt.Scale(scheme="blues")))).resolve_scale(color='independent')
    return base3,


@app.cell
def __(mo):
    mo.md("""### Some map overlay testing""")
    return


@app.cell
def __(alt, df):
    map = (
        alt.Chart(df)
        .mark_circle(size=15)
        .encode(
            alt.X("x_pos:Q"),
            alt.Y("z_pos:Q"),
            tooltip=['x_pos:Q','z_pos:Q' ]
        )
    )
    map
    return map,


@app.cell
def __(alt, b64_image, map, pl):
    PLOT_SIZE = 370

    image_chart = alt.Chart(pl.DataFrame({'url': [b64_image]})).mark_image(
        width=alt.expr('width'),
        height=alt.expr('height')
    ).encode(
        url='url:N',
         x=alt.XDatum(2).scale(domain=[-100,100]),
        y=alt.YDatum(-4).scale(domain=[-100,100]),
    ).properties(
        width=PLOT_SIZE,
        height=PLOT_SIZE,
    )
    image_chart + map
    return PLOT_SIZE, image_chart


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
