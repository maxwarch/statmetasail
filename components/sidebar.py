import streamlit as st
from utils.load import *

selected_race = -1
race_list = []

def render_sb():
  id_race = st.sidebar.text_input("Indiquez l'id de la régate", value="428")

  if id_race != "":
      race_list = get_race_list(id_race)

  if len(race_list) > 0:
      selected_race = st.sidebar.selectbox('Sélectionnez une course',  race_list.index,
                                          format_func=lambda x: race_list.loc[x].text)

  return (race_list, selected_race)

def render_sb_multiselect_coureurs(df):
  coureurs = st.session_state['coureurs'] if 'coureurs' in st.session_state else []
  st.session_state['coureurs'] = coureurs

  dfunique = df.id.unique()
  c = df[df.id.isin(coureurs)].id.unique()

  if len(c) == 0:
      st.session_state.coureurs = []
  else:
      st.session_state.coureurs = c.tolist()

  selected_coureurs = st.sidebar.multiselect(
      'Sélectionner des coureurs (8 max)',
      dfunique,
      max_selections=8,
      format_func=lambda x: df[df.id == str(x)].nom.unique()[0],
      default=c if len(c) > 0 else None,
      key='coureurs'
  )

  return (selected_coureurs)