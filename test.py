  
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt      
import math
import seaborn as sns
from collections import Counter
from sklearn.decomposition import PCA
from datetime import datetime
from dateutil.relativedelta import relativedelta

date = []
new_cases = []
total_cases = []
new_vaccined = []
total_vaccined = []
population = []
location = []
sick_of_pop = []

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
#######
#Dataset handeling and spliting to pre vaccaine and after vaccaine
#######
#pre_vaccaine = pd.DataFrame(pre_vaccaine.loc[pre_vaccaine['new vaccined'] < 1])
updated_df = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population,"precent of population":sick_of_pop})
updated_df = updated_df.fillna(0.0)
updated_df['date'] = pd.to_datetime(updated_df['date'])
updated_df = updated_df[~(updated_df['date'] < '2021-01-01')]
pre_vaccaine = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] < 1])
pre_vaccaine = pre_vaccaine.reset_index(drop=True)
final_pre = pre_vaccaine.copy()[0:0]
final_vaccained = pre_vaccaine.copy()[0:0]
for location in pre_vaccaine.copy().drop_duplicates(['location'])['location']:
	temp = pre_vaccaine.where(pre_vaccaine['location']==location).dropna().nlargest(1, ['precent of population'])
	final_pre.loc[temp.index[0]] = temp.iloc[0]
top_10_pre = final_pre.nlargest(8, ['precent of population'])
pre = pre_vaccaine.loc[pre_vaccaine['location'].isin(top_10_pre['location'])]
vaccained = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] > 0])
vaccained = vaccained.loc[vaccained['location'].isin(top_10_pre['location'])]

fig, axs = plt.subplots(2)
fig.suptitle('Corona Virus vaccine effects in top 10 countrys')
plt.ylabel('Infected of population by %')
plt.xticks(rotation = 45, ha = 'right')
i = 0
axs[0].set_title("Pre Vaccaine")
axs[1].set_title("Vaccaine")
for location in (pre.drop_duplicates(['location']))['location']:
	axs[0].plot(pre['date'].where(pre['location'] == location) ,pre['precent of population'].where(pre['location'] == location),linewidth=2.0,label = location , linestyle = "-.")
	i = i+1

i = 0
for location in (vaccained.drop_duplicates(['location']))['location']:
	axs[1].plot(vaccained['date'].where(vaccained['location'] == location) ,vaccained['precent of population'].where(vaccained['location'] == location),linewidth=2.0,label = location , linestyle = "-.")
	i = i+1
axs[0].legend()
axs[1].legend()

figure,ax = plt.subplots(8)
figure.suptitle('Corona Virus vaccine effects in top 10 countrys')
plt.ylabel('Infected of population by %')
plt.xticks(rotation = 45, ha = 'right')
i=0
for location in (vaccained.drop_duplicates(['location']))['location']:
	ax[i].set_title(location)
	ax[i].plot(pre['date'].where(pre['location'] == location), pre['precent of population'].where(pre['location'] == location),linewidth=2.0,label = "Pre Veccaine" , linestyle = "-.")
	ax[i].plot(vaccained['date'].where(vaccained['location'] == location), vaccained['precent of population'].where(vaccained['location'] == location),linewidth=2.0,label = "Veccained" , linestyle = "-.")
	ax[i].legend()
	i=i+1
plt.show()
