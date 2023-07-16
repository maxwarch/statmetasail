import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class DrawGraph:
    def __init__(self, stat_selection, stat_compare, df, selection):
        self.stat_compare = stat_compare
        self.stat_selection = stat_selection
        self.df = df
        self.selection = selection

    def add_graph(self, index, fig, df, row, col):
        try:
            mean = np.nanmean(df['s' + index + self.stat_compare])
            text_index = index if index == str(self.df.loc[0].nb_segments) else int(index) + 1

            t = go.Bar(
                x=self.selection.nom,
                y=self.selection['s' + index + self.stat_selection],
                name=str(round(mean, 2)),
                text=self.selection['s' + str(text_index) + '_rankentersegment']
            )

            fig.append_trace(t, row, col)
            fig.add_hline(y=mean, line_color='red', row=row, col=col)
        except KeyError:
            return

    def change_graph(self, title='', fig_rows=3, fig_cols=2):
        titles = []
        for i in range(self.df.loc[0].nb_segments):
            titles.append('Leg ' + str(i + 1))

        fig = make_subplots(rows=fig_rows, cols=fig_cols, start_cell='top-left', subplot_titles=titles)
        index = 1
        for row in range(fig_rows):
            for col in range(fig_cols):
                self.add_graph(str(index), fig, self.df, row + 1, col + 1)
                index += 1

        fig.update_layout(title=title, title_x=0.3, height=900, width=1000)
        fig.update_yaxes(type='log')
        return fig
