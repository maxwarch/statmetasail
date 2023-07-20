import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math

graph_types = pd.DataFrame({
    'type': ['Vitesse/flotte', 'Distance parcourue/longueur du segment'],
})

def render_tab1(tab, df, selected_coureurs):
	selection = df[df.id.isin(selected_coureurs)]
	graph = DrawGraph(df, selection)
	try:
		figs = graph.change_graph()
		cols = st.columns(len(figs[0]))

		index = 1
		with tab:
			for fig in figs:
				graph_index = 0
				for col in cols:
					col.markdown('<b><center>Leg' + str(index) + ' </center></b>', unsafe_allow_html=True)
					col.plotly_chart(fig[graph_index], use_container_width=True)
					graph_index += 1
					index += 1
	except KeyError:
		st.write('Pas de donnée valable')



class DrawGraph:
	def __init__(self, df, selection):
		self.df = df
		self.selection = selection

	def add_graph(self, index):
		try:
			general = self.df[self.df.s_leg == int(index)]
			mean_speed = np.nanmean(general['s_avgspeed'])
			long_segment = np.nanmean(general['s_longueursegment'])
			selection = self.selection[self.selection.s_leg == int(index)]
			min_dist = long_segment if np.min(general['s_distancesursegment']) > long_segment else np.min(general['s_distancesursegment'])

			range_x_dist= [min_dist - 20, np.max(selection['s_distancesursegment'])]
			range_x_speed = [math.floor(np.min(general['s_avgspeed'])), np.max(general['s_avgspeed'])]

			data = [
					go.Bar(
							name="vitesse",
							x=selection['s_avgspeed'],
							y=selection.nom, 
							text=selection['s_rankentersegment'],
							orientation='h',
							xaxis='x',
							offsetgroup=1
					),
					go.Bar(
							name="distance",
							x=selection['s_distancesursegment'],
							y=selection.nom, 
							text=selection['s_rankentersegment'],
							orientation='h',
							xaxis='x2',
							offsetgroup=2
					)
			]

			layout = go.Layout(
				xaxis = go.layout.XAxis(title = 'Vitesse', range = range_x_speed, showline=True, ticklen=5, tickcolor='black'),
				xaxis2 = go.layout.XAxis(title = 'Distance', side = 'top', overlaying = 'x', range = range_x_dist, showline=True, ticklen=5, tickcolor='black'),
			)

			fig = go.Figure(data, layout)
			fig.add_vline(x=mean_speed, line_color='red', 
										annotation_text="vmoy de la flotte " + str(round(mean_speed, 2)) + ' knt', 
										annotation_position="bottom right",
										annotation_bgcolor="white",
										annotation_borderpad=3,
									)
			
			fig.add_vline(x=long_segment, line_color='orange', 
										annotation_text='long segment ' + str(round(long_segment, 2)) + ' m', 
										annotation_position="top right",
										annotation_bgcolor="white",
										annotation_borderpad=3,
										xref='x2'
									)
			return fig

		except KeyError:
				return

	def change_graph(self, fig_rows=3, fig_cols=2):
		result = []
		index = 1
		for row in range(fig_rows):
			new_row = []
			for col in range(fig_cols):
				graph = self.add_graph(str(index))
				new_row.append(graph)
				index += 1
			result.append(new_row)

		return result