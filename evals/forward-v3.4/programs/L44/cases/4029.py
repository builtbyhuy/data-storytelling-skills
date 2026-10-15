"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
attributes,players=frames
# Player attributes contain repeated dated snapshots. Count distinct players per foot/year.
a=attributes[['player_api_id','preferred_foot']].dropna().drop_duplicates()
m=a.merge(players[['player_api_id','birthday']],on='player_api_id',validate='many_to_one')
m['birth_year']=pd.to_datetime(m.birthday).dt.year
m=m[m.birth_year.between(1980,1989)]
for i,(foot,g) in enumerate(m.groupby('preferred_foot')):
    s=g.groupby('birth_year').player_api_id.nunique().reindex(range(1980,1990),fill_value=0)
    ax.plot(s.index,s.values,label=str(foot),color=colors[i%len(colors)],marker=['o','s','^'][i%3],linestyle=['-','--','-.'][i%3])
ax.set(xlabel='Birth year',ylabel='Number of distinct players',title='Players born in 1980–1989 by preferred foot',ylim=(0,None))
ax.set_xticks(range(1980,1990));ax.legend(title='Preferred foot')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
