"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
d=frames[0].copy()
d['opened_year']=pd.to_datetime(d.date_account_opened).dt.year
p=d.groupby(['opened_year','other_account_details']).size().unstack('other_account_details',fill_value=0).sort_index()
# Follow the actual request's ascending X order, regardless of the filename suffix.
if 'descending' in nl_query.lower() or 'desc' in nl_query.lower():p=p.sort_index(ascending=False)
for i,c in enumerate(p.columns):
    ax.plot(p.index,p[c],label=str(c),color=colors[i%len(colors)],marker=['o','s','^'][i%3],linestyle=['-','--','-.'][i%3])
ax.set(xlabel='Year account opened',ylabel='Number of accounts',title='Account openings by year and account details',ylim=(0,None))
ax.set_xticks(p.index);ax.legend(title='Other account details')
if len(p)>1 and p.index[0]>p.index[-1]:ax.invert_xaxis()

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
