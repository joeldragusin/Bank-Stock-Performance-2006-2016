import pandas_datareader.data as web
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)

# Bank Of America
BAC = yf.download("BAC", start=start, end=end)
# CitiGroup
C = yf.download("C", start=start, end=end)
# Goldman Sachs
GS = yf.download("GS", start=start, end=end)
# JPMorgan Chase
JPM = yf.download("JPM", start=start, end=end)
# Morgan Stanley
MS = yf.download("MS", start=start, end=end)
# Wells Fargo
WFC = yf.download("WFC", start=start, end=end)

tickers = ['BAC','C','GS','JPM','MS','WFC']

bank_stocks = pd.concat([BAC,C,GS,JPM,MS,WFC], axis=1, keys=tickers)

bank_stocks.columns.names = ['Bank Ticker','Stock Info']

returns = pd.DataFrame()

for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()

dictionary = {-0.02300886942418079: 8.76991150442478,
              0.008928605640421639: -0.8991071428571429,
              0.09695019542210614: 0.08410914927768864,
              -0.0002926052697974635: 0.011548711874444617,
              0.14322252868437624: 0.14833759590792828}

returns['C Return'].replace(dictionary, inplace=True)

sns.pairplot(returns[1:])
plt.show()

print(returns.idxmin())
print(returns.idxmax())
print(returns.std())
print(returns.loc['2015-01-01':'2015-12-31'].std())

sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color='green', bins=50)
plt.show()

sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color='red', bins=50)
plt.show()

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4), label=tick)
plt.legend()
plt.show()

bank_stocks.xs(key='Close', axis=1, level='Stock Info').plot()
plt.show()

# Plotly (optional, if you have Plotly installed)
import plotly.graph_objs as go
import plotly.io as pio

# Convert pandas DataFrame to Plotly-friendly format
plotly_data = bank_stocks.xs(key='Close', axis=1, level='Stock Info')

# Create traces
traces = []
for ticker in tickers:
    trace = go.Scatter(x=plotly_data.index, y=plotly_data[ticker], mode='lines', name=ticker)
    traces.append(trace)

# Create layout
layout = go.Layout(title='Bank Stocks', xaxis=dict(title='Date'), yaxis=dict(title='Price'))

# Create figure
fig = go.Figure(data=traces, layout=layout)

# Show the plot using Plotly
pio.show(fig)

BAC.loc['2008-01-01':'2009-01-01']['Close'].rolling(window=30).mean().plot(label='30 Day Mov Avg')
BAC.loc['2008-01-01':'2009-01-01']['Close'].plot(label='BAC Close')
plt.legend()
plt.show()

sns.heatmap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)
plt.show()

sns.clustermap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)
plt.show()
