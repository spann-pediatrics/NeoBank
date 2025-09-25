
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

####--------------------------------------------------------------------------------------------------------------
############### Overview section ###############
st.header("Next Steps & Future Directions")


with st.container():
    st.markdown("""
        <div style="
            background-color: #e8f4ff;
            padding: 1.25rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: #000000;
            font-size: 1rem;
            line-height: 1.5;
        ">
         <h3 style="margin-top:0;">Next Steps</h3>
        To expand upon this preliminary dataset, future studies should consider:
        <ol>
            <li>
                <strong>Supporting Cohorts</strong> - Collect both maternal and infant metadata to combine with BM bioactive composition 
            </li>
            <li>
                <strong>Cross-cohort Analysis</strong> – Analyze BM profiles and infant outcomes across multiple NICU cohorts
            </li>
                </li>
                *The following graphs are synthetic examples of what cross-cohort analyses could look like* 
        </ol>
        </div>
        </div>
    """, unsafe_allow_html=True)



    # st.markdown("""
    #     <div style="
    #         background-color: #ffe8e8;
    #         padding: 1.25rem;
    #         border-radius: 10px;
    #         margin-bottom: 1.5rem;
    #         color: #000000;
    #         font-size: 1rem;
    #         line-height: 1.5;
    #     ">
    #      <h3 style="margin-top:0;">Questions / Clarification Needed:</h3>
    #      <ul>
    #         <li>What does TPN mean for the infant?</li>
    #         <li>Could we get get the amount of fortifier added to the sample? 
    #             <p>
    #                 **Fortifier dilutes the HMO concentrations</li>
    #         <li>What does the “switched to fortifier” mean for infants?</li>
    #         <li>Are there other outcomes we can get aside from growth metrics?</li>
    #      </ul>
    #     </div>
    # """, unsafe_allow_html=True)



######## regional charts



# Expanded dataset
data = {
    "Region": [
        "San Diego, CA", "Boston, MA", "New York, NY",
        "Toronto, Canada", "Montreal, Canada", 
        "Mexico City, Mexico", "Monterrey, Mexico",
        "Houston, TX", "New Orleans, LA", "San Francisco, CA"
    ],
    "lat": [
        32.7157, 42.3601, 40.7128, 
        43.6532, 45.5017, 
        19.4326, 25.6866,
        29.7604, 29.9511, 37.7749
    ],
    "lon": [
        -117.1611, -71.0589, -74.0060, 
        -79.3832, -73.5673, 
        -99.1332, -100.3161,
        -95.3698, -90.0715, -122.4194
    ],
    "n_cohorts": [6, 4, 5, 2, 1, 2, 1, 2, 1, 3],
    "n_subjects": [120, 95, 110, 70, 40, 60, 30, 65, 25, 80],
    "n_samples": [867, 640, 720, 350, 180, 250, 120, 410, 95, 500],
    "start_date": [
        "2021-01-01","2020-06-01","2021-02-01",
        "2020-08-01","2021-03-01",
        "2021-05-01","2022-01-15",
        "2021-04-01","2022-06-10","2021-09-01"
    ],
    "end_date": [
        "2024-07-01","2023-12-15","2024-01-01",
        "2023-06-15","2022-11-01",
        "2023-09-30","2023-12-31",
        "2023-10-20","2023-12-31","2024-03-01"
    ]
}
df_map = pd.DataFrame(data)

# Create map
fig = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="Region",
    hover_data={
        "n_cohorts": True,
        "n_subjects": True,
        "n_samples": True,
        "start_date": True,
        "end_date": True,
    },
    size="n_samples",
    size_max=35,
    zoom=2.5,
    color="n_cohorts",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(center={"lat": 37, "lon": -96}, zoom=3),
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.subheader("NICU Cohorts Across North America (Synthetic Data)")
st.plotly_chart(fig, use_container_width=True)









####--------------------------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st

# Synthetic data
data = {
    "Region": [
        "San Diego, CA", "Boston, MA", "New York, NY", 
        "Toronto, Canada", "Mexico City, Mexico"
    ],
    "Subjects": [120, 95, 110, 70, 60],
    "Samples": [867, 640, 720, 350, 250],
    "Avg CGA at Birth (weeks)": [28.5, 29.2, 28.8, 29.0, 28.3],
    "Avg LOS (days)": [72, 65, 68, 62, 70],
    "% Received MOM": [90, 85, 88, 80, 75],
    "% Recieved Formula": [2, 6, 3, 5, 11],
    "% Sepsis": [30, 20, 25, 15, 10]
}

df = pd.DataFrame(data).set_index("Region")

# Define formatting
format_dict = {
    "Subjects": "{:,.0f}",
    "Samples": "{:,.0f}",
    "Avg CGA at Birth (weeks)": "{:.1f}",
    "Avg LOS (days)": "{:.0f}",
    "% Sepsis": "{:.0f}%",
    "% Recieved Formula": "{:.0f}%",
    "% Received MOM": "{:.0f}%"
}

# Display
st.subheader("Combined Cohort Summary (by Region)")
st.dataframe(df.style.format(format_dict))




####--------------------------------------------------------------------------------------------------------------



# --- Synthetic NICU disease data ---
data = {
    "Region": [
        "San Diego, CA", "Boston, MA", "New York, NY",
        "Toronto, Canada", "Mexico City, Mexico"
    ],
    "lat": [32.7157, 42.3601, 40.7128, 43.6532, 19.4326],
    "lon": [-117.1611, -71.0589, -74.0060, -79.3832, -99.1332],
    "n_cohorts": [6, 4, 5, 2, 2],
    "n_subjects": [120, 95, 110, 70, 60],
    "n_samples": [867, 640, 720, 350, 250],
    # synthetic disease counts
    "NEC": [30, 20, 25, 15, 10],
    "Sepsis": [40, 35, 30, 20, 15],
    "BPD": [50, 40, 55, 25, 20],
}
df_map = pd.DataFrame(data)


df_disease = df_map.melt(
    id_vars=["Region"],
    value_vars=["NEC", "Sepsis", "BPD"],
    var_name="Disease",
    value_name="n_infants"
)


color_map = {
    "NEC": "#ddadab",
    "Sepsis": "#b8cdeb",
    "BPD": "#e7ccb3"
}


# Proportion stacked bar by region
fig1 = px.bar(
    df_disease,
    x="Region",
    y="n_infants",
    color="Disease",
    title="Proportion of Infants by Disease (per Region)",
    text="n_infants",
    color_discrete_map=color_map   # ✅ custom colors
)

st.plotly_chart(fig1, use_container_width=True)





















 ####--------------------------------------------------------------------------------------------------------------


df = pd.read_excel("Cleaned Data/Unlinked_Merged.xlsx")


hmo_columns = ["2FL", "DFLAC", "3SL", "6SL", "LNT", "LNnT", "LNFPI",
               "LNFPII", "LNFPIII", "LSTc", "DFLNT", "DSLNT", 
               "DFLNH", "FDSLNH", "DSLNH"]





st.subheader ("Longitudinal HMO Heatmap with Growth Metric & Clinical Events")
# --- Load data ---


hmo_columns = ["2FL", "DFLAC", "3SL", "6SL", "LNT", "LNnT", "LNFPI",
               "LNFPII", "LNFPIII", "LSTc", "DFLNT", "DSLNT", 
               "DFLNH", "FDSLNH", "DSLNH"]

# --- Identify longitudinal subjects ---
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts >= 3].index.tolist()

# --- Streamlit selectors ---
subject_id = "NB00002"

growth_metric = st.selectbox("Select Growth Metric", ["Current Weight", "Current Height", "Current HC"])

# --- Filter subject data ---
subject_df = df[df["Subject ID"] == subject_id].copy()
subject_df = subject_df.sort_values("DOL").reset_index(drop=True)

# Normalize HMOs per column
hmo_values = subject_df[hmo_columns]
hmo_norm = (hmo_values - hmo_values.min()) / (hmo_values.max() - hmo_values.min())
hmo_norm["Sample #"] = range(1, len(hmo_norm) + 1)
hmo_norm["DOL"] = subject_df["DOL"].values

# Melt for heatmap
hmo_long = hmo_norm.melt(
    id_vars=["Sample #","DOL"], 
    value_vars=hmo_columns, 
    var_name="HMO", 
    value_name="Relative Abundance"
)

# Example: synthetic clinical events (replace with real when available)
disease_events = pd.DataFrame({
    "DOL": [2, 4, 8, 15], 
    "Event": ["NEC", "Sepsis", "Feeding Intolerance", "Feeding Intolerance"]
})

# --- Build subplot with 3 rows ---
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    row_heights=[0.6, 0.3, 0.1],
    vertical_spacing=0.05,
    subplot_titles=[
        f"HMO Relative Abundance Heatmap for {subject_id}",
        f"{growth_metric} Over Time",
        "Clinical Events (Hypothetical)"
    ]
)

# Row 1: Heatmap
fig.add_trace(
    go.Heatmap(
        x=hmo_long["Sample #"],
        y=hmo_long["HMO"],
        z=hmo_long["Relative Abundance"],
        colorscale="Blues",
        colorbar=dict(title="Relative Abundance")
    ),
    row=1, col=1
)

# Row 2: Growth line
fig.add_trace(
    go.Scatter(
        x=list(range(1, len(subject_df)+1)),
        y=subject_df[growth_metric],
        mode="lines+markers",
        name=growth_metric,
        line=dict(color="black", width=2)
    ),
    row=2, col=1
)

# Row 3: Clinical events (hypothetical)
fig.add_trace(
    go.Scatter(
        x=disease_events["DOL"],
        y=[1]*len(disease_events),
        mode="markers+text",
        marker=dict(size=12, color="red"),
        text=disease_events["Event"],
        textposition="top center",
        name="Events"
    ),
    row=3, col=1
)

# Replace x-axis ticks with actual DOL
fig.update_xaxes(
    tickmode="array",
    tickvals=list(range(1, len(subject_df["DOL"]) + 1)),
    ticktext=subject_df["DOL"].tolist(),
    title="Day of Life"
)

# Hide y-axis for events
fig.update_yaxes(visible=False, row=3, col=1)

# Layout polish
fig.update_layout(
    height=800,
    template="simple_white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


