import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def render_tab2(tab, df, selected_coureurs):
    with tab:
        st.write('En cours...')
