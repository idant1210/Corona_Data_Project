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
sick_of_pop = []

def one_dim_plot(sr, plot_type, axis):
    sr.plot (kind =plot_type ,ax=axis)

def get_frequent_elements(df, col_name,num_top_elements):
    df_frequent= df.copy()
    df_frequent = df_frequent.drop_duplicates(['location'],keep = 'last')
    df_frequent= df_frequent[col_name].value_counts()[:num_top_elements].index.tolist()
    return df_frequent

complete_dataset = pd.read_csv("owid-covid-data.csv")
complete_dataset.dropna()
for index,row in complete_dataset.iterrows():
	date.append(row['date'])
	new_cases.append(row['new_cases'])
	total_cases.append(row['total_cases'])
	new_vaccined.append(row['new_vaccinations'])
	total_vaccined.append(row['people_fully_vaccinated'])
	location.append(row['location'])
	population.append(row['population'])
	try:
		precent = (int(row['total_cases']) / int(row['population'])*100)
	except ValueError:
		precent= 0.0
	sick_of_pop.append(precent)
updated_df = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population,"precent of population":sick_of_pop})
updated_df = updated_df.fillna(0.0)
updated_df['date'] = pd.to_datetime(updated_df['date'])
updated_df = updated_df[~(updated_df['date'] < '2021-01-01')]
pre_vaccaine = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] < 1])
pre_vaccaine = pd.DataFrame(pre_vaccaine.loc[pre_vaccaine['new vaccined'] < 1])
vaccained = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] > 0])
pre_vaccaine = pre_vaccaine.reset_index(drop=True)
final_pre = pre_vaccaine.copy()[0:0]
for location in pre_vaccaine.copy().drop_duplicates(['location'])['location']:
	temp = pre_vaccaine.where(pre_vaccaine['location']==location).dropna().nlargest(1, ['precent of population'])
	final_pre.loc[temp.index[0]] = temp.iloc[0]
top_10 = final_pre.nlargest(10, ['precent of population'])
pre_vaccaine = pre_vaccaine.where( pre_vaccaine['location'] in top_10['location'])
print(pre_vaccaine)
'''
fig = plt.figure(figsize=(400,600))
for location in (pre_vaccaine.drop_duplicates(['location']))['location']:
	ax = fig.add_subplot(111)
	plt.plot(pre_vaccaine['date'],pre_vaccaine['total cases'],linewidth=1.0)
	plt.ylabel('Number of cases')
	plt.xticks(rotation = 45, ha = 'right')

plt.show()

fig = plt.figure(figsize=(50, 20))
ax = fig.add_subplot(111)
plt.plot(pre_vaccaine['date'],pre_vaccaine['total cases'],linewidth=1.0, color='r')
plt.ylabel('Number of cases')
plt.xticks(rotation = 45, ha = 'right')
plt.show()'''
