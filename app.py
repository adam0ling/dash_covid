import dash
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import pandas as pd
import numpy as np

from covid import getCovid, getTimeline

# external stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# launch app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

class DashCallbackVariables:
    """Class to store information useful to callbacks"""

    def __init__(self):
        self.n_clicks = {1: 0}

    def update_n_clicks(self, nclicks, bt_num):
        self.n_clicks[bt_num] = nclicks


callbacks_vars = DashCallbackVariables()

colors = {
    'background': '#383c4a',
    'text': '#FFFFFF',
    'styledBackground': '#30333d'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'border': colors['text'],
    'backgroundColor': colors['text'],
    'color':colors['background'],
    'padding': '6px'
}

tab_selected_style = {
    'border': colors['background'],
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': colors['background'],
    'color': colors['text'],
    'padding': '6px',
    'fontWeight' : 'bold'
}

widthCell = '125px'

style_cell_plan={
    'font-size': 14,
    'color': colors['text'],
    'backgroundColor': colors['background'],
    'minWidth': widthCell, 
    'width': widthCell, 
    'maxWidth': widthCell,
    'overflow': 'hidden'
}

style_cell={
    'font-size': 14,
    'color': colors['text'],
    'backgroundColor': colors['background'],
    'whiteSpace':'normal'
}

app.layout = html.Div([
    html.Div([], style={'padding':10}),
    html.H1(
        children='This is a simple example dash app',
        style={
            'textAlign': 'center',
            'color': colors['text']
            }
            ),
    html.Div(
        children=['It shows dash capabilities with some plots and tables. Data used is coronavirus data.', 
        ' Data source: https://github.com/Kamaropoulos/COVID19Py'], 
        style={
        'textAlign': 'center',
        'color': colors['text']
        }),
    html.Div([], style={'padding':10}),
    html.Div(
        children=['Timeline by country code. Check country codes at:',
                html.A('Country code',href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')], 
        style={
        'textAlign': 'center',
        'color': colors['text']
        }),
    html.Div([], style={'padding':10}),
    html.Div([
                dcc.Input(
                    id='country-code',
                    type='text',
                    placeholder='Input country code',
                    style=style_cell,
                    value='US'
                ),
            ],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
    html.Div([], style={'padding':10}),
    html.Div([], id='output-timeline', style={'padding':40}),
    html.Div([], style={'padding':10}),
    html.Div([], id='output', style={'padding':40}),
    html.Div([], style={'padding':10}),
    html.Div([
        dcc.RadioItems(
            id= 'chart-select',
            options=[
                {'label': 'BarChart', 'value': 'bar'},
                {'label': 'Scatter', 'value': 'sca'},
                {'label': 'Table', 'value': 'table'}
            ],
            value='bar',
            style = style_cell
        )  
    ], style={
            'textAlign': 'center',
            'color': colors['text'],
            }
            ),
    html.Div([], style={'padding':10}),
    html.Div(html.Button(id='show-10', children='Show top 10', style = style_cell),
            style={
            'textAlign': 'center',
            'color': colors['text'],
            }),
    html.Div([], style={'padding':800}),
], style={'backgroundColor': colors['background']})

@app.callback(Output('output', 'children'),
            [Input('chart-select', 'value'),
            Input('show-10', 'n_clicks')])
def updatePlot(value, nclicks):
    df = getCovid()
    if nclicks:
        df = df.iloc[:9,]
    if value == 'bar':
        barFig = go.Figure(
            data=
            [
                go.Bar(name='confirmed', x=df.country, y=df.confirmed),
                go.Bar(name='deaths', x=df.country, y=df.deaths),
            ],                
                layout=go.Layout(barmode='group', plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font={
                    'color': colors['text']
                }, margin=dict(t=10),
                legend={'x':1,
                        'y':0.5},
                hovermode='x'))
        barChart = dcc.Graph(id='bar-plot', figure=barFig)
        return barChart
    elif value == 'sca':
        scaFig = go.Figure(
            data=
            [
                go.Scatter(name='confirmed', x=df.country, y=df.confirmed),
                go.Scatter(name='deaths', x=df.country, y=df.deaths),
            ],                
                layout=go.Layout(barmode='group', plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font={
                    'color': colors['text']
                }, margin=dict(t=10),
                legend={'x':1,
                        'y':0.5},
                hovermode='x'))
        scaChart = dcc.Graph(id='sca-plot', figure=scaFig)
        return scaChart
    elif value == 'table':
        table = dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        style_cell=style_cell,
                        style_as_list_view=True,
                        style_header={
                            'fontWeight': 'bold'
                        }
                        )
        return table

@app.callback(Output('output-timeline', 'children'),
            [Input('country-code', 'value')])
def updateTimeline(countryCode):
    df = getTimeline(countryCode)
    scaFig = go.Figure(
            data=
            [
                go.Scatter(name='confirmed', x=df.date, y=df.confirmed),
                go.Scatter(name='deaths', x=df.date, y=df.deaths),
            ],                
                layout=go.Layout(barmode='group', plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font={
                    'color': colors['text']
                }, margin=dict(t=10),
                legend={'x':1,
                        'y':0.5},
                hovermode='x'))
    scaChart = dcc.Graph(id='sca-timeline', figure=scaFig)
    return html.Div(children=['Showing: {}'.format(countryCode), scaChart], style={
            'textAlign': 'center',
            'color': colors['text']
            })

if __name__ == '__main__':
    app.run_server()