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
j=data(0); n=data(1)
d=n[['journalist_id','work_type']].drop_duplicates().merge(j,on='journalist_id',validate='many_to_one')
v=d.groupby('work_type')[['age','years_working']].mean()
for role,r in v.iterrows():ax.scatter(r['age'],r['years_working'],s=65,label=str(role))
ax.set(xlabel='Average age (years)',ylabel='Average working experience (years)',title='Journalist age and experience by role')
ax.legend(title='Work type')

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
