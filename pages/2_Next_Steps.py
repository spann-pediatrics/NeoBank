
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
####--------------------------------------------------------------------------------------------------------------
############### Overview section ###############
st.header("Next Steps & Future Directions")


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
         <h3 style="margin-top:0;">Suggested Next Steps</h3>
        To expand upon this preliminary dataset, future studies should consider:
        <ol>
            <li>
                <strong>Outcome Measurements</strong>
            </li>
            <li>
                <strong>HMO Analysis</strong> – Each sample was analyzed for 
                <strong>15 human milk oligosaccharides (HMOs)</strong>. 
        </ol>
        </div>
        </div>
    """, unsafe_allow_html=True)