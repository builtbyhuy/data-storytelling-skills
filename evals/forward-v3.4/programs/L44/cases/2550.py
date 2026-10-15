"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
s=frames[0].groupby('PetType').pet_age.agg(['mean','max'])
for i,(name,r) in enumerate(s.iterrows()):ax.scatter([r['mean']],[r['max']],label=str(name),color=colors[i%len(colors)],marker=['o','s','^','D'][i%4],s=90)
ax.set(xlabel='Average pet age',ylabel='Maximum pet age',title='Average and maximum ages by pet type')
ax.legend(title='Pet type')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
