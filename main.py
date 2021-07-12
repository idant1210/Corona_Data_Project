import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt      
import math
import seaborn as sns
from collections import Counter
import sklearn
from sklearn import preprocessing, linear_model, model_selection
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from dateutil.relativedelta import relativedelta


plt.rcParams.update({'figure.max_open_warning': 0})

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
new_df = (updated_df.where(updated_df['total vaccined'] != 0)).dropna()
day_count = pd.DataFrame({"location": new_df['location'],"day count": int(0),"new cases":new_df['new cases'],"total cases":new_df['total cases'],"new vaccined":new_df['new vaccined'],"total vaccined":new_df['total vaccined'],"population":new_df['population'],"precent of population":new_df['precent of population'],"new cases of population":new_df['new cases of population']})
for location in day_count['location'].drop_duplicates():
	i=1
	for index, row in (day_count.where(day_count['location']==location).dropna()).iterrows():
		day_count.at[index,['day count']] = i
		i = i+1
i=0
'''
for location in day_count.drop_duplicates('location')['location']:
	fig, axs = plt.subplots(2)
	axs[0].plot(day_count['day count'].where(day_count['location'] == location).dropna() ,day_count['precent of population'].where(day_count['location'] == location).dropna(),linewidth=2.0,label = location , linestyle = "-", color = "#FF0000")
	axs[1].plot(day_count['day count'].where(day_count['location'] == location).dropna() ,day_count['new cases of population'].where(day_count['location'] == location).dropna(),linewidth=2.0,label = location , linestyle = "-", color = "#4400FF")
	axs[0].legend()
	axs[1].legend()
	fig.savefig('./countrys/'+location+'.png', bbox_inches='tight')
'''
######
#Mechine learning
######

