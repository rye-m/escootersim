import marimo

__generated_with = "0.7.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from pathlib import Path
    import polars as pl
    import json
    import altair as alt
    from utils.survey_tools import get_participant_data, get_flow_data, get_order
    from utils.process_sim_csv import read_trials, Task, Prototype
    return (
        Path,
        Prototype,
        Task,
        alt,
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
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
