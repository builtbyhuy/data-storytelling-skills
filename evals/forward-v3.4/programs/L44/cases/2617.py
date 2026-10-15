"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0];d=d[pd.to_numeric(d.amount_paid,errors='coerce').gt(300)|d.payment_type_code.eq('Check')]
s=d.groupby('payment_date').size().sort_index()
ax.plot(s.index.astype(str),s.values,marker='o',color=colors[0])
ax.tick_params(axis='x',labelrotation=35)
ax.set(xlabel='Payment date and time',ylabel='Number of payments',title='Payments over 300 or paid by Check',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
