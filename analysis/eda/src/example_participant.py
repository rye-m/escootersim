import marimo

__generated_with = "0.8.0"
app = marimo.App(width="full")


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
    )
    from utils.plotting import downsample
    return (
        Path,
        Prototype,
        Task,
        alt,
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
def __(data_dir, get_flow_data, get_participant_data, participant_id):
    participant_dir = data_dir / f"P{participant_id.selected_key}"

    survey_data_path = next(data_dir.glob("Scooterseim*"))
    participant_survey = get_participant_data(participant_id, survey_data_path)
    flow_map = get_flow_data(data_dir / "FlowMap.json")
    # study_order = get_order(participant_survey, flow_map)
    return flow_map, participant_dir, participant_survey, survey_data_path


@app.cell
def __(participant_dir, read_trials):
    study_df = read_trials(participant_dir)
    study_df.head()
    return study_df,


@app.cell
def __(mo):
    mo.md(
        """
        ## Looking at paths and timing
        You can click the lines to see each session isolated
        we do have to downsample to render plots on the web but thats fine for this.
        """
    )
    return


@app.cell
def __(Task, alt, downsample, study_df):
    downsample(study_df).shape
    selection = alt.selection_point(fields=["combined"])
    nearest = alt.selection_point(
        nearest=True, on="pointerover", fields=["ScenarioTime"], empty=False
    )

    base1 = (
        (
            alt.Chart(
                downsample(study_df)[
                    "ScenarioTime",
                    "x_pos",
                    "z_pos",
                    "Task",
                    "Prototype",
                    "accel_magnitude",
                    "velocity_magnitude",
                ]
            )
        )
        .encode(
            color=alt.Color(
                "combined:N", legend=alt.Legend(title="Task + Prototype")
            ),
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.1)),
            tooltip=["x_pos:Q", "z_pos:Q", "combined:N"],
        )
        .transform_calculate(combined='datum.Task + " - " + datum.Prototype')
    ).add_params(selection)

    base_xz = base1.mark_circle(size=10).encode(
        alt.X("x_pos:Q").scale(domain=[-100, 100]),
        alt.Y("z_pos:Q").scale(domain=[-100, 100]),
    )

    rolling_window = 12
    velocity_base = (
        base1.mark_line(size=4)
        .encode(alt.X("ScenarioTime"), alt.Y("velocity_magnitude"))
        .transform_window(
            rolling_mean_velocity="mean(velocity_magnitude)",
            frame=[-rolling_window, rolling_window],
        )
        .encode(y="rolling_mean_velocity:Q")
        .properties(title="velocity")
    )

    velocity_song = velocity_base.transform_filter(
        alt.datum.Task == Task.SONG.value
    )
    velocity_nback = velocity_base.transform_filter(
        alt.datum.Task == Task.NBACK.value
    )

    song = base_xz.transform_filter(
        (alt.datum.Task == Task.SONG.value)
    ).properties(title="Song Task")
    nback = base_xz.transform_filter(
        (alt.datum.Task == Task.NBACK.value)
    ).properties(title="Nback Task")


    (song | velocity_song.properties(width=675)) & (
        nback | velocity_nback.properties(width=675)
    )
    return (
        base1,
        base_xz,
        nback,
        nearest,
        rolling_window,
        selection,
        song,
        velocity_base,
        velocity_nback,
        velocity_song,
    )


@app.cell
def __(Prototype, alt, downsample, pl, study_df):
    facet_base1 = alt.Chart(
        downsample(study_df.filter(pl.col("Prototype") != Prototype.CONTROL))[
            "ScenarioTime",
            "x_pos",
            "z_pos",
            "Task",
            "Prototype",
            "A escooter accel",
            "velocity_magnitude",
        ]
    )
    return facet_base1,


@app.cell
def __(alt, facet_base1, rolling_window):
    velocity_facet = (
        facet_base1.mark_line(size=4)
        .encode(
            alt.X("ScenarioTime"),
            alt.Y("velocity_magnitude"),
            alt.Color("Task"),
            alt.Facet("Prototype", columns=3),
        )
        .transform_window(
            rolling_mean_velocity="mean(velocity_magnitude)",
            frame=[-rolling_window, rolling_window],
        )
        .encode(y="rolling_mean_velocity:Q")
    )
    velocity_facet
    return velocity_facet,


@app.cell
def __(alt, facet_base1):
    facet_base1.mark_bar().encode(
        alt.X("Prototype"),
        alt.Y("median(velocity_magnitude)"),
        alt.Color("Task"),
        xOffset="Task:N",
    )
    return


@app.cell
def __(alt, facet_base1):
    acceleration_facet = facet_base1.mark_circle().encode(
        alt.X("x_pos").scale(domain=[-100, 100]),
        alt.Y("z_pos").scale(domain=[-100, 100]),
        alt.Color("Task"),
        alt.Facet("Prototype", columns=3),
    )
    acceleration_facet
    return acceleration_facet,


@app.cell
def __(alt, facet_base1):
    accel_window = 3
    accel_facet = (
        facet_base1.mark_line(size=4)
        .encode(
            alt.X("ScenarioTime"),
            alt.Y("A escooter accel"),
            alt.Color("Task"),
            alt.Facet("Prototype", columns=3),
        )
        .transform_window(
            rolling_mean_accel="mean(A escooter accel)",
            frame=[-accel_window, accel_window],
        )
        .encode(y="rolling_mean_accel:Q")
    )
    accel_facet
    return accel_facet, accel_window


@app.cell
def __(Prototype, Task, scenario_df, study_df):
    test_df = scenario_df(study_df, task=Task.SONG, prototype=Prototype.VOICE)
    return test_df,


@app.cell
def __(test_df):
    test_df["Websocket_message_action"].drop_nulls().to_list()
    return


@app.cell
def __():
    import re

    nback_look_up = (
        [
            ("\s[0-9]", "N_BACK_DIGIT"),
            ("yes|no", "N_BACK_CLIENT_RESPONSE"),
            ("Accuracy=", "N_BACK_CLIENT_ACCURACY"),
            ("Total=", "N_BACK_CLIENT_TOTAL"),
            ("end", "N_BACK_MCU_END"),
            ("begin", "N_BACK_MCU_BEGIN")(
                "start_nback", "N_BACK_START_COMMAND_BY_RESEARCHER"
            ),
            ("finish_nback", "N_BACK_END_COMMAND_BY_RESEARCHER")("ping", "PING"),
            ("correct|incorrect", "N_BACK_SERVER_RESPONSE"),
        ],
    )

    song_look_up = [("play", "SONG_PLAY")]
    return nback_look_up, re, song_look_up


if __name__ == "__main__":
    app.run()
