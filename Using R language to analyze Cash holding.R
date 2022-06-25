#Import library
library(tidyverse)
library(readxl)
library(zoo)
library(pastecs)
library(car)
library(Metrics)
library(forecast) 
library(tseries)
library(lmtest) 
library(stats) 

###### Task: Data collection and input ######
# Read file 
filedata = read_excel('K194141741.xlsx')
view(filedata)

#Calculate independent and dependent variables 
data <- filedata %>%
  mutate(Cash_holding = Cash/TA) %>% 
  mutate(Capex = FA/TA) %>% 
  mutate(Growth = (Sales-lag(Sales))/lag(Sales)) %>% 
  mutate(Leverage = TD/TA) %>% 
  mutate(Firm_size = log(TA))
view(data)

# Select necessary columns
data <- data %>%
  select(Time,Cash_holding,Capex,Growth,Leverage,Firm_size) %>% 
  na.omit(Growth) 

# Check number of na in data
sum(is.na(data))

# Check type of column Time, convert right format and create variable Covid
typeof(data$Time)
data$Covid <- ifelse(data$Time >= as.yearqtr('2010 Q2', format = '%Y Q%q') &
                     data$Time < as.yearqtr('2020 Q2', format = '%Y Q%q'), 0, 1)

###### Task: Provide descriptive statistics of all the variables ######
# 1. Descriptive statistics of period before Covid-19
Before <- data %>% 
  filter(Covid == 0) %>%
  select(-Time,-Covid) %>%
  stat.desc() %>% 
  t() %>%
  subset(select = c(min,max,median,mean,std.dev))
view(Before)

# 2. Descriptive statistics of period after Covid-19
After <- data %>% 
  filter(Covid == 1) %>%
  select(-Time,-Covid) %>%
  stat.desc() %>% 
  t() %>%
  subset(select = c(min,max,median,mean,std.dev))
view(After)


###### Task: Provide box & whisker plot and histogram of Cash holding ######
# 1. Box & whisker plot 
ggplot(data = data, aes(y = Cash_holding)) + 
  geom_boxplot(fill='burlywood3') + 
  scale_x_discrete() +
  labs(title = 'Distribution of Cash holding from 2010-2021',
       y = 'Cash holding') +
  coord_flip()

# 2. Histogram
ggplot(data, aes(x=Cash_holding)) + 
  geom_histogram(fill='lightsteelblue3', color='white', binwidth = 0.05)+
  labs(title='Distribution of Cash holding from 2010-2021',
       x='Cash holding',
       y='Count')

###### Task: Perform multiple regression ######
# 1. With the usual individual variables (model 1) 
# Build model
model_1 <- lm(Cash_holding ~ Leverage+Capex+Firm_size+Growth
             , data = data)
summary(model_1)

# Correlation among independent variables
corr <- data[ , c('Leverage','Capex','Firm_size','Growth')]
cor(corr)

# Test multicollinearity with VIF method
vif(model_1)
mean(vif(model_1))

# Adjust model after considering
modeladjust_1 <- lm(Cash_holding ~ Leverage+Capex+Firm_size
              , data = data)
summary(modeladjust_1)
# 2. With the usual individual variables and the interaction between Covid-19 dummy variable and the independent variables (model 2)
# The interaction between Covid-19 dummy variable and the independent variables  
data <- data %>% 
  mutate(Leverage_Covid = Leverage*Covid) %>% 
  mutate(Capex_Covid = Capex*Covid) %>% 
  mutate(Firm_size_Covid = Firm_size*Covid) 
view(data)

# Build model
model_2 <- lm(Cash_holding ~ Leverage+Capex+Firm_size+Leverage_Covid+Capex_Covid+Firm_size_Covid
              ,data = data)
summary(model_2)

# 3. Predict the value of the variable of assigned topic for all the quarters of the sample using Model 1 
# Predict value
predictions <- predict(modeladjust_1, data)

# Create result dataframe of actual and predicted value 
result <- data %>% 
  select(Time,Cash_holding)
names(result)[2] <- 'Actual'
result$Prediction <- predictions
view(result)

# RMSE,RSE
rmse(result$Actual,result$Prediction)
mae(result$Actual,result$Prediction)

###### Task: Perform ARIMA model to predict  ######
# Plot cash holding and ACF, PACF for cash holding
CH <- result$Actual
plot(CH)
acf(CH,main='ACF for Cash holding')
pacf(CH,main='PACF for Cash holding')

# Test stationary of cash holding
adf.test(CH) 

# Diff cash holding with differences=1 
d_CH <- diff(CH, differences =1)

# Test stationary of cash holding after diff
adf.test(d_CH,alternative='stationary') 

# Build model and select best model by auto.arima function
model=auto.arima(d_CH,seasonal=F,trace = T,lambda = 'auto',ic='aic')

# Obtain the coefficients
coeftest(auto.arima(d_CH,seasonal=F))

# Apply diagnostic test of the residuals to validate the model
acf(model$residuals)
pacf(model$residuals)
Box.test(model$residuals,lag=20,type='Ljung-Box')

# Forecast cash holding for 4 quarters in 2022
forecast(model,h=4) 

# Plot actual and forecasting cash holding 
plot(forecast(model,h=4))


