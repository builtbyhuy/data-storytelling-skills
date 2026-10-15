import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Replay provides ordered DataFrames, or ordered CSV paths in tables.
if 'dfs' not in globals():
    dfs = [pd.read_csv(path) for path in tables]
def data(i=0):
    frame = dfs[i].copy()
    frame.columns = [str(c).lower() for c in frame.columns]
    return frame
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.figsize': (10, 6)})
fig, ax = plt.subplots()
d=data(); d['product_price']=pd.to_numeric(d['product_price'],errors='coerce')
v=d.groupby('product_type_code')['product_price'].agg(['min','max'])
for name,r in v.iterrows():ax.scatter(r['min'],r['max'],s=65,label=str(name))
ax.set(xlabel='Minimum product price (source units)',ylabel='Maximum product price (source units)',title='Product price range by product type')
ax.legend(title='Product type')

if ax.get_ylabel().startswith('Number'):
    from matplotlib.ticker import MaxNLocator
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
if 'date and time' in ax.get_xlabel().lower():
    import matplotlib.dates as mdates
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.tick_params(axis='x', rotation=25)
fig.tight_layout()
plt.figure(fig.number)
