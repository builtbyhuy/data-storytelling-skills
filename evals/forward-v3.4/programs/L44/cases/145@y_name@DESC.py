"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
skills,faults,required=frames
# A fault-skill relation is counted once even if the linking row repeats.
m=required.drop_duplicates(['part_fault_id','skill_id']).merge(faults[['part_fault_id','fault_short_name']],on='part_fault_id',validate='many_to_one').merge(skills[['skill_id','skill_description']],on='skill_id',validate='many_to_one')
p=m.groupby(['skill_description','fault_short_name']).part_fault_id.nunique().unstack('fault_short_name',fill_value=0)
p=p.loc[p.sum(axis=1).sort_values(ascending=False,kind='stable').index]
bottom=np.zeros(len(p))
for i,c in enumerate(p.columns):
    ax.bar(p.index.astype(str),p[c].values,bottom=bottom,label=str(c),color=colors[i%len(colors)],edgecolor='white',hatch=['','//','..','xx'][i%4]);bottom+=p[c].to_numpy()
ax.set(xlabel='Skill description',ylabel='Number of distinct faults',title='Faults by required skill and short name — descending total',ylim=(0,None));ax.legend(title='Fault short name')

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
