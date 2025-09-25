import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="NeoBANK Cohort Dashboard", layout="wide")
st.title("NeoBANK Cohort: Linked + Unlinked Samples")

# Load your files
unlinked = pd.read_excel("Cleaned Data/Unlinked_Merged.xlsx")
linked = pd.read_excel("Cleaned Data/Linked_Merged.xlsx")
combined = pd.read_excel("Cleaned Data/merged_ALL.xlsx")

# st.success(f"Combined dataset has {combined.shape[0]} samples and {combined['Subject ID'].nunique()} unique subjects.")


st.markdown("""
    <div style="
        background-color: #e0e7ef;
        color: #1B4A81;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 1rem;
        display: inline-block;
    ">
        Cohort Location: San Diego, CA
    </div>
""", unsafe_allow_html=True)


# Count metrics
num_subjects = combined["Subject ID"].nunique()
num_samples = combined["sample_unique_id"].nunique()

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
    metric_card("Total Samples", combined["sample_unique_id"].nunique())

with col2:
    metric_card("Unique Subjects", combined["Subject ID"].nunique())


#############-------------------------

st.subheader("Sample Count per Subject")

sample_counts = combined["Subject ID"].value_counts().sort_index()
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
total_aliquots = combined["Aliquots_num"].sum()
metric_card("Number of Total Aliquots", total_aliquots)

# Aliquots per subject
aliquots_per_subject = combined.groupby("Subject ID")["Aliquots_num"].sum().reset_index()
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
st.subheader("Subject Demographics")

col_linked, col_sample_source = st.columns(2)


# Left: Bar chart for number of 'N' and 'Y' in "Linked?"
with col_linked:
    linked_counts = combined["Linked"].value_counts().loc[["N", "Y"]]
    fig_linked = px.bar(
        linked_counts.reset_index(),
        x="Linked",
        y="count",
        color="Linked",
        color_discrete_map={"N": "#6B6B6B", "Y": "#658891"},
        text="count",
        title="Number of Linked vs Unlinked Samples"
    )
    fig_linked.update_layout(
        xaxis_title="Linked",
        yaxis_title="Number of Samples",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font_color="#000000"
    )
    st.plotly_chart(fig_linked, use_container_width=True)


with col_sample_source:
    # Pie chart for "Sample Source"
    sample_source_counts = combined["Sample Source"].dropna().value_counts()
    # Define colors: "Scavenged" dark grey, others light grey
    color_map = {src: "#6B6B6B" if src == "Scavenged" else "#E0E0E0" for src in sample_source_counts.index}
    fig_sample_source = px.pie(
        names=sample_source_counts.index,
        values=sample_source_counts.values,
        title="Distribution of Samples by Source",
        color=sample_source_counts.index,
        color_discrete_map=color_map
    )
    fig_sample_source.update_traces(textinfo='percent+label')
    fig_sample_source.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font_color="#000000"
    )
    st.plotly_chart(fig_sample_source, use_container_width=True)


# Bar chart for number of Female and Male infants
sex_counts = combined["Infant Sex"].value_counts().loc[["Female", "Male"]]
fig_sex = px.bar(
    sex_counts.reset_index(),
    x="Infant Sex",
    y="count",
    color="Infant Sex",
    color_discrete_map={"Female": "#F09EC7", "Male": "#A0C8F0"},  # Pink for Female, Blue for Male
    text="count",
    title="Number of Infants by Sex"
)

fig_sex.update_layout(
    xaxis_title="Infant Sex",
    yaxis_title="Number of Infants",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="#000000"
)

st.plotly_chart(fig_sex, use_container_width=True)

#############-----------------
st.subheader("Milk & Nutrition Details")

milk_vars = [
    # "Scavenged/Fresh?",
    "Type of Milk",
    "HMF",
    "TPN",
    'Iron'
]

selected_milk_var = st.selectbox("Select a milk-related variable to explore:", milk_vars)

if selected_milk_var:
    st.markdown(f"**Distribution of** `{selected_milk_var}`")

    value_counts = combined[selected_milk_var].value_counts()

    # Show value counts
    st.write(value_counts.to_frame().rename(columns={selected_milk_var: "Count"}))

    # Bar chart
    st.bar_chart(value_counts)







st.subheader("Growth Metric Overview")

#############-----------------


# Filter subjects with >3 timepoints
subject_counts = combined["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

st.markdown("📍 Showing only subjects with > 3 timepoints")
selected_subject = st.selectbox("Select a subject:", sorted(longitudinal_subjects))

# Filter and sort by DOL
subject_df = combined[combined["Subject ID"] == selected_subject].copy()
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


################-----------------  

st.header("Human Milk Oligosaccharides (HMO) Overview")



# Find which subjects ever had MOM
subjects_with_mom = combined.loc[combined["Type of Milk"] == "MOM", "Subject ID"].unique()
n_with_mom = len(subjects_with_mom)

# All unique subjects
all_subjects = combined["Subject ID"].unique()
n_total = len(all_subjects)

# Those who never had MOM
n_without_mom = n_total - n_with_mom

# Display counts
st.markdown(f"**Subjects who recieved MOM during sample collection period:** {n_with_mom}")
st.markdown(f"**Subjects who DID NOT recieve MOM during sample collection period:** {n_without_mom}")



st.subheader("Maternal Secretor Status (First MOM Sample per Subject)")

# 1. Keep only MOM rows
mom_df = combined[combined["Type of Milk"] == "MOM"].copy()

# 2. Deduplicate by Subject ID (keeps the first MOM per subject)
mom_unique = mom_df.sort_values("sample_unique_id").drop_duplicates("Subject ID", keep="first")

# 3. Count distribution
secretor_counts = mom_unique["moms_secretor_status"].value_counts().reset_index()
secretor_counts.columns = ["moms_secretor_status", "count"]

# 4. Plot bar chart
fig = px.bar(
    secretor_counts,
    x="moms_secretor_status",
    y="count",
    color="moms_secretor_status",
    text="count",
    color_discrete_map={"Secretor": "#4CAF50", "Non-Secretor": "#F44336"},
    title="Maternal Secretor Status (Unique Mothers)"
)

fig.update_layout(
    xaxis_title="Secretor Status",
    yaxis_title="Number of Mothers",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="#000000"
)

st.plotly_chart(fig, use_container_width=True)








#### SPECIFICS HMO x META #####################
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

st.subheader("HMO and Growth Relationship (Longitudinal Subjects)")

# --- Identify longitudinal subjects ---
subject_counts = combined["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts >= 3].index.tolist()

# Dropdown only shows longitudinal subjects
subject_id = st.selectbox("Select a Subject ID", sorted(longitudinal_subjects))

growth_metric = st.selectbox("Select Growth Metric", ["Current Weight", "Current Height", "Current HC"])

# --- Define HMO columns (nmol/mL block only) ---
# Explicit ordered list of HMO columns (nmol/mL only, 2'FL through DSLNH)
hmo_columns = [
    "2FL [nmol/mL]",
    "DFLac [nmol/mL]",
    "3SL [nmol/mL]",
    "6SL [nmol/mL]",
    "LNT [nmol/mL]",
    "LNnT [nmol/mL]",
    "LNFP I [nmol/mL]",
    "LNFP II [nmol/mL]",
    "LNFP III [nmol/mL]",
    "LSTc [nmol/mL]",
    "DFLNT [nmol/mL]",
    "DSLNT [nmol/mL]",
    "DFLNH [nmol/mL]",
    "FDSLNH [nmol/mL]",
    "DSLNH [nmol/mL]"
]


# --- Filter and sort subject ---
subject_df = combined[combined["Subject ID"] == subject_id].copy()
subject_df = subject_df.sort_values("DOL").reset_index(drop=True)

# --- Check if this subject has any HMO values ---
if subject_df[hmo_columns].notna().any().any():

    # Normalize HMO values (0–1 per subject)
    hmo_values = subject_df[hmo_columns]
    hmo_norm = (hmo_values - hmo_values.min()) / (hmo_values.max() - hmo_values.min())
    hmo_norm["Sample #"] = range(1, len(hmo_norm) + 1)
    hmo_norm["DOL"] = subject_df["DOL"].values

    # Melt into long format
    hmo_long = hmo_norm.melt(
        id_vars=["Sample #", "DOL"], 
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

    # Heatmap
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

    # Growth line
    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(subject_df) + 1)),
            y=subject_df[growth_metric],
            mode="lines+markers",
            name=growth_metric,
            line=dict(color="black", width=2)
        ),
        row=2, col=1
    )

    # Replace x-axis ticks with DOL
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, len(subject_df["DOL"]) + 1)),
        ticktext=subject_df["DOL"].tolist(),
        title="Day of Life"
    )

    fig.update_layout(
        height=600,
        template="simple_white"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning(f"No HMO data available for subject {subject_id}.")






###################################################################



import plotly.graph_objects as go
import pandas as pd
import streamlit as st

st.subheader("Individual HMO Relative Abundance & Growth")

# Color and symbol maps
mbm_colors = {
    "MOM": "#BF68BE",
    "DBM": "#F59227",
    "MOM + DBM": "#C2A4EC",
    "Other": "#1C1C1C"
}

symbol_map = {
    "Residual": "triangle-up",
    "Scavenged": "circle",
    "Other": "cross"
}

# HMO columns (nmol/mL block, 2'FL through DSLNH only)
hmo_columns = [
    "2FL [nmol/mL]",
    "DFLac [nmol/mL]",
    "3SL [nmol/mL]",
    "6SL [nmol/mL]",
    "LNT [nmol/mL]",
    "LNnT [nmol/mL]",
    "LNFP I [nmol/mL]",
    "LNFP II [nmol/mL]",
    "LNFP III [nmol/mL]",
    "LSTc [nmol/mL]",
    "DFLNT [nmol/mL]",
    "DSLNT [nmol/mL]",
    "DFLNH [nmol/mL]",
    "FDSLNH [nmol/mL]",
    "DSLNH [nmol/mL]"
]


# Growth metric options
growth_metric_options = {
    "Weight": "Current Weight",
    "Height": "Current Height",
    "Head Circumference": "Current HC"
}

# Filter subjects with >3 timepoints
subject_counts = combined["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()

# Dropdowns
selected_subject = st.selectbox("Select a Subject ID", sorted(longitudinal_subjects))
selected_hmo = st.selectbox("Select an HMO to plot", hmo_columns)
selected_growth_label = st.selectbox("Select Growth Metric", list(growth_metric_options.keys()))
selected_growth_column = growth_metric_options[selected_growth_label]

# Prepare subject data
subject_df = combined[combined["Subject ID"] == selected_subject].copy()
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
for mbm_type in subject_df["Type of Milk"].dropna().unique():
    for sample_source in subject_df["Sample Source"].dropna().unique():
        filtered = subject_df[
            (subject_df["Type of Milk"] == mbm_type) &
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
                    filtered["TPN"],
                    filtered["HMF"],
                    filtered["CGA"],
                    filtered["Iron"],
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
        title=f"{selected_hmo} (nmol/mL)",
        overlaying="y",
        side="right"
    ),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="black"
)

st.plotly_chart(fig, use_container_width=True)
