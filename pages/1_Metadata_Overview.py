import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Set up the dashboard
st.set_page_config(page_title="NeoBank HMO Dashboard", layout="wide")
st.title("NeoBank: HMO and Clinical Metadata Dashboard")
#st.markdown("Explore "Unlinked" sample clinical metadata with human milk oligosaccaride data.")

# Load the merged dataset
df = pd.read_excel("Unlinked_Merged.xlsx")

####--------------------------------------------------------------------------------------------------------------
############### Overview section ###############
st.header("Unlinked Sample Overview")

# Count metrics
num_subjects = df["Subject ID"].nunique()
num_samples = df["sample_unique_id"].nunique()

def metric_card(title, value, icon=""):
    st.markdown(f"""
        <div style="
            background-color: #262730;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 0 5px rgba(0,0,0,0.2);
        ">
            <div style="font-size: 14px; color: #bbb;">{icon} {title}</div>
            <div style="font-size: 32px; font-weight: bold; color: white;">{value}</div>
        </div>
    """, unsafe_allow_html=True)


# Overview metric cards
col1, col2 = st.columns(2)

with col1:
    metric_card("Total Samples", df["sample_unique_id"].nunique())

with col2:
    metric_card("Unique Subjects", df["Subject ID"].nunique())


#############-------------------------

st.subheader("Sample Count per Subject")

# Count how many samples per subject
sample_counts = df["Subject ID"].value_counts().sort_index()
sample_counts_df = sample_counts.reset_index()
sample_counts_df.columns = ["Subject ID", "Sample Count"]

# Plot bar chart using Plotly for better styling
import plotly.express as px

fig = px.bar(
    sample_counts_df,
    x="Subject ID",
    y="Sample Count",
    text="Sample Count",
    color="Sample Count",
    color_continuous_scale="Blues"
)

fig.update_layout(
    xaxis_title="Subject ID",
    yaxis_title="Number of Samples",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)



#############-----------------
st.subheader("Milk & Nutrition Details")

milk_vars = [
    "Scavenged/Fresh?",
    "MBM/DMB?",
    "HMF Y/N?",
    "TPN Y/N?",
    'Iron Y/N? '
]

selected_milk_var = st.selectbox("Select a milk-related variable to explore:", milk_vars)

if selected_milk_var:
    st.markdown(f"**Distribution of** `{selected_milk_var}`")

    value_counts = df[selected_milk_var].value_counts()

    # Show value counts
    st.write(value_counts.to_frame().rename(columns={selected_milk_var: "Count"}))

    # Bar chart
    st.bar_chart(value_counts)


#############-----------------
st.subheader("Growth Metric Overview")

#############-----------------


# Filter subjects with >2 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

st.markdown("📍 Showing only subjects with > 3 timepoints")
selected_subject = st.selectbox("Select a subject:", longitudinal_subjects)
subject_df = df[df["Subject ID"] == selected_subject]

# Define columns for layout
col1, col2, col3 = st.columns(3)

# Standard figure style function
def make_growth_plot(x, y, title):
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    ax.plot(subject_df[x], subject_df[y], marker="o", color="#4A90E2")
    ax.set_xlabel(x, color='white')
    ax.set_ylabel(y, color='white')
    ax.set_title(title, color='white')
    ax.tick_params(colors='white')

    # Add tick marks every 2 DOL units
    x_vals = subject_df[x].dropna().sort_values()
    if not x_vals.empty:
        tick_range = np.arange(x_vals.min(), x_vals.max() + 2, 3)
        ax.set_xticks(tick_range)
    return fig

# Weight
with col1:
    st.pyplot(make_growth_plot("DOL ", "Current Weight", "Weight (g)"))

# Height
with col2:
    st.pyplot(make_growth_plot("DOL ", "Current Height", "Height (cm)"))

# Head Circumference
with col3:
    st.pyplot(make_growth_plot("DOL ", "Current HC", "Head Circumference (cm)"))
