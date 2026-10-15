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
s=data(0); f=data(1); req=data(2)
d=req.merge(s[['skill_id','skill_description']],on='skill_id',validate='many_to_one').merge(f[['part_fault_id','fault_short_name']],on='part_fault_id',validate='many_to_one')
v=d.groupby(['skill_description','fault_short_name']).size().unstack(fill_value=0)
v=v.loc[v.sum(axis=1).sort_values(ascending=False,kind='stable').index]
v.plot.bar(stacked=True,ax=ax,colormap='tab10')
ax.set(xlabel='Skill description',ylabel='Number of faults',title='Faults by required skill and fault short name',ylim=(0,None))
ax.legend(title='Fault short name');ax.tick_params(axis='x',rotation=0)

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
