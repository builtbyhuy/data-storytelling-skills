"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
s=frames[0].groupby('Openning_year').Capacity.mean().sort_index()
ax.plot(s.index,s.values,marker='o',color=colors[0])
ax.set(xlabel='Opening year',ylabel='Average cinema capacity',title='Average capacity of cinemas by opening year',ylim=(0,None))
ax.set_xticks(s.index)

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
