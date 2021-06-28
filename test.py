  
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

#colors = ["#FF0000","#33FF00","#3300FF","#A200FF","#F7FF00","#00FFFF","#FF009A","#00E3FC","#6500FC","#F0658B"]
def one_dim_plot(sr, plot_type, axis, color):
    sr.plot (kind =plot_type ,ax=axis, color = color)


def plot_frequent_elements(df, df_in_params):
    i=0
    fig, axes= plt.subplots(1, 3, figsize=(20,5))
    for indexs in df_in_params.index :
        sr = get_frequent_elements(df , df_in_params["col_name"][indexs], df_in_params["num_top_elements"][indexs])
        one_dim_plot(sr , df_in_params ["plot_type"][indexs] , axes[i] , color[i])
        i = i+1

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
top_10 = final_pre.nlargest(8, ['precent of population'])
pre = pre_vaccaine.loc[pre_vaccaine['location'].isin(top_10['location'])]
vaccained = vaccained.loc[vaccained['location'].isin(top_10['location'])]
colors = ["#e74c3c", "#2ecc71", "#3498db" , "#e04c0c", "#02c701", "#30480b" , "#e00c3c", "#2ec001", "#3008db" , "#004c3c", "#2ecc00", "#34900db"]
fig = plt.figure(figsize=(20,5))
i=0
ax = fig.add_subplot(111)
plt.ylabel('Sick our of population by %')
plt.xticks(rotation = 45, ha = 'right')
for location in (pre.drop_duplicates(['location']))['location']:
	plt.plot(pre['date'].where(pre['location'] == location) ,pre['precent of population'].where(pre['location'] == location),linewidth=2.0,label = location , linestyle = "-.")
	i = i+1
plt.legend()
plt.show()

fig = plt.figure(figsize=(20,5))
i=0
ax = fig.add_subplot(111)
plt.ylabel('Sick our of population by %')
plt.xticks(rotation = 45, ha = 'right')
for location in (pre.drop_duplicates(['location']))['location']:
	plt.plot(pre['date'].where(pre['location'] == location) ,pre['precent of population'].where(pre['location'] == location),linewidth=2.0,label = location , linestyle = "-.")
	i = i+1
plt.legend()
plt.show()
