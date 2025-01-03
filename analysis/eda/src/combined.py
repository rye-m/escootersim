import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _():
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


    # Convert glob iterator to list of paths
    parquet_files = list(data_dir.glob("*.parquet"))

    # First, let's check what files we found
    print("Found parquet files:", parquet_files)

    # Then read the files
    df = pl.read_parquet(parquet_files)
    print(df.head())


    # # print(data_dir.glob("*.parquet"))
    # df = pl.read_parquet(data_dir.glob("*.parquet"))
    # print(df.head())
    # # alt.data_transformers.enable('marimo_csv')
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
        parquet_files,
        pl,
        process_csv,
        product,
    )


@app.cell
def _(Path, Task, combine_dataset, data_dir, pl, process_csv):
    optimal_path_path = Path('./Data/Optimal_path.csv')
    optimal_df = process_csv(optimal_path_path)
    optimal_df.write_csv('./Data/Optimal_path_expanded.csv')
    combined_df = combine_dataset(data_dir, str(data_dir/ "combined_dataset"))

    for tsk in Task:
        partition = combined_df.filter(pl.col('Task').eq(tsk))
        # combined_df.write_csv(f"./Data/combined_{tsk.value}.csv")
        partition.write_parquet(data_dir / f"combined_{tsk.value}.parquet", compression_level=22)
    return combined_df, optimal_df, optimal_path_path, partition, tsk


@app.cell
def _(df, pl):
    with_experience_ID = ['P3844', 'P641', 'P9570', 'P1453', 'P91', 'P6167', 'P3864', 'P1676', 'P8001', 'P3890', 'P7045', 'P8867', 'P837', 'P8655', 'P8559', 'P2297', 'P6333', 'P5863', 'P7895']
    without_experience_ID = ['P1011', 'P2808', 'P725', 'P1026', 'P5778', 'P321', 'P840', 'P2750', 'P5995', 'P8880', 'P6795', 'P5174', 'P61', 'P2579', 'P9631', 'P1528']

    df_with = df.filter(pl.col('participantID').is_in(with_experience_ID))
    df_without = df.filter(pl.col('participantID').is_in(without_experience_ID))
    df_with
    return df_with, df_without, with_experience_ID, without_experience_ID


@app.cell
def _(df_with, df_without, pl):
    scatter_df_with = df_with.group_by(["participantID", "Task", "Prototype"]).agg(
        pl.col("ScenarioTime").max().alias("duration"),
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
    )
    scatter_df_without = df_without.group_by(["participantID", "Task", "Prototype"]).agg(
        pl.col("ScenarioTime").max().alias("duration"),
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
    )


    bar_df_with = df_with.group_by(["Task", "Prototype"]).agg(
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
        pl.col("ScenarioTime").max().alias("duration"),
    )
    bar_df_without = df_without.group_by(["Task", "Prototype"]).agg(
        pl.col("velocity_magnitude").mean().alias("mean_velocity"),
        pl.col("velocity_magnitude").median().alias("median_velocity"),
        pl.col("ScenarioTime").max().alias("duration"),
    )

    scatter_df_with.head()
    return bar_df_with, bar_df_without, scatter_df_with, scatter_df_without


@app.cell
def _(alt, scatter_df_with, scatter_df_without):
    # Plot for "scatter_df_with"
    chart_with = alt.Chart(scatter_df_with).mark_circle(size=40).encode(
        alt.X("duration", scale=alt.Scale(domain=[0, 300])),
        alt.Y("median_velocity"),
        alt.Color("Prototype"),
        alt.Column("Task"),
        alt.Tooltip(["participantID"]),
    ).properties(title="Plot: With Experience of Riding Escooter")

    # Plot for "scatter_df_without"
    chart_without = alt.Chart(scatter_df_without).mark_circle(size=40).encode(
        alt.X("duration", scale=alt.Scale(domain=[0, 300])),
        alt.Y("median_velocity"),
        alt.Color("Prototype"),
        alt.Column("Task"),
        alt.Tooltip(["participantID"]),
    ).properties(title="Plot: Without Experience of Riding Escooter")

    # Combine the two charts side-by-side
    # combined_chart = chart_with | chart_without

    # Stack the charts vertically
    combined_chart = chart_with & chart_without

    # Show or save the combined chart
    combined_chart.show()

    return chart_with, chart_without, combined_chart


@app.cell
def _():
    return


@app.cell
def _(alt, bar_df_with, bar_df_without):
    sorted_prototypes = [
        proto for proto in list(bar_df_with["Prototype"].unique()) if proto != "Control"
    ] + ["Control"]

    bar_with = alt.Chart(bar_df_with).mark_bar().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration", scale=alt.Scale(domain=[0, 300])),
        alt.Color("Task"),
        xOffset="Task:N",
    ).properties(title="Bar: With Experience of Riding Escooter")

    bar_without = alt.Chart(bar_df_without).mark_bar().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration", scale=alt.Scale(domain=[0, 300])),
        alt.Color("Task"),
        xOffset="Task:N",
    ).properties(title="Bar: Without Experience of Riding Escooter")

    # Combine the two charts side-by-side
    combined_bar = bar_with | bar_without

    # Show or save the combined bar
    combined_bar.show()
    return bar_with, bar_without, combined_bar, sorted_prototypes


@app.cell
def _(alt, scatter_df_with, scatter_df_without, sorted_prototypes):
    Nback_chart_with = alt.Chart(scatter_df_with).mark_circle().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration", scale=alt.Scale(domain=[0, 300])),
        alt.Color("Task"),
        tooltip="participantID",
        xOffset="Task:N",
    ).properties(title="Chart: With Experience of Riding Escooter")

    Nback_chart_without = alt.Chart(scatter_df_without).mark_circle().encode(
        alt.X("Prototype", sort=sorted_prototypes),
        alt.Y("duration"),
        alt.Color("Task"),
        tooltip="participantID",
        xOffset="Task:N",
    ).properties(title="Chart: Without Experience of Riding Escooter")


    Nback_combined_chart = Nback_chart_with | Nback_chart_without

    # Show or save the combined chart
    Nback_combined_chart.show()

    return Nback_chart_with, Nback_chart_without, Nback_combined_chart


@app.cell
def _(scatter_df_with, scatter_df_without):
    from scipy.stats import ttest_ind, mannwhitneyu, shapiro

    # Example DataFrames (replace with your actual data)
    # df_with = pd.DataFrame({
    #     "duration": [100, 120, 110, 90, 95],
    #     "median_velocity": [5.5, 6.0, 5.8, 5.2, 5.4]
    # })

    # df_without = pd.DataFrame({
    #     "duration": [80, 85, 78, 82, 88],
    #     "median_velocity": [5.3, 5.0, 5.1, 5.2, 5.4]
    # })

    # Function for normality check
    def check_normality(data, column_name):
        stat, p = shapiro(data[column_name])
        print(f"Shapiro-Wilk test for {column_name}: W-statistic = {stat}, p-value = {p}")
        return p >= 0.05  # Returns True if data is normally distributed

    # Perform hypothesis testing
    def hypothesis_test(group1, group2, column_name, alpha=0.05):
        print(f"\nTesting for {column_name}:")
        
        # Check normality for both groups
        is_group1_normal = check_normality(group1, column_name)
        is_group2_normal = check_normality(group2, column_name)

        # Select test based on normality
        if is_group1_normal and is_group2_normal:
            # Perform t-test
            t_stat, p_value = ttest_ind(group1[column_name], group2[column_name], equal_var=False)
            test_name = "T-Test"
        else:
            # Perform Mann-Whitney U test
            t_stat, p_value = mannwhitneyu(group1[column_name], group2[column_name], alternative='two-sided')
            test_name = "Mann-Whitney U Test"

        # Print results
        print(f"{test_name}: Test-statistic = {t_stat}, p-value = {p_value}")
        
        # Interpret results
        if p_value < alpha:
            print(f"Result: Reject the null hypothesis (there is NOT a significant difference).")
        else:
            print(f"Result: Fail to reject the null hypothesis (there IS a significant difference).")

    # Run tests for both "duration" and "median_velocity"
    hypothesis_test(scatter_df_with, scatter_df_without, "duration")
    hypothesis_test(scatter_df_with, scatter_df_without, "median_velocity")
    hypothesis_test(scatter_df_with, scatter_df_without, "mean_velocity")

    return (
        check_normality,
        hypothesis_test,
        mannwhitneyu,
        shapiro,
        ttest_ind,
    )


@app.cell(disabled=True)
def _(Prototype, Task, alt, df, downsample, out_path, pl, product):
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
def _(charts, mo):
    mo.ui.altair_chart((charts[0] | charts[2] | charts[4]))
    return


@app.cell
def _(charts, mo):
    mo.ui.altair_chart((charts[1] | charts[3] | charts[5]))
    return


@app.cell
def _(charts, mo):
    mo.ui.altair_chart((charts[6] | charts[10] | charts[8]))
    return


@app.cell
def _(charts, mo):
    mo.ui.altair_chart((charts[7] | charts[11] | charts[9]))
    return


@app.cell(hide_code=True)
def _(charts, mo):
    mo.ui.altair_chart(charts[12])
    return


@app.cell
def _(Task, df, downsample, pl):
    nback_df = downsample(df.filter(pl.col("Task") == Task.NBACK))
    song_df = downsample(df.filter(pl.col("Task") == Task.SONG))
    return nback_df, song_df


@app.cell
def _(Prototype, Task, df, pl):
    nback_button = df.filter((pl.col("Task") == Task.NBACK )& (pl.col("Prototype") == Prototype.BUTTON))
    nback_button
    return (nback_button,)


@app.cell
def _(alt, nback_button, pl):
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
def _(df):
    # Get unique values in ws_action column
    unique_actions = df["ws_action"].unique()
    print("Unique values in ws_action column:")
    print(unique_actions)
    return (unique_actions,)


@app.cell
def _():
    return


app._unparsable_cell(
    r"""
    # Filter for N-back task and group by Prototype
    result_Nback_df = df.filter(pl.col(\"Task\") == \"Nback\" &&pl.col(\"ws_action\") == \"\") \
                 .group_by(\"Prototype\") \
                 .agg(pl.len()) \
                 .sort(\"Prototype\")

    result_song_df = df.filter(pl.col(\"Task\") == \"Song\") \
                 .group_by(\"Prototype\") \
                 .agg(pl.len()) \
                 .sort(\"Prototype\")

    # Convert to a format where prototypes are columns
    result_Nback_df = result_Nback_df.transpose(include_header=True)
    result_song_df = result_song_df.transpose(include_header=True)

    # Set the first row as column names
    new_columns = result_Nback_df.row(0)
    result_Nback_df = result_Nback_df.slice(1)
    result_Nback_df.columns = new_columns

    print(result_Nback_df)

    # Set the first row as column names
    new_columns = result_song_df.row(0)
    result_song_df = result_song_df.slice(1)
    result_song_df.columns = new_columns

    print(result_song_df)
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
