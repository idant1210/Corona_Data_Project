import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt      
import math
import seaborn as sns
from collections import Counter
from sklearn.decomposition import PCA
from datetime import datetime

date = []
new_cases = []
total_cases = []
new_vaccined = []
total_vaccined = []
population = []
location = []

def one_dim_plot(sr, plot_type, axis):
    sr.plot (kind =plot_type ,ax=axis)

def get_frequent_elements(df, col_name):
    df_frequent= df.copy()
    df_frequent= df_frequent[col_name]
    return df_frequent

complete_dataset = pd.read_csv("owid-covid-data.csv")

for index,row in complete_dataset.iterrows():
	date.append(row['date'])
	new_cases.append(row['new_cases'])
	total_cases.append(row['total_cases'])
	new_vaccined.append(row['new_vaccinations'])
	total_vaccined.append(row['people_fully_vaccinated'])
	location.append(row['location'])
	population.append(row['population'])
updated_df = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population})
updated_df = updated_df.fillna(0.0)
updated_df['date'] = pd.to_datetime(updated_df['date'])
updated_df = updated_df[~(updated_df['date'] < '2021-01-01')]
pre_vaccaine = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] < 1])
pre_vaccaine = pd.DataFrame(pre_vaccaine.loc[pre_vaccaine['new vaccined'] < 1])
vaccained = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] > 0])
pre_vaccaine = pre_vaccaine.reset_index(drop=True)
i=0
fig, axes= plt.subplots(1, 3, figsize=(20,5))
for indexs in pre_vaccaine['total cases'].index :
	sr = get_frequent_elements(pre_vaccaine ,'total cases')
	one_dim_plot(sr , pre_vaccaine["total cases"][indexs] , axes[i])
	i = i+1
'''
fig = plt.figure(figsize=(50, 20))
ax = fig.add_subplot(111)
plt.plot(pre_vaccaine['date'],pre_vaccaine['total cases'],linewidth=1.0, color='r')
plt.ylabel('Number of cases')
plt.xticks(rotation = 45, ha = 'right')
plt.show()'''