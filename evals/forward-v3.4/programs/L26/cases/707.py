"""Derive the requested figure from the supplied ordered dataframes.
Replay contract: globals dfs, tables, pd, np, plt, nl_query.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({'font.size': 11, 'axes.titlesize': 14, 'axes.labelsize': 11,
    'figure.facecolor': 'white', 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
palette = ['#165d7d','#bd5c24','#437e54','#7c5b91','#8d7026','#4a7586','#a3435d','#6b6b6b']

def bar(s, title, xlabel, ylabel, order=None):
    if order == 'asc':
        s=s.rename_axis('category').reset_index(name='value').sort_values(['value','category'],kind='stable').set_index('category')['value']
    elif order == 'desc':
        s=s.rename_axis('category').reset_index(name='value').sort_values(['value','category'],ascending=[False,True],kind='stable').set_index('category')['value']
    ax.bar(s.index.astype(str),s.to_numpy(),color=palette[0])
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x',labelrotation=35)
    for t in ax.get_xticklabels(): t.set_ha('right')
    ax.grid(axis='y',alpha=.2)
    ax.set_axisbelow(True)

def lines(p, title, xlabel, ylabel):
    p=p.sort_index()
    for i,col in enumerate(p.columns):
        ax.plot(p.index,p[col],label=str(col),marker='o',markersize=4,color=palette[i%len(palette)])
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=.2)
    ax.legend(title=p.columns.name,loc='best')

def date_line(s,title,xlabel,ylabel):
    s=s.sort_index()
    ax.plot(s.index,s.values,color=palette[0],marker='o')
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    locator=mdates.AutoDateLocator(minticks=4,maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.set_ylim(bottom=0)
    ax.grid(alpha=.2)

def scatter(g,x,y,title,xlabel,ylabel,grouped=True):
    if grouped:
        for i,(name,row) in enumerate(g.iterrows()):
            ax.scatter([row[x]],[row[y]],label=str(name),s=65,color=palette[i%len(palette)])
        ax.legend(title=g.index.name,loc='best')
    else:
        ax.scatter(g[x],g[y],s=65,color=palette[0])
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    ax.grid(alpha=.2)

def pie(s,title):
    wedges,labels,percentages=ax.pie(s.values,labels=s.index.astype(str),autopct='%1.1f%%',startangle=90,
           colors=[palette[i%len(palette)] for i in range(len(s))],wedgeprops={'edgecolor':'white'})
    for wedge,text in zip(wedges,percentages):
        rgb=wedge.get_facecolor()[:3]
        linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        luminance=sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))
        text.set_color('white' if 1.05/(luminance+.05)>=(luminance+.05)/.05 else 'black')
    ax.set_title(title)
    ax.axis('equal')

def stacked(p,title,xlabel,order=None):
    if order:
        totals=p.sum(axis=1)
        domain=sorted(p.index,key=lambda x:((-totals[x] if order=='desc' else totals[x]),str(x)))
        p=p.reindex(domain)
    bottom=np.zeros(len(p))
    for i,col in enumerate(p.columns):
        vals=p[col].to_numpy()
        ax.bar(p.index.astype(str),vals,bottom=bottom,label=str(col),color=palette[i%len(palette)])
        bottom=bottom+vals
    ax.set(title=title,xlabel=xlabel,ylabel='Count')
    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x',labelrotation=30)
    for t in ax.get_xticklabels(): t.set_ha('right')
    ax.legend(title=p.columns.name,bbox_to_anchor=(1.02,1),loc='upper left')
    ax.grid(axis='y',alpha=.2)
    ax.set_axisbelow(True)

counties,cities=dfs[0].copy(),dfs[1].copy()
d=cities.merge(counties[['County_ID','Crime_rate']],on='County_ID',validate='many_to_one')
scatter(d,'White','Crime_rate','City white percentage and county crime rate','White population in city (%)','County crime rate (source units)',grouped=False)
