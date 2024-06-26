from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import data_handling
from dash_bootstrap_templates import load_figure_template
from date_helper import timezone_to_offset
from dash import ctx
import plotly.express as px

datasets = data_handling.get_datasets()

app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server = app.server
load_figure_template(["darkly"])
row0 = dbc.Row(
            [
                dbc.Col(
                dcc.Dropdown(
                                    options=[
                                        {'label': dataset , 'value': dataset }for dataset in datasets.index.values.tolist()
                                        
                                    ],
                                    value=datasets.index.values.tolist()[0],
                                    multi=False,
                                    id='dataset-input',
                                    style={'color':'rgb(48,48,48)'}
                                ),
            md=2, align='center'),
            dbc.Col(
                html.H1("None", className='text-center', id='ticker-name')
            ,md=8,style={"border-left": "1px solid rgb(82,82,82)",
                         "border-right": "1px solid rgb(82,82,82)"}),
            dbc.Col(
                html.Table(
                    [
                        html.Tr([
                            html.Th('Currency'),
                            html.Td('', id='currency')
                        ]),
                        html.Tr([
                            html.Th('Timezone'),
                            html.Td('',id='timezone')
                        ]),                       
                    ]
                ,style={'table-layout': 'fixed',
                        'width': '100%',
                        'color':'#E5E5E5'
                        })
                ,md=2)
            ]
        )
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
                        #max_intervals=1000,    #number of times the interval will be fired.
                                            #if -1, then the interval has no limit (the default)
                                            #and if 0 then the interval stops running.
                ),
                dcc.Graph(id="ohlc", config= {'displaylogo': False})
                ])
                
        
    ]
)
row1_v2 = dbc.Row(
    [
        dbc.Col([
            dbc.Row(
                dcc.Graph(id='close', config= {'displaylogo': False})
            ),
            dbc.Row(
                dcc.Graph(id='open', config= {'displaylogo': False})
            )
        ]
        , md=4),
        dbc.Col(
            dcc.Graph(id="price", config= {'displaylogo': False}),
            md=4
        ),
        dbc.Col([
            dbc.Row(
                dcc.Graph(id='high', config= {'displaylogo': False})
            ),
            dbc.Row(
                dcc.Graph(id='low', config= {'displaylogo': False})
            )
        ]
        , md=4)
    ])
row_button = dbc.Row(
    [
        dbc.Col(
                html.Div(
                            [
                                dcc.RadioItems(['1D', '1M','1Y', '5Y'], '1D', inline=True, inputClassName='radio', id='date-input', className='group')
                            ]
                        ,className='text-center')
            ,md=6),
        dbc.Col(
                html.Div(
                            [
                                dcc.RadioItems(['Line', 'OHLC'], 'OHLC', inline=True, inputClassName='radio', id='graph-input', className='group')
                            ]
                        ,className='text-center')
            ,md=6),

    ]
    
)
app.layout = dbc.Container(
    [
        row0,
        html.Hr(),
        row1_v2,
        html.Hr(),
        row_button,
        row2,
    ],
    fluid=True,
)

@app.callback(
    [Output('ticker-name', 'children'),
     Output('ticker-name', 'style'),
     Output('currency', 'children'),
     Output('timezone', 'children'),
     Output('ohlc', 'figure'),
     Output('price', 'figure'),
     Output('open', 'figure'),
     Output('high', 'figure'),
     Output('low', 'figure'),
     Output('close', 'figure')],
    [Input('my_interval', 'n_intervals'),
     Input('dataset-input', 'value'),
     Input('date-input', 'value'),
     Input('graph-input', 'value'),]
)
def update_graph(num, dataset_input, date_input, graph_input):
    """update every 3 seconds"""
    try:
        if dataset_input is None:
            raise PreventUpdate
        finance = data_handling.get_data(dataset_input, date_input)
        df = finance.data
        high = finance.high
        low = finance.low
        open = df.Open.iloc[0]
        last_close = finance.previous_close
        close = df.Close.iloc[-1]
        timezone = timezone_to_offset(finance.timezone) 
        currency = finance.currency

        if close > last_close:
            color = {'color':'#3D9970'}
        else:
            color = {'color':'#FF4136'}

        if graph_input == 'OHLC':
            fig = go.Figure(data=go.Ohlc(x=df['Date'],
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close']))
        else:
            fig = px.line(x=df['Date'], y=df['Close'])
            
        fig.update_layout(uirevision=dataset_input,
                        height=500)
        
        fig_close = go.Figure()
        fig_close.add_trace(go.Indicator(
            mode = "number+delta",
            value = last_close,
            domain = {'row': 0, 'column': 1}))
        fig_close.update_layout(
            height=150,
            template = {'data' : {'indicator': [{
                'title': {'text': "Last Close",'font.size':20},
                'mode' : "number",
                'number' : {'valueformat':'.3f','font.size':25}},
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
            height=150,
            template = {'data' : {'indicator': [{
                'title': {'text': "Open",'font.size':20},
                'mode' : "number+delta",
                'number' : {'valueformat':'.3f','font.size':25},}]
                                }})

        fig_high = go.Figure()
        fig_high.add_trace(go.Indicator(
            mode = "number+delta",
            value = high,
            domain = {'row': 0, 'column': 1}))
        fig_high.update_layout(
            height=150,
            template = {'data' : {'indicator': [{
                'title': {'text': "High",'font.size':20},
                'mode' : "number+delta",
                'number' : {'valueformat':'.3f','font.size':25}}]
                                }})


        fig_low = go.Figure()
        fig_low.add_trace(go.Indicator(
            mode = "number+delta",
            value = low,
            domain = {'row': 0, 'column': 1}))
        fig_low.update_layout(
            height=150,
            template = {'data' : {'indicator': [{
                'title': {'text': "Low",'font.size':20},
                'mode' : "number+delta",
                'number' : {'valueformat':'.3f','font.size':25}}]
                                }})
    except:
        raise PreventUpdate
    
    return(datasets.loc[finance.symbol]['Name'], color, currency, timezone, fig, fig_price, fig_open, fig_high, fig_low, fig_close)
