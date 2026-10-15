"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
journalists,reports=frames
# Count a journalist once within each work type, avoiding repeated assignments weighting their age.
m=reports[['journalist_ID','Work_Type']].drop_duplicates().merge(journalists,on='journalist_ID',validate='many_to_one')
s=m.groupby('Work_Type')[['Age','Years_working']].mean()
for i,(name,r) in enumerate(s.iterrows()):ax.scatter([r.Age],[r.Years_working],label=str(name),color=colors[i%len(colors)],marker=['o','s','^','D'][i%4],s=90)
ax.set(xlabel='Average age (years)',ylabel='Average experience (years working)',title='Journalists: average age and experience by role')
ax.legend(title='Work type')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
