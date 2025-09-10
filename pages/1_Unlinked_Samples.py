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
        Each milk sample was analyzed for <strong>15 different human milk oligosaccharides (HMOs)</strong> using HPLC. 
                <p>
        Results are expressed as <em>area under the curve (AUC)</em> values.  
                </p>
        <strong>2’FL</strong> is used to classify <em>secretor status</em> with a threshold of 5 million AUC.
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


# ---- Sample Source Counts ----
# Count values in the Sample Source column
# Deduplicate by subject → take the first non-null record for each subject
df_unique = (
    df.sort_values("Subject ID")  # keep stable order
      .groupby("Subject ID", as_index=False)
      .first()   # first row for each subject
)

# Now df_unique has exactly 34 rows (one per subject)
# Count secretor status
secretor_counts = (
    df_unique["Secretor Status"]
      .value_counts()
      .rename_axis("Secretor Status")
      .reset_index(name="Unique Subjects")
)

# Plot pie chart
fig = px.pie(
    secretor_counts,
    names="Secretor Status",
    values="Unique Subjects",
    title="Secretor Status (by Unique Subjects)",
    color="Secretor Status",
    color_discrete_map=secretor_colors
)

fig.update_layout(
    template="simple_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black"
)

st.plotly_chart(fig, use_container_width=True, theme=None)

# Optional sanity check
st.write("Unique Subject IDs:", df["Subject ID"].nunique())


# ---- Table for Secretor Status x Sample Source Groups ----
# Create a pivot table for counts by Secretor Status (rows) and Sample Source (columns)
# Prepare data

st.subheader("Secretor Status by Sample Source")

view_unique = st.toggle("Count unique subjects (not samples)", value=False)
show_percent = st.toggle("Show percentages instead of counts", value=False)

if view_unique:
    # one row per subject+source (if a subject has both sources, they can appear once in each source)
    df_unique = (
        df.sort_values(["Subject ID"])
          .dropna(subset=["Secretor Status", "Sample Source"])
          .drop_duplicates(subset=["Subject ID", "Sample Source"])
    )
    grouped = (
        df_unique.groupby(["Sample Source", "Secretor Status"])
                 .size()
                 .reset_index(name="Count")
    )
else:
    # raw sample counts
    grouped = (
        df.dropna(subset=["Secretor Status", "Sample Source"])
          .groupby(["Sample Source", "Secretor Status"])
          .size()
          .reset_index(name="Count")
    )

if show_percent:
    grouped["Total"] = grouped.groupby("Sample Source")["Count"].transform("sum")
    grouped["Percent"] = (grouped["Count"] / grouped["Total"] * 100).round(1)
    y_col = "Percent"
    y_title = "Percent of Samples" if not view_unique else "Percent of Subjects"
    text_col = "Percent"
else:
    y_col = "Count"
    y_title = "Number of Samples" if not view_unique else "Number of Subjects"
    text_col = "Count"

fig_ss = px.bar(
    grouped,
    x="Sample Source",
    y=y_col,
    color="Secretor Status",
    barmode="group",              # use "stack" if you prefer stacked bars
    text=text_col,
    color_discrete_map=secretor_colors,
    title="Secretor Status by Sample Source"
)

fig_ss.update_traces(textposition="outside", cliponaxis=False)

fig_ss.update_layout(
    template="simple_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black",
    yaxis_title=y_title,
    xaxis_title="Sample Source",
    legend_title="Secretor Status",
    margin=dict(t=60, r=20, l=20, b=40)
)

st.plotly_chart(fig_ss, use_container_width=True, theme=None)



st.subheader("Secretor Status Consistency Across Timepoints")

# Clean col names
df.columns = df.columns.str.strip()

# For each subject, check if secretor status ever changes
status_change = (
    df.groupby("Subject ID")["Secretor Status"]
      .nunique()   # number of distinct statuses per subject
      .reset_index(name="n_statuses")
)

status_change["Change Flag"] = status_change["n_statuses"].apply(
    lambda x: "Changed" if x > 1 else "No Change"
)

# Count how many subjects in each category
change_counts = (
    status_change["Change Flag"]
      .value_counts()
      .rename_axis("Change Flag")
      .reset_index(name="Subjects")
)

# Plot
fig_change = px.bar(
    change_counts,
    x="Change Flag",
    y="Subjects",
    text="Subjects",
    color="Change Flag",
    color_discrete_map={"No Change": "#357b8d", "Changed": "#d97b7b"},
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

# Optional: show which subjects changed
changed_subjects = status_change[status_change["Change Flag"] == "Changed"]["Subject ID"].tolist()
if changed_subjects:
    st.markdown(f"**Subjects with changed status:** {', '.join(changed_subjects)}")
else:
    st.markdown("✅ All subjects had consistent secretor status across timepoints.")



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
        If a subject's secretor status changes across timepoints, this may indicate differences in milk given (MBM vs DBM) or potential sample mix-ups.
    </div>
""", unsafe_allow_html=True)



# ---- HMO Relative Abundance ----=---------------------------------------
# ---- Milk Type ----
group1_options = sorted(df["Secretor Status"].dropna().unique())
group2_options = ['Residual', 'Scavenged']
group3_options = sorted(df["MBM/DMB?"].dropna().unique())  

selected_secretor = st.selectbox("Select Secretor Status", group1_options, key="secretor_group")
selected_source = st.selectbox("Select Sample Source", group2_options, key="sample_source")
selected_milk = st.selectbox("Select Milk Type", group3_options, key="milk_type")


filtered_df = df[
    (df["Secretor Status"] == selected_secretor) &
    (df["Sample Source"] == selected_source) &
    (df["MBM/DMB?"] == selected_milk)  
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
    title=f"HMO AUC for {selected_secretor} + {selected_source} + {selected_milk} Samples"
)

fig.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black",
    xaxis_title="",
    yaxis_title="Area under the Curve (AUC)",
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("HMO Relative Abundance Over Time (Longitudinal Subjects)")


####SPECIFICS HMO x META#####################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------- SETUP ----------

# Clean column names
df.columns = df.columns.str.strip()

# Legend: Color + Symbol
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #6f768fff; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong style="color:white;">Color (Type of Milk) </strong><br>
        * Color codes is based on the type of milk given to infant
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #6f768fff; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong style="color:white;">Shape (Sample Source)</strong><br>
        ● Residual<br>
        × Scavenged
    </div>
    """, unsafe_allow_html=True)

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
                    filtered["Iron Y/N"],
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
