import json
import plotly.colors
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc, html

house_file = "./Data/house_members.json"
senate_file = "./Data/senate_members.json"

with open(house_file, "r") as f:
    house_members = json.load(f)

with open(senate_file, "r") as f:
    senate_members = json.load(f)

congress_data = house_members + senate_members

state_party_map = {}
for member in congress_data:
    state = member['state']
    party = member['party']
    if state not in state_party_map:
        state_party_map[state] = {'D': 0, 'R': 0, 'ID': 0, 'I': 0, 'L': 0}
    state_party_map[state][party] += 1

state_party_df = []
for state, parties in state_party_map.items():
    total = sum(parties.values())
    proportion_d = parties['D'] / total
    proportion_r = parties['R'] / total
    proportion_o = (parties['ID'] + parties['I'] + parties['L']) / total
    r, g, b = proportion_r * 255, proportion_o * 255, proportion_d * 255
    state_party_df.append({
        'state': state,
        'democrats': parties['D'],
        'republicans': parties['R'],
        'other': parties['ID'] + parties['I'] + parties['L'],
        'color': (int(r), int(g), int(b))
    })
state_party_df = pd.DataFrame(state_party_df)

app = dash.Dash(__name__)

custom_scale = [    (0.0, 'rgb(255,0,0)'),    (0.5, 'rgb(128,0,128)'),    (1.0, 'rgb(0,0,255)')]

fig = px.choropleth(
    data_frame=state_party_df,
    locationmode='USA-states',
    locations='state',
    scope='usa',
    color='democrats',
    hover_name='state',
    hover_data={
        'democrats': ':,',
        'republicans': ':,',
        'other': ':,'
    },
    color_continuous_scale='RdBu',
    labels={
        'color': 'Party',
        'democrats': 'Total Democrats',
        'republicans': 'Total Republicans',
        'other': 'Total Other'
    }
)

fig.update_layout(
    title={
        'text': 'Political Party by State',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 28
        }
    },
    margin=dict(l=0, r=0, t=70, b=0),
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgb(255, 255, 255)')
)

app.layout = html.Div([
    html.H1('US Congress: Political Party by State'),
    dcc.Graph(figure=fig),
], style={'textAlign': 'center'})

app.run_server(debug=True, use_reloader=False)