import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.express as px

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

# Filter and sort by DOL
subject_df = df[df["Subject ID"] == selected_subject].copy()
subject_df["DOL "] = pd.to_numeric(subject_df["DOL "], errors="coerce")  # ensure numeric
subject_df = subject_df.sort_values("DOL ")  # 👈 ensures line plots follow correct order


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





##############################################################
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

# Define consistent color maps
sample_source_colors = {
    "Residual": "#faff00",    # bright yellow
    "Scavenged": "#ffc000"    # orange-ish
}

secretor_colors = {
    "Secretor": "#8ecfff",        # light blue
    "Non-Secretor": "#ffffff"     # white
}


# ---- Sample Source Counts ----
# Count values in the Sample Source column
source_counts = df["Sample Source"].value_counts().reset_index()
source_counts.columns = ["Sample Source", "Count"]

# Create the pie chart
fig_source = px.pie(
    source_counts,
    names="Sample Source",
    values="Count",
    title="Milk Collection Type",
    color="Sample Source",
    color_discrete_map= sample_source_colors
)

fig_source.update_layout(
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)


# ---- Secretor Status Pie Chart ----
status_counts = df["Secretor Status"].value_counts().reset_index()
status_counts.columns = ["Secretor Status", "Count"]

fig_pie = px.pie(
    status_counts,
    names="Secretor Status",
    values="Count",
    title="Secretor Status Classification",
    color="Secretor Status",
    color_discrete_map= secretor_colors
)

fig_pie.update_layout(
    title="Secretor Status Classification",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

# ---- Layout Section ----
col1, col2 = st.columns([1,1])

with col1:
    # st.markdown("**Milk Collection Type**")
    st.plotly_chart(fig_source, use_container_width=True)


with col2:
    # st.markdown("**Secretor Status**")
    st.plotly_chart(fig_pie, use_container_width=True)


# ---- Table for Secretor Status x Sample Source Groups ----
# Create a pivot table for counts by Secretor Status (rows) and Sample Source (columns)
# Prepare data
count_df = (
    df[df["Sample Source"].isin(["Residual", "Scavenged"])]
    .groupby(["Secretor Status", "Sample Source"])
    .size()
    .reset_index(name="Count")
)

# Plot
fig = px.bar(
    count_df,
    x="Secretor Status",
    y="Count",
    color="Sample Source",
    barmode="group",
    text="Count",
    title="Sample Counts by Secretor Status and Sample Source",
    color_discrete_map=sample_source_colors
)

fig.update_layout(
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)


# ---- Milk Type ----
group1_options = sorted(df["Secretor Status"].dropna().unique())
group2_options = sorted(df["Sample Source"].dropna().unique())

selected_secretor = st.selectbox("Select Secretor Status", group1_options, key="secretor_group")
selected_source = st.selectbox("Select Sample Source", group2_options, key="sample_source")


filtered_df = df[
    (df["Secretor Status"] == selected_secretor) &
    (df["Sample Source"] == selected_source)
]

hmo_ranges = filtered_df[hmo_columns].agg(["min", "max"]).T
hmo_ranges["Range"] = hmo_ranges["max"] - hmo_ranges["min"]
hmo_ranges = hmo_ranges.reset_index().rename(columns={"index": "HMO"})

fig = px.bar(
    hmo_ranges,
    x="HMO",
    y="Range",
    text="Range",
    color="Range",
    color_continuous_scale="Reds",
    title=f"HMO Relative Abundance for {selected_secretor} + {selected_source}"
)

fig.update_layout(
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white",
    xaxis_title="",
    yaxis_title="Relative Abundance Range (AUC)",
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("HMO Relative Abundance Over Time (Longitudinal Subjects)")


####SPECIFICS HMO x META#####################

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #333; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong style="color:white;">Color (MBM/DBM?)</strong><br>
        🩷 MBM<br>
        ⚪ DBM<br>
        🟪 MBM + DBM<br>
        💚 Other
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #333; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong style="color:white;">Shape (Sample Source)</strong><br>
        ● Residual<br>
        × Scavenged
    </div>
    """, unsafe_allow_html=True)



# Clean column names
df.columns = df.columns.str.strip()

# Define HMO columns
hmo_columns = ["2FL", "DFLAC", "3SL", "6SL", "LNT", "LNnT", "LNFPI",
               "LNFPII", "LNFPIII", "LSTc", "DFLNT", "DSLNT", 
               "DFLNH", "FDSLNH", "DSLNH"]

# Filter to subjects with > 3 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()
df_long = df[df["Subject ID"].isin(longitudinal_subjects)].copy()

# Dropdowns with unique keys to prevent conflicts
selected_subject = st.selectbox("Select a Subject ID", sorted(df_long["Subject ID"].unique()), key="subject")
selected_hmo = st.selectbox("Select an HMO to plot", hmo_columns, key="hmo")

# Preprocessing
df_long["Iron Size"] = df_long["Iron Y/N"].map({"Y": 20, "N": 10}).fillna(10)
df_long["DOL"] = pd.to_numeric(df_long["DOL"], errors="coerce")

subject_df = df_long[df_long["Subject ID"] == selected_subject].copy()

mbm_colors = {
    "MBM": "#E24ADF",     # pink
    "DBM": "#F4F4F4",     # white
    "MBM + DBM": "#C2A4EC", # purple
    "Other": "#959191"    # Fallback (optional)
}

symbol_map = {
    "Residual": "triangle-up",  # or "circle", "diamond", "square", "triangle-up", etc.
    "Scavenged": "circle",     # or "diamond", "square", "triangle-up", etc.
    "Other": "cross"
}

size_map = {
    "Very Preterm": 10,
    "Moderate Preterm": 20,
    "Late Preterm": 30,
    "Term": 40
}

subject_df["CGA_Size"] = subject_df["CGA_cat"].map(size_map)


# Plot
fig = px.scatter(
    subject_df,
    x="DOL",
    y=selected_hmo,
    color="MBM/DMB?",
    symbol="Sample Source",
    size="CGA_Size",
    hover_data={
        "TPN Y/N?": True,
        "HMF Y/N?": True,
        "Iron Y/N": True,
        "CGA": True,
        "CGA_cat": True,
        "Sample Source": True
    },
    title=f"{selected_hmo} over Time for {selected_subject}",
    symbol_map=symbol_map,
    color_discrete_map=mbm_colors
)

fig.update_layout(
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)
