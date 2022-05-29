library(tidyverse)
library('readxl')

#Read file 
filedata = read_excel('040522 Data Mid-term test Final.xlsx')
view(filedata)

#Task 2
#Fill NA with the median value of the corresponding variable
data <- filedata %>% 
  mutate_if(is.numeric, function(x) ifelse(is.na(x), median(x, na.rm = T), x))

#Create dataset
set.seed(741)
data <- 
  data[sample(1:nrow(data),100,replace=F), ] 

#Task 1
#Select necessary columns, calculate continuous variables and transform discrete variable
data <- data %>%
  select(firmname,totalasset,totaldebt,cash,cash_dividend,industry) %>%
  mutate(leverage = totaldebt/totalasset) %>% 
  mutate(cashholding = cash/totalasset) %>% 
  mutate(cash_dividend=ifelse(cash_dividend > 0,'1','0')) %>% 
view(data)

#Task 3
#1. 5 firms with highest cash holding
highest <- data %>%
  arrange(desc(cashholding)) %>% 
  slice_head(n=5)
view(data1)

#2. 5 firms with lowest cash holding
lowest <- data %>% 
  arrange(cashholding) %>% 
  slice_head(n=5)
view(data2)

#3. The name of industries which the firms belong to
unique(data$industry)

#4. Provide descriptive statistics with median, mean, max, min, standard deviation of leverage/cash holding of: 
# 4.1 Different categories of the discrete variable
#data$cash_dividend=factor(data$cash_dividend)
describe1 <- data %>% 
  group_by(cash_dividend) %>% 
  summarise(
    median = median(cashholding, na.rm = T),
    mean = mean(cashholding, na.rm = T),
    max = max(cashholding, na.rm = T),
    min = min(cashholding, na.rm = T),
    sd = sd(cashholding, na.rm = T)
  )
describe1
# 4.2 Groups of above/below median of the continuous variable
dd <- data %>% 
  mutate(leverage=ifelse(leverage>median(leverage),'Higher median','Lower median'))
view(dd)
describe2 <- dd %>% 
  group_by(leverage) %>% 
  summarise(
    median = median(cashholding, na.rm = T),
    mean = mean(cashholding, na.rm = T),
    max = max(cashholding, na.rm = T),
    min = min(cashholding, na.rm = T),
    sd = sd(cashholding, na.rm = T)
  )
describe2

#Task 4
#1. Provide histogram of cash holding
#data$cashholding=factor(data$cashholding)
data %>% 
  filter(!is.na(cashholding)) %>% 
  ggplot(aes(x=cashholding))+
  geom_histogram(fill='lightsteelblue3', color='white')       

#2. Provide scatter plot of leverage/cash holding with the continuous variable
#data$nwc = factor(data$nwc)
#data$leverage = factor(data$leverage)

data %>% 
  filter(!is.na(leverage), !is.na(cashholding)) %>% 
  ggplot(aes(x=leverage,y=cashholding))+
  geom_point(size = 2, fill='lightsteelblue3', color='white')

#3. Provide boxplot of cash holding with the discrete variable (different colour for different categories of discrete variable)

data %>% 
  filter(!is.na(cash_dividend), !is.na(cashholding)) %>% 
  ggplot(aes(x = cash_dividend, y = cashholding))+
  geom_boxplot(aes(fill=cash_dividend)) 

#4. Provide a plot that allow the combination of continuous, discrete variables and cash holding 

data %>% 
  filter(!is.na(cash_dividend), !is.na(leverage), !is.na(cashholding)) %>% 
  ggplot(aes(x = leverage, y = cashholding)) + 
  geom_point()+
  labs(title='Cashholding by Leverage and Cash dividend',
       x='Leverage',
       y='Casholding') +
  facet_wrap(~ cash_dividend, nrow = 1)

#Task 5
#1. Count the number of firms in an industry
industry <- c(unique(data$industry))
count <- function(industry) {
  k = 0
  for (i in industry) {
    for (y in 1:nrow(data)){
      if (data$industry[y]==i) 
        k = k+1
    }
  }
  return(k)
}
#Example count the number of firms in Financial industry
print(count('Financials'))

#2. Count the number of firms in an industry and with cash holding above a certain value 
industry <- c(unique(data$industry))
cashholdings <- c(data$cashholding)
count <- function(industry,cashholdings) {
  k = 0
  for (i in industry) {
    for (y in cashholdings) {
      for (z in 1:nrow(data)){
        if (data$industry[z]==i & data$cashholding[z]>y) 
          k = k+1
      }
    }
  }
  return(k)
}
#Example count the number of firms in Consumer Non-Cyclicals industry having cashholding above 0.0228015938
print(count('Consumer Non-Cyclicals','0.0228015938'))