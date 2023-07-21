import streamlit as st
import plotly.graph_objects as go
import numpy as np
from components.plotly_colorbar import *
import math

def render_tab1(tab, df, selected_coureurs):
	selection = df[df.id.isin(selected_coureurs)]
	max = selection.s_leg.max()
	nb_col = st.number_input('Nombre de colonne (' + str(max) + ' max)', min_value=1, max_value=max, value=2)
	graph = DrawGraph(df, selection)
	try:
		figs = graph.change_graph(fig_cols=nb_col)
		cols = st.columns(nb_col)

		index = 1
		with tab:
			for rowidx in range(len(figs)):
				graph_index = 0
				for col in cols:
					try:
						col.plotly_chart(figs[rowidx][graph_index], use_container_width=True)
						graph_index += 1
						index += 1
					except IndexError:
						break
	except KeyError:
		st.error('Pas de donnée valable')



class DrawGraph:
	def __init__(self, df, selection):
		self.df = df
		self.selection = selection

	def add_graph(self, index):
		try:
			general = self.df[self.df.s_leg == int(index)]
			#if general.empty:
			#	return None
			
			mean_speed = np.nanmean(general['s_avgspeed'])
			long_segment = np.nanmean(general['s_longueursegment'])
			selection = self.selection[self.selection.s_leg == int(index)]
			min_dist = long_segment if np.min(general['s_distancesursegment']) > long_segment else np.min(general['s_distancesursegment'])

			def dist_exceedtext(s_distancesursegment):
				d = np.round(((s_distancesursegment * 100) / min_dist) - 100, 2)
				for id, it in d.items():
					if it > 0:
						d.loc[id] = '+' + str(it) + '%' 
					else:
						d.loc[id] = ''
				return d
			
			def speed_exceedtext(s_avgspeed, format='percent'):
				d = np.round(((s_avgspeed * 100) / mean_speed) - 100, 2)
				for id, it in d.items():
					if it > 0:
						d.loc[id] = '+' + str(it) + '%' if format=='percent' else it
					else:
						d.loc[id] = str(it) + '%' if format=='percent' else it
				return d

			selection = selection.assign(
				nom_rank = lambda row: '#' + row.s_rankentersegment.astype(str) + ' ' + row.nom,
				dist_exceed = lambda row: dist_exceedtext(row.s_distancesursegment),
				speed_exceed = lambda row: speed_exceedtext(row.s_avgspeed),
				speed_exceed_float = lambda row: speed_exceedtext(row.s_avgspeed, 'float'),
			)

			range_x_dist= [min_dist - 20, np.max(selection['s_distancesursegment'])]
			range_x_speed = [np.floor(np.min(general['s_avgspeed'])), np.max(general['s_avgspeed'])]

			data = [
					go.Bar(
							name="vitesse",
							x=selection.s_avgspeed,
							y=selection.nom_rank,
							text=selection.speed_exceed,
							orientation='h',
							xaxis='x',
							offsetgroup=1,
							marker=dict(
								color = list(map(set_graph_color, selection.speed_exceed_float)),
							),
							showlegend=False
					),
					go.Bar(
							name="distance",
							x=selection.s_distancesursegment,
							y=selection.nom_rank, 
							text=selection.dist_exceed,
							orientation='h',
							xaxis='x2',
							offsetgroup=2
					),
			]

			layout = go.Layout(
				xaxis = go.layout.XAxis(title = { 'text': 'Vitesse (knt)', 'standoff': 40 }, range = range_x_speed, showline=True, ticklen=5, tickcolor='black'),
				xaxis2 = go.layout.XAxis(title = 'Distance (m)', side = 'top', overlaying = 'x', range = range_x_dist, showline=True, ticklen=5, tickcolor='black'),
				title='Leg ' + str(index),
				height=(len(selection) + 1) * (100 if len(selection) > 4 else 150),
				
				showlegend=True,
				legend=dict(
					orientation="h",
					yanchor="bottom",
					xanchor="left",
					y=0,
					x=0,
				),
			)

			colorbar = create_colorbar()
			fig = go.Figure(data + colorbar, layout)
			
			fig.add_shape(
				type="line",
				xref="x",
				x0=mean_speed, y0=-1.3, x1=mean_speed, y1=len(selection) - 0.55,
				line=dict(
					color="red",
					width=2,
				),
			)
			fig.add_shape(
				type="line",
				xref="x2",
				x0=long_segment, y0=-0.45, x1=long_segment, y1=len(selection) - 0.5,
				line=dict(
					color="DarkOrange",
					width=2,
				),
			)
			fig.add_annotation(
				x=mean_speed,
				y= -0.63,
				text="vmoy " + str(np.round(mean_speed, 2)) + 'knt',
				showarrow=False,
				bgcolor="red",
				borderpad=4,
				font=dict(color="white")
			)

			fig.add_annotation(
				x=long_segment,
				y=len(selection) - 0.4,
				text="segment " + str(np.round(long_segment, 2)) + 'm',
				showarrow=False,
				bgcolor="DarkOrange",
				font=dict(color="white"),
				borderpad=4,
				xref='x2'
			)

			return fig

		except KeyError:
				return

	def change_graph(self, fig_cols=2):
		result = []
		index = 1
		fig_rows = math.ceil(self.selection.s_leg.max() / fig_cols)
		for row in range(fig_rows):
			new_row = []
			for col in range(fig_cols):
				graph = self.add_graph(str(index))
				if graph is not None:
					new_row.append(graph)
					index += 1
			result.append(new_row)

		return result