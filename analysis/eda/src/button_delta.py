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

    alt.data_transformers.enable("marimo_csv")
    return (
        Path,
        Prototype,
        Task,
        alt,
        combine_dataset,
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
def __(Path, mo):
    data_dir = Path("./Data/")
    participants = [p.name[1:] for p in data_dir.glob("P*") if p.is_dir()]
    participants
    participant_id = mo.ui.dropdown(
        participants, value="8001", label="participant"
    )

    mo.md(f"# Choose participant\n{participant_id}")
    return data_dir, participant_id, participants


@app.cell
def __(data_dir, participant_id, read_trials):
    participant_dir = data_dir / f"P{participant_id.selected_key}"
    study_df = read_trials(participant_dir)
    return participant_dir, study_df


@app.cell
def __(Prototype, Task, pl, study_df):
    window = 1.25
    TESTING_PTY = Prototype.WATCH.value

    nb = (
        study_df.filter(pl.col("Task").eq(Task.NBACK))
        .select(
            [
                "ScenarioTime",
                "A escooter accel",
                "velocity_magnitude",
                "ws_action",
                "ws_value",
                "Prototype",
            ]
        )
        .with_row_index()
    )

    # label each button press for each prototype with a count
    nb = nb.with_columns(
        [
            pl.when(pl.col("ws_action").eq("NBACK_CLIENT_RESPONSE"))
            .then(pl.col("ScenarioTime"))
            .otherwise(None)
            .alias("button_press")
        ]
    )

    nb = nb.with_columns(
        [
            pl.col("button_press")
            .fill_null(strategy="forward")
            .over("Prototype")
            .alias("last_event_timestamp")
            .fill_null(0),
            pl.col("button_press")
            .shift(-1)
            .alias("next_event_timestamp")
            .fill_null(strategy="backward")
            .over("Prototype"),
            (
                pl.col("ScenarioTime")
                - pl.col("button_press").fill_null(strategy="forward")
            )
            .over("Prototype")
            .alias("time_since_last_event"),
        ]
    )

    nb = nb.with_columns(
        [
            (pl.col("next_event_timestamp") - pl.col("ScenarioTime")).alias(
                "time_until_next_event"
            )
        ]
    )


    nb = nb.with_columns(
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
            pl.col("velocity_magnitude")
            .diff()
            .rolling_mean(90)
            .over("Prototype")
            .alias("acc"),
            pl.col("velocity_magnitude")
            .rolling_mean(30)
            .over("Prototype")
            .alias("smooth_vel"),
        ]
    )

    nb.filter(
        (pl.col("ScenarioTime") > 7.0) & (pl.col("Prototype") == TESTING_PTY)
    )
    return TESTING_PTY, nb, window


@app.cell
def __(alt, nb, pl):
    selection = alt.selection_point(fields=["Prototype"])
    chart = (
        alt.Chart(nb)
        .mark_line()
        .encode(
            x="ScenarioTime",
            y="smooth_vel",
            color="Prototype",
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.05)),
        )
        .properties(width=600)
    ).add_params(selection)

    numbers = (
        alt.Chart(nb.filter(pl.col("ws_action").eq("NBACK_DIGIT")))
        .mark_point(size=160, shape="triangle", filled=True)
        .encode(
            alt.X("ScenarioTime"),
            alt.Y("smooth_vel"),
            color="Prototype",
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.05)),
        )
        .add_params(selection)
    )

    presses = (
        alt.Chart(nb.filter(pl.col("ws_action").eq("NBACK_CLIENT_RESPONSE")))
        .mark_circle(size=90)
        .encode(
            alt.X("ScenarioTime"),
            alt.Y("smooth_vel"),
            color="Prototype",
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.05)),
        )
        .add_params(selection)
    )

    (chart + (presses + numbers)).interactive()
    return chart, numbers, presses, selection


@app.cell
def __(mo):
    mo.md("""## Response Timing""")
    return


@app.cell
def __(Task, data_dir, pl):
    dat = pl.read_parquet(data_dir / "*.parquet")
    data = dat.filter(pl.col("Task").ne(Task.PRACTICE))
    return dat, data


@app.cell
def __(data, pl):
    timings = (
        data.filter(
            pl.col("ws_action").eq("NBACK_SERVER_RESPONSE")
            | pl.col("ws_action").eq("NBACK_TIMEOUT")
            | pl.col("ws_action").eq("NBACK_DIGIT")
        )
        .sort(["participantID", 'Prototype',"ScenarioTime"])
        .filter( #awaiting kyon fix in the data
            (
                pl.col("participantID").ne("P2579")
                | pl.col("Prototype").ne("Footbutton")
            )
        )
    )
    return timings,


@app.cell
def __():
    # timings.select(
    #     [
    #         pl.col("ws_action")
    #         .shift()
    #         .over(["Prototype", "participantID"])
    #         .alias("shifted"),
    #         pl.col("*"),
    #     ]
    # ).filter(pl.col("shifted").eq(pl.col("ws_action"))).select(
    #     [
    #         "ScenarioTime",
    #         "Websocket_message_timestamp",
    #         "Prototype",
    #         "ws_action",
    #         "ws_value",
    #         "participantID",
    #     ]
    # )
    return


@app.cell
def __():
    # timings.select('ScenarioTime', 'ws_action', 'participantID', "Prototype").with_columns(pl.col('ScenarioTime').diff().over(['participantID', 'Prototype']).alias('diff'))
    return


@app.cell
def __(pl, timings):
    df = timings.group_by(["Prototype", "participantID"]).agg(pl.col('ws_action').value_counts()).explode('ws_action').unnest('ws_action')
    return df,


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md("""### timeout percentage""")
    return


@app.cell
def __(df, pl):
    (df.group_by('Prototype').agg([
            (pl.col('count').filter(pl.col('ws_action') == 'NBACK_TIMEOUT').sum().alias('TIMEOUT_COUNT')),
            (pl.col('count').filter(pl.col('ws_action') == 'NBACK_DIGIT').sum().alias('DIGIT_COUNT'))
        ])
        .with_columns([
            (pl.when(pl.col('DIGIT_COUNT') != 0)
             .then(pl.col('TIMEOUT_COUNT') / pl.col('DIGIT_COUNT') * 100)
             .otherwise(None)
             .alias('TIMEOUT_PERCENTAGE'))
        ])
        .select(['Prototype', 'TIMEOUT_PERCENTAGE'])
        .sort('TIMEOUT_PERCENTAGE', descending=True))
    return


@app.cell
def __(mo):
    mo.md("""### Comparing timing""")
    return


@app.cell
def __(pl, timings):
    timings.group_by(['participantID', 'Prototype']).agg(pl.col('ScenarioTime').diff())
    return


@app.cell
def __(pl, timings):
    timings.select('ScenarioTime','Prototype', 'ws_action', 'ws_value','participantID', pl.col('ScenarioTime').shift().over(['Prototype', 'participantID']).alias('shift')).filter(pl.col('ws_action').ne('NBACK_DIGIT')).with_columns([
        (pl.col('ScenarioTime')-pl.col('shift')).alias('responseTime')
    ]).group_by('Prototype').agg([
        pl.col('responseTime').mean().alias('mean response time'),
        # pl.col('responseTime').median().alias('median response time'),
        pl.col('responseTime').std().alias('std response time'),

    ])
    return


@app.cell
def __(mo):
    mo.md("""scatter plot with velocity in time frame?""")
    return


@app.cell
def __(mo):
    mo.md(r"""## song stuff?""")
    return


@app.cell
def __(Task, dat, pl):
    song = dat.filter(pl.col('Task').eq(Task.SONG))
    prssed = ["SONG_NEXT_PREVIOUS", "SONG_USER_PLAY_PAUSE", "SONG_OOB"]
    song = song.filter(pl.col("ws_action").is_in(prssed)).with_columns(pl.col('ws_value').abs())
    return prssed, song


@app.cell
def __(pl, song):
    print(song.group_by('Prototype').agg(pl.col('ws_value').sum().alias('counts')).sort('counts'))
    return


@app.cell
def __(song):
    song['ws_action'].value_counts()
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
