"""Derive a Matplotlib figure from the replay's ordered source DataFrames."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
frames = [d.copy() for d in dfs] if 'dfs' in globals() else [pd.read_csv(t) for t in tables]
fig, ax = plt.subplots(figsize=(9, 5.5), layout='constrained')
colors = ['#0072B2', '#D55E00', '#009E73', '#AA3377', '#4477AA', '#882255', '#117733']
enrolments,tests=frames
m=tests[tests.test_result.eq('Pass')].merge(enrolments,on='registration_id',validate='many_to_one')
s=m.groupby('date_of_enrolment').size().sort_index()
ax.plot(s.index.astype(str),s.values,marker='o',color=colors[0])
ax.tick_params(axis='x',labelrotation=35)
ax.set(xlabel='Enrollment date and time',ylabel='Number of passed tests',title='Passed tests by enrollment date — ascending date',ylim=(0,None))

ax.spines[['top','right']].set_visible(False)
plt.sca(ax)
