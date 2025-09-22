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
combined = pd.read_excel("Cleaned Data/merged_df.xlsx")

# st.success(f"Combined dataset has {combined.shape[0]} samples and {combined['Subject ID'].nunique()} unique subjects.")

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


# Bar chart for number of Female and Male infants
sex_counts = combined["Infant Sex"].value_counts().loc[["Female", "Male"]]

fig_sex = px.bar(
    sex_counts.reset_index(),
    x="Infant Sex",
    y="count",
    color="Infant Sex",
    color_discrete_map={"Female": "#FF69B4", "Male": "#1E90FF"},  # Pink for Female, Blue for Male
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

    st.subheader("Milk Collection Notes")

    # Count the occurrences of each unique note (excluding NaN)
    notes_counts = combined["Sample Source"].dropna().value_counts()

    if not notes_counts.empty:
        st.write(notes_counts.to_frame().rename(columns={"Sample Source": "Count"}))
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





st.subheader("Growth Metrics by Infant Sex (Subjects with > 3 Timepoints)")


# Filter subjects with >3 timepoints
subject_counts = combined["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts > 3].index.tolist()
filtered = combined[combined["Subject ID"].isin(longitudinal_subjects)].copy()

# Clean DOL
filtered["DOL"] = pd.to_numeric(filtered["DOL"], errors="coerce")


# Bar chart: Number of females and males with >3 timepoints
sex_long_counts = filtered.groupby("Infant Sex")["Subject ID"].nunique().loc[["Female", "Male"]]

fig_sex_long = px.bar(
    sex_long_counts.reset_index(),
    x="Infant Sex",
    y="Subject ID",
    color="Infant Sex",
    color_discrete_map={"Female": "#FF69B4", "Male": "#1E90FF"},
    text="Subject ID",
    title="Number of Subjects with >3 Timepoints by Sex"
)
fig_sex_long.update_layout(
    xaxis_title="Infant Sex",
    yaxis_title="Number of Subjects",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font_color="#000000"
)
st.plotly_chart(fig_sex_long, use_container_width=True)


# Sex labels and colors
sex_labels = {"Female": "Girls", "Male": "Boys"}
sex_colors = {"Female": "#FF69B4", "Male": "#1E90FF"}  # pink and blue

# Loop through each sex
for sex in ["Female", "Male"]:
    df_sex = filtered[filtered["Infant Sex"] == sex].copy()

    if df_sex.empty:
        st.markdown(f"### {sex_labels[sex]}")
        st.warning("No data available.")
        continue

    st.markdown(f"### {sex_labels[sex]}")

    fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharex=True)
    fig.patch.set_facecolor("#ffffff")

    # Plot each growth metric
    for ax, (metric, label) in zip(
        axs,
        [("Current Weight", "Weight (g)"), ("Current Height", "Height (cm)"), ("Current HC", "Head Circumference (cm)")]
    ):
        for sid in df_sex["Subject ID"].unique():
            subject_df = df_sex[df_sex["Subject ID"] == sid].sort_values("DOL")
            ax.plot(subject_df["DOL"], subject_df[metric], marker="o", label=sid, color=sex_colors[sex], alpha=0.3)

        ax.set_title(label, fontsize=10)
        ax.set_xlabel("DOL")
        ax.set_ylabel(label)
        ax.grid(True)

    plt.tight_layout()
    st.pyplot(fig)

    








### 

st.header("Clinical Outcomes - TPN")



