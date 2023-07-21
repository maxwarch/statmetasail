import plotly.graph_objects as go
import pandas as pd

colors = pd.DataFrame({
  'min':   [-1000,      -10,        0,    5.01,     10.01],
  'max':   [-10.01,   -0.01,        5,      10,     1000],
  'color': ['red', 'orange', 'yellow',  'blue',   'green'],
  'legend': ['v < -10%', '-10% >= v > 0%', '0% < v < 5%', '5% < v <= 10%', 'v > 10%']
})

def set_graph_color(val):
  mask = colors[(val >= colors['min']) & (val <= colors['max'])]
  return mask.iloc[0].color if mask is not None else 'grey'

def create_colorbar():
  result = []
  for idx in colors.index:
    result.append(
      go.Scatter(
                  x=[None],
                  y=[None],
                  mode="markers",
                  name=colors.legend[idx],
                  marker=dict(size=10, color=colors.color[idx], symbol='square'),
              )
    )
  return result