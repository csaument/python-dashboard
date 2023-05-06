import requests
import plotly.express as px
import dash
from dash import dcc, html
from config import PROPUBLICA_API_KEY

def get_congress_data():
    headers = {'X-API-Key': PROPUBLICA_API_KEY}
    url = 'https://api.propublica.org/congress/v1/members/current.json'
    response = requests.get(url, headers=headers)
    data = response.json()['results'][0]['members']
    return data

congress_data = get_congress_data()

state_party_map = {}
for member in congress_data:
    state = member['state']
    party = member['party']
    if state not in state_party_map:
        state_party_map[state] = {}
    if party not in state_party_map[state]:
        state_party_map[state][party] = 0
    state_party_map[state][party] += 1

state_party_df = []
for state, parties in state_party_map.items():
    state_party_df.append({
        'state': state,
        'democrats': parties.get('D', 0),
        'republicans': parties.get('R', 0),
        'other': parties.get('ID', 0) + parties.get('I', 0) + parties.get('L', 0)
    })
state_party_df = pd.DataFrame(state_party_df)

fig = px.choropleth(
    state_party_df, 
    locationmode="USA-states",
    locations="state",
    scope="usa",
    color_discrete_sequence=['green', 'blue', 'red'],
    color='democrats',
    hover_data={
        'state': True,
        'democrats': ':,d',
        'republicans': ':,d',
        'other': ':,d',
    },
    labels={
        'democrats': 'Democrats',
        'republicans': 'Republicans',
        'other': 'Third Party',
    },
    title='US Congressional Action'
)

fig.update_layout(
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'),
    coloraxis_colorbar=dict(
        title="Representatives",
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=300,
        yanchor="middle", y=0.5,
        ticks="inside", ticksuffix=" rep",
        ),
)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("US Congressional Action", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)
