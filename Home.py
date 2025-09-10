import streamlit as st
import pandas as pd


st.title("NeoBANK Dashboard 2025")

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
        <h3 style="margin-top:0;">About This Dashboard:</h3>
        <p>
        This dashboard is a visualzing human milk components from NeoBANK samples.  
        </p>
        <p>
        With only 34 subjects in this dataset, results are preliminary — but the goal is to show the 
        <strong>possibilities</strong>:  
        <ul>
            <li>Defining human milk oligosaccharide (HMO) composition </li>
            <li>Visualizing how HMOs may support individualized nutrition</li>
            <li>Identifying trends in NICU settings</li>
        </ul>
        </p>
        </div>
    """, unsafe_allow_html=True)


st.title("Raw Data")

# Load the data
df = pd.read_excel("Unlinked_Merged.xlsx")

st.subheader("📄 UNLINKED - Raw Data Preview")
st.dataframe(df.head(10))  # Show only the first 10 rows for now

# Convert to CSV for download
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=csv,
    file_name="Unlinked_Merged.csv",
    mime="text/csv"
)

# Column descriptions dictionary (customize as needed)
column_descriptions = {
    "Subject ID": "Unique patient identifier",
    "Patient Consented": "Whether the patient consented to participate in the study",
    "sample_unique_id": "Unique identifier for each sample (subject + timepoint)",
    "CGA": "Corrected Gestational Age at time of collection (weeks)",
    "DOL": "Day of Life when sample was collected",
    "Current Weight": "Infant’s current weight at collection (g)",
    "Current Height": "Infant’s current length at collection (cm)",
    "Current HC": "Head circumference (cm)",
    "Scavenged/Fresh?": "Whether sample was scavenged or freshly collected",
    "MBM/DBM?": "Type of milk: Mom’s Breast Milk or Donor Breast Milk",
    "HMF Y/N?": "Whether Human Milk Fortifier was used",
    "TPN Y/N?": "Whether the infant received Total Parenteral Nutrition",
    "Iron Y/N?": "Whether the infant was on iron supplementation",
    "Additional Comments": "Any additional comments or notes about the sample",
    "2FL": "Concentration of 2'-Fucosyllactose (HMO) in area units",
    "Secretor Status": "Classified as Secretor or Non-Secretor based on 2'FL concentration",
    "Aliquots_num": "Number of aliquots collected from the sample",
    "Scavenged Notes": "Notes related to scavenged samples",
    # Add other HMOs here if needed
}

# Expander to display column descriptions
with st.expander("🧾 Column Descriptions"):
    for col, desc in column_descriptions.items():
        st.markdown(f"**{col}**: {desc}")


####### Ability to download specific data (filter via subject ID if longitudinal) -----
st.subheader("Individual Subject Data Exploration")
st.write("Select a Subject ID to explore their data, click top right 'download' for CSV file(s):")

subject_counts = df["Subject ID"].value_counts()
eligible_subjects = subject_counts[subject_counts > 3].index.tolist()


selected_subject = st.selectbox("Select a Subject ID (with >3 timepoints)", sorted(eligible_subjects))


subject_df = df[df["Subject ID"] == selected_subject].copy()
st.dataframe(subject_df)

