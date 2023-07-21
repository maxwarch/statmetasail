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
	# remove namespace
	tree = ET.iterparse(StringIO(src))
	
	for _, el in tree:
			prefix, has_namespace, postfix = el.tag.partition('}')
			if has_namespace:
					el.tag = postfix

	root = tree.root
	rows = []
	for node in root:
		curr_segment = 1
		for segment in node.find('lstSegments').iter('cInfoRaceSegment'):
			row = {
				'id': node.find('Seriale').text if node is not None else None,
				'nom': node.find('Nome').text if node is not None else None,
				'long_parcours': int(node.find('TotLungLato').text) if node is not None else None,
				'dist_parcouru': int(node.find('TotDistPerc').text) if node is not None else None,
				'temps_total': int(node.find('TotTempPerc').text) if node is not None else None,
			}
			row['s_topspeed'] = float(segment.find('TopSpeed').text)
			row['s_topvmg'] = float(segment.find('TopVMG').text)
			row['s_avgspeed'] = float(segment.find('AvgSpeed').text)
			row['s_tempsgauche'] = int(segment.find('CrtRaceSegSX').text)
			row['s_tempsdroite'] = int(segment.find('CrtRaceSegDX').text)
			row['s_tempssursegment'] = int(segment.find('TimeSecPercorsi').text)
			row['s_distancesursegment'] = int(segment.find('SegDistRealePercorsa').text)
			row['s_longueursegment'] = int(segment.find('LungLato').text)
			row['s_rankentersegment'] = int(segment.find('SegEnteredRank').text)
			row['s_leg'] = curr_segment
			rows.append(row)
			curr_segment += 1

	return pd.DataFrame(rows, columns=[k for k in rows[0]]) if len(rows) > 0 else None


@st.cache_data
def get_race_list(id):
    r = requests.get(
        'https://www.metasail.it/wp-content/themes/metasail/ajax/event.php?id=' + str(id))

    c = r.text.removeprefix("b'").removesuffix("'")

    soup = BeautifulSoup(c, 'html.parser')
    data = [{'text': '', 'idrace': -1, 'url': '',  'id': -1}]

    for a in soup.find_all('a', href=True):
        if 'metasail.it' in a['href']:
            idrace = url_query_parameter(a['href'], 'idgara')
            data.append({'text': a.text, 'idrace': idrace,
                        'url': a['href'],  'id': idrace})

    result = pd.DataFrame(data)
    result.set_index('id', inplace=True)

    return result
