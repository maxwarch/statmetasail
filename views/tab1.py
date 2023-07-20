import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re

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

			def dist_exceedtext(s_distancesursegment):
				d = np.round(((s_distancesursegment * 100) / min_dist) - 100, 2)
				for id, it in d.items():
					if it > 0:
						d.loc[id] = '+' + str(it) + '%' 
					else:
						d.loc[id] = ''
				return d
			
			def speed_exceedtext(s_avgspeed):
				d = np.round(((s_avgspeed * 100) / mean_speed) - 100, 2)
				for id, it in d.items():
					if it > 0:
						d.loc[id] = '+' + str(it) + '%' 
					else:
						d.loc[id] = str(it) + '%' 
				return d

			selection = selection.assign(
				nom_rank = lambda row: '#' + row.s_rankentersegment.astype(str) + ' ' + row.nom,
				dist_exceed = lambda row: dist_exceedtext(row.s_distancesursegment),
				speed_exceed = lambda row: speed_exceedtext(row.s_avgspeed),
			)

			range_x_dist= [min_dist - 20, np.max(selection['s_distancesursegment'])]
			range_x_speed = [np.floor(np.min(general['s_avgspeed'])), np.max(general['s_avgspeed'])]

			def SetColor(y):
				y = re.findall(r"[-+]?(?:\d*\.*\d+)", y)
				y = float(y[0])
				if(y >= 10):
					return "green"
				if(y >= 5):
					return "blue"
				elif(y > 0):
					return "yellow"
				elif(y <= -10):
					return "red"
				elif(y <= 0):
					return "orange"

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
								color = list(map(SetColor, selection.speed_exceed)),
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
					y=1.1,
					xanchor="right",
					x=1
				),
			)

			fig = go.Figure(data, layout)
			
			fig.add_shape(type="line",
				xref="x", yref="y",
				x0=mean_speed, y0=-0.6, x1=mean_speed,
				y1=len(selection) - 0.55,
				line=dict(
					color="red",
					width=2,
				),
			)
			fig.add_shape(type="line",
				xref="x2", yref="y",
				x0=long_segment, y0=-0.45, x1=long_segment,
				y1=len(selection) - 0.5,
				line=dict(
					color="DarkOrange",
					width=2,
				),
			)
			fig.add_annotation(
				x=mean_speed,
				y= - 0.6,
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