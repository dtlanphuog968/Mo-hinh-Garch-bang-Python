#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[2]:


import warnings
import requests
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from arch import arch_model
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import het_arch
from statsmodels.graphics.tsaplots import plot_pacf 
from statsmodels.graphics.tsaplots import plot_acf 
import cufflinks as cf
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode()


# Đọc dữ liệu từ trang web twelvwdata bằng khóa riêng API

# In[3]:


ticker = 'SONY'
api_key = 'dfb57946806a4f30985a037482f4c40b'
interval = '1day'

url = f'https://api.twelvedata.com/time_series?symbol={ticker}&start_date=2007-01-01&end_date=2022-01-11&interval={interval}&apikey={api_key}'
data = requests.get(url).json()
   
sony_data = pd.DataFrame(data['values'])
sony_data.head(10)


# Kiểm tra và chỉnh sửa kiểu dữ liệu

# In[4]:


sony_data.dtypes


# In[5]:


# Chỉnh sửa kiểu dữ liệu
sony_data[['open','high','low','close']] = sony_data[['open','high','low','close']].astype('float')
sony_data[['volume']] = sony_data[['volume']].astype('int')
sony_data.dtypes


# Set index bởi cột "datetime" và sắp xếp đúng thứ tự

# In[6]:


sony_data = sony_data.sort_values(by=['datetime'])
sony_data.set_index('datetime',inplace=True)
sony_data


# Kiểm tra null trong dataframe

# In[7]:


sony_data.isnull().sum()


# In[8]:


#Biểu đồ giá cổ phiếu SONY 
sony_data1 = cf.QuantFig(sony_data,title='SONY Stock Price',legend='top',name='SONY')
sony_data1.add_ema(periods=20, color='green') 
sony_data1.iplot()


# In[9]:


#Giá cổ phiếu thấp và cao nhất của SONY
print(sony_data['close'].min())
print(sony_data['close'].max())


# Tính tỷ suất sinh lời của cổ phiếu SONY

# In[10]:


sony_data = sony_data.loc[:, ['close']]
sony_data['returns'] = sony_data.close.pct_change()*100
sony_data = sony_data.dropna()
sony_data


# Trực quan hóa chuỗi dữ liệu giá đóng cửa và tỷ suất sinh lời

# In[11]:


sony_data.iplot(subplots=True, shape=(3,1), shared_xaxes=True, title='Sony time series')


# In[12]:


# Biểu đồ của tỷ suất sinh lời
fig = plt.figure()
fig.set_figwidth(12)
plt.plot(sony_data['returns'], label = 'Daily Returns')
plt.legend(loc='upper right')
plt.title('Daily Returns Over Time')
plt.show()


# In[13]:


#Phân phối xác suất của chuỗi tỷ suất lợi nhuận
plt.hist(sony_data['returns'], bins = 20, facecolor = 'tomato', label = 'Mean returns')
plt.legend(loc = 'upper left')
plt.show()


# Tính toán độ biến động theo ngày, tháng và năm

# In[14]:


daily_volatility = sony_data['returns'].std()
print('Daily volatility: ', '{:.2f}%'.format(daily_volatility))

monthly_volatility = math.sqrt(20) * daily_volatility
print ('Monthly volatility: ', '{:.2f}%'.format(monthly_volatility))

annual_volatility = math.sqrt(250) * daily_volatility
print ('Annual volatility: ', '{:.2f}%'.format(annual_volatility ))


# Kiểm định tính dừng bằng kiểm định ADF

# In[15]:


def adf_test(x):
    indices = ['Test Statistic', 'p-value', '# of Lags Used', '# of Observations Used']
    adf_test = adfuller(x)
    results = pd.Series(adf_test[0:4], index=indices)
    for key, value in adf_test[4].items():
        results[f'Critical Value ({key})'] = value
    return results
adf_test(sony_data['returns'])


# Kiểm định hiệu ứng ARCH trong kiểm định LM

# In[16]:


# Test by LM
arch_test = het_arch(sony_data['returns'])
print('LM: ',arch_test[0])
print('p_value: ',arch_test[1])


# Biểu đồ ACF và PACF

# In[17]:


fig, ax = plt.subplots(2, figsize = (16,8))
plot_acf(sony_data['returns'], ax = ax[0], lags = 40, alpha = 0.05)
plt.close()
plot_pacf(sony_data['returns'], ax = ax[1], lags = 40, alpha = 0.05)


# Mô hình GARCH

# In[18]:


#Mô hình GARCH(1,1)
garch_model = arch_model(sony_data['returns'], p = 1, q = 1,
                      mean = 'Zero', vol = 'GARCH', dist = 'normal')

gm_result = garch_model.fit(disp='off')

gm_result


# In[19]:


#Mô hình GARCH(2,2)
garch_model1 = arch_model(sony_data['returns'], p = 2, q = 2,
                      mean = 'Zero', vol = 'GARCH', dist = 'normal')

gm_result1 = garch_model1.fit(disp='off')

gm_result1


# In[20]:


#Mô hình GARCH(3,3)
garch_model2 = arch_model(sony_data['returns'], p = 3, q = 3,
                      mean = 'Zero', vol = 'GARCH', dist = 'normal')

gm_result2 = garch_model2.fit(disp='off')

gm_result2


# In[ ]:




