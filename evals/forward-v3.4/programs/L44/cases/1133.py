"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0]
s=d.groupby('product_type_code').product_price.agg(['min','max'])
for i,(name,r) in enumerate(s.iterrows()):ax.scatter([r['min']],[r['max']],label=str(name),color=colors[i%len(colors)],marker=['o','s','^','D'][i%4],s=90)
ax.set(xlabel='Minimum product price',ylabel='Maximum product price',title='Minimum and maximum prices by product type')
ax.legend(title='Product type code')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
