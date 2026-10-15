"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
ships,deaths=frames
m=deaths.merge(ships[ships.tonnage.eq('t')][['id']],left_on='caused_by_ship_id',right_on='id',validate='many_to_one',suffixes=('_event','_ship'))
ax.scatter(m.killed,m.injured,color=colors[0],s=60)
ax.set(xlabel='People killed',ylabel='People injured',title="Deaths and injuries associated with ships of tonnage 't'")

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
