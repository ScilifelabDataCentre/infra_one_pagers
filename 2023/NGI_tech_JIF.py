import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from colour_science_2023 import (
    SCILIFE_COLOURS,
    FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB,
)

from Data_prep import JIF_data

# only want certain NGI technologies for 2022
NGI_tech_2022 = JIF_data.loc[JIF_data["Year"] == 2022]
NGI_tech_JIF = NGI_tech_2022.loc[
    NGI_tech_2022["Unit"].isin(
        [
            "NGI Long read",
            "NGI Proteomics",
            "NGI Short read",
            "NGI Single cell",
            "NGI SNP genotyping",
            "NGI Spatial omics",
        ]
    )
]

# split down dataframes to enable stacking
UnknownJIF = NGI_tech_JIF[(NGI_tech_JIF["JIFcat"] == "JIF unknown")]
Undersix = NGI_tech_JIF[(NGI_tech_JIF["JIFcat"] == "JIF <6")]
sixtonine = NGI_tech_JIF[(NGI_tech_JIF["JIFcat"] == "JIF 6-9")]
ninetotwentyfive = NGI_tech_JIF[(NGI_tech_JIF["JIFcat"] == "JIF 9-25")]
overtwentyfive = NGI_tech_JIF[(NGI_tech_JIF["JIFcat"] == "JIF >25")]
# Make stacked bar chart
fig = go.Figure(
    data=[
        go.Bar(
            name="JIF unknown",
            x=UnknownJIF.Unit,
            y=UnknownJIF.Count,
            marker=dict(color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="JIF < 6",
            x=Undersix.Unit,
            y=Undersix.Count,
            marker=dict(color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="JIF 6 - 9",
            x=sixtonine.Unit,
            y=sixtonine.Count,
            marker=dict(color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="JIF 9 - 25",
            x=ninetotwentyfive.Unit,
            y=ninetotwentyfive.Count,
            marker=dict(color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="JIF > 25",
            x=overtwentyfive.Unit,
            y=overtwentyfive.Count,
            marker=dict(color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=1)),
        ),
    ]
)

fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    autosize=False,
    font=dict(size=23),
    margin=dict(r=250, t=0, b=0, l=0),
    width=1000,
    height=600,
    showlegend=True,
)
# List technologies to use in x-axis
# Years = JIFcounts["Year"].unique().astype(str)
techs = NGI_tech_JIF["Unit"].unique()
# modify x-axis
fig.update_xaxes(
    title=" ",
    showgrid=True,
    linecolor="black",
    ticktext=[
        "<b>" + techs[0] + "</b>",
        "<b>" + techs[1] + "</b>",
        "<b>" + techs[2] + "</b>",
        "<b>" + techs[3] + "</b>",
        "<b>" + techs[4] + "</b>",
        "<b>" + techs[5] + "</b>",
    ],
    tickvals=[techs[0], techs[1], techs[2], techs[3], techs[4], techs[5]],
)

tech_one = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[0])]
tech_two = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[1])]
tech_three = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[2])]
tech_four = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[3])]
tech_five = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[4])]
tech_six = NGI_tech_JIF[(NGI_tech_JIF["Unit"] == techs[5])]

highest_y_value = max(
    tech_one["Count"].sum(),
    tech_two["Count"].sum(),
    tech_three["Count"].sum(),
    tech_four["Count"].sum(),
    tech_five["Count"].sum(),
)

# highest_y_value = max(NGI_tech_JIF["Count"])

if highest_y_value < 10:
    yaxis_tick = 1
if highest_y_value >= 10:
    yaxis_tick = 2
if highest_y_value > 20:
    yaxis_tick = 5
if highest_y_value > 50:
    yaxis_tick = 10
if highest_y_value > 100:
    yaxis_tick = 20
if highest_y_value > 150:
    yaxis_tick = 40
if highest_y_value > 200:
    yaxis_tick = 50
if highest_y_value > 1000:
    yaxis_tick = 100

# modify y-axis
fig.update_yaxes(
    title=" ",
    showgrid=True,
    gridcolor="black",
    linecolor="black",
    dtick=yaxis_tick,
    range=[0, int(highest_y_value * 1.15)],
)
if not os.path.isdir("Plots/NGI_JIF_plots/"):
    os.mkdir("Plots/NGI_JIF_plots/")
# fig.write_image("Plots/NGI_JIF_plots/NGI_JIF_2022.svg")

# for i in affiliate_data["Year"].unique():
#     Aff_pies_func_stacked_text(temp[(temp["Unit"] == "AIDA Data Hub")])

# for i in JIF_data["Unit"].unique():
#     JIF_graph_func(JIF_data[(JIF_data["Unit"] == i)])
# fig.show()
# print(UnknownJIF)
# print(Undersix)
# print(sixtonine)
# print(ninetotwentyfive)
# print(overtwentyfive)
