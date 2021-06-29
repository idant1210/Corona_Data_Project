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
vaccained_of_pop = []
ncases_of_pop = []

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
		precent = (int(row['people_fully_vaccinated']) / int(row['population'])*100)
	except ValueError:
		precent= -1
	vaccained_of_pop.append(precent)
	try:
		precent = (int(row['new_cases']) / int(row['population'])*100)
	except ValueError:
		precent = -1
	ncases_of_pop.append(precent)

#######
#Dataset handeling and spliting to pre vaccaine and after vaccaine
#######
updated_df = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population,"precent of population":vaccained_of_pop,"new cases of population":ncases_of_pop})
updated_df = updated_df.fillna(0.0)
updated_df['date'] = pd.to_datetime(updated_df['date'])
updated_df = updated_df[~(updated_df['date'] < '2021-01-01')]
updated_df = updated_df[~(updated_df['date'] > '2021-05-01')]
updated_df = updated_df[updated_df['location'] != 'Gibraltar']
updated_df = updated_df[updated_df['location'] != 'Falkland Islands']
updated_df = updated_df[updated_df['location'] != 'Saint Helena']
updated_df = updated_df[updated_df['precent of population'] != -1]
updated_df = updated_df[updated_df['new cases of population'] != -1]

top_8_vac = updated_df.drop_duplicates('location',keep='last').nlargest(8, ['precent of population'])
top_8_total = updated_df.where(updated_df['location'].isin(top_8_vac['location'])).dropna()
fig, axs = plt.subplots(2)
fig.suptitle('Corona Virus vaccine effects in top 8 countrys')

i = 0
axs[0].set_title("Precent of vaccained out of total population")
axs[1].set_title("Precent of new cases out of total population")
for location in (top_8_vac['location']):
	axs[0].plot(top_8_total['date'].where(top_8_total['location'] == location).dropna() ,top_8_total['precent of population'].where(top_8_total['location'] == location).dropna(),linewidth=2.0,label = location , linestyle = "-")
	i = i+1
i = 0
for location in (top_8_vac['location']):
	axs[1].plot(top_8_total['date'].where(top_8_total['location'] == location).dropna() ,top_8_total['new cases of population'].where(top_8_total['location'] == location).dropna(),linewidth=2.0,label = location , linestyle = "-")
	i = i+1
axs[0].legend()
axs[1].legend()
plt.show()
