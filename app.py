# %%
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import datetime


# %%
# Read in the CSV
""" Set everything to an object to avoid working with dates"""

df = pd.read_csv(
    "Sample_data_analysis1.csv",
    sep=",",
    dtype={"DATE": object, "CCSA": object},
    encoding="utf-8",
)
# %%
df
# %%
# Slice out values from the date string to pull years, decades, and months
df["year"] = df["DATE"].str.slice(start=2, stop=4)
df["yod"] = df["DATE"].str.slice(start=3, stop=4)
df["moy"] = df["DATE"].str.slice(start=5, stop=7)
# %%
# Set the date column to a date type so we can pull the week of the month
df["DATE"] = pd.to_datetime(df["DATE"], errors="ignore")
df["woy"] = df["DATE"].apply(lambda x: x.strftime("%U")).astype(int)
# %%
# Set the CCSA data column to be numeric type
df["CCSA"] = pd.to_numeric(df["CCSA"])

# Set up the outputs and roll...
# %%
# Summary of raw data
df_summary = df["CCSA"].describe()
df_summary = df_summary.map(lambda x: "{:.0f}".format(x))
# %%
# Summary of yearly averages
df_year = df.groupby(["year"]).mean()  # Mean can be changed to min, max, etc.
df_year.drop(["DATE", "yod", "moy", "woy"], axis=1, inplace=True)
df_year_summary = df_year["CCSA"].describe()
# %%
# Sumary of years in each decade
df_yod = df.groupby(["yod"]).mean()
df_yod.drop(["DATE", "year", "moy", "woy"], axis=1, inplace=True)
df_yod_summary = df_yod["CCSA"].describe()
# %%
# Summary of months in each year
df_moy = df.groupby(["moy"]).mean()
df_moy.drop(["DATE", "year", "yod", "woy"], axis=1, inplace=True)
df_moy_summary = df_moy["CCSA"].describe()
# %%
# Summary of weeks in each year
df_woy = df.groupby(["woy"]).mean()
df_woy.drop(["DATE", "year", "yod", "moy"], axis=1, inplace=True)
df_woy_summary = df_woy["CCSA"].describe()

# %%
# Data
print("Years in Decade Data")
df_yod = df_yod.apply(lambda s: s.apply("{0:.5f}".format))
print()
# %%
# Summary of years in each decade
print("Years in Decade Summary")
df_yod_summary = df_yod_summary.map(lambda x: "{:.0f}".format(x))
print()
# %%
print("Months of Years Data")
df_moy = df_moy.apply(lambda s: s.apply("{0:.5f}".format))
print()
# %%
# Summary of months in each year
print("Months in Year Summary")
df_moy_summary = df_moy_summary.map(lambda x: "{:.0f}".format(x))
print()

# %%
df["Decade"] = df["DATE"].dt.year // 10 * 10  # Group by decades
# %%
df_dec = df.groupby("Decade")["CCSA"].describe()

# %%
# Format the statistics columns to remove scientific notation
df_dec = df_dec.apply(lambda x: x.apply(lambda y: f"{y:.2f}"))

# %%
df["full_year"] = df["DATE"].dt.year  # Group by years
# %%
df_full_year = df.groupby("full_year")["CCSA"].describe()

# %%
df_full_year = df_full_year.apply(lambda x: x.apply(lambda y: f"{y:.2f}"))
# %%
df["month"] = df["DATE"].dt.to_period("M")  # Group by months

# %%
df_month = df.groupby("month")["CCSA"].describe()
# %%
df_month = df_month.apply(lambda x: x.apply(lambda y: f"{y:.2f}"))

# %%
df_summary = df_summary.reset_index()

# %%
df_yod = df_yod.reset_index()
# %%
df_yod_summary = df_yod_summary.reset_index()
# %%
df_moy = df_moy.reset_index()
# %%
df_moy_summary = df_moy_summary.reset_index()
# %%
df_dec = df_dec.reset_index()
# %%
df_full_year = df_full_year.reset_index()
# %%
df_month = df_month.reset_index()

# %%
# %% ouputs
# cr.df_out(df_summary)
# # %%
# cr.df_out(df_yod)
# # %%
# cr.df_out(df_yod_summary)
# # %%
# cr.df_out(df_moy)

# # %%
# cr.df_out(df_moy_summary)
# # %%
# cr.df_out(df_dec)
# # %%
# cr.df_out(df_full_year)
# # %%
# cr.df_out(df_month)
# # %%
# df_full_year
# %%
full_year_line_graph = px.line(
    df_full_year, x="full_year", y="mean", title="Mean by Year"
)
# %%
full_year_line_graph.update_layout(autotypenumbers="convert types")
# %%
df_full_year.dtypes

# %%
df_month = df_month.astype(str)
# %%
df_month.dtypes
# %%
month_line_graph = px.line(
    df_month, x="month", y="mean", title="Mean by Month"
)
# %%
month_line_graph.update_layout(
    autotypenumbers="convert types",
    xaxis_rangeslider_visible=True,
    xaxis_range=[0, 10],
)

# %%
df_moy.dtypes
# %%
moy_line_graph = px.line(df_moy, x="moy", y="CCSA", title="Mean by MOY")
# %%
moy_line_graph.update_layout(autotypenumbers="convert types")
# %%
df_yod

# %%
yod_line_graph = px.line(df_yod, x="yod", y="CCSA", title="Mean by YOD")
# %%
yod_line_graph.update_layout(autotypenumbers="convert types")

# %%
app = dash.Dash(__name__)
server = app.server
# %%
app.layout = html.Div(
    children=[
        html.Img(src="https://fred.stlouisfed.org/images/fred-logo-2x.png"),
        html.H1("Continued Claims (Insured Unemployement)"),
        html.Span(
            children=[
                f"Last updated: {datetime.datetime.now().date()}",
                html.Br(),
                " by ",
                html.B("Alex Jurado, "),
                html.Br(),
                html.I("aka Mr. Python"),
            ]
        ),
        dcc.Graph("month_line_graph", figure=month_line_graph),
        dcc.Graph("yod_line_graph", figure=yod_line_graph),
        dcc.Graph("moy_line_graph", figure=moy_line_graph),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
# %%
month_line_graph.write_html(
    "C:/python_testing/exercise1_brads_results (1).py.html"
)

# %%
# print(datetime.__version__)
# # %%

df
# %%
