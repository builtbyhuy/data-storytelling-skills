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
a=data(0); p=data(1)
a=a[pd.to_numeric(a['overall_rating'],errors='coerce').ge(75)]
p['birth_year']=pd.to_datetime(p['birthday'],errors='coerce').dt.year
# A player qualifies if at least one recorded overall rating is >=75.
d=p[['player_api_id','birth_year']].merge(a[['player_api_id','preferred_foot']].dropna().drop_duplicates(),on='player_api_id',validate='one_to_many')
v=d.groupby(['birth_year','preferred_foot'])['player_api_id'].nunique().unstack().sort_index().fillna(0)
for foot in v.columns:ax.plot(v.index,v[foot],marker='o',markersize=3,label=str(foot))
ax.set(xlabel='Birth year',ylabel='Number of qualifying players',title='Players with a recorded overall rating ≥75',ylim=(0,None))
ax.legend(title='Preferred foot')

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
