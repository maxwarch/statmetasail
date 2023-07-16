import streamlit as st
import pandas as pd
from utils.load import *
from utils.drawGraph import DrawGraph

stat_type = ('_avgspeed', '_avgspeed')
selected_race = -1
race_list = []
coureurs = st.session_state['coureurs'] if 'coureurs' in st.session_state else []
st.session_state['coureurs'] = coureurs
st.markdown('<style>h1 a, h1 a:hover{text-decoration: none; margin-left: 20px}</style>', unsafe_allow_html=True)

#"session", st.session_state

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

    indexdf = df.set_index('id')

    c = indexdf[indexdf.index.isin(coureurs)].index.values
    if len(c) == 0:
        st.session_state.coureurs = []
    else:
        st.session_state.coureurs = c.tolist()

    options = st.sidebar.multiselect(
        'Coureurs',
        indexdf.index,
        max_selections=8,
        format_func=lambda x: indexdf.loc[str(x)].nom,
        default=c if len(c) > 0 else None,
        key='coureurs'
    )

    selection = indexdf[indexdf.index.isin(options)]
    graph = DrawGraph(stat_selection, stat_compare, df, selection)
    try:
        fig = graph.change_graph(title=graph_types.type[select_graph_type])
        st.title(selected_race.text.rstrip() + ' [:movie_camera:](' + selected_race.url + ')')

        st.plotly_chart(fig, use_container_width=True)
    except KeyError:
        st.write('Pas de donnée valable')

if selected_race != -1:
    s = race_list.loc[selected_race]
    df = load_xml(s.idrace)

    start(s)
