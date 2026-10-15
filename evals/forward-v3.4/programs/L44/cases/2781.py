"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
attributes,players=frames
# A player qualifies when at least one supplied rating snapshot is >=75.
a=attributes[pd.to_numeric(attributes.overall_rating,errors='coerce').ge(75)][['player_api_id','preferred_foot']].dropna().drop_duplicates()
m=a.merge(players[['player_api_id','birthday']],on='player_api_id',validate='many_to_one')
m['birth_year']=pd.to_datetime(m.birthday).dt.year
p=m.groupby(['birth_year','preferred_foot']).player_api_id.nunique().unstack('preferred_foot',fill_value=0).sort_index()
for i,c in enumerate(p.columns):
    ax.plot(p.index,p[c],label=str(c),color=colors[i%len(colors)],marker=['o','s'][i%2],linestyle=['-','--'][i%2])
ax.set(xlabel='Birth year',ylabel='Number of distinct qualifying players',title='Players rated at least 75 by birth year and preferred foot',ylim=(0,None))
ax.legend(title='Preferred foot')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
