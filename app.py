import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import requests
from fbprophet import Prophet

import plotly.graph_objs as go


def trace(df, df1, title):
    # trace for yhat from fbprophet
    yhat = go.Scatter(x = df['ds'], y = df['yhat'],
                      mode = 'lines', line = dict(color='red'), name = 'yhat')
    
#    trend = go.Scatter(x = df['ds'], y= df['trend'], name = 'trend', line = dict(color = 'green'))

    # trace for lower
    yhat_lower = go.Scatter(x = df['ds'], y = df['yhat_lower'],
                            mode = 'lines', line = dict(color = ('rgb(140, 188, 250)')), name = 'yhat_lower')

    # trace for upper
    yhat_upper = go.Scatter(x = df['ds'],y = df['yhat_upper'],
                            mode = 'lines',fill = 'tonexty',
                            line = dict(color = ('rgb(140, 188, 250)')), name = 'yhat_upper')

    # trace for actual data
    actual = go.Scatter(x = df1['ds'], y = df1['y'], name = 'actual',
                        mode = 'markers', marker = dict(color = ('rgb(0,0,0)'), size = 3))

    moving_average = go.Scatter(x = df1[::-1]['ds'], y = df1[::-1]['y'].rolling(window=100, min_periods=5).mean(), name = 'moving_average',
                        mode = 'lines', marker = dict(color = ('rgb(255,140,0)')))
    
    data = [yhat, yhat_lower, yhat_upper, actual, moving_average]

    # style plot and add rangeselector
    layout = dict(
    title=title+' Future',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(count=5,
                     label='5y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date',
    )
    )
    
    return dict(data=data, layout=layout)


def trace_act(df1, title):
    # trace for actual data
    # actual = go.Scatter(x = df1['ds'], y = df1['y'], name = 'actual',
    #                       mode = 'lines', line = dict(color = 'red'))

    # moving_average = go.Scatter(x = df1[::-1]['ds'], y = df1[::-1]['y'].rolling(window=100, min_periods=5).mean(), name = 'moving_average',
    #                       mode = 'lines', marker = dict(color = ('rgb(255,140,0)')))
    
    # data = [actual, moving_average]

    moving_average = go.Scatter(x = df1[::-1].index, y = df1[::-1]['4. close'].rolling(window=100, min_periods=5).mean(), name = 'moving_average',
                        mode = 'lines', marker = dict(color = ('rgb(255,140,0)')))
    
    cs = go.Candlestick(x=df1.index,
                    open=df1['1. open'],
                    high=df1['2. high'],
                    low=df1['3. low'],
                    close=df1['4. close'], name=title)
    
    
    data = [cs, moving_average]

    # style plot and add rangeselector
    layout = dict(
    title=title+' Actual',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(count=5,
                     label='5y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date',
    )
    )
    
    return dict(data=data, layout=layout)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(style={'backgroundColor': '#111111'}, children=[
    html.H1(children='Stocks', style={'color': '#7FDBFF', 'textAlign': 'center'}),

    html.Div(children='View any stock price and future predictions.',
             style={'color':'#7FDBFF', 'textAlign': 'center', 'font-size':'12', 'line-height': '-2'}),
    
    html.Div(dcc.Input(id='input-1-submit', type='text', value='',
                       placeholder='Enter a Stock...', size='40'), style={'textAlign':'center'}),
    html.Br(),

    dcc.Graph(id='output-act'),

    dcc.Graph(id='output-submit'),
    
])


@app.callback(Output('output-submit', 'figure'),
              [Input('input-1-submit', 'n_submit'), Input('input-1-submit', 'n_blur')],
              [State('input-1-submit', 'value')])

def update_output(ns1, nb1, input1):
    api_key = 'U6ZCFDY7F487XP4G' # your api key from https://www.alphavantage.co/documentation/#daily
    
    if input1 == '':
        return dict() # return an empty dict so you dont make a bad request
    
    else:
        # api request
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input1}&apikey={api_key}&outputsize=full'
        resp = requests.get(url)
        j = resp.json()

        # pandas to convert json to a pandas DataFrame
        df = pd.DataFrame(j['Time Series (Daily)']).T
        df = df.reset_index().rename(columns={'4. close': 'y', 'index':'ds'})[['ds', 'y']]
        df['y'] = df['y'].astype('float')

        # fbprophet future predictions
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)
        
        return trace(forecast, df, input1)

@app.callback(Output('output-act', 'figure'),
              [Input('input-1-submit', 'n_submit'), Input('input-1-submit', 'n_blur')],
              [State('input-1-submit', 'value')])

def update_output_act(ns1, nb1, input1):
    api_key = 'your_api_key' # your api key from https://www.alphavantage.co/documentation/#daily
    
    if input1 == '':
        return dict() # return an empty dict so you dont make a bad request
    
    else:
        # api request
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input1}&apikey={api_key}&outputsize=full'
        resp = requests.get(url)
        j = resp.json()

        # pandas to convert json to a pandas DataFrame
        df = pd.DataFrame(j['Time Series (Daily)']).T
        
        return trace_act(df, input1)

if __name__ == '__main__':
    app.run_server(debug=True)

