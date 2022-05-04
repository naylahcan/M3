# -*- coding: utf-8 -*-
"""
Created on Mon May  2 00:30:42 2022

@author: sincl
"""

import pandas as pd
import finalClassdictionaryM3code
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import plotly
import chart_studio


mapdata = finalClassdictionaryM3code.mapdata
fields = finalClassdictionaryM3code.fields
mapper = pd.DataFrame(mapdata, columns = fields)
api_token = "pk.eyJ1IjoibmF5bGFoY2FuIiwiYSI6ImNrdzl1czM5ODFqZGkycG8wcGRhaGp6OGgifQ.JYQnAnXt7kdsdKuPFOZLbA"

fig = px.scatter_mapbox(mapper, lat="lat", lon="lon", hover_name="Building #", hover_data=["Building #", "Student Count"],
                        color_discrete_sequence=["red"], zoom=15.5, height=600, width=1000, center = {"lat": 42.360, "lon": -71.088},
                        size = "Student Count")

fig.update_layout(font_size=16,  title={'xanchor': 'center','yanchor': 'top'}, 
        title_font_size = 24, mapbox_accesstoken = api_token, mapbox_style = "mapbox://styles/naylahcan/cl26k904t001e14p7qdo1b0pl")


fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#mapDiv = plotly.offline.plot(fig, output_type = 'div',config={'displayModeBar': False})


#plotly.offline.plot(fig)

username = 'naylahcan' # your username
api_key = 'Asd02n3iDKuv2bmR6et1' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
import chart_studio.plotly as py
maplink = str(py.plot(fig, filename = 'm3map', auto_open=True))
embed = chart_studio.tools.get_embed(maplink)

py.plot(fig, filename = 'm3map', auto_open=True)
