import marimo

__generated_with = "0.8.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import polars as pl
    import altair as alt
    return alt, mo, pl


@app.cell
def __(pl):
    df = pl.read_parquet("./Data/combined_dataset.parquet")
    return df,


@app.cell
def __(df):
    df.head()
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
    ).interactive()
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


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
