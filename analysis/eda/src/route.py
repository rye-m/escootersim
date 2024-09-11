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
    from scipy.spatial.distance import directed_hausdorff
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
    from tqdm import tqdm

    alt.data_transformers.enable("marimo_csv")
    return (
        Path,
        Prototype,
        Task,
        alt,
        combine_dataset,
        directed_hausdorff,
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
        tqdm,
    )


@app.cell
def __(Path, pl):
    data_dir = Path("./Data/")
    data = pl.read_parquet(data_dir / "*.parquet")

    # data = data.filter((pl.col("Task").eq(Task.SONG))& (pl.col('participantID').eq('P8001'))).select(["x_pos", "z_pos", "Prototype"])
    return data, data_dir


@app.cell
def __(pl):
    optimal = pl.read_csv("./Data/Optimal_path_expanded.csv").select(
        ["x_pos", "z_pos", "Prototype"]
    )
    return optimal,


@app.cell
def __(optimal):
    optimal
    return


@app.cell
def __(alt, data, downsample):
    # todo, it would be nice to overlay the optimal with all the other ones, leaving that off for now
    # base = (
    #     alt.Chart(optimal)
    #     .encode(
    #         alt.X("x_pos:Q").scale(domain=[-100, 100]),
    #         alt.Y("z_pos:Q").scale(domain=[-100, 100]),
    #     )
    # )

    # optimal_route = base.mark_circle(size=30, color="red")


    routes = alt.Chart(downsample(data, 4)).mark_circle(opacity=.03).encode(
        alt.X("x_pos:Q").scale(domain=[-100, 100]),
        alt.Y("z_pos:Q").scale(domain=[-100, 100]),
        alt.Color('Prototype'),
        alt.Facet('Prototype', columns=3)
    )
    routes
    # (routes + optimal_route).facet('Prototype')
    return routes,


@app.cell
def __():
    from similaritymeasures import frechet_dist
    return frechet_dist,


@app.cell
def __(optimal):
    optimal_np = optimal.select(["x_pos", "z_pos"]).to_numpy()
    # test_voice = (
    #     data.filter(pl.col("Prototype").eq(Prototype.VOICE))
    #     .select(["x_pos", "z_pos"])
    #     .to_numpy()
    # )
    # # test_foot = data.filter(pl.col('Prototype').eq(Prototype.FOOTBUTTON)).select(['x_pos', 'z_pos']).to_numpy()
    # frechet_dist(optimal_np, test_voice)
    return optimal_np,


@app.cell
def __(Prototype, data, pl):
    test_foot = (
        data.filter(pl.col("Prototype").eq(Prototype.FOOTBUTTON))
        .select(["x_pos", "z_pos"])
        .to_numpy()
    )
    # frechet_dist(optimal_np, test_foot)
    return test_foot,


@app.cell
def __():
    # dists = []
    # for name, dat in mo.status.progress_bar(
    #     data.group_by("Prototype", "participantID"),
    #     total=data["participantID"].unique().shape[0]
    #     * data["Prototype"].unique().shape[0],
    # ):
    #     route = dat.sort("ScenarioTime").select(["x_pos", "z_pos"]).to_numpy()
    #     f_dist = frechet_dist(optimal_np, route)
    #     h_dist = max(directed_hausdorff(optimal_np, route)[0],directed_hausdorff(route, optimal_np)[0])
    #     dists.append((*name, h_dist, f_dist))
    return


@app.cell
def __(dists, pl):
    dists_df = pl.DataFrame(dists, schema=['Prototype', 'ID', 'h_dist', 'f_dist'], orient="row")
    return dists_df,


@app.cell
def __(dists_df, pl):
    dists_df.group_by('Prototype').agg(pl.col('h_dist').median(), pl.col('f_dist').median()).sort('f_dist')
    return


@app.cell
def __(dists_df):
    dists_df
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
