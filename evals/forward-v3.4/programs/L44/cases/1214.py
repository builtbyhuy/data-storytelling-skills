"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
s=frames[0].groupby('gender').agg(dorm_count=('dormid','count'),total_capacity=('student_capacity','sum'))
for i,(name,r) in enumerate(s.iterrows()):ax.scatter([r.dorm_count],[r.total_capacity],label=str(name),color=colors[i%len(colors)],marker=['o','s','^','D'][i%4],s=90)
ax.set(xlabel='Number of dorms',ylabel='Total student capacity',title='Dorm count and total capacity by gender')
ax.legend(title='Gender')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
