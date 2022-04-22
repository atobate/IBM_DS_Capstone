# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites=spacex_df[['Launch Site']].groupby(['Launch Site'], as_index=False).count()
site1=launch_sites['Launch Site'][0]
site2=launch_sites['Launch Site'][1]
site3=launch_sites['Launch Site'][2]
site4=launch_sites['Launch Site'][3]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'All Sites', 'value':'ALL'},
                                {'label':site1, 'value':site1}, {'label':site2, 'value':site2},
                                {'label':site3, 'value':site3}, {'label':site4, 'value':site4}],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'},value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure'), Input('site-dropdown','value'))
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        filtered_df = spacex_df[['Launch Site', 'class']].groupby(['Launch Site'], as_index=False).sum()
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['class'], as_index=False).count()
        filtered_df.rename(columns={'Unnamed: 0':'count'}, inplace=True)
        fig = px.pie(filtered_df, values='count', 
        names='class', 
        title='Total Success Launches for Site '+entered_site)
        return fig
        
              

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart','figure'), 
              Input('site-dropdown','value'),
             Input('payload-slider','value'))
def get_scatter_chart(entered_site, payload_range):
    
    filt_plrange1 = spacex_df['Payload Mass (kg)']>=payload_range[0]
    filt_plrange2 = spacex_df['Payload Mass (kg)']<=payload_range[1]
    filt_plrange = filt_plrange1 & filt_plrange2
    
    filt_site = spacex_df['Launch Site']==entered_site
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[filt_plrange]
        fig = px.scatter(filtered_df, y='class', x='Payload Mass (kg)',
        color='Booster Version Category', 
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:  
        filtered_df = spacex_df[filt_site & filt_plrange]
        fig = px.scatter(filtered_df, y='class', x='Payload Mass (kg)',
        color='Booster Version Category', 
        title='Correlation between Payload and Success for Site '+entered_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
