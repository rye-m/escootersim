import marimo

__generated_with = "0.8.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import polars as pl
    import altair as alt
    from utils.plotting import downsample, image_to_altair
    from utils.process_sim_csv import Prototype, Task, process_csv, combine_dataset
    from itertools import product
    from pathlib import Path

    data_path = Path("./Data/")
    b64_image = image_to_altair(data_path / "map2.png", data_path / "b64_map2.txt")
    out_path = Path("./Figures/")
    data_dir = Path("./Data/")
    df = pl.read_parquet(data_dir.glob("*.parquet"))
    alt.data_transformers.enable('marimo_csv')
    return (
        Path,
        Prototype,
        Task,
        alt,
        b64_image,
        combine_dataset,
        data_dir,
        data_path,
        df,
        downsample,
        image_to_altair,
        mo,
        out_path,
        pl,
        process_csv,
        product,
    )


@app.cell
def __():
    # optimal_path_path = Path('./Data/Optimal_path.csv')
    # optimal_df = process_csv(optimal_path_path)
    # optimal_df.write_csv('./Data/Optimal_path_expanded.csv')
    # combined_df = combine_dataset(data_dir, str(data_dir/ "combined_dataset"))

    # for tsk in Task:
    #     partition = combined_df.filter(pl.col('Task').eq(tsk))
    #     partition.write_parquet(data_dir / f"combined_{tsk.value}.parquet", compression_level=22)
    return


@app.cell
def __(df, pl):
    scatter_df = df.group_by(["participantID", "Task", "Prototype"]).agg(
        pl.col("ScenarioTime").max().alias("duration"),
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
    )


    bar_df = df.group_by(["Task", "Prototype"]).agg(
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
        pl.col("ScenarioTime").max().alias("duration"),
    )

    scatter_df.head()
    return bar_df, scatter_df


@app.cell
def __(alt, scatter_df):
    alt.Chart(scatter_df).mark_circle(size=40).encode(
        alt.X("duration"),
        alt.Y("median_velocity"),
        alt.Color("Prototype"),
        alt.Column("Task"),
        alt.Tooltip(["participantID"]),
    )
    return


@app.cell
def __():
    return


@app.cell
def __(alt, bar_df):
    sorted_prototypes = [
        proto for proto in list(bar_df["Prototype"].unique()) if proto != "Control"
    ] + ["Control"]

    alt.Chart(bar_df).mark_bar().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration"),
        alt.Color("Task"),
        xOffset="Task:N",
    )
    return sorted_prototypes,


@app.cell
def __(alt, scatter_df, sorted_prototypes):
    alt.Chart(scatter_df).mark_circle().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration"),
        alt.Color("Task"),
        tooltip="participantID",
        xOffset="Task:N",
    )
    return


@app.cell(disabled=True)
def __(Prototype, Task, alt, df, downsample, out_path, pl, product):
    dfs = []
    charts = []
    for proto, task in product(
        Prototype,
        Task,
    ):
        scenatio_df = df.filter(
            (pl.col("Prototype").eq(proto)) & (pl.col("Task").eq(task))
        )
        if scenatio_df.shape[0] > 0:
            down = downsample(scenatio_df, 3)
            dfs.append(down)
            chart = (
                alt.Chart(
                    scenatio_df[["x_pos", "z_pos", "Prototype", "participantID"]]
                )
                .mark_circle(size=10, opacity=0.05)
                .encode(
                    alt.X("x_pos:Q").scale(domain=[-100, 100]),
                    alt.Y("z_pos:Q").scale(domain=[-100, 100]),
                    tooltip="participantID:N",
                )
                .properties(title=f"{proto.value} doing {task.value}")
            )
            charts.append(chart)
            chart.save(out_path / f"{proto.value}_{task.value}.svg")

        # print(f"Item from list1: {proto}, Item from list2: {task}")
    return chart, charts, dfs, down, proto, scenatio_df, task


@app.cell
def __(charts, mo):
    mo.ui.altair_chart((charts[0] | charts[2] | charts[4]))
    return


@app.cell
def __(charts, mo):
    mo.ui.altair_chart((charts[1] | charts[3] | charts[5]))
    return


@app.cell
def __(charts, mo):
    mo.ui.altair_chart((charts[6] | charts[10] | charts[8]))
    return


@app.cell
def __(charts, mo):
    mo.ui.altair_chart((charts[7] | charts[11] | charts[9]))
    return


@app.cell
def __(charts, mo):
    mo.ui.altair_chart(charts[12])
    return


@app.cell
def __(Task, df, downsample, pl):
    nback_df = downsample(df.filter(pl.col("Task") == Task.NBACK))
    song_df = downsample(df.filter(pl.col("Task") == Task.SONG))
    return nback_df, song_df


@app.cell
def __(Prototype, Task, df, pl):
    nback_button = df.filter((pl.col("Task") == Task.NBACK )& (pl.col("Prototype") == Prototype.BUTTON))
    nback_button
    return nback_button,


@app.cell
def __(alt, nback_button, pl):
    route = (
        alt.Chart(nback_button)
        .mark_circle(size=30)
        .encode(
            alt.X("x_pos:Q").scale(domain=[-100, 100]),
            alt.Y("z_pos:Q").scale(domain=[-100, 100]),
            alt.Color("velocity_magnitude"),
        )
    )

    points = (
        alt.Chart(
            nback_button.filter(pl.col("ws_action").eq("NBACK_CLIENT_RESPONSE"))
        )
        .mark_circle(color="yellow", size=50, opacity=0.3)
        .encode(
            alt.X("x_pos:Q").scale(domain=[-100, 100]),
            alt.Y("z_pos:Q").scale(domain=[-100, 100]),
        )
    )


    (route + points) 
    return points, route


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
