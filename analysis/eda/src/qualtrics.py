import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd 
    import matplotlib.pyplot as plt 
    import seaborn as sns
    import collections
    import numpy as np 

    # import data
    qual_results = pd.read_csv("/Users/ryem/Desktop/Cornell_Tech/escootersim/analysis/eda/Data/qualtrics.csv")

    # print data
    qual_results = qual_results.drop(0)
    # qual_results = qual_results.drop(1)
    qual_results
    # len(qual_results)
    return collections, np, pd, plt, qual_results, sns


@app.cell
def _(qual_results):
    qual_results.query('randomID =="2579"')
    return


@app.cell
def _(qual_results):
    # Get column names only
    first_column_name = qual_results[:0]
    print(first_column_name)
    return (first_column_name,)


@app.cell
def _(qual_results):
    demog = qual_results.loc[:,["randomID", "Q12", "Q12_5_TEXT", "Q13"]]
    # mo.ui.table(demog, page_size=50)  # Shows 50 rows per page
    demog
    return (demog,)


@app.cell
def _(qual_results):
    # get average of every col with Q35* 
    with_experience = qual_results.query('Q12.str.contains("E-Scooter", na=False)')
    without_experience = qual_results.query('~Q12.str.contains("E-Scooter", na=False)')

    with_experience_ID = map(lambda x: "P" + x, with_experience["randomID"].tolist())
    without_experience_ID = map(lambda x: "P" + x,without_experience["randomID"].tolist())

    print("with_experience_ID =", list(with_experience_ID))
    print("without_experience_ID =", list(without_experience_ID))
    return (
        with_experience,
        with_experience_ID,
        without_experience,
        without_experience_ID,
    )


@app.cell
def _(pd, plt, qual_results, sns):
    # import data
    # qual_results = pd.read_csv("/Users/ryem/Downloads/Scooterseim Aug 27 2024.csv")


    # get average of every col with Q159 <Test Ride>
    q159 = qual_results.filter(regex='Q159_*')
    q159 = q159.filter(regex='Q159_.*[^DO]')
    # q159 = q159.drop(0)
    q159 = q159.drop(1)
    # q159 = q159.dropna().astype(int)

    # get average of every col with Q149 <Song + Phone>
    q149 = qual_results.filter(regex='Q149_*')
    q149 = q149.filter(regex='Q149_.*[^DO]')
    q149 = q149.drop('Q149_4_TEXT', axis='columns')
    # q149 = q149.drop(0)
    q149 = q149.drop(1)
    # q149 = q149.dropna().astype(int) 

    # get average of every col with Q145 <Song + Watch>
    q145 = qual_results.filter(regex='Q145_*')
    q145 = q145.filter(regex='Q145_.*[^DO]')
    # q145 = q145.drop(0)
    q145 = q145.drop(1)
    # q145 = q145.dropna().astype(int)

    # get average of every col with Q125 <Song + Footbutton>
    q125 = qual_results.filter(regex='Q125_*')
    q125 = q125.filter(regex='Q125_.*[^DO]')
    # q125 = q125.drop(0)
    q125 = q125.drop(1)
    # q125 = q125.dropna().astype(int) 

    # get average of every col with Q153 <Nback + Phone>
    q153 = qual_results.filter(regex='Q153_*')
    q153 = q153.filter(regex='Q153_.*[^DO]')
    # q153 = q153.drop(0)
    q153 = q153.drop(1)
    # q153 = q153.dropna().astype(int) 

    # get average of every col with Q121 <Song + Voice>
    q121 = qual_results.filter(regex='Q121_*')
    q121 = q121.filter(regex='Q121_.*[^DO]')
    # q121 = q121.drop(0)
    q121 = q121.drop(1)
    # q121 = q121.dropna().astype(int) 

    # get average of every col with Q117 <Song + Button>
    q117 = qual_results.filter(regex='Q117_*')
    q117 = q117.filter(regex='Q117_.*[^DO]')
    # q117 = q117.drop(0)
    q117 = q117.drop(1)
    # q117 = q117.dropna().astype(int) 

    # get average of every col with Q109 <Song + Throttle>
    q109 = qual_results.filter(regex='Q109_*')
    q109 = q109.filter(regex='Q109_.*[^DO]')
    # q109 = q109.drop(0)
    q109 = q109.drop(1)
    # q109 = q109.dropna().astype(int) 

    # get average of every col with Q143 <Nback + Watch>
    q143 = qual_results.filter(regex='Q143_*')
    q143 = q143.filter(regex='Q143_.*[^DO]')
    # q143 = q143.drop(0)
    q143 = q143.drop(1)
    # q143 = q143.dropna().astype(int) 

    # get average of every col with Q137 <Nback + Footbutton>
    q137 = qual_results.filter(regex='Q137_*')
    q137 = q137.filter(regex='Q137_.*[^DO]')
    # q137 = q137.drop(0)
    q137 = q137.drop(1)
    # q137 = q137.dropna().astype(int) 

    # get average of every col with Q135 <Nback + Voice>
    q135 = qual_results.filter(regex='Q135_*')
    q135 = q135.filter(regex='Q135_.*[^DO]')
    # q135 = q135.drop(0)
    q135 = q135.drop(1)
    # q135 = q135.dropna().astype(int) 

    # get average of every col with Q139 <Nback + Button>
    q139 = qual_results.filter(regex='Q139_*')
    q139 = q139.filter(regex='Q139_.*[^DO]')
    # q139 = q139.drop(0)
    q139 = q139.drop(1)
    # q139 = q139.dropna().astype(int) 

    # get average of every col with Q133 <Nback + Throttle>
    q133 = qual_results.filter(regex='Q133_*')
    q133 = q133.filter(regex='Q133_.*[^DO]')
    # q133 = q133.drop(0)
    q133 = q133.drop(1)
    # q133 = q133.dropna().astype(int) 

    # Create a single figure with a 4x3 grid of subplots
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20, 15))

    # List of all DataFrames
    data_list = [q149, q145, q125, q153, q121, q117, q109, q143, q137, q135, q139, q133]
    # List of all axes
    ax_list = axes.flatten()

    # Plot each DataFrame on the corresponding subplot
    for data, ax in zip(data_list, ax_list):
        # sns.boxplot(data=data, orient='h', ax=ax)
        data = data.apply(pd.to_numeric, errors='coerce')
        # print(data.dtypes)
        if not data.empty:
            # plt.boxplot(data=data, ax=ax)
            # ax.boxplot(data.values.T)
            sns.boxplot(data=data, orient='h', ax=ax)
        else:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center')  # Show 'No Data' if empty


    # Define common labels
    x_label = '1 = Very Low, 4 = Moderate, 7 = Very High'
    # y_label = 'Interface Order'

    # Set common x-axis label for all plots
    fig.text(0.5, 0.04, x_label, ha='center')

    # Convert the list to a single string for y-axis label
    questionnaire_order_str = ', '.join(['Mental demand', 'Physical demand', 'Temporal demand', 'Performance', 'Effort', 'Frustration'])
    interfaceXtask_order_lst = ['Song + Phone', 'Song + Watch', 'Song + Footbutton', 'Nback + Phone', 'Song + Voice', 'Song + Button', 'Song + Throttle', 'Nback + Watch', 'Nback + Footbutton', 'Nback + Voice', 'Nback + Button', 'Nback + Throttle']
    # Set y-axis labels for all subplots
    i = 0
    for ax in ax_list:
        # ax.set_yticklabels(questionnaire_order_str.split(', '))
        # ax.set_title(interfaceXtask_order_lst[i])
        # i += 1

        # Calculate the number of labels
        labels = questionnaire_order_str.split(', ')
        ax.set_yticks(range(len(labels)))  # Explicitly set the tick positions
        ax.set_yticklabels(labels)  # Assign the tick labels
        ax.set_title(interfaceXtask_order_lst[i])
        i += 1

    # Improve layout
    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.9])  # Adjust layout to fit common labels

    # Save the figure
    # plt.savefig("../figures/qual_results_nasatlx_boxplot.png", dpi=300)

    # Show the plot
    plt.show()

    return (
        ax,
        ax_list,
        axes,
        data,
        data_list,
        fig,
        i,
        interfaceXtask_order_lst,
        labels,
        q109,
        q117,
        q121,
        q125,
        q133,
        q135,
        q137,
        q139,
        q143,
        q145,
        q149,
        q153,
        q159,
        questionnaire_order_str,
        x_label,
    )


if __name__ == "__main__":
    app.run()
