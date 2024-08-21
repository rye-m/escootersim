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
    from utils.process_sim_csv import read_trials, Task, Prototype
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
        json,
        mo,
        pl,
        read_trials,
    )


@app.cell
def __(Path, get_flow_data, get_order, get_participant_data):
    participant_id = 8001

    data_dir = Path("./Data/")
    participant_dir = data_dir / f"P{participant_id}"

    survey_data_path = next(data_dir.glob("Scooterseim*"))
    trial_paths = Path(participant_dir).glob("CSV_Scenario-*.csv")

    participant_survey = get_participant_data(participant_id, survey_data_path)
    flow_map = get_flow_data(data_dir / "FlowMap.json")
    study_order = get_order(participant_survey, flow_map)
    return (
        data_dir,
        flow_map,
        participant_dir,
        participant_id,
        participant_survey,
        study_order,
        survey_data_path,
        trial_paths,
    )


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
def __(mo):
    mo.md(r"""## Faceted plots of velocity""")
    return


@app.cell
def __(Prototype, alt, downsample, pl, rolling_window, study_df):
    facet_base1 = alt.Chart(
        downsample(study_df.filter(pl.col("Prototype") != Prototype.CONTROL))[
            "ScenarioTime",
            "x_pos",
            "z_pos",
            "Task",
            "Prototype",
            "accel_magnitude",
            "velocity_magnitude",
        ]
    )
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
    return facet_base1, velocity_facet


@app.cell
def __(alt, facet_base1):
    acceleration_facet = (
        facet_base1.mark_circle()
        .encode(
            alt.X("x_pos").scale(domain=[-100, 100]),
            alt.Y("z_pos").scale(domain=[-100, 100]),
            alt.Color("Task"),
            alt.Facet("Prototype", columns=3),
        )
    )
    acceleration_facet
    return acceleration_facet,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
