import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO
import requests
from bs4 import BeautifulSoup
from w3lib.url import url_query_parameter
import streamlit as st


@st.cache_data
def load_xml(id):
    r = requests.get(
        'https://app.metasail.it/(S(usryiluj43x0xh10ztf4whfp))/MetaSailWS.asmx/getStatistiche?idgara=' + str(id))
    src = r.text
    print('load_xml')
    # remove namespace
    tree = ET.iterparse(StringIO(src))
    for _, el in tree:
        prefix, has_namespace, postfix = el.tag.partition('}')
        if has_namespace:
            el.tag = postfix

    root = tree.root

    df_cols = ['id', 'nom', 'long_parcours', 'dist_parcouru', 'temps_total']

    def add_row(colname, value, row):
        row[colname] = value
        if colname not in df_cols:
            df_cols.append(colname)

    rows = []
    for node in root:
        row = {
            'id': node.find('Seriale').text if node is not None else None,
            'nom': node.find('Nome').text if node is not None else None,
            'long_parcours': int(node.find('TotLungLato').text) if node is not None else None,
            'dist_parcouru': int(node.find('TotDistPerc').text) if node is not None else None,
            'temps_total': int(node.find('TotTempPerc').text) if node is not None else None,
        }
        curr_segment = 1
        for segment in node.find('lstSegments').iter('cInfoRaceSegment'):
            add_row('s' + str(curr_segment) + '_topspeed',
                    float(segment.find('TopSpeed').text), row)
            add_row('s' + str(curr_segment) + '_topvmg',
                    float(segment.find('TopVMG').text), row)
            add_row('s' + str(curr_segment) + '_avgspeed',
                    float(segment.find('AvgSpeed').text), row)
            add_row('s' + str(curr_segment) + '_tempsgauche',
                    int(segment.find('CrtRaceSegSX').text), row)
            add_row('s' + str(curr_segment) + '_tempsdroite',
                    int(segment.find('CrtRaceSegDX').text), row)
            add_row('s' + str(curr_segment) + '_tempssursegment',
                    int(segment.find('TimeSecPercorsi').text), row)
            add_row('s' + str(curr_segment) + '_distancesursegment',
                    int(segment.find('SegDistRealePercorsa').text), row)
            add_row('s' + str(curr_segment) + '_longueursegment',
                    int(segment.find('LungLato').text), row)
            add_row('s' + str(curr_segment) + '_rankentersegment',
                    int(segment.find('SegEnteredRank').text), row)
            curr_segment += 1
        rows.append(row)

    df = pd.DataFrame(rows, columns=df_cols)
    df.set_index('id', inplace=True)

    return df


@st.cache_data
def get_race_list(id):
    r = requests.get(
        'https://www.metasail.it/wp-content/themes/metasail/ajax/event.php?id=' + str(id))

    c = r.text.removeprefix("b'").removesuffix("'")

    soup = BeautifulSoup(c, 'html.parser')
    data = []

    for a in soup.find_all('a', href=True):
        if 'metasail.it' in a['href']:
            idrace = url_query_parameter(a['href'], 'idgara')
            data.append({'text': a.text, 'idrace': idrace,
                        'url': a['href'],  'id': idrace})

    result = pd.DataFrame(data)
    result.set_index('id', inplace=True)

    return result
