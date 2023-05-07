import json
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc, html, Input, Output

# Import data from json files
house_file = "./Data/house_members.json"
senate_file = "./Data/senate_members.json"

with open(house_file, "r") as f:
    house_members = json.load(f)

with open(senate_file, "r") as f:
    senate_members = json.load(f)

congress_data = house_members + senate_members

# Process data into dictionary for application
state_party_map = {}
for member in congress_data:
    state = member['state']
    party = member['party']
    if state not in state_party_map:
        state_party_map[state] = {'D': 0, 'R': 0, 'ID': 0, 'I': 0, 'L': 0}
    state_party_map[state][party] += 1

# Process dictionary into DataFrame for Pandas manipulation
state_party_df = []
for state, parties in state_party_map.items():
    total = sum(parties.values())
    proportion_d = parties['D'] / total
    proportion_r = parties['R'] / total
    proportion_o = (parties['ID'] + parties['I'] + parties['L']) / total
    color = 2*(proportion_d-.5) if proportion_d > proportion_r else -2*(proportion_r-.5)
    state_party_df.append({
        'state': state,
        'democrats': parties['D'],
        'republicans': parties['R'],
        'other': parties['ID'] + parties['I'] + parties['L'],
        'color': color
    })
state_party_df = pd.DataFrame(state_party_df)

# Create Dash-based application
app = dash.Dash(__name__)

def filter_by_chamber(chamber_value, data):
    filtered_data = []
    if chamber_value == 0:
        filtered_data = [d for d in data if d['short_title'] == 'Sen.']
    elif chamber_value == 2:
        filtered_data = [d for d in data if d['short_title'] == 'Rep.']
    else:
        filtered_data = data
    return filtered_data

def filter_by_party(party_value, data):
    filtered_data = []
    if party_value == 0:  # Democrat
        filtered_data = [d for d in data if d['party'] == 'D']
    elif party_value == 2:  # Republican
        filtered_data = [d for d in data if d['party'] == 'R']
    elif party_value == 3:  # Independent
        filtered_data = [d for d in data if d['party'] == 'I']
    else:  # All
        filtered_data = data
    return filtered_data

app.layout = html.Div([
    html.H1('US Congress: Political Party by State'),
    dcc.Graph(id='state-map'),
    
    # Slider to select chamber
    dcc.Slider(
        id='chamber-slider',
        min=0,
        max=2,
        step=1,
        marks={
            0: 'Senate',
            1: 'All',
            2: 'House'
        },
        value=1
    ),

    # Slider to select party
    dcc.Slider(
        id='party-slider',
        min=0,
        max=3,
        step=1,
        marks={
            0: 'Democrat',
            1: 'All',
            2: 'Republican',
            3: 'Independent'
        },
        value=1
    ),
], style={'textAlign': 'center'})

@app.callback(
    Output('state-map', 'figure'),
    Input('chamber-slider', 'value'),
    Input('party-slider', 'value')
)

# Update map based on filters
def update_state_map(chamber, party):
    filtered_chamber = filter_by_chamber(chamber, congress_data)

    filtered_data = filter_by_party(party, filtered_chamber)

    filtered_map = {}
    for member in filtered_data:
        state = member['state']
        party = member['party']
        if state not in filtered_map:
            filtered_map[state] = {'D': 0, 'R': 0, 'ID': 0, 'I': 0, 'L': 0}
        filtered_map[state][party] += 1
    
    filtered_df = []
    for state, parties in filtered_map.items():
        total = sum(parties.values())
        proportion_d = parties['D'] / total
        proportion_r = parties['R'] / total
        proportion_o = (parties['ID'] + parties['I'] + parties['L']) / total
        color = 2*(proportion_d-.5) if proportion_d > proportion_r else -2*(proportion_r-.5)
        filtered_df.append({
            'state': state,
            'democrats': parties['D'],
            'republicans': parties['R'],
            'other': parties['ID'] + parties['I'] + parties['L'],
            'color': color
        })

    filtered_df = pd.DataFrame(filtered_df)

    # Build choropleth for US state map
    fig = px.choropleth(
        data_frame=filtered_df,
        locationmode='USA-states',
        locations='state',
        scope='usa',
        color='color',
        hover_name='state',
        hover_data={
            'democrats': ':,',
            'republicans': ':,',
            'other': ':,'
        },
        color_continuous_scale='RdBu',
        labels={
            'state': 'State',
            'color': 'Party',
            'democrats': 'D',
            'republicans': 'R',
            'other': 'Other'
        }
    )

    # Build layout for figure
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

    return fig

app.run_server(debug=True, use_reloader=False)