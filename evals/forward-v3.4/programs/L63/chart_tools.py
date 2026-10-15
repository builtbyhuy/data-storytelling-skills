"""Chart semantics derived solely from the supplied queries and relational CSVs."""
import pandas as pd
import numpy as np
import textwrap

COLORS=['#24527a','#b25a28','#36735a','#8a4c73','#777127','#416f86','#966742','#3c6b67','#705c8c','#7c4444','#59615c','#80733b']
def setup(plt,title,xlabel,ylabel):
    fig,ax=plt.subplots(figsize=(10,6))
    ax.set_title(title,loc='left',pad=16)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.spines[['top','right']].set_visible(False)
    return fig,ax
def finish(fig,ax):
    fig.tight_layout()
def bar(plt,s,title,xlabel,ylabel,ascending=None):
    if ascending is not None: s=s.sort_values(ascending=ascending,kind='stable')
    fig,ax=setup(plt,title,xlabel,ylabel)
    ax.bar(s.index.astype(str),s.values,color=COLORS[0])
    ax.set_ylim(bottom=0)
    if len(s)>5 or max(map(len,s.index.astype(str)),default=0)>16:
        plt.setp(ax.get_xticklabels(),rotation=40,ha='right')
    finish(fig,ax)
def line(plt,s,title,xlabel,ylabel):
    s=s.sort_index();fig,ax=setup(plt,title,xlabel,ylabel)
    # Retain exact source date/time strings unless the query explicitly requests year bins.
    ax.plot(s.index.astype(str),s.values,marker='o',color=COLORS[0],linewidth=1.8)
    if len(s)>7 or max(map(len,s.index.astype(str)),default=0)>12: plt.setp(ax.get_xticklabels(),rotation=45,ha='right',fontsize=9)
    ax.set_ylim(bottom=0);finish(fig,ax)
def grouped_line(plt,p,title,xlabel,ylabel):
    p=p.sort_index().fillna(0);fig,ax=setup(plt,title,xlabel,ylabel)
    for i,c in enumerate(p.columns):
        ax.plot(p.index.astype(str),p[c].values,marker=['o','s','^','D'][i%4],color=COLORS[i%len(COLORS)],label=str(c),linewidth=1.8)
    ax.set_ylim(bottom=0); ax.legend(title=p.columns.name)
    if len(p)>12: plt.setp(ax.get_xticklabels(),rotation=45,ha='right',fontsize=9)
    finish(fig,ax)
def scatter(plt,df,x,y,title,xlabel,ylabel,group=None):
    fig,ax=setup(plt,title,xlabel,ylabel)
    if group:
        for i,(k,z) in enumerate(df.groupby(group,sort=True,dropna=False)):
            ax.scatter(z[x],z[y],label=str(k),s=48,color=COLORS[i%len(COLORS)],marker=['o','s','^','D','v'][i%5])
        ax.legend(title=group)
    else: ax.scatter(df[x],df[y],s=48,color=COLORS[0])
    finish(fig,ax)
def pie(plt,s,title):
    fig,ax=plt.subplots(figsize=(9,7))
    labels=[textwrap.fill(str(x),24) for x in s.index]
    ax.pie(s.values,labels=labels,autopct='%1.1f%%',colors=COLORS[:len(s)],startangle=90,textprops={'fontsize':10})
    ax.set_title(title,loc='left',pad=18);ax.axis('equal');fig.tight_layout()
def stacked(plt,p,title,xlabel,series_label,descending=False):
    p=p.fillna(0)
    if descending:p=p.loc[p.sum(axis=1).sort_values(ascending=False,kind='stable').index]
    fig,ax=setup(plt,title,xlabel,'Count')
    bottom=np.zeros(len(p),dtype=float)
    for i,c in enumerate(p.columns):
        ax.bar(p.index.astype(str),p[c].to_numpy(),bottom=bottom,label=str(c),color=COLORS[i%len(COLORS)])
        bottom+=p[c].to_numpy()
    ax.set_ylim(bottom=0);ax.legend(title=series_label,bbox_to_anchor=(1.02,1),loc='upper left')
    if len(p)>4 or max(map(len,p.index.astype(str)),default=0)>16: plt.setp(ax.get_xticklabels(),rotation=40,ha='right')
    finish(fig,ax)

def render(case,t,q,plt):
    if case=='926':
        bar(plt,t['Accounts'].groupby('other_account_details').size(),'Accounts by account details','Other account details','Number of accounts')
    elif case=='1320@y_name@ASC':
        bar(plt,t['election'].groupby('Committee')['Delegate'].count(),'Delegates by committee','Committee','Number of delegates',True)
    elif case=='2805@y_name@ASC':
        # The only supplied relation is Products; no event relation or event key is available.
        # All supplied product names are therefore the available product set for this request.
        bar(plt,t['Products'].groupby('Product_Name').size(),'Product names (event membership unavailable)','Product name','Number of products',True)
    elif case=='2596@x_name@ASC':
        a=t['Catalog_Contents_Additional_Attributes']
        a=a[pd.to_numeric(a['attribute_value'],errors='coerce').eq(0)]
        z=t['Attribute_Definitions'].merge(a,on='attribute_id')
        s=z.groupby('attribute_name').size().sort_index()
        bar(plt,s,'Attributes with value 0','Attribute name','Number of attributes')
    elif case in ('4029','2781'):
        a=t['Player_Attributes'];p=t['Player']
        if case=='2781':a=a[pd.to_numeric(a['overall_rating'],errors='coerce').ge(75)]
        z=p[['player_api_id','birthday']].merge(a[['player_api_id','preferred_foot']],on='player_api_id')
        z['birth_year']=pd.to_datetime(z['birthday'],errors='coerce').dt.year
        if case=='4029':z=z[z['birth_year'].ge(1980)&z['birth_year'].lt(1990)]
        # Count the joined player attribute records: each source rating/foot observation is retained.
        g=z.groupby(['birth_year','preferred_foot'],dropna=True).size().unstack(fill_value=0)
        g.index=g.index.astype(int)
        grouped_line(plt,g,'Player records by birth year and preferred foot'+(' (rating ≥ 75)' if case=='2781' else ' (1980–1989)'),'Birth year','Number of player records')
    elif case=='1349@x_name@ASC':
        z=t['hiring'].copy(); n=pd.to_numeric(z['Start_from'],errors='coerce')
        z['start_year']=n if n.notna().all() else pd.to_datetime(z['Start_from'],errors='coerce').dt.year
        g=z.groupby(['start_year','Is_full_time']).size().unstack(fill_value=0);g.index=g.index.astype(int)
        grouped_line(plt,g,'Hiring records by start year and full-time status','Start year','Number of hiring records')
    elif case=='942@x_name@DESC':
        z=t['Accounts'].copy();z['opened_year']=pd.to_datetime(z['date_account_opened']).dt.year
        grouped_line(plt,z.groupby(['opened_year','other_account_details']).size().unstack(fill_value=0),'Accounts opened by year and account details','Year opened','Number of accounts')
    elif case=='1133':
        z=t['Products'].groupby('product_type_code',as_index=False).agg(minimum_price=('product_price','min'),maximum_price=('product_price','max'))
        scatter(plt,z,'minimum_price','maximum_price','Minimum and maximum product price by type','Minimum product price','Maximum product price','product_type_code')
    elif case=='2479':
        z=t['journalist'].merge(t['news_report'],on='journalist_ID').groupby('Work_Type',as_index=False).agg(average_age=('Age','mean'),average_experience=('Years_working','mean'))
        scatter(plt,z,'average_age','average_experience','Average age and experience by work role','Average age (years)','Average experience (years)','Work_Type')
    elif case in ('2548','2550'):
        z=t['Pets'].groupby('PetType',as_index=False).agg(average_age=('pet_age','mean'),maximum_age=('pet_age','max'))
        scatter(plt,z,'average_age','maximum_age','Average and maximum pet age by type','Average pet age (years)','Maximum pet age (years)','PetType' if case=='2550' else None)
    elif case=='1214':
        z=t['Dorm'].groupby('gender',as_index=False).agg(dorm_count=('dormid','count'),total_capacity=('student_capacity','sum'))
        scatter(plt,z,'dorm_count','total_capacity','Dorm count and total capacity by gender','Number of dorms','Total student capacity','gender')
    elif case=='471':
        line(plt,t['cinema'].groupby('Openning_year')['Capacity'].mean(),'Average cinema capacity by opening year','Opening year','Average capacity')
    elif case=='1285':
        z=t['Student_Tests_Taken'];z=z[z['test_result'].eq('Pass')]
        line(plt,z.groupby('date_test_taken').size(),'Passed tests by date taken','Date test taken','Number of passed tests')
    elif case=='2617':
        z=t['Payments'];z=z[pd.to_numeric(z['amount_paid'],errors='coerce').gt(300)|z['payment_type_code'].eq('Check')]
        line(plt,z.groupby('payment_date').size(),'Payments above 300 or made by check','Payment date','Number of payments')
    elif case=='1254@x_name@ASC':
        z=t['Student_Tests_Taken'];z=z[z['test_result'].eq('Pass')]
        z=t['Student_Course_Enrolment'].merge(z,on='registration_id')
        line(plt,z.groupby('date_of_enrolment').size(),'Passed test records by enrollment date','Date of enrollment','Number of passed test records')
    elif case=='2506':
        pie(plt,t['party'].groupby('Location').size(),'Parties by location')
    elif case=='1310':
        z=t['election'].merge(t['party'][['Party_ID','Party']].rename(columns={'Party':'party_name'}),left_on='Party',right_on='Party_ID')
        pie(plt,z.groupby('party_name')['Delegate'].count(),'Delegates by party')
    elif case=='1527':
        z=t['Procedures'];z=z[pd.to_numeric(z['Cost'],errors='coerce').gt(5000)]
        z=t['Trained_In'].merge(z[['Code']],left_on='Treatment',right_on='Code').merge(t['Physician'][['EmployeeID','Name']],left_on='Physician',right_on='EmployeeID')
        pie(plt,z.groupby('Name').size(),'Training records for procedures costing more than 5000')
    elif case=='2847':
        z=t['tracks'].merge(t['genres'].rename(columns={'id':'genre_key','name':'genre_name'}),left_on='genre_id',right_on='genre_key')
        s=z.groupby('genre_name').size().sort_values(ascending=False,kind='stable').head(5)
        pie(plt,s,'Top five genres by track count')
    elif case=='707':
        z=t['city'].merge(t['county_public_safety'][['County_ID','Crime_rate']],on='County_ID')
        scatter(plt,z,'White','Crime_rate','City white percentage and county crime rate','City white population (%)','County crime rate')
    elif case=='175':
        z=t['ship'];z=z[z['tonnage'].eq('t')]
        z=z[['id']].merge(t['death'],left_on='id',right_on='caused_by_ship_id')
        scatter(plt,z,'killed','injured','Deaths and injuries for ships with tonnage t','Deaths','Injuries')
    elif case=='354':
        scatter(plt,t['body_builder'],'Snatch','Total','Snatch and total lifted weight','Snatch','Total')
    elif case=='4018':
        z=t['Products'][['product_id','product_category_code']].merge(t['Complaints'],on='product_id')
        stacked(plt,z.groupby(['product_category_code','complaint_status_code']).size().unstack(fill_value=0),'Complaints by product category and status','Product category','Complaint status')
    elif case=='680@y_name@DESC':
        z=t['company']
        stacked(plt,z.groupby(['Headquarters','Industry']).size().unstack(fill_value=0),'Company counts by headquarters and industry','Headquarters','Industry',True)
    elif case=='145@y_name@DESC':
        z=t['Skills'].merge(t['Skills_Required_To_Fix'],on='skill_id').merge(t['Part_Faults'],on='part_fault_id')
        stacked(plt,z.groupby(['skill_description','fault_short_name']).size().unstack(fill_value=0),'Faults by required skill and short name','Skill description','Fault short name',True)
    elif case=='4007':
        z=t['accelerator_compatible_browser'].merge(t['browser'][['id','name']].rename(columns={'id':'browser_key','name':'browser_name'}),left_on='browser_id',right_on='browser_key')
        z=z.merge(t['Web_client_accelerator'][['id','name']].rename(columns={'id':'accelerator_key','name':'accelerator_name'}),left_on='accelerator_id',right_on='accelerator_key')
        stacked(plt,z.groupby(['browser_name','accelerator_name']).size().unstack(fill_value=0),'Accelerator compatibility by browser','Browser','Accelerator')
    elif case=='2398@y_name@DESC':
        z=t['Movie'].dropna(subset=['director']);z=z[z['director'].astype(str).str.strip().ne('')&z['director'].astype(str).str.upper().ne('NULL')]
        z=z.merge(t['Rating'],on='mID')
        bar(plt,z.groupby('director')['stars'].max(),'Highest movie rating by director','Director','Highest star rating',False)
    else: raise ValueError('Unsupported case '+str(case))
