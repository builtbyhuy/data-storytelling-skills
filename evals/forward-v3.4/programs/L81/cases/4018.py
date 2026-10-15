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
p=data(0); c=data(1)
d=c.merge(p[['product_id','product_category_code']],on='product_id',validate='many_to_one')
v=d.groupby(['product_category_code','complaint_status_code']).size().unstack(fill_value=0).sort_index()
v.plot.bar(stacked=True,ax=ax,colormap='tab10')
ax.set(xlabel='Product category',ylabel='Number of complaints',title='Complaints by category and status',ylim=(0,None))
ax.legend(title='Complaint status');ax.tick_params(axis='x',rotation=0)

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
