import streamlit as st

st.title("🧪 HMO Overview")

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
        15 different HMOs were analyzed per sample, including the internal standard <em>iso</em>. This allows for quantitative comparisons of individual HMO concentrations across subjects and timepoints.
        </div>
    """, unsafe_allow_html=True)
