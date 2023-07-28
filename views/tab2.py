import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import math

def render_tab2(tab, df):
	max = df.s_leg.max()
	nb_col = tab.number_input('Nombre de colonne (' + str(max) + ' max)', min_value=1, max_value=max, value=1)
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
			sel = df_leg.iloc[group:group + 5]
			data.append({
				'rank': str(group) + ' - ' + str(group + 5),
				'vmoy': sel.s_avgspeed.mean(),
				'dmoy': sel.s_distancesursegment.mean(),
				'tdroite': sel.s_tempsdroite.mean(),
				'tgauche': sel.s_tempsgauche.mean(),
				'leg': sel.s_leg.mean()
			})
			
		df = pd.DataFrame(data)
		fig, axs = plt.subplots(1, 2, figsize=(12, 3))

		width = 0.25
		pos = np.arange(0, df.shape[0])

		ax1 = plt.twinx(axs[0])
		axs[0].set_xticks(pos)
		axs[0].set_xticklabels(df['rank'].values, rotation=45)
		axs[0].set_xlabel('Position')
		axs[0].set_ylabel('Vitesse')
		axs[0].set_facecolor('none')
		ax1.grid(axis='y')
		ax1.set_ylabel('% côté')

		ax2 = plt.twinx(axs[1])
		axs[1].set_xticks(pos)
		axs[1].set_xticklabels(df['rank'].values, rotation=45)
		axs[1].set_xlabel('Position')
		axs[1].set_ylabel('Distance')
		axs[1].set_facecolor('none')
		ax2.grid(axis='y')
		ax2.set_ylabel('% côté')

		lns = []
		# vitesse
		lns.append(axs[0].plot(pos, df.vmoy, label="Vitesse", color="#dde02d", linewidth=3, zorder=1))
		lns.append(ax1.bar(pos - (width / 2), df.tgauche, label="% gauche", width=width, zorder=10))
		lns.append(ax1.bar(pos + (width / 2), df.tdroite, label="% droite", width=width, zorder=10))
		lines, labels = axs[0].get_legend_handles_labels()
		lines2, labels2 = ax1.get_legend_handles_labels()
		axs[0].legend(lines + lines2, labels + labels2, loc=0)

		lns = []
		# distance
		lns.append(axs[1].plot(pos, df.dmoy, label="Distance", color="#dde02d", linewidth=3, zorder=1))
		lns.append(ax2.bar(pos - (width / 2), df.tgauche, label="% gauche", width=width, zorder=10))
		lns.append(ax2.bar(pos + (width / 2), df.tdroite, label="% droite", width=width, zorder=10))
		lines, labels = axs[1].get_legend_handles_labels()
		lines2, labels2 = ax2.get_legend_handles_labels()
		axs[1].legend(lines + lines2, labels + labels2, loc=0)

		axs[0].set_zorder(10)
		axs[1].set_zorder(10)
		fig.suptitle('Leg ' + str(index))
		fig.tight_layout()
		return fig