"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0]
s=d.groupby('Committee',dropna=False).size().sort_values(kind='stable')
ax.bar(s.index.astype(str),s.values,color=colors[0])
ax.tick_params(axis='x',labelrotation=30)
ax.set(xlabel='Committee',ylabel='Number of delegates',title='Delegates by committee — ascending count',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
