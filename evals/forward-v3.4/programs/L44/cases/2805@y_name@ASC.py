"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0]
# The supplied Products table has no event relation; count the supplied names.
s=d.groupby('Product_Name',dropna=False).size().sort_values(kind='stable')
ax.bar(s.index.astype(str),s.values,color=colors[0])
ax.tick_params(axis='x',labelrotation=35)
ax.set(xlabel='Product name',ylabel='Number of products',title='Product names — event membership unavailable (ascending count)',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
