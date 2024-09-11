import marimo

__generated_with = "0.8.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from pathlib import Path
    import polars as pl
    import json
    import altair as alt
    from utils.survey_tools import get_participant_data, get_flow_data, get_order
    from utils.process_sim_csv import (
        read_trials,
        Task,
        Prototype,
        process_csv,
        get_scenario,
        scenario_df,
        combine_dataset,
    )
    from utils.plotting import downsample

    data_dir = Path("./Data/")
    alt.data_transformers.enable("marimo_csv")
    return (
        Path,
        Prototype,
        Task,
        alt,
        combine_dataset,
        data_dir,
        downsample,
        get_flow_data,
        get_order,
        get_participant_data,
        get_scenario,
        json,
        mo,
        pl,
        process_csv,
        read_trials,
        scenario_df,
    )


@app.cell
def __(Task, data_dir, pl):
    data = pl.read_parquet(data_dir / "*.parquet")
    data = data.filter(pl.col("Task").ne(Task.PRACTICE))
    return data,


@app.cell
def __(mo):
    mo.md("""## Naive gyro""")
    return


@app.cell
def __(data, pl):
    gyro_rms = (
        data.group_by(["participantID", "Task", "Prototype"])
        .agg((pl.col("gyro_magnitude") ** 2).mean().sqrt().alias("gyro_rms"))
        .group_by(["Prototype", "Task"])
        .agg(
            [
                pl.col("gyro_rms").mean().alias("mean"),
                pl.col("gyro_rms").std().alias("std"),
            ]
        )
    )
    return gyro_rms,


@app.cell
def __(gyro_rms):
    gyro_rms
    return


@app.cell
def __(alt, gyro_rms):
    base = alt.Chart(gyro_rms).encode(
        x=alt.X("Prototype:N", axis=alt.Axis(title="Task")),
        color=alt.Color("Prototype:N", legend=alt.Legend(title="Prototype")),
        xOffset="Task:N",
    )

    # Create the bar chart
    bars = base.mark_bar().encode(y=alt.Y("mean:Q", axis=alt.Axis(title="Mean")))

    # Create the error bars
    error_bars = base.mark_errorbar(extent="ci").encode(
        y=alt.Y("mean:Q"), yError=alt.YError("std:Q")
    )

    # Combine the bars and error bars
    chart = (bars + error_bars).properties(
        width=400, height=300, title="Mean Values with Standard Deviation"
    )

    # Display the chart
    chart
    return bars, base, chart, error_bars


@app.cell
def __():
    # alt.Chart(gyro_rms).mark_bar().encode(
    #     alt.X("Prototype"),
    #     alt.Y("gyro_rms"),
    #     alt.Color("Task"),
    #     # tooltip="participantID",
    #     xOffset="Task:N",
    # )
    return


@app.cell
def __():
    # def remove_outliers(df, column, lower_quantile=0.25, upper_quantile=0.75, k=1.5):
    #     # Calculate Q1, Q3, and IQR
    #     q1 = df[column].quantile(lower_quantile)
    #     q3 = df[column].quantile(upper_quantile)
    #     iqr = q3 - q1

    #     # Calculate lower and upper bounds
    #     lower_bound = q1 - k * iqr
    #     upper_bound = q3 + k * iqr

    #     # Filter out the outliers
    #     return df.filter((pl.col(column) >= lower_bound) & (pl.col(column) <= upper_bound))
    # gyro_rms_no_outliers = remove_outliers(gyro_rms, 'gyro_rms').group_by(['Prototype', 'Task']).agg(pl.col('gyro_rms').mean())
    return


@app.cell
def __(mo):
    mo.md("""## setup windows""")
    return


@app.cell
def __(pl):
    def windows(df: pl.DataFrame, window_action, window: float):
        df = df.with_row_index()
        # break out button presses into a column
        df = df.with_columns(
            [
                pl.when(pl.col("ws_action").eq(window_action))
                .then(pl.col("ScenarioTime"))
                .otherwise(None)
                .alias("button_press")
            ]
        )

        df = df.with_columns(
            [
                pl.col("button_press")
                .over(["Prototype", "participantID"])
                .fill_null(strategy="forward")
                .alias("last_event_timestamp")
                .fill_null(0),
                pl.col("button_press")
                .over(["Prototype", "participantID"])
                .shift(-1)
                .alias("next_event_timestamp")
                .fill_null(strategy="backward"),
                (
                    pl.col("ScenarioTime").over(["Prototype", "participantID"])
                    - pl.col("button_press")
                    .over(["Prototype", "participantID"])
                    .fill_null(strategy="forward")
                ).alias("time_since_last_event"),
            ]
        )

        df = df.with_columns(
            [
                (pl.col("next_event_timestamp") - pl.col("ScenarioTime")).alias(
                    "time_until_next_event"
                )
            ]
        )

        df = df.with_columns(
            [
                pl.when(
                    (pl.col("time_until_next_event") <= window)
                    & (pl.col("time_until_next_event") > 0)
                )
                .then(-1)
                .when(
                    (pl.col("time_since_last_event") <= window)
                    & (pl.col("time_since_last_event") > 0)
                )
                .then(1)
                .otherwise(0)
                .alias("event_window"),
                pl.when(
                    (pl.col("time_until_next_event") <= window)
                    & (pl.col("time_until_next_event") > 0)
                )
                .then(1)
                .when(
                    (pl.col("time_since_last_event") <= window)
                    & (pl.col("time_since_last_event") >= 0)
                )
                .then(1)
                .otherwise(0)
                .alias("event"),
            ]
        )
        df = df.with_columns(
            pl.col("event")
            .over(["Prototype", "participantID"])
            .diff()
            .ne(0)
            .cum_sum()
        )
        return df
    return windows,


@app.cell
def __(CENTER, Task, WINDOW, data, pl, windows):
    nbacks = data.filter(pl.col("Task").eq(Task.NBACK))
    nbacks = windows(nbacks, CENTER, WINDOW)

    nbacks = nbacks.with_columns(
        [
            (
                pl.col("A escooter acc_x")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_x"),
            (
                pl.col("A escooter acc_y")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_y"),
            (
                pl.col("A escooter acc_z")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_z"),
        ]
    )
    nbacks = nbacks.with_columns(
        [
            (pl.col("jerk_x") ** 2 + pl.col("jerk_y") ** 2 + pl.col("jerk_z") ** 2)
            .sqrt()
            .alias("jerk_magnitude")
        ]
    )

    # .filter(pl.col("event_window").ne(0))
    # .group_by(["Prototype", "Task", "participantID", "event_window", "event"])
    nbacks
    return nbacks,


@app.cell
def __(Prototype, nbacks, pl):
    nbacks.filter(
        (
            (pl.col("participantID").eq("P7895"))
            & pl.col("Prototype").eq(Prototype.PHONE.value)
        )
    ).select(
        [
            "ScenarioTime",
            "last_event_timestamp",
            "next_event_timestamp",
            "time_since_last_event",
            "event_window",
            "event",
        ]
    )
    return


@app.cell
def __(nbacks, pl):
    test = (
        nbacks.filter(pl.col("event_window").ne(0))
        .group_by(["Prototype", "Task", "participantID", "event_window", "event"])
        .agg((pl.col("gyro_magnitude") ** 2).mean().sqrt().alias("gyro_rms"))
        .sort("event", "event_window")
        .with_columns(pl.col("gyro_rms").diff().alias("diff"))
        .filter(pl.col("event_window").eq(1))
    )
    test
    return test,


@app.cell
def __(pl, test):
    test.group_by(
        [
            "Prototype",
        ]
    ).agg(
        [
            pl.col("diff").mean().alias("average_gyro_difference"),
            pl.col("diff").std().alias("std"),
        ]
    ).plot.bar(x="Prototype", y="average_gyro_difference")
    return


@app.cell
def __(nbacks, pl):
    (
        nbacks.filter(pl.col("event_window").ne(0))
        .group_by(["Prototype", "Task", "participantID", "event_window", "event"])
        .agg((pl.col("gyro_magnitude") ** 2).mean().sqrt().alias("gyro_rms"))
        .sort("event", "event_window")
        .with_columns(pl.col("gyro_rms").diff().alias("diff"))
    )
    return


@app.cell
def __(nbacks, pl):
    jerk = nbacks.with_columns(
        [
            (
                pl.col("A escooter acc_x")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_x"),
            (
                pl.col("A escooter acc_y")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_y"),
            (
                pl.col("A escooter acc_z")
                .over(["Prototype", "Task", "participantID"])
                .diff()
                / pl.col("ScenarioTime")
            ).alias("jerk_z"),
        ]
    )
    jerk = jerk.with_columns(
        [
            (pl.col("jerk_x") ** 2 + pl.col("jerk_y") ** 2 + pl.col("jerk_z") ** 2)
            .sqrt()
            .alias("jerk_magnitude")
        ]
    )

    # .filter(pl.col("event_window").ne(0))
    # .group_by(["Prototype", "Task", "participantID", "event_window", "event"])
    return jerk,


@app.cell
def __(jerk, pl):
    jerk.filter(pl.col("event_window").ne(0)).group_by(
        ["Prototype", "event_window"]
    ).agg(
        [
            pl.col("jerk_magnitude").mean().alias("mean"),
            pl.col("jerk_magnitude").std().alias("std"),
        ]
    ).sort("Prototype", "event_window")
    return


@app.cell
def __(jerk, pl):
    test_jerk = (
        jerk.group_by(
            ["Prototype", "Task", "participantID", "event_window", "event"]
        )
        .agg((pl.col("jerk_magnitude")).abs().max().alias("jerk_mean"))
        .sort("event", "event_window")
        .with_columns(pl.col("jerk_mean").diff().alias("diff"))
        .filter(pl.col("event_window").eq(1))
    )
    test_jerk
    return test_jerk,


@app.cell
def __(pl, test_jerk):
    test_jerk.group_by(
        [
            "Prototype",
        ]
    ).agg(
        [
            pl.col("diff").mean().alias("average_gyro_difference"),
            pl.col("diff").std().alias("std"),
        ]
    ).plot.bar(x="Prototype", y="average_gyro_difference")
    return


@app.cell
def __(Prototype, Task, mo):
    PARTICIPANT = "P8001"
    TASK = Task.NBACK.value
    PROTO = Prototype.PHONE.value
    mo.md(f"## View single participant: {PARTICIPANT}, {TASK}, {PROTO}")
    return PARTICIPANT, PROTO, TASK


@app.cell
def __(PARTICIPANT, PROTO, TASK, data, pl):
    individual = data.filter(
        (pl.col("Task").eq(TASK))
        & (pl.col("Prototype").eq(PROTO))
        & (pl.col("participantID").eq(PARTICIPANT))
    )
    individual = individual.with_columns(
        [
            pl.col("A escooter acc_x").rolling_std(100).alias("accel_std_x"),
            pl.col("A escooter acc_y").rolling_std(100).alias("accel_std_y"),
            pl.col("A escooter acc_z").rolling_std(100).alias("accel_std_z"),
            pl.col("A escooter rot_x").rolling_std(100).alias("rot_std_x"),
            pl.col("A escooter rot_y").rolling_std(100).alias("rot_std_y"),
            pl.col("A escooter rot_z").rolling_std(100).alias("rot_std_z"),
            pl.col("velocity_magnitude").rolling_mean(50).alias("vel_mean"),
            pl.col("velocity_magnitude").rolling_std(50).alias("vel_std")
        ]
    )
    individual
    return individual,


@app.cell
def __(alt, individual, pl):
    Y = 'vel_mean'

    stdy = (
        alt.Chart(individual)
        .mark_line()
        .encode(
            alt.X("ScenarioTime:Q"), alt.Y(f"{Y}:Q"), alt.Color("Prototype")
        )
    )


    numbers = (
        alt.Chart(individual.filter(pl.col("ws_action").eq("NBACK_DIGIT")))
        .mark_circle(size=90, shape="triangle", filled=True, color="red")
        .encode(
            alt.X("ScenarioTime"),
            alt.Y(f"{Y}"),
        )
    )

    presses = (
        alt.Chart(
            individual.filter(pl.col("ws_action").eq("NBACK_CLIENT_RESPONSE"))
        )
        .mark_circle(size=90, color="green")
        .encode(
            alt.X("ScenarioTime"),
            alt.Y(Y),
        )
    )

    # stdy[0].properties(width=700).interactive()

    (stdy + numbers + presses).properties(width=600).interactive()
    return Y, numbers, presses, stdy


@app.cell
def __(nbacks, pl):
    test_std = (
        nbacks.filter(
            (
                pl.col("event_window").ne(0)
                # & (pl.col("participantID").eq(PARTICIPANT))
            )
        )
        .group_by(["Prototype", "Task", "participantID", "event_window", "event"])
        .agg(
            [
                pl.col("A escooter acc_x").std().alias("acc_x_std"),
                pl.col("A escooter acc_y").std().alias("acc_y_std"),
                pl.col("A escooter acc_z").std().alias("acc_z_std"),
                pl.col("A escooter rot_x").std().alias("rot_x_std"),
                pl.col("A escooter rot_y").std().alias("rot_y_std"),
                pl.col("A escooter rot_z").std().alias("rot_z_std"),
                pl.col("A escooter acc_x").mean().alias("acc_x_mean"),
                pl.col("A escooter acc_y").mean().alias("acc_y_mean"),
                pl.col("A escooter acc_z").mean().alias("acc_z_mean"),
                pl.col("A escooter rot_x").mean().alias("rot_x_mean"),
                pl.col("A escooter rot_y").mean().alias("rot_y_mean"),
                pl.col("A escooter rot_z").mean().alias("rot_z_mean"),
                pl.col("A escooter acc_x").median().alias("acc_x_median"),
                pl.col("A escooter acc_y").median().alias("acc_y_median"),
                pl.col("A escooter acc_z").median().alias("acc_z_median"),
                pl.col("A escooter rot_x").median().alias("rot_x_median"),
                pl.col("A escooter rot_y").median().alias("rot_y_median"),
                pl.col("A escooter rot_z").median().alias("rot_z_median"),
                pl.col("accel_magnitude").mean().alias("accel_mean"),
                pl.col("accel_magnitude").median().alias("accel_median"),
                pl.col("accel_magnitude").std().alias("accel_std"),
                pl.col("gyro_magnitude").mean().alias("gyro_mean"),
                pl.col("gyro_magnitude").median().alias("gyro_median"),
                pl.col("gyro_magnitude").std().alias("gyro_std"),
                pl.col("jerk_magnitude").mean().alias("jerk_mean"),
                pl.col("jerk_magnitude").median().alias("jerk_median"),
                pl.col("jerk_magnitude").std().alias("jerk_std"),
                pl.col("A escooter steering")
                .pow(2)
                .sum()
                .alias("steering_energy"),
            ]
        )
        .sort("event", "event_window")
        # .with_columns(pl.col("jerk_mean").diff().alias("diff"))
        # .filter(pl.col("event_window").eq(1))
    )
    test_std = test_std.with_columns(
        [
            (
                pl.col("acc_x_std") ** 2
                + pl.col("acc_y_std") ** 2
                + pl.col("acc_z_std") ** 2
            )
            .sqrt()
            .alias("accel_std_mag"),
            (
                pl.col("rot_x_std") ** 2
                + pl.col("rot_y_std") ** 2
                + pl.col("rot_z_std") ** 2
            )
            .sqrt()
            .alias("gyro_std_mag"),
        ]
    )
    test_std = test_std.filter(
        pl.col("event").is_in(
            test_std.group_by("event")
            .agg(pl.count("event").alias("count"))
            .filter(pl.col("count") == 2)
            .select("event")
        )
    )
    return test_std,


@app.cell
def __():
    return


@app.cell
def __(pl, test_std):
    test_std.select([pl.col("Prototype"), pl.col("^.*_.*$").diff()]).filter(
        pl.col("event_window").eq(2)
    )
    return


@app.cell
def __(test_std):
    test_std
    return


@app.cell
def __():
    0.1096236469780945 - 0.1445138489554305
    return


app._unparsable_cell(
    r"""
        nbacks
    """,
    name="__"
)


@app.cell
def __():
    CENTER = "NBACK_CLIENT_RESPONSE"
    WINDOW = 0.75
    DEPENDANT = "gyro_std_mag"
    return CENTER, DEPENDANT, WINDOW


@app.cell
def __(DEPENDANT, alt, pl, test_std):
    combined = test_std.group_by(pl.col(["Prototype", "event_window"])).agg(
        pl.col(DEPENDANT).mean()
    )

    base_std = alt.Chart(test_std).encode(
        x=alt.X("event_window:N"),
        y=alt.Y(
            f"{DEPENDANT}:Q",
            axis=alt.Axis(title="Acceleration Magnitude Std Dev"),
        ),
        color=alt.Color("Prototype:N", legend=alt.Legend(title="Prototype")),
    )

    points = base_std.mark_point(size=60, opacity=0.15).encode(
        tooltip=["Prototype", "Task", "participantID", "event", "gyro_std_mag"]
    )


    # combined_lines = combined_base.mark_line(opacity=1).encode(detail="event")
    lines = base_std.mark_line(opacity=0.15).encode(detail="event")

    mean_lines = base_std.mark_line(size=3).encode(detail="Prototype")

    chart_std = (
        (points + lines)
        .properties(width=200, height=200)
        .facet(facet="Prototype", columns=3)
        .properties(
            title="Acceleration Magnitude Std Dev Comparison Before and After Event"
        )
    )

    # Display the chart_std
    chart_std.interactive()
    return base_std, chart_std, combined, lines, mean_lines, points


@app.cell
def __(test_std):
    test_std.select(['Prototype', 'participantID', 'event_window', 'event','accel_std_mag', 'gyro_std_mag'])
    return


@app.cell
def __(CENTER, DEPENDANT, alt, combined):
    combined_base = alt.Chart(combined).encode(
        x=alt.X("event_window:N"),
        y=alt.Y(f"{DEPENDANT}:Q"),
        color=alt.Color("Prototype:N", legend=alt.Legend(title="Prototype")),
    )

    combined_points = combined_base.mark_circle(
        size=100, color="purple", opacity=0.8
    ).encode(tooltip=["Prototype", DEPENDANT])

    c_lines = combined_base.mark_line().encode(detail="Prototype")

    (combined_points + c_lines).properties(
        width=300, title=f"before and after {CENTER}"
    ).interactive()
    return c_lines, combined_base, combined_points


@app.cell
def __(combined):
    combined
    return


@app.cell
def __(combined):
    combined
    return


@app.cell
def __(data, pl):
    df = data.group_by(["participantID", "Prototype", "Task"]).agg(
        [
            pl.col("accel_magnitude").std().alias("accel_std"),
            pl.col("gyro_magnitude").std().alias("gyro_std"),
            pl.col("velocity_magnitude").mean().alias("avg_vel"),
            pl.col("ScenarioTime").max(),
            pl.col("A escooter steering").pow(2).sum().alias("steering_energy"),
        ]
    )
    return df,


@app.cell
def __(Task, alt, df, pl):
    alt.Chart(df.filter(pl.col("Task").eq(Task.NBACK))).mark_point().encode(
        alt.X("gyro_std"), alt.Y("avg_vel"), alt.Color("Prototype")
    ).interactive()
    return


@app.cell
def __(df, pl):
    df.group_by("Prototype").agg(pl.col("steering_energy").std()).plot.bar(
        x="Prototype"
    )
    return


@app.cell
def __(df):
    df.plot.bar(x="Prototype", y="accel_std")
    return


@app.cell
def __(df, pl):
    df.group_by("Prototype").agg(pl.col("accel_std").mean()).plot.bar(
        x="Prototype"
    )
    return


@app.cell
def __(pl, test_std):
    filtered_df = test_std.filter(
        pl.col("event").is_in(
            test_std.group_by("event")
            .agg(pl.count("event").alias("count"))
            .filter(pl.col("count") == 2)
            .select("event")
        )
    )
    filtered_df
    return filtered_df,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
