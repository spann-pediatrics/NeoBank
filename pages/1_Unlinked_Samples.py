import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Set up the dashboard
st.set_page_config(page_title="NeoBank HMO Dashboard", layout="wide")
st.title("NeoBank: Unlinked Samples")
#st.markdown("Explore "Unlinked" sample clinical metadata with human milk oligosaccaride data.")

# Load the merged dataset
df = pd.read_excel("Unlinked_Merged.xlsx")

####--------------------------------------------------------------------------------------------------------------
############### Overview section ###############
st.header("Unlinked Metadata Overview")

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


############ Aliquots Overview
st.subheader("Aliquots Overview")

# Metric card for total aliquots
total_aliquots = df["Aliquots_num"].sum()
metric_card("Number of Total Aliquots", total_aliquots)

# Aliquots per subject
aliquots_per_subject = df.groupby("Subject ID")["Aliquots_num"].sum().reset_index()
aliquots_per_subject.columns = ["Subject ID", "Total Aliquots"]

fig_aliquots = px.bar(
    aliquots_per_subject,
    x="Subject ID",
    y="Total Aliquots",
    text="Total Aliquots",
    color="Total Aliquots",
    color_continuous_scale="Greys"
    )

fig_aliquots.update_layout(
    xaxis_title="Subject ID",
    yaxis_title="Number of Aliquots",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
    )

st.plotly_chart(fig_aliquots, use_container_width=True)




#############-----------------
st.subheader("Milk & Nutrition Details")

milk_vars = [
    "Scavenged/Fresh?",
    "MBM/DMB?",
    "HMF Y/N?",
    "TPN Y/N?",
    'Iron Y/N'
]

selected_milk_var = st.selectbox("Select a milk-related variable to explore:", milk_vars)

if selected_milk_var:
    st.markdown(f"**Distribution of** `{selected_milk_var}`")

    value_counts = df[selected_milk_var].value_counts()

    # Show value counts
    st.write(value_counts.to_frame().rename(columns={selected_milk_var: "Count"}))

    # Bar chart
    st.bar_chart(value_counts)

    st.subheader("Additional Notes Overview")

    # Count the occurrences of each unique note (excluding NaN)
    notes_counts = df["Additional Comments"].dropna().value_counts()

    if not notes_counts.empty:
        st.write(notes_counts.to_frame().rename(columns={"Additional Comments": "Count"}))
        # Pie chart using Plotly
        import plotly.express as px
        fig_notes = px.pie(
            names=notes_counts.index,
            values=notes_counts.values,
            title="Distribution of Additional Notes"
        )
        fig_notes.update_traces(textinfo='percent+label')
        fig_notes.update_layout(
            plot_bgcolor="#1E1E1E",
            paper_bgcolor="#1E1E1E",
            font_color="white"
        )
        st.plotly_chart(fig_notes, use_container_width=True)
    else:
        st.info("No data available in the 'additional notes' column.")


#############-----------------
st.subheader("Growth Metric Overview")

#############-----------------


# Filter subjects with >2 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

st.markdown("📍 Showing only subjects with > 3 timepoints")
selected_subject = st.selectbox("Select a subject:", longitudinal_subjects)
subject_df = df[df["Subject ID"] == selected_subject]

# Show number of subjects with >3 timepoints
num_longitudinal_subjects = len(longitudinal_subjects)
st.markdown(f"""
    <div style="
        background-color: #444;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.2);
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: italic;
    ">
        {num_longitudinal_subjects} subjects with > 3 timepoints
    </div>
""", unsafe_allow_html=True)

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






st.title("Unlinked HMO Overview")

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






st.subheader("HMO Concentrations Over Time (Longitudinal Subjects)")

# Identify HMO columns (from 2FL to DSLNT), excluding "Iso (control)" if present
hmo_start = "2FL"
hmo_end = "DSLNT"
hmo_columns = df.loc[:, hmo_start:hmo_end].columns.tolist()
# Remove "Iso (control)" if it exists in the list
hmo_columns = [col for col in hmo_columns if col != "Iso (control)"]

# Filter subjects with >3 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

if not longitudinal_subjects:
    st.warning("No subjects with more than 3 timepoints.")
elif not hmo_columns:
    st.warning("No HMO columns found in the dataset (2FL to DSLNT).")
else:
    selected_subject = st.selectbox("Select a subject (with >3 timepoints):", longitudinal_subjects)
    selected_hmo = st.selectbox("Select an HMO to plot:", hmo_columns)
    subject_df = df[df["Subject ID"] == selected_subject]

    st.markdown(f"**{selected_hmo} concentrations over time for subject `{selected_subject}`**")

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')

    # Plot HMO concentration vs DOL for the selected subject
    ax.plot(
        subject_df["DOL "], 
        subject_df[selected_hmo], 
        marker="o", 
        color="#E24A4A"
    )
    ax.set_xlabel("DOL", color='white')
    ax.set_ylabel(f"{selected_hmo} Concentration", color='white')
    ax.set_title(f"{selected_hmo} over Time", color='white')
    ax.tick_params(colors='white')

    # Add tick marks every 3 DOL units
    x_vals = subject_df["DOL "].dropna().sort_values()
    if not x_vals.empty:
        tick_range = np.arange(x_vals.min(), x_vals.max() + 2, 3)
        ax.set_xticks(tick_range)

    st.pyplot(fig)