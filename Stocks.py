class Stocks(object):
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.df = None
        self.filename = None
        

    def get_daily(self, stock_name):
        resp = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_name}&apikey={self.api_key}&outputsize=full')
        j = resp.json()
        self.df = pd.DataFrame(j['Time Series (Daily)']).T
        self.filename = stock_name
        return self
    
    def get_hourly(self, stock_name, interval):
        # interval can be 1min, 5min, 15min, 30min, 60min 
        resp = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_name}&interval={interval}&apikey={self.api_key}&outputsize=compact')
        j = resp.json()
        
#         if interval == '1min':
#             self.df = pd.DataFrame(j['Time Series (1min)']).T
#             self.filename = stock_name
#             return self
        
        if interval == '5min':
            self.df = pd.DataFrame(j['Time Series (5min)']).T.iloc[:78, :]
            self.filename = stock_name
            return self
        
        elif interval == '15min':
            self.df = pd.DataFrame(j['Time Series (15min)']).T.iloc[:26, :]
            self.filename = stock_name
            return self
        
        elif interval == '30min':
            self.df = pd.DataFrame(j['Time Series (30min)']).T.iloc[:13, :]
            self.filename = stock_name
            return self

        elif interval == '60min':
            self.df = pd.DataFrame(j['Time Series (60min)']).T.iloc[:7, :]
            self.filename = stock_name
            return self
        
        else:
            raise ValueError(f'"{interval}" is not in ["5min", "15min", "30min", "60min"]')
    
    @staticmethod
    def candle_moving(df1, filename, window, offline=False):     
        moving_average = go.Scatter(x = df1[::-1].index, y = df1[::-1]['4. close'].rolling(window=window,
                                                                                           min_periods=5).mean(),
                                    name = 'moving_average', mode = 'lines', 
                                    marker = dict(color = ('rgb(255,140,0)')), yaxis = 'y2')
        
        cs = go.Candlestick(x=df1.index,
                        open=df1['1. open'],
                        high=df1['2. high'],
                        low=df1['3. low'],
                        close=df1['4. close'], name = filename, yaxis = 'y2')
        
        vol = go.Bar(x=df1.index, y=df1['5. volume'],                         
                   yaxis='y', name='Volume', marker = dict(color = 'rgb(140, 188, 250)'))

        data = [cs, moving_average, vol]

        layout = dict(
        title='Stocks',
        margin = dict( t=40, b=40, r=40, l=40 ),
        yaxis = dict(showgrid=False, showticklabels=False, domain = [0, 0.2]),
        yaxis2 = dict(domain = [0.2, 0.8], zeroline=False),
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
                visible = True,
            ),
            type='date'
        )
        )
        
        fig = dict(data=data, layout=layout)
        
        if offline:
            return plot(fig, filename = filename+'.html')
        return iplot(fig, filename = filename)
    

    @staticmethod
    def candle(df1, filename, offline=False):
        cs = go.Candlestick(x=df1.index,
                        open=df1['1. open'],
                        high=df1['2. high'],
                        low=df1['3. low'],
                        close=df1['4. close'], name = filename, yaxis = 'y2')
        
        vol = go.Bar(x=df1.index, y=df1['5. volume'],                         
                   yaxis='y', name='Volume', marker = dict(color = 'rgb(140, 188, 250)'))

        data = [cs,vol]

        layout = dict(
        title='Stocks',
        margin = dict( t=40, b=40, r=40, l=40 ),
        yaxis = dict(showgrid=False, showticklabels=False, domain = [0, 0.2]),
        yaxis2 = dict(domain = [0.2, 0.8], zeroline=False),
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
                visible = True,
            ),
            type='date'
        )
        )
        
        fig = dict(data=data, layout=layout)
        
        if offline:
            return plot(fig, filename = filename+'.html')
        return iplot(fig, filename = filename)
    

    @staticmethod
    def h_plot(df1, filename, offline=False):
        cs = go.Candlestick(x=df1.index,
                        open=df1['1. open'],
                        high=df1['2. high'],
                        low=df1['3. low'],
                        close=df1['4. close'], name = filename, yaxis = 'y2')
        
        vol = go.Bar(x=df1.index, y=df1['5. volume'],                         
                   yaxis='y', name='Volume', marker = dict(color = 'rgb(140, 188, 250)'))

        data = [cs,vol]

        layout = dict(
        title='Stocks',
        margin = dict( t=40, b=40, r=40, l=40 ),
        yaxis = dict(showgrid=False, showticklabels=False, domain = [0, 0.2]),
        yaxis2 = dict(domain = [0.2, 0.8], zeroline=False),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1h',
                         step='hour',
                         stepmode='backward'),
                    dict(count=3,
                         label='3h',
                         step='hour',
                         stepmode='backward'),
                    dict(count=5,
                        label='5h',
                        step='hour',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True,
            ),
            type='date'
        )
        )
        
        fig = dict(data=data, layout=layout)
        
        if offline:
            return plot(fig, filename = filename+'.html')
        return iplot(fig, filename = filename)
    

    def widget(self,window):
        if window == 5:
            Stocks.candle_moving(self.df, self.filename, 5)
        elif window == 10:
            Stocks.candle_moving(self.df, self.filename, 10)
        elif window == 20:
            Stocks.candle_moving(self.df, self.filename, 20)
        elif window == 50:
            Stocks.candle_moving(self.df, self.filename, 50)
        elif window == 100:
            Stocks.candle_moving(self.df, self.filename, 100)
        elif window == 'None':
            Stocks.candle(self.df, self.filename)
            
    
    @staticmethod
    def trace(df, df1, filename, offline=False):
        yhat = go.Scatter(x = df['ds'], y = df['yhat'],
                          mode = 'lines', line = dict(color='red'), name = 'yhat')


        yhat_lower = go.Scatter(x = df['ds'], y = df['yhat_lower'],
                                mode = 'lines', line = dict(color = ('rgb(140, 188, 250)')), name = 'yhat_lower')

        yhat_upper = go.Scatter(x = df['ds'],y = df['yhat_upper'],
                                mode = 'lines',fill = 'tonexty',
                                line = dict(color = ('rgb(140, 188, 250)')), name = 'yhat_upper')

        actual = go.Scatter(x = df1['ds'], y = df1['y'], name = 'actual',
                            mode = 'markers', marker = dict(color = ('rgb(0,0,0)'), size = 3))


        data = [yhat, yhat_lower, yhat_upper, actual]

        layout = dict(
        title='Stocks',
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
            type='date'
        )
        )

        fig = dict(data=data, layout=layout)
        if offline:
            return plot(fig, filename=filename+'.html')
        return iplot(fig, filename=filename)

    
    
    def plot_future(self):
        f_df = self.df.reset_index().rename(columns={'4. close': 'y', 'index':'ds'})[['ds', 'y']]
        f_df['y'] = f_df['y'].astype('float')

        m = Prophet()
        m.fit(f_df)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)
        
        fig = m.plot_components(forecast)
        
        return Stocks.trace(forecast, f_df, filename=self.filename)
    
    def ma_plot(self):
        interact(self.widget, window = widgets.Dropdown(options=['None', 5,10,20,50,100], value = 'None',
                                          description='MA Window ', disabled=False))
        return self
