import pandas as pd
import numpy as np


### FAC MAP
# to their labels in the publication database
fac_map_input = pd.read_excel(
    "Data/Reporting Units 2022.xlsx",
    sheet_name="Reporting units",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
fac_map_input["PDB label"] = fac_map_input["PDB label"].str.replace(
    r"\(.*\)", "", regex=True
)
# You need the above to make sure you don't get spaces in file names
fac_map_input = fac_map_input[["Unit", "PDB label"]]
fac_map_input = fac_map_input.replace("", np.nan)
fac_map_input["PDB label"] = fac_map_input["PDB label"].fillna(fac_map_input["Unit"])
fac_map_input.rename(columns={"PDB label": "Label"}, inplace=True)
fac_map = dict(zip(fac_map_input.Label, fac_map_input.Unit))

### AFFILIATES
# Years of interest in 2023 - 2020-22
# We have 3 data files from OO for this (one for each year)

aff_2020_raw = pd.read_excel(
    "Data/Users 2020.xlsx",
    sheet_name="Unit Users 2020",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_2021_raw = pd.read_excel(
    "Data/Users 2021.xlsx",
    sheet_name="Unit Users 2021",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_2022_raw = pd.read_excel(
    "Data/Users 2022.xlsx",
    sheet_name="Users Duplc. for Units removed",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Want to get counts of how many of each individual affiliation
# for each unit

affiliates_data_2020 = (
    aff_2020_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)
affiliates_data_2021 = (
    aff_2021_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)
affiliates_data_2022 = (
    aff_2022_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)

affiliates_data_2020.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_2021.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_2022.columns = ["Unit", "PI_aff", "Count"]

affiliates_data_2020.insert(loc=2, column="Year", value="2020")
affiliates_data_2021.insert(loc=2, column="Year", value="2021")
affiliates_data_2022.insert(loc=2, column="Year", value="2022")

aff_comb = pd.concat([affiliates_data_2020, affiliates_data_2021, affiliates_data_2022])
# print(aff_comb)
# Now need to replace all of the affiliation names with a shortened version

aff_map_abbr = {
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

affiliate_data = aff_comb.replace(aff_map_abbr, regex=True)
# print(affiliate_data.PI_aff.unique())


### UNIT DATA ## changes to unit from facility, will change throughout the script.
# Single data contains all basic data for unit
# Read in to pdf almost directly
# rename columns for clarity
Unit_data = pd.read_excel(
    "Data/Single data 2022.xlsx",
    sheet_name="Single Data",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# below, mostly changed year in header
Unit_data.rename(
    columns={
        "Head of Unit": "HOU",  # updated from Head of facility (HOF)
        "Platform Scientific Director": "PSD",  # updated from Facility director (FD) now needs to come AFTER head (was before previously)
        "SciLifeLab unit since": "SLL_since",
        "Host university": "H_uni",
        "FTEs financed by Scilifelab": "SLL_FTEs",
        "Funding 2022 SciLifeLab (kSEK)": "Amount (kSEK)",
        "Resource allocation 2022 Acadmia (national)": "RA_nat",
        "Resource allocation 2022 Acadmia (international)": "RA_int",
        "Resource allocation 2022 Internal tech. dev.": "RA_tech",
        "Resource allocation 2022 Industry": "RA_Ind",
        "Resource allocation 2022 Healthcare": "RA_Health",
        "Resource allocation 2022 Other gov. agencies": "RA_ogov",
        "User Fees 2022 Total (kSEK)": "UF_Tot",
        "Cost reagents": "UF_reag",
        "Cost instrument": "UF_instr",
        "Cost salaries": "UF_sal",
        "Cost rents": "UF_rent",
        "Cost other": "UF_other",
        "SciLifeLab Instrument Funding 2022": "SLL_Instr_fund",  # This is new for 2021, need to integrate in
        "User fees by sector 2022 Academia (national)": "UF_sect_nat",
        "User fees by sector 2022 Academia (international)": "UF_sect_int",
        "User fees by sector 2022 Industry": "UF_sect_ind",
        "User fees by sector 2022 Healthcare": "UF_sect_health",
        "User fees by sector 2022 Other gov. agencies": "UF_sect_othgov",
    },
    inplace=True,
)

### FUNDING
# This involves data from 'other funding' and 'single data'
# both files provided by OO
# Need to add SLL funding to other funding data and get a total

other_funding = pd.read_excel(
    "Data/Other Funding 2022.xlsx",
    sheet_name="QC Other Funding",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Some funding info also included in the unit data
# extract SLL funding data from single(unit) data

SLL_funding = Unit_data[["Unit", "Platform", "Amount (kSEK)"]]
SLL_funding.insert(loc=2, column="Financier", value="SciLifeLab")

# Need to add instrument funding for 2022 statistics

instru_funding = Unit_data[["Unit", "Platform", "SLL_Instr_fund"]]
instru_funding.insert(loc=2, column="Financier", value="SciLifeLab Instrument")
instru_funding = instru_funding[instru_funding.SLL_Instr_fund != 0]
instru_funding.rename(
    columns={
        "SLL_Instr_fund": "Amount (kSEK)",
    },
    inplace=True,
)

# need to drop 'platform no' column from other data before bringing these datasets together

other_funding = other_funding[["Unit", "Platform", "Financier", "Amount (kSEK)"]]

# now concatenate this with other funding
# also calculate total funding
Funding_comb = pd.concat([SLL_funding, instru_funding, other_funding])
tot_fund = Funding_comb.groupby(["Unit"]).sum().reset_index()
tot_fund.insert(loc=2, column="Financier", value="Total")
Funding = pd.concat([Funding_comb, tot_fund])
print(Funding)

# ###PUBLICATIONS!

# # Used in the two graphs for one-pagers
# # Need to use this data in 2 ways:
# # (1) Make a barplot of publications by category
# # (2) Make the barplot with JIF scores
# # whilst the rest of the data comes from OO,
# # This data is taken from:
# # (1) publications database
# # (2) publications db and JIF scores

# # import raw publications data

# # Focus on data for (1) - extract individual labels for records from pub db

# Pubs_cat_raw = pd.read_excel(
#     "Data/infra_1921_singlelab_juneupdate.xlsx",
#     sheet_name="Publications",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )

# # Need to get data for (fac) and groupby

# pub_sub = Pubs_cat_raw[["Year", "Labels", "Qualifiers"]]
# pub_sub = pub_sub.replace(r"^\s*$", "No category", regex=True)
# pub_sub["Qualifiers"] = pub_sub["Qualifiers"].astype("category")

# # Clinical Biomarkers and PLA and Single Cell Proteomics merged to Affinity Proteomics Uppsala.
# # Manually deleted 'duplicates' for labels in file - so only one of the above labels for any paper
# pub_sub = pub_sub.replace(
#     "Clinical Biomarkers", "Affinity Proteomics Uppsala", regex=True
# )

# pub_sub = pub_sub.replace(
#     "PLA and Single Cell Proteomics", "Affinity Proteomics Uppsala", regex=True
# )

# pub_cat_group = pub_sub.groupby(["Year", "Labels", "Qualifiers"]).size().reset_index()

# pub_cat_group["Labels"] = pub_cat_group["Labels"].str.replace(r"\(.*\)", "", regex=True)

# pub_cat_data = pub_cat_group.replace(fac_map, regex=True)

# # # in 2021, don't need the previous duplication for the two mass cytometry centres

# # Need to name the column produced by groupby
# pub_cat_data.columns = ["Year", "Unit", "Qualifiers", "Count"]

# # Now for data for (2)
# # This time work with pub data with labels combined
# # i.e. one record per publication

# Pubs_JIF_raw = pd.read_excel(
#     "Data/infra_1921_comblab_juneupdate.xlsx",
#     sheet_name="Publications",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )

# JIF_scores_raw = pd.read_excel(
#     "Data/JIF_scores_2021.xlsx",
#     sheet_name="Sheet 1 - JournalHomeGrid",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )

# # Need to join the two above files and align JIF with ISSN/ISSN-L
# # simpler to work with only columns of interest

# Pubs_JIF_sub = Pubs_JIF_raw[
#     [
#         "Title",
#         "Year",
#         "Labels",
#         "Journal",
#         "ISSN",
#         "ISSN-L",
#     ]
# ]

# JIF_scores_sub = JIF_scores_raw[
#     [
#         "ISSN",
#         "Full Journal Title",
#         "JCR Abbreviated Title",
#         "Impact Factor without Journal Self Cites",
#     ]
# ]

# # Must maximise matching of JIF. I recommend checking over
# # May be necessary to do some manual work

# Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
# JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
# Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "", regex=True)
# JIF_scores_sublow["JCR Abbreviated Title"] = JIF_scores_sublow[
#     "JCR Abbreviated Title"
# ].str.replace("-basel", "", regex=True)

# JIF_merge = pd.merge(
#     Pubs_JIF_sublow,
#     JIF_scores_sublow,
#     how="left",
#     on="ISSN",
# )

# JIF_mergebackori = pd.merge(
#     Pubs_JIF_sublow,
#     JIF_merge,
#     on=[
#         "Title",
#         "Year",
#         "Labels",
#         "Journal",
#         "ISSN",
#         "ISSN-L",
#     ],
# )

# JIF_mergebackori.drop_duplicates(subset="Title", keep="first", inplace=True)

# JIF_merge_ISSNL = pd.merge(
#     JIF_mergebackori,
#     JIF_scores_sublow,
#     how="left",
#     left_on="ISSN-L",
#     right_on="ISSN",
# )

# JIF_merge_ISSNL.drop_duplicates(subset="Title", keep="first", inplace=True)

# JIF_merge_ISSNL["Impact Factor without Journal Self Cites_x"] = JIF_merge_ISSNL[
#     "Impact Factor without Journal Self Cites_x"
# ].fillna(JIF_merge_ISSNL["Impact Factor without Journal Self Cites_y"])

# JIF_merge_ISSNL = JIF_merge_ISSNL.drop(
#     [
#         "ISSN_y",
#         "Full Journal Title_y",
#         "JCR Abbreviated Title_y",
#         "Impact Factor without Journal Self Cites_y",
#     ],
#     axis=1,
# )

# # now attempt to match on journal names

# JIF_merge_abbnames = pd.merge(
#     JIF_merge_ISSNL,
#     JIF_scores_sublow,
#     how="left",
#     left_on="Journal",
#     right_on="JCR Abbreviated Title",
# )

# JIF_merge_abbnames["Impact Factor without Journal Self Cites_x"] = JIF_merge_abbnames[
#     "Impact Factor without Journal Self Cites_x"
# ].fillna(JIF_merge_abbnames["Impact Factor without Journal Self Cites"])

# JIF_merge_abbnames.drop_duplicates(subset="Title", keep="first", inplace=True)

# JIF_merge_abbnames = JIF_merge_abbnames.drop(
#     [
#         "ISSN",
#         "Full Journal Title",
#         "JCR Abbreviated Title",
#         "Impact Factor without Journal Self Cites",
#     ],
#     axis=1,
# )

# JIF_merge_fullnames = pd.merge(
#     JIF_merge_abbnames,
#     JIF_scores_sublow,
#     how="left",
#     left_on="Journal",
#     right_on="Full Journal Title",
# )

# JIF_merge_fullnames.drop_duplicates(subset="Title", keep="first", inplace=True)

# JIF_merge_fullnames["Impact Factor without Journal Self Cites_x"] = JIF_merge_fullnames[
#     "Impact Factor without Journal Self Cites_x"
# ].fillna(JIF_merge_fullnames["Impact Factor without Journal Self Cites"])

# JIF_merge_fullnames = JIF_merge_fullnames.drop(
#     [
#         "ISSN",
#         "Full Journal Title",
#         "JCR Abbreviated Title",
#         "Impact Factor without Journal Self Cites",
#     ],
#     axis=1,
# )

# ## below prints out a file that can be checked to determine whether
# ## manual work may increase the number of matches

# JIF_merge_fullnames.rename(
#     columns={
#         "ISSN_x": "ISSN",
#         "Full Journal Title_x": "Full Journal Title",
#         "JCR Abbreviated Title_x": "JCR Abbreviated Title",
#         "Impact Factor without Journal Self Cites_x": "JIF",
#     },
#     inplace=True,
# )

# JIF_merge_fullnames.to_excel("Check_me_manual_improve_june22.xlsx")

# # Match this to the database with the labels seperated (easiest way to seperate out labels)

# JIF_merge_fullnames_sub = JIF_merge_fullnames[["Title", "JIF"]]

# Pubs_cat_raw["Title"] = Pubs_cat_raw["Title"].str.lower()

# match_JIF_seplabs = pd.merge(
#     Pubs_cat_raw,
#     JIF_merge_fullnames_sub,
#     how="left",
#     on="Title",
# )

# match_JIF_seplabs["JIF"] = match_JIF_seplabs["JIF"].fillna(-1)
# match_JIF_seplabs["JIF"] = pd.to_numeric(match_JIF_seplabs["JIF"])
# match_JIF_seplabs["JIFcat"] = pd.cut(
#     match_JIF_seplabs["JIF"],
#     bins=[-1, 0, 6, 9, 25, 1000],
#     include_lowest=True,
#     labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
# )

# # replace facility labels

# match_JIF_seplabs["Labels"] = match_JIF_seplabs["Labels"].str.replace(
#     r"\(.*\)", "", regex=True
# )

# JIF_match_basic = match_JIF_seplabs.replace(fac_map, regex=True)

# # Need to do a group by and check the sums work! (and align with above pub numbers)

# JIF_data = JIF_match_basic[["Year", "Labels", "JIFcat"]]

# JIF_data = JIF_data.groupby(["Year", "Labels", "JIFcat"]).size().reset_index()

# JIF_data.columns = ["Year", "Unit", "JIFcat", "Count"]

# # # As a check, can compare publications data divided by category and JIF for each unit
# # # The total numbers for each unit and for each year should align.
# JIF_data.to_excel("Check_JIFdata_june22.xlsx")
# pub_cat_data.to_excel("Check_pubcatdata_june22.xlsx")
