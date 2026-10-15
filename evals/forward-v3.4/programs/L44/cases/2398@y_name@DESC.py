"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
movies,ratings=frames
m=ratings.merge(movies[movies.director.notna()][['mID','director']],on='mID',validate='many_to_one')
s=m.groupby('director').stars.max().sort_values(ascending=False,kind='stable')
ax.bar(s.index.astype(str),s.values,color=colors[0])
ax.tick_params(axis='x',labelrotation=30)
ax.set(xlabel='Director',ylabel='Highest movie rating (stars)',title='Highest rating across each director’s movies',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
