import streamlit as st
from utils.load import *
from components.sidebar import *
from views.tab1 import *
from views.tab2 import *

st.set_page_config(page_title='Analyse de régate', layout='wide')

css = open('./style.css', 'r').read()
st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)

race_list, selected_race = render_sb()
if selected_race != -1:
    s = race_list.loc[selected_race]
    df = load_xml(s.idrace)
    
    if df is not None:
        selected_coureurs = render_sb_multiselect_coureurs(df)
        st.title(s.text.rstrip() + ' [:movie_camera:](' + s.url + ')')

        if len(selected_coureurs) > 0:
            tab1, tab2 = st.tabs(["Par segment", "Global"])
            render_tab1(tab1, df, selected_coureurs)
            render_tab2(tab2, df, selected_coureurs)
        else:
            st.write(':arrow_left: Choisissez des coureurs')
    else:
        st.error('Les données de cette manche ne sont pas exploitables')
else:
    st.markdown('')
    st.markdown('## :arrow_left: Choisissez une course')