"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
definitions,attributes=frames
m=attributes[pd.to_numeric(attributes.attribute_value,errors='coerce').eq(0)].merge(definitions,on='attribute_id',validate='many_to_one')
s=m.groupby('attribute_name',dropna=False).size().sort_index()
ax.bar(s.index.astype(str),s.values,color=colors[0])
ax.set(xlabel='Attribute name',ylabel='Number of attributes with value 0',title='Zero-valued attributes by definition',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
