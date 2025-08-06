import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.title("NeoBank: Linked Samples")


meta = pd.read_excel("cleaned_linkedmeta_updated.xlsx")


####--------------------------------------------------------------------------------------------------------------
############### Overview section ###############
st.header("Linked Metadata Overview")

# Count metrics
num_subjects = meta["Subject ID"].nunique()
num_samples = meta["Subject ID"].count()

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
    metric_card("Total Samples", meta["Subject ID"].count())

with col2:
    metric_card("Unique Subjects", meta["Subject ID"].nunique())


#############-------------------------

st.subheader("Sample Count per Subject")

# Count how many samples per subject
sample_counts = meta["Subject ID"].value_counts().sort_index()
sample_counts_df = sample_counts.reset_index()
sample_counts_df.columns = ["Subject ID", "Sample Count"]

# Plot bar chart using Plotly for better styling
import plotly.express as px

fig_milk = px.bar(
    sample_counts_df,
    x="Subject ID",
    y="Sample Count",
    text="Sample Count",
    color="Sample Count",
    color_continuous_scale="Blues"
)

fig_milk.update_layout(
    xaxis_title="Subject ID",
    yaxis_title="Number of Samples",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

st.plotly_chart(fig_milk, use_container_width=True)



############ Aliquots Overview
st.subheader("Aliquots Overview")

# Metric card for total aliquots
total_aliquots = meta["Aliquots"].sum()
metric_card("Number of Total Aliquots", total_aliquots)

# Aliquots per subject
aliquots_per_subject = meta.groupby("Subject ID")["Aliquots"].sum().reset_index()
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
    "Type of Milk",
    "HMF",
    "TPN",
    'Iron'
]

selected_milk_var = st.selectbox("Select a milk-related variable to explore:", milk_vars)

if selected_milk_var:
    st.markdown(f"**Distribution of** `{selected_milk_var}`")

    value_counts = meta[selected_milk_var].value_counts()

    # Show value counts
    st.write(value_counts.to_frame().rename(columns={selected_milk_var: "Count"}))

    # Bar chart
    st.bar_chart(value_counts)



pie_col1, pie_col2 = st.columns(2)

with pie_col1:
    feeding_counts = meta["Feeding Time Period"].value_counts(dropna=False)
    fig_feeding = px.pie(
        names=feeding_counts.index.astype(str),
        values=feeding_counts.values,
        title="Feeding Time Period"
    )
    fig_feeding.update_traces(textinfo='percent+label')
    fig_feeding.update_layout(
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#1E1E1E",
        font_color="white"
    )
    st.plotly_chart(fig_feeding, use_container_width=True)

with pie_col2:
    pressed_counts = meta["Is Prepped"].value_counts(dropna=False)
    fig_pressed = px.pie(
        names=pressed_counts.index.astype(str),
        values=pressed_counts.values,
        title="Is Prepped"
    )
    fig_pressed.update_traces(textinfo='percent+label')
    fig_pressed.update_layout(
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#1E1E1E",
        font_color="white"
    )
    st.plotly_chart(fig_pressed, use_container_width=True)




st.subheader("Additional Notes Overview")

# Count the occurrences of each unique note (excluding NaN)
notes_counts = meta["Additional Comments"].dropna().value_counts()

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





        
#############----------------------------------
st.subheader("DOL Category per Subject")

# Prepare data: group by Subject ID and DOL Category, count occurrences
dol_cat_counts = meta.groupby(["Subject ID", "DOL Category"]).size().reset_index(name="Count")

# Pivot for plotting
dol_cat_pivot = dol_cat_counts.pivot(index="Subject ID", columns="DOL Category", values="Count").fillna(0)

# Melt the pivoted DataFrame for Plotly
dol_cat_long = dol_cat_pivot.reset_index().melt(id_vars="Subject ID", var_name="DOL Category", value_name="Count")

# Plot as stacked bar chart using Plotly
fig_dol_cat = px.bar(
    dol_cat_long,
    x="Subject ID",
    y="Count",
    color="DOL Category",
    labels={"Count": "Count", "Subject ID": "Subject ID"},
    title="DOL Category Distribution per Subject"
)

fig_dol_cat.update_layout(
    barmode="stack",
    xaxis_title="Subject ID",
    yaxis_title="Count",
    plot_bgcolor="#1E1E1E",
    paper_bgcolor="#1E1E1E",
    font_color="white"
)

st.plotly_chart(fig_dol_cat, use_container_width=True)


        
#############-----------------
st.subheader("Growth Metric Overview")

#############-----------------


# Filter subjects with >2 timepoints
subject_counts = meta["Subject ID"].value_counts()
longitudinal_subjects = subject_counts[subject_counts >= 3].index.tolist()

st.markdown("📍 Showing only subjects with > 3 timepoints")
selected_subject = st.selectbox("Select a subject:", longitudinal_subjects)

# Filter and sort by DOL
subject_df = meta[meta["Subject ID"] == selected_subject].copy()
subject_df["DOL"] = pd.to_numeric(subject_df["DOL"], errors="coerce")  # ensure numeric
subject_df = subject_df.sort_values("DOL")  # 👈 ensures line plots follow correct order

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
    fig1, ax = plt.subplots(figsize=(4, 3))
    fig1.patch.set_facecolor('#1E1E1E')
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
    return fig1

# Weight
with col1:
    st.pyplot(make_growth_plot("DOL", "Current Weight", "Weight (g)"))

# Height
with col2:
    st.pyplot(make_growth_plot("DOL", "Current Height", "Height (cm)"))

# Head Circumference
with col3:
    st.pyplot(make_growth_plot("DOL", "Current HC", "Head Circumference (cm)"))
