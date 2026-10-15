"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0]
p=d.groupby(['Industry','Headquarters']).size().unstack('Headquarters',fill_value=0)
p=p.loc[p.sum(axis=1).sort_values(ascending=False,kind='stable').index]
bottom=np.zeros(len(p))
for i,c in enumerate(p.columns):
    ax.bar(p.index.astype(str),p[c].values,bottom=bottom,label=str(c),color=colors[i%len(colors)],edgecolor='white',hatch=['','//','..','xx'][i%4]);bottom+=p[c].to_numpy()
ax.tick_params(axis='x',labelrotation=30)
ax.set(xlabel='Industry',ylabel='Number of companies',title='Companies by industry and headquarters — descending total',ylim=(0,None));ax.legend(title='Headquarters')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
