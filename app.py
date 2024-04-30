from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import data_handling
from dash_bootstrap_templates import load_figure_template

datasets = data_handling.get_datasets()

app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server = app.server
load_figure_template(["darkly"])
row1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='close'), md=2
        ),
        dbc.Col(
            dcc.Graph(id="open"),
            md=2
        ),
        dbc.Col(
            dcc.Graph(id="price"),
            md=4
        ),
        dbc.Col(
            dcc.Graph(id='high'), md=2
        ),
        dbc.Col(
            dcc.Graph(id='low'), md=2
        )
    ])
row2 = dbc.Row(
    [        
        html.Div([
                dcc.Interval(
                        id='my_interval',
                        disabled=False,     #if True, the counter will no longer update
                        interval=1*3000,    #increment the counter n_intervals every interval milliseconds
                        n_intervals=0,      #number of times the interval has passed
                        max_intervals=1000,    #number of times the interval will be fired.
                                            #if -1, then the interval has no limit (the default)
                                            #and if 0 then the interval stops running.
                ),
                dcc.Graph(id="ohlc")
                ])
                
        
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                dcc.Dropdown(
                                    options=[
                                        {'label': dataset , 'value': dataset }for dataset in datasets
                                    ],
                                    value=datasets[0],
                                    multi=False,
                                    id='dataset-input'
                                ),
            md=2, align='center'),
            dbc.Col(
                html.H1("None", className='text-center', id='ticker-name')
            ,md=10),
            ]
        ), 
        html.Hr(),
        row1,
        html.Hr(),
        row2,
    ],
    fluid=True,
)

@app.callback(
    [Output('ticker-name', 'children'),
     Output('ticker-name', 'style'),
     Output('ohlc', 'figure'),
     Output('price', 'figure'),
     Output('open', 'figure'),
     Output('high', 'figure'),
     Output('low', 'figure'),
     Output('close', 'figure')],
    [Input('my_interval', 'n_intervals'),
     Input('dataset-input', 'value'),]
)
def update_graph(num, dataset_input):
    """update every 3 seconds"""
    if dataset_input is None:
        raise PreventUpdate
    finance = data_handling.get_data(dataset_input)
    df = finance.data
    high = finance.day_high
    low = finance.day_low
    open = df.Open.iloc[0]
    last_close = finance.previous_close
    close = df.Close.iloc[-1]

    if close > last_close:
        color = {'color':'green'}
    else:
        color = {'color':'red'}

    fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']))
    
    fig.update_layout(uirevision=dataset_input,
                      height=500)
    
    fig_close = go.Figure()
    fig_close.add_trace(go.Indicator(
        mode = "number+delta",
        value = last_close,
        domain = {'row': 0, 'column': 1}))
    fig_close.update_layout(
        height=300,
        template = {'data' : {'indicator': [{
            'title': {'text': "Last Close"},
            'mode' : "number",
            'number' : {'valueformat':'.3f'}},
            ]
                             }})
    

    fig_price = go.Figure()
    fig_price.add_trace(go.Indicator(
        mode = "number+delta",
        value = close,
        domain = {'row': 0, 'column': 1}))
    fig_price.update_layout(
        height=300,
        template = {'data' : {'indicator': [{
            'title': {'text': "Price"},
            'mode' : "number+delta",
            'number' : {'valueformat':'.3f'},
            'delta' : {'reference': last_close, 'valueformat':'.3f','suffix': f" ({(close-last_close)/last_close:.3%})"}}]
                             }})

    fig_open = go.Figure()
    fig_open.add_trace(go.Indicator(
        mode = "number+delta",
        value = open,
        domain = {'row': 0, 'column': 1}))
    fig_open.update_layout(
        height=300,
        template = {'data' : {'indicator': [{
            'title': {'text': "Open"},
            'mode' : "number+delta",
            'number' : {'valueformat':'.3f'},}]
                             }})

    fig_high = go.Figure()
    fig_high.add_trace(go.Indicator(
        mode = "number+delta",
        value = high,
        domain = {'row': 0, 'column': 1}))
    fig_high.update_layout(
        height=300,
        template = {'data' : {'indicator': [{
            'title': {'text': "High"},
            'mode' : "number+delta",
            'number' : {'valueformat':'.3f'}}]
                             }})


    fig_low = go.Figure()
    fig_low.add_trace(go.Indicator(
        mode = "number+delta",
        value = low,
        domain = {'row': 0, 'column': 1}))
    fig_low.update_layout(
        height=300,
        template = {'data' : {'indicator': [{
            'title': {'text': "Low"},
            'mode' : "number+delta",
            'number' : {'valueformat':'.3f'}}]
                             }})
    
    return(finance.symbol, color,fig, fig_price, fig_open, fig_high, fig_low, fig_close)



