import streamlit as st
import pandas as pd

import numpy as np

def render_tab2(tab, df):
	graph = DrawGraph(df)
	try:
		with tab:
			tab.pyplot(graph.add_graph())
	except KeyError:
		st.error('Pas de donnée valable')



class DrawGraph:
	def __init__(self, df):
		self.df = df

	def add_graph(self, index):
		general = self.df[self.df.s_leg == self.df.s_leg.max()]
		if general.empty:
			return None
		
        print(general)