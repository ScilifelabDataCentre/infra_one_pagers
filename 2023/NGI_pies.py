import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px
from colour_science_2023 import (
    SCILIFE_COLOURS,
    FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB,
)

# want pie charts splitting the users between different technologies at NGI

NGI_tech_users = pd.read_excel(
    "Data/NGI Users Technologies 2022.xlsx",
    sheet_name="NGI lists dublets removed",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# want to group by the PI affiliation and different technologies used in 2022
NGI_tech_group = (
    NGI_tech_users.groupby(["Technology", "PI affiliation"]).size().reset_index()
)
NGI_tech_group.columns = ["Technology", "PI_aff", "Count"]

NGI_tech_group_abbr = {
    "Chalmers University of Technology": "Chalmers",
    "KTH Royal Institute of Technology": "KTH",
    "Swedish University of Agricultural Sciences": "SLU",
    "Karolinska Institutet": "KI",
    "Linköping University": "LiU",
    "Lund University": "LU",
    "Naturhistoriska Riksmuséet": "NRM",
    "Stockholm University": "SU",
    "Umeå University": "UmU",
    "University of Gothenburg": "GU",
    "Uppsala University": "UU",
    "Örebro University": "ÖU",
    "International University": "Int Univ",
    "Other Swedish University": "Other Swe Univ",
    "Other Swedish organization": "Other Swe Org",
    "Other international organization": "Other Int Org",
    "Industry ": "Industry",
    "Industry": "Industry",
    "Healthcare": "Healthcare",
}

abbreviated_tech_data = NGI_tech_group.replace(NGI_tech_group_abbr, regex=True)


def tech_pies_func(input):
    tech_data = input
    if sum(tech_data.Count) < 2:
        pi_plural = "PI"
    else:
        pi_plural = "PIs"
    colours = np.array([""] * len(tech_data["PI_aff"]), dtype=object)
    for i in tech_data["PI_aff"]:
        colours[
            np.where(tech_data["PI_aff"] == i)
        ] = FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB[str(i)]
    fig = go.Figure(
        go.Pie(
            #    aff_data,
            values=tech_data["Count"],
            labels=tech_data["PI_aff"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )

    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} (%{percent:.1%f})",
        # the :.1%f does to 1 decimal place. do .0 to round to whole numbers. HOWEVER! whole numbers tend to give 0% as a value. Wouldnt recommend
    )  # textinfo="percent+label")
    fig.update_layout(
        margin=dict(
            l=100, r=100, b=100, t=100
        ),  # original values l=200, r=200 b=100 t=300
        font=dict(size=34),  # 36 works for most
        annotations=[
            dict(
                showarrow=False,
                text="{} {}".format(sum(tech_data.Count), pi_plural),
                font=dict(size=50),  # should work for all centre bits
                x=0.5,
                y=0.5,
            )
        ],
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/NGI_tech_pies/"):
        os.mkdir("Plots/NGI_tech_pies/")
    if sum(tech_data.Count) > 0:
        fig.write_image(
            "Plots/NGI_tech_pies/{}_NGItech.svg".format(
                input["Technology"][input["Technology"].first_valid_index()],
            )
        )
    else:
        print(
            "Warning: not all unit year combinations have data - check whether this is expected"
        )


for i in abbreviated_tech_data["Technology"].unique():
    tech_pies_func(
        abbreviated_tech_data[(abbreviated_tech_data["Technology"] == "NGI Long read")]
    ),
    tech_pies_func(
        abbreviated_tech_data[(abbreviated_tech_data["Technology"] == "NGI Proteomics")]
    )
    tech_pies_func(
        abbreviated_tech_data[(abbreviated_tech_data["Technology"] == "NGI Short read")]
    )
    tech_pies_func(
        abbreviated_tech_data[
            (abbreviated_tech_data["Technology"] == "NGI Single cell")
        ]
    )
    tech_pies_func(
        abbreviated_tech_data[
            (abbreviated_tech_data["Technology"] == "NGI SNP genotyping")
        ]
    )
    tech_pies_func(
        abbreviated_tech_data[
            (abbreviated_tech_data["Technology"] == "NGI Spatial omics")
        ]
    )
    # Aff_pies_func(temp[(temp["Unit"] == z)])
