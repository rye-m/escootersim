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
    qual_results = qual_results.drop(1)
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
def _():
    return


if __name__ == "__main__":
    app.run()
