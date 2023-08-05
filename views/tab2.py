import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import math

def render_tab2(tab, df):
	max = df.s_leg.max()
	nb_col = 1	#tab.number_input('Nombre de colonne (' + str(max) + ' max)', min_value=1, max_value=max, value=1)
	graph = DrawGraph(df)
	try:
		figs = graph.add_graph(nb_col)

		index = 1
		with tab:
			cols = st.columns(nb_col)
			for rowidx in range(math.floor(max / nb_col)):
				for col in cols:
					if index <= max:
						col.pyplot(graph.add_graph(index), use_container_width=True)
						index += 1
	except KeyError:
		st.error('Pas de donnée valable')


class DrawGraph:
	def __init__(self, df):
		self.df = df

	def add_graph(self, index):
		df_leg = self.df[self.df.s_leg == index].sort_values('s_rankentersegment')
		if df_leg.empty:
			return None
		
		nb = 1
		data = []
		for group in range(nb, len(df_leg), 5):
			gp = group + 1 if group > 1 else group
			sel = df_leg.iloc[gp:group + 5]
			data.append({
				'rank': str(gp) + ' - ' + str(group + 5),
				'vmoy': sel.s_avgspeed.mean(),
				'dmoy': sel.s_distancesursegment.mean(),
				'tdroite': sel.s_tempsdroite.mean(),
				'tgauche': sel.s_tempsgauche.mean(),
				'leg': sel.s_leg.mean()
			})
			
		df = pd.DataFrame(data)
		fig, ax = plt.subplots(figsize=(12, 3))

		width = 0.25
		pos = np.arange(0, df.shape[0])

		ax.set_xticks(pos)
		ax.set_xticklabels(df['rank'].values, rotation=45)
		ax.set_xlabel('Position')
		ax.set_ylabel('Vitesse')
		ax.set_facecolor('none')

		ax1 = ax.twinx()
		ax1.set_ylabel('Distance')

		ax2 = ax.twinx()
		ax2.set_ylabel('% côté')
		ax2.spines.right.set_position(("axes", 1.1))
		#ax2.grid(axis='y')

		# vitesse
		ax.plot(pos, df.vmoy, label="Vitesse", color="#0b709c", linewidth=3)
		ax1.plot(pos, df.dmoy, label="Distance", color="#f27d0f", linewidth=3)
		ax2.bar(pos - (width / 2), df.tgauche, label="% gauche", color="#c93532", width=width)
		ax2.bar(pos + (width / 2), df.tdroite, label="% droite", color="#1e8f5a", width=width)

		lines, labels = ax.get_legend_handles_labels()
		lines1, labels1 = ax1.get_legend_handles_labels()
		lines2, labels2 = ax2.get_legend_handles_labels()

		tkw = dict(size=2, width=1)
		ax.tick_params(axis='y', colors=lines[0].get_color(), **tkw)
		ax.yaxis.label.set_color(lines[0].get_color())
		ax1.tick_params(axis='y', colors=lines1[0].get_color(), **tkw)
		ax1.yaxis.label.set_color(lines1[0].get_color())
		
		ax.legend(lines + lines1 + lines2, labels + labels1 + labels2, loc=0)

		ax.set_zorder(10)
		ax1.set_zorder(9)
		fig.suptitle('Leg ' + str(index))
		fig.tight_layout()
		return fig