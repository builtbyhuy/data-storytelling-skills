"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0].copy()
d['start_year']=pd.to_numeric(d.Start_from,errors='coerce').astype('Int64')
p=d.groupby(['start_year','Is_full_time']).size().unstack('Is_full_time',fill_value=0).sort_index()
for i,c in enumerate(p.columns):
    ax.plot(p.index.astype(int),p[c],label=str(c),color=colors[i%len(colors)],marker=['o','s'][i%2],linestyle=['-','--'][i%2])
ax.set(xlabel='Start year',ylabel='Number of hiring records',title='Hires by start year and full-time status',ylim=(0,None))
ax.set_xticks(p.index.astype(int));ax.legend(title='Is full time')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
