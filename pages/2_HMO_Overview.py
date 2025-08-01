import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("HMO Overview")

with st.container():
    st.markdown("""
        <div style="
            background-color: #262730;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: white;
        ">
        <strong>Summary:</strong><br>
        15 different HMOs were analyzed per sample and recorded is the area under the curve (AUC) for each HMO. The 2’FL HMO is used to classify secretor status, with a threshold of 5 million AUC.
        </div>
    """, unsafe_allow_html=True)


df = pd.read_excel("Unlinked_Merged.xlsx")

# Get HMO columns
hmo_columns = ['2FL','DFLAC', '3SL', '6SL', 'LNT', 'LNnT', 'LNFPI',
       'LNFPII', 'LNFPIII', 'LSTc', 'DFLNT', 'DSLNT', 'DFLNH', 'FDSLNH',
       'DSLNH']



# ---- Classify Secretor Status ----
cutoff = 5_000_000  # AUC threshold for 2’FL
df["Secretor Status"] = df["2FL"].apply(
    lambda x: "Secretor" if x >= cutoff else "Non-Secretor"
)

# ---- HMO Range Bar Chart ----
hmo_ranges = df[hmo_columns].agg(['min', 'max']).T
hmo_ranges['Range'] = hmo_ranges['max'] - hmo_ranges['min']
hmo_ranges = hmo_ranges.reset_index().rename(columns={'index': 'HMO'})

fig_range = px.bar(
    hmo_ranges,
    x="HMO",
    y="Range",
    text="Range",
    color="Range",
    color_continuous_scale="Viridis"
)
fig_range.update_layout(
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white",
    xaxis_title="",
    yaxis_title="Range of Concentration",
)

# ---- Secretor Status Pie Chart ----
status_counts = df["Secretor Status"].value_counts().reset_index()
status_counts.columns = ["Secretor Status", "Count"]

fig_pie = px.pie(
    status_counts,
    names="Secretor Status",
    values="Count",
    color="Secretor Status",
    color_discrete_map={
        "Secretor": "#76C7F0",       # light blue
        "Non-Secretor": "#FFFFFF"    # white
    }
)

fig_pie.update_layout(
    title="Secretor Status Classification (2’FL ≥ 5M AUC)",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

# ---- Layout Section ----
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("**Range of HMO Concentrations**")
    st.plotly_chart(fig_range, use_container_width=True)

with col2:
    st.markdown("**Secretor Status (2’FL ≥ 5M AUC)**")
    st.plotly_chart(fig_pie, use_container_width=True)



import seaborn as sns
import matplotlib.pyplot as plt

hmo_data = df[hmo_columns].copy()
hmo_data.index = df["sample_unique_id"]  # or Subject ID

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(hmo_data.fillna(0), cmap="viridis", ax=ax)
st.pyplot(fig)
