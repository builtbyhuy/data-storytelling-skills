"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
accelerators,browsers,compatible=frames
m=compatible.drop_duplicates(['accelerator_id','browser_id']).merge(accelerators[['id','name']],left_on='accelerator_id',right_on='id',validate='many_to_one').rename(columns={'name':'accelerator_name'}).merge(browsers[['id','name']],left_on='browser_id',right_on='id',validate='many_to_one',suffixes=('_accelerator','_browser')).rename(columns={'name':'browser_name'})
p=m.groupby(['browser_name','accelerator_name']).size().unstack('accelerator_name',fill_value=0).sort_index()
bottom=np.zeros(len(p))
for i,c in enumerate(p.columns):
    ax.bar(p.index.astype(str),p[c].values,bottom=bottom,label=str(c),color=colors[i%len(colors)],edgecolor='white',hatch=['','//','..','xx'][i%4]);bottom+=p[c].to_numpy()
ax.set(xlabel='Browser',ylabel='Number of compatible accelerators',title='Compatible accelerators by browser',ylim=(0,None));ax.legend(title='Accelerator')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
