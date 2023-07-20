import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

graph_types = pd.DataFrame({
    'type': ['Distance parcourue/longueur parcours', 'Vitesse/flotte'],
})

def render_tab2(tab, df, selected_coureurs):
  with tab:
    select_graph_type = st.radio(label='null', label_visibility='collapsed', options=graph_types.index,
                                          format_func=lambda x: graph_types.loc[x].type, horizontal=True)
    
  match select_graph_type:
      case 1:
          stat_type = ('s_avgspeed', 's_avgspeed', 'knt')
      case _:
          stat_type = ('dist_parcouru', 'long_parcours', 'mètre')

  selection = df[df.id.isin(selected_coureurs)]
  graph = DrawGraph(stat_type, df, selection)
  try:
      fig = graph.change_graph(title=graph_types.type[select_graph_type])
      with tab:
        st.plotly_chart(fig, use_container_width=True)
  except KeyError:
      st.write('Pas de donnée valable')



class DrawGraph:
  def __init__(self, stat_type, df, selection):
      self.stat_selection, self.stat_compare, self.stat_unite = stat_type
      self.df = df
      self.selection = selection

  def add_graph(self):
      try:
          max_leg = self.selection.s_leg.max()
          c = self.selection[self.selection.s_leg == max_leg]
          fig = px.bar(
             self.selection,
              y=c.nom, 
              x=c[self.stat_selection], 
              #name=str(self.selection.iloc[0][self.stat_compare]) + ' ' + self.stat_unite,
              text=c.s_rankentersegment,
              labels={'x': self.stat_unite, 'y': 'régatier'},
              orientation='h',
              height=600,
              log_x=True
          )
          # fig = go.Figure([
          #   go.Bar(
          #     y=self.selection.nom, 
          #     x=self.selection[self.stat_selection], 
          #     name=str(self.selection.iloc[0][self.stat_compare]) + ' ' + self.stat_unite,
          #     text=c.s_rankentersegment,
          #     showlegend=True,
          #     orientation='h',
          #     height=400,
          #   )
          # ])
          # fig.add_vline(x=self.selection.iloc[0].long_parcours, line_color='red')
          # fig.update_yaxes(type='log', title={'text':self.stat_unite})
          return fig
      except KeyError:
          return

  def change_graph(self, title):
      return self.add_graph()
