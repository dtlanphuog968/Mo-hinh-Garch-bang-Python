#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime as dt


# In[3]:


df_price = pd.read_csv('Price.csv')

df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='ERROR')))]
df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='DELIST')))]
df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='DEAD')))]
df_price


# In[48]:


df_price = pd.read_csv('Price.csv')

df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='ERROR')))]
df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='DELIST')))]
df_price = df_price[df_price.columns.drop(list(df_price.filter(regex='DEAD')))]

def tachcode(s):
    code = s.split('(')[0]
    return code
df_price.loc[0] = df_price.loc[0].apply(tachcode)

header1 = df_price.loc[0]
df_price = df_price[1:]
df_price.columns = header1
df_price.set_index('Code',inplace=True)

dele = []
for i in df_price.columns:
    if (len(i) > 6) or ('VT:' not in i):
        dele.append(i)
df_pr = df_price.drop(dele,axis = 1)
df_pr


# In[49]:


df_market = pd.read_csv('Marketvalue.csv')
df_market = df_market[df_market.columns.drop(list(df_market.filter(regex='ERROR')))]
df_market = df_market[df_market.columns.drop(list(df_market.filter(regex='DELIST')))]
df_market = df_market[df_market.columns.drop(list(df_market.filter(regex='DEAD')))]

df_market.loc[0] = df_market.loc[0].apply(tachcode)
header3 = df_market.loc[0]
df_market = df_market[1:]
df_market.columns = header3
df_market.set_index('Code',inplace=True)

dele2 = []
for i in df_market.columns:
    if (len(i) > 6) or ('VT:' not in i):
        dele2.append(i)
df_mr=df_market.drop(dele2,axis = 1)
df_mr


# In[50]:


df_book = pd.read_csv('Bookvalue.csv')

df_book = df_book[df_book.columns.drop(list(df_book.filter(regex='ERROR')))]

df_book.loc[0] = df_book.loc[0].apply(tachcode)

header2 = df_book.loc[0]
df_book = df_book[1:]
df_book.columns = header2
df_book.set_index('Code',inplace=True)


dele1 = []
for i in df_book.columns:
    if (len(i) > 6) or ('VT:' not in i):
        dele1.append(i)
df_b = df_book.drop(dele1,axis = 1)
df_b


# In[51]:


#Dua ve cung hang, cot
h1 = df_pr.columns
h2 = df_b.columns
h3 = df_mr.columns


# In[52]:


lst = []
for i in h1:
    if i in h2:
        lst.append(i)
df_pr= df_pr.loc[:,lst] 

ls = []
for i in h2:
    if i in h1:
        ls.append(i)
df_b = df_b.loc[:,ls]


# In[53]:


lst1 = []
for i in h3:
    if i in h2:
        lst1.append(i)
df_mr = df_mr.loc[:,lst1] 

ls1 = []
for i in h2:
    if i in h3:
        ls1.append(i)
df_b = df_b.loc[:,ls1]


# In[54]:


# Dinh dang time chuan quoc te
df_pr.index = pd.to_datetime(df_pr.index)
df_b.index = pd.to_datetime(df_b.index)
df_mr.index = pd.to_datetime(df_mr.index)      


# In[55]:


df1 = df_pr.loc['2015-01-01':'2020-12-31']
df2 = df_b.loc['2015-01-01':'2020-12-31']
df3 = df_mr.loc['2011-01-01':'2020-12-31']


# In[56]:


index = pd.bdate_range(start='2015-01-01', end='2020-12-31', freq='BM')
day19 = []
for i in index:
    day19.append(pd.datetime(i.year, i.month, 19))
index1=pd.Index(day19)
index1


# In[57]:


df1 = df1.reindex(index1, method='nearest')
price = df1.bfill()
price


# In[58]:


df2 = df2.reindex(index1, method='nearest')
book = df2.drop([df2.index[0]]).astype(float)
book


# In[59]:


df3 = df3.reindex(index1, method='nearest')
df3 = df3.bfill()
market = df3.drop([df3.index[0]]).astype(float)
market


# In[60]:


return_price = price.pct_change().drop([price.index[0]]).astype(float)
return_price


# In[61]:


r_smb=[]
r_hml=[]
for i in range(0,return_price.shape[0]):
    df_fama= pd.DataFrame({'Ri':return_price.iloc[i,:],'Size':market.iloc[i,:],'B/P':book.iloc[i,:]/price.iloc[i,:]})
    df_fama.dropna(inplace=True)
    small = df_fama[df_fama['Size'] < df_fama['Size'].values.mean()]
    big = df_fama[df_fama['Size'] >= df_fama['Size'].values.mean()]
    small.sort_values(by='B/P',axis=0,ascending=True,inplace=True)
    big.sort_values(by='B/P',axis=0,ascending=True,inplace=True)
    SL = small.iloc[:102,:]
    SN = small.iloc[102:237,:]
    SH = small.iloc[237:,:]
    BL = big.iloc[:14,:]
    BN = big.iloc[14:31,:]
    BH = big.iloc[31:,:]
    R_SMB = 1/3*(SL['Ri'].values.mean() + SN['Ri'].values.mean() + SH['Ri'].values.mean()) - 1/3*(BL['Ri'].values.mean() + BN['Ri'].values.mean()+ BH['Ri'].values.mean())
    R_HML = 1/2*(BH['Ri'].values.mean() + SH['Ri'].values.mean()) - 1/2*(BL['Ri'].values.mean() + SL['Ri'].values.mean())
    r_smb.append(R_SMB)
    r_hml.append(R_HML)


# In[62]:


df4 =pd.read_excel('Bond Yiled.xlsx', parse_dates=True, skiprows = 4).dropna()
df4.rename(columns = {"Code":"Date","VIGBOND.": "Free risk"}, inplace = True)
df4.set_index("Date", inplace = True)
df4= df4.reindex(index1, method='nearest')
df4 =df4.loc['2015-02-01':'2020-12-31']
df4


# In[63]:


df4['R_SMB']=  r_smb
df4['R_HML']= r_hml
df4


# In[ ]:




