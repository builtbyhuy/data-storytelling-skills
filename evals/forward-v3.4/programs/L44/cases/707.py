"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
counties,cities=frames
m=cities.merge(counties[['County_ID','Crime_rate']],on='County_ID',validate='many_to_one')
ax.scatter(m.White,m.Crime_rate,color=colors[0],s=45,alpha=.8)
ax.set(xlabel='White population in city (%)',ylabel='County crime rate (source units)',title='City White percentages and corresponding county crime rates')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
