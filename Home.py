import streamlit as st
import pandas as pd

st.title("Raw Data")

# Load the data
df = pd.read_excel("Unlinked_Merged.xlsx")

st.subheader("📄 Raw Data Preview")
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
