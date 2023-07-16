import streamlit as st
import pandas as pd
from utils.load import *
from utils.drawGraph import DrawGraph

stat_type = ('_avgspeed', '_avgspeed')
selected_race = -1
race_list = []

id_race = st.sidebar.text_input("Indiquez l'id de la régate", value="428")

if id_race != "":
    race_list = get_race_list(id_race)

if len(race_list) > 0:
    selected_race = st.sidebar.selectbox('Sélectionnez une course',  race_list.index,
                                         format_func=lambda x: race_list.loc[x].text)


def start(selected_race):
    graph_types = pd.DataFrame({
        'type': ['Vitesse/flotte par segment', 'Distance parcourue par segment'],
    })

    select_graph_type = st.sidebar.radio('Quel graph ?', graph_types.index,
                                         format_func=lambda x: graph_types.loc[x].type)
    match select_graph_type:
        case 1:
            stat_type = ('_distancesursegment', '_longueursegment')
        case _:
            stat_type = ('_avgspeed', '_avgspeed')

    stat_selection, stat_compare = stat_type

    options = st.sidebar.multiselect(
        'Coureurs',
        df.index,
        max_selections=8,
        format_func=lambda x: df.loc[str(x)].nom
    )

    selection = df[df.index.isin(options)]
    graph = DrawGraph(stat_selection, stat_compare, df, selection)
    fig = graph.change_graph()
    st.write('[Replay](' + selected_race.url + ')')
    st.title(selected_race.text + ' :: ' + graph_types.type[select_graph_type])

    st.plotly_chart(fig, use_container_width=True)


if selected_race != -1:
    s = race_list.loc[selected_race]
    df = load_xml(s.idrace)

    start(s)
