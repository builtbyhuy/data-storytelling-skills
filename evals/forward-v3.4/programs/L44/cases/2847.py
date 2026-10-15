"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
genres,tracks=frames
m=tracks.merge(genres[['id','name']],left_on='genre_id',right_on='id',suffixes=('_track','_genre'),validate='many_to_one')
s=m.groupby('name_genre').size().sort_values(ascending=False,kind='stable').head(5)
ax.pie(s.values,labels=s.index.astype(str),autopct='%1.1f%%',startangle=90,colors=colors,wedgeprops={'edgecolor':'white','linewidth':1})
ax.set_title('Top 5 genres by number of tracks');ax.set_aspect('equal')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
