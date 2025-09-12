import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up the dashboard
st.set_page_config(page_title="NeoBank HMO Dashboard", layout="wide")
st.title("NeoBank: Unlinked Samples")


#st.markdown("Explore "Unlinked" sample clinical metadata with human milk oligosaccaride data.")

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
         <h3 style="margin-top:0;">Data Analysis</h3>
        <p><em>Sample Workup Conducted: June 2025</em></p>
        </p>
        This dashboard highlights two key components of the NeoBANK dataset:
        <ol>
            <li>
                <strong>Sample Overview</strong>
            </li>
            <li>
                <strong>HMO Analysis</strong> – Each sample was analyzed for 
                <strong>15 human milk oligosaccharides (HMOs)</strong>. 
        </ol>

        <p>By linking these measurements with infant growth data (weight, length, head circumference), 
        we can begin exploring potential trends and future clinical applications.</p>
        </div>
        </div>
    """, unsafe_allow_html=True)

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
            background-color: #5e6077ff;
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
    color_continuous_scale="Teal"
)

fig.update_layout(
    xaxis_title="Subject ID",
    yaxis_title="Number of Samples",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="#000000"
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
    color_continuous_scale="Teal"
    )

fig_aliquots.update_layout(
    xaxis_title="Subject ID",
    yaxis_title="Number of Aliquots",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black"
    )

st.plotly_chart(fig_aliquots, use_container_width=True)




#############-----------------
st.subheader("Milk & Nutrition Details")

milk_vars = [
    # "Scavenged/Fresh?",
    "MBM/DMB?",
    "HMF Y/N?",
    "TPN Y/N?",
    'Iron Y/N?'
]

selected_milk_var = st.selectbox("Select a milk-related variable to explore:", milk_vars)

if selected_milk_var:
    st.markdown(f"**Distribution of** `{selected_milk_var}`")

    value_counts = df[selected_milk_var].value_counts()

    # Show value counts
    st.write(value_counts.to_frame().rename(columns={selected_milk_var: "Count"}))

    # Bar chart
    st.bar_chart(value_counts)

    st.subheader("Milk Collection Notes")

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
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            font_color="black"
        )
        st.plotly_chart(fig_notes, use_container_width=True)
    else:
        st.info("No data available in the 'additional notes' column.")


#############-----------------
st.subheader("Growth Metric Overview")

#############-----------------


# Filter subjects with >3 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

st.markdown("📍 Showing only subjects with > 3 timepoints")
selected_subject = st.selectbox("Select a subject:", longitudinal_subjects)

# Filter and sort by DOL
subject_df = df[df["Subject ID"] == selected_subject].copy()
subject_df["DOL"] = pd.to_numeric(subject_df["DOL"], errors="coerce")  # ensure numeric
subject_df = subject_df.sort_values("DOL")  # 👈 ensures line plots follow correct order


# Show number of subjects with >3 timepoints
num_longitudinal_subjects = len(longitudinal_subjects)
st.markdown(f"""
    <div style="
        background-color: #5e6077ff;
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
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.plot(subject_df[x], subject_df[y], marker="o", color="#1B4A81")
    ax.set_xlabel(x, color='black')
    ax.set_ylabel(y, color='black')
    ax.set_title(title, color='black')
    ax.tick_params(colors='black')

    # Add tick marks every 2 DOL units
    x_vals = subject_df[x].dropna().sort_values()
    if not x_vals.empty:
        tick_range = np.arange(x_vals.min(), x_vals.max() + 2, 3)
        ax.set_xticks(tick_range)
    return fig

# Weight
with col1:
    st.pyplot(make_growth_plot("DOL", "Current Weight", "Weight (g)"))

# Height
with col2:
    st.pyplot(make_growth_plot("DOL", "Current Height", "Height (cm)"))

# Head Circumference
with col3:
    st.pyplot(make_growth_plot("DOL", "Current HC", "Head Circumference (cm)"))





##############################################################
st.title("Unlinked HMO Overview")

with st.container():
    st.markdown("""
        <div style="
            background-color: #5e6077ff;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: white;
        ">
            <strong>Summary:</strong><br>
        - Each milk sample was analyzed for <strong>15 different human milk oligosaccharides (HMOs)</strong> using HPLC. 
                <p>
        - 28 out of the 34 subjects received MBM (mother's own milk).
                </p>
        - Results are expressed as <em>area under the curve (AUC)</em> values.  
                </p>
        - <strong>2’FL</strong> is used to classify <em>secretor status</em> with a threshold of 5 million AUC.
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
    "Secretor": "#357b8d",        # light blue
    "Non-Secretor": "#999ad2"     # white
}




##############################################################
# ---- Table for Secretor Status x Sample Source Groups ----
# Create a pivot table for counts by Secretor Status (rows) and Sample Source (columns)
# Prepare data

st.subheader("MOM Secretor Status by Sample Source")


status_check = pd.read_excel("Secretor_status_check.xlsx")

# Box showing number of unique subject IDs that received MBM
num_mbm_subjects = status_check.shape[0]
st.markdown(f"""
    <div style="
        background-color: #5e6077ff;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.2);
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    ">
        {num_mbm_subjects} Unique Subject IDs that received MBM
    </div>
""", unsafe_allow_html=True)


# Bar chart: Secretor Status counts (unique subjects)
secretor_counts = status_check["secretorstatus_mom"].value_counts().reset_index()
secretor_counts.columns = ["Secretor Status", "Count"]

fig_secretor = px.bar(
    secretor_counts,
    x="Secretor Status",
    y="Count",
    text="Count",
    color="Secretor Status",
    color_discrete_map=secretor_colors,
    title="Count of Secretor vs Non-Secretor Subjects"
)

fig_secretor.update_traces(textposition="outside")
fig_secretor.update_layout(
    template="simple_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black",
    yaxis_title="Number of Subjects",
    xaxis_title="Secretor Status",
    margin=dict(t=40, r=20, l=20, b=40)
)

st.plotly_chart(fig_secretor, use_container_width=True)


# -------------------------------------------------------------------
# Consistency of Secretor Status (per subject)
# -------------------------------------------------------------------
st.subheader("Secretor Status Consistency Across Timepoints")

# Use the per-subject summary from status_check
change_counts = (
    status_check["Change Flag"]
    .value_counts()
    .rename_axis("Change Flag")
    .reset_index(name="Subjects")
)

fig_change = px.bar(
    change_counts,
    x="Change Flag",
    y="Subjects",
    text="Subjects",
    color="Change Flag",
    color_discrete_map={"No Change": "#081d02", "Changed": "#a19090"},
    title="Subjects with Stable vs Changed Secretor Status"
)

fig_change.update_traces(textposition="outside")
fig_change.update_layout(
    template="simple_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black",
    yaxis_title="Number of Subjects",
    xaxis_title="Secretor Status Consistency"
)

st.plotly_chart(fig_change, use_container_width=True, theme=None)

# Optional: list changed subjects
changed_subjects = status_check.query("`Change Flag` == 'Changed'")["Subject ID"].tolist()
if changed_subjects:
    st.markdown(f"**Subjects with changed status:** {', '.join(map(str, changed_subjects))}")
else:
    st.markdown("✅ All subjects had consistent secretor status across timepoints.")

# Explanatory box
st.markdown("""
    <div style="
        background-color: #f9e6e6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #a94442;
        font-size: 1rem;
        box-shadow: 0 0 5px rgba(169,68,66,0.1);
    ">
        <strong>What does inconsistency in secretor status mean?</strong><br>
        If a subject's secretor status changes across timepoints, this may indicate differences in milk given (MBM vs DBM) 
        or potential sample mix-ups.
    </div>
""", unsafe_allow_html=True)













# ---- HMO Relative Abundance ----=---------------------------------------
# ---- Milk Type ----

st.subheader("Number of Samples by Group")

sample_counts = (
    df.groupby(["Secretor Status", "Sample Source", "MBM/DMB?"])
      .size()
      .reset_index(name="Count")
)

fig_counts = px.bar(
    sample_counts,
    x="Sample Source",
    y="Count",
    color="Secretor Status",
    facet_col="MBM/DMB?",
    barmode="group",
    title="Sample Counts per Group",
    color_discrete_map=secretor_colors
)

# Remove "MBM/DMB?=" prefix in facet titles
fig_counts.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Show axis titles only once
# Remove x-axis labels completely
fig_counts.update_xaxes(title_text="")

fig_counts.update_yaxes(title_text="", showticklabels=True)  # clear all facet y-axis labels

# Add single global axis titles
fig_counts.update_layout(
    xaxis_title="Sample Source",
    yaxis_title="Number of Samples",
    template="simple_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black"
)

st.plotly_chart(fig_counts, use_container_width=True, theme=None)


##################
st.subheader("Average HMO Relative Abundance by Sample Groups")

# Dropdown options
milk_type_options = sorted(df["MBM/DMB?"].dropna().unique())
sample_source_options = ['Prepped in Milk Room', 'Scavenged']
secretor_options = sorted(df["Secretor Status"].dropna().unique())

# Dropdown widgets
selected_milk = st.selectbox("Select Milk Type", milk_type_options, key="milk_type")
selected_source = st.selectbox("Select Sample Source", sample_source_options, key="sample_source")
selected_secretor = st.selectbox("Select Secretor Status", secretor_options, key="secretor_group")

# Filter the data correctly
filtered_df = df[
    (df["MBM/DMB?"] == selected_milk) &
    (df["Sample Source"] == selected_source) &
    (df["Secretor Status"] == selected_secretor)
]

# --- Compute mean HMO values ---
hmo_means = filtered_df[hmo_columns].mean().reset_index()
hmo_means.columns = ["HMO", "Mean AUC"]

fig = px.bar(
    hmo_means,
    x="HMO",
    y="Mean AUC",
    text="Mean AUC",
    color="Mean AUC",
    color_continuous_scale="Blues",
    title=f"Average HMO Relative Abundance: {selected_milk} + {selected_source} + {selected_secretor}"
)

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black",
    xaxis_title="",
    yaxis_title="Mean Area under the Curve (AUC)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("HMO Relative Abundance Over Time (Longitudinal Subjects)")




####SPECIFICS HMO x META#####################
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Identify longitudinal subjects ---
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts >= 3].index.tolist()

# Dropdown only shows longitudinal subjects
subject_id = st.selectbox("Select a Subject ID", sorted(longitudinal_subjects))


growth_metric = st.selectbox("Select Growth Metric", ["Current Weight", "Current Height", "Current HC"])

# Filter and sort
subject_df = df[df["Subject ID"] == subject_id].copy()
subject_df = subject_df.sort_values("DOL")

# --- Normalize HMO values ---
hmo_values = subject_df[hmo_columns]
hmo_norm = (hmo_values - hmo_values.min()) / (hmo_values.max() - hmo_values.min())
hmo_norm["Sample #"] = range(1, len(hmo_norm) + 1)
hmo_norm["DOL"] = subject_df["DOL"].values

# Melt only HMO columns
hmo_long = hmo_norm.melt(
    id_vars=["Sample #","DOL"], 
    value_vars=hmo_columns, 
    var_name="HMO", 
    value_name="Relative Abundance"
)

# --- Build figure ---
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.05,
    subplot_titles=[f"HMO Relative Abundance Heatmap for {subject_id}", f"{growth_metric} Over Time"]
)

# Heatmap with evenly spaced columns
fig.add_trace(
    go.Heatmap(
        x=hmo_long["Sample #"],   # evenly spaced sample index
        y=hmo_long["HMO"],
        z=hmo_long["Relative Abundance"],
        colorscale="Blues",
        colorbar=dict(title="Relative Abundance")
    ),
    row=1, col=1
)

# Growth line
# Growth line
fig.add_trace(
    go.Scatter(
        x=subject_df["Sample #"] if "Sample #" in subject_df else list(range(1, len(subject_df)+1)),
        y=subject_df[growth_metric],
        mode="lines+markers",
        name=growth_metric,
        line=dict(color="black", width=2)
    ),
    row=2, col=1
)


# Replace x-axis ticks with actual DOL labels
fig.update_xaxes(
    tickmode="array",
    tickvals=list(range(1, len(subject_df["DOL"]) + 1)),
    ticktext=subject_df["DOL"].tolist(),
    title="Day of Life"
)

# Layout polish
fig.update_layout(
    height=600,
    template="simple_white"
)

st.plotly_chart(fig, use_container_width=True)
















import plotly.graph_objects as go

# ---------- SETUP ----------

# Clean column names
df.columns = df.columns.str.strip()

st.subheader ("Individual HMO Relative Abundance & Growth")
# Color and symbol maps
mbm_colors = {
    "MBM": "#E24ADF",
    "DBM": "#817287",
    "MBM + DBM": "#C2A4EC",
    "Other": "#1C1C1C"
}

symbol_map = {
    "Residual": "triangle-up",
    "Scavenged": "circle",
    "Other": "cross"
}

# HMO and Growth Columns
hmo_columns = ["2FL", "DFLAC", "3SL", "6SL", "LNT", "LNnT", "LNFPI",
               "LNFPII", "LNFPIII", "LSTc", "DFLNT", "DSLNT", 
               "DFLNH", "FDSLNH", "DSLNH"]

growth_metric_options = {
    "Weight": "Current Weight",
    "Height": "Current Height",
    "Head Circumference": "Current HC"
}

# Filter subjects with >3 timepoints
subject_counts = df["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

# Dropdowns
selected_subject = st.selectbox("Select a Subject ID", sorted(longitudinal_subjects))
selected_hmo = st.selectbox("Select an HMO to plot", hmo_columns)
selected_growth_label = st.selectbox("Select Growth Metric", list(growth_metric_options.keys()))
selected_growth_column = growth_metric_options[selected_growth_label]

# Prepare subject data
subject_df = df[df["Subject ID"] == selected_subject].copy()
subject_df["DOL"] = pd.to_numeric(subject_df["DOL"], errors="coerce")
subject_df = subject_df.sort_values("DOL")

# CGA Binning
subject_df["CGA_cat"] = pd.cut(
    subject_df["CGA"],
    bins=[0, 32, 34, 36, 45],
    labels=["Very Preterm", "Moderate Preterm", "Late Preterm", "Term"],
    include_lowest=True
)

# ---------- BUILD FIG ----------
fig = go.Figure()

# Growth line
fig.add_trace(go.Scatter(
    x=subject_df["DOL"],
    y=subject_df[selected_growth_column],
    mode="lines+markers",
    name=f"{selected_growth_label}",
    marker=dict(color="#1B4A81", size=10),
    yaxis="y1"
))

# HMO points by MBM/DBM and Sample Source
for mbm_type in subject_df["MBM/DMB?"].dropna().unique():
    for sample_source in subject_df["Sample Source"].dropna().unique():
        filtered = subject_df[
            (subject_df["MBM/DMB?"] == mbm_type) &
            (subject_df["Sample Source"] == sample_source)
        ]
        fig.add_trace(go.Scatter(
            x=filtered["DOL"],
            y=filtered[selected_hmo],
            mode="markers",
            name=f"{mbm_type} / {sample_source}",
            marker=dict(
                color=mbm_colors.get(mbm_type, "#959191"),
                symbol=symbol_map.get(sample_source, "circle"),
                size=14
            ),
            yaxis="y2",
            hovertext=[
                f"TPN: {t}<br>HMF: {h}<br>CGA: {c}<br>Iron: {i}<br>Source: {s}" 
                for t, h, c, i, s in zip(
                    filtered["TPN Y/N?"],
                    filtered["HMF Y/N?"],
                    filtered["CGA"],
                    filtered["Iron Y/N?"],
                    filtered["Sample Source"]
                )
            ],
            hoverinfo="text"
        ))

# Layout
fig.update_layout(
    title=f"{selected_growth_label} and {selected_hmo} Over Time for {selected_subject}",
    xaxis=dict(title="Day of Life (DOL)"),
    yaxis=dict(title=selected_growth_label, side="left"),
    yaxis2=dict(
        title=f"{selected_hmo} (AUC)",
        overlaying="y",
        side="right"
    ),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black"
)

st.plotly_chart(fig, use_container_width=True)
