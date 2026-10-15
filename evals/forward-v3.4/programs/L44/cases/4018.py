"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
products,complaints=frames
m=complaints.merge(products[['product_id','product_category_code']],on='product_id',validate='many_to_one')
p=m.groupby(['product_category_code','complaint_status_code']).size().unstack('complaint_status_code',fill_value=0).sort_index()
bottom=np.zeros(len(p))
for i,c in enumerate(p.columns):
    ax.bar(p.index.astype(str),p[c].values,bottom=bottom,label=str(c),color=colors[i%len(colors)],edgecolor='white',hatch=['','//','..','xx'][i%4]);bottom+=p[c].to_numpy()
ax.set(xlabel='Product category',ylabel='Number of complaints',title='Complaints by product category and status',ylim=(0,None));ax.legend(title='Complaint status')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
