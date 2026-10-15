"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0]
ax.scatter(d.Snatch,d.Total,color=colors[0],s=60)
ax.set(xlabel='Snatch (source units)',ylabel='Total (source units)',title='Snatch and total in body-builder records')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
