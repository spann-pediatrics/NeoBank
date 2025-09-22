
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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
         <h3 style="margin-top:0;">Suggested Next Steps</h3>
        To expand upon this preliminary dataset, future studies should consider:
        <ol>
            <li>
                <strong>Outcome Measurements</strong>
            </li>
            <li>
                <strong>HMO Analysis</strong> – Each sample was analyzed for 
                <strong>15 human milk oligosaccharides (HMOs)</strong>. 
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


df = pd.read_excel("Cleaned Data/Unlinked_Merged.xlsx")


hmo_columns = ["2FL", "DFLAC", "3SL", "6SL", "LNT", "LNnT", "LNFPI",
               "LNFPII", "LNFPIII", "LSTc", "DFLNT", "DSLNT", 
               "DFLNH", "FDSLNH", "DSLNH"]

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.subheader ("EXAMPLE) Longitudinal HMO Heatmap with Growth Metric & Clinical Events")
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




import streamlit as st
import pandas as pd
import plotly.express as px

# --- Synthetic NICU disease data ---
data = {
    "Disease": ["NEC", "Sepsis", "BPD"],
    "Count": [15, 20, 25],            # number of infants with each disease
    "Avg LOS": [75, 60, 90]           # average length of stay in days
}
df_disease = pd.DataFrame(data)

# --- Normalize counts into percentages ---
df_disease["Percent"] = (df_disease["Count"] / df_disease["Count"].sum()) * 100

# Add a "Cohort" column so all rows align on one stacked bar
df_disease["Cohort"] = "NICU Cohort"

st.subheader("NICU Disease Burden (Synthetic Data)")

# --- Stacked bar for proportions ---
fig_prop = px.bar(
    df_disease,
    x="Cohort",   # same for all rows
    y="Percent",
    color="Disease",
    text="Percent",
    title="Proportion of Infants by Disease",
    color_discrete_map={"NEC": "#d97b7b", "Sepsis": "#4da6ff", "BPD": "#82c91e"}
)
fig_prop.update_layout(
    yaxis_title="Percent of Infants",
    xaxis_title="",
    template="simple_white"
)

# --- Bar for average LOS ---
fig_los = px.bar(
    df_disease,
    x="Disease",
    y="Avg LOS",
    text="Avg LOS",
    color="Disease",
    title="Average Length of Stay by Disease",
    color_discrete_map={"NEC": "#d97b7b", "Sepsis": "#4da6ff", "BPD": "#82c91e"}
)
fig_los.update_layout(
    yaxis_title="Average LOS (days)",
    xaxis_title="Disease",
    template="simple_white"
)

# --- Display in Streamlit side-by-side ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_prop, use_container_width=True, theme=None)
with col2:
    st.plotly_chart(fig_los, use_container_width=True, theme=None)

