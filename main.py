import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt      
import math
import seaborn as sns
from collections import Counter
from sklearn.decomposition import PCA


sampled_coutrys = ["Israel","United States","United Kindom"]
date = []
new_cases = []
total_cases = []
new_vaccined = []
total_vaccined = []
population = []
location = []

complete_dataset = pd.read_csv("owid-covid-data.csv")

for index,row in complete_dataset.iterrows():
	if row['location'] in sampled_coutrys:
		date.append(row['date'])
		new_cases.append(row['new_cases'])
		total_cases.append(row['total_cases'])
		new_vaccined.append(row['new_vaccinations'])
		total_vaccined.append(row['people_fully_vaccinated'])
		location.append(row['location'])
		population.append(row['population'])
updated_df = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population})
updated_df = updated_df.fillna(0)
pre_veccaine = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] < 1])
vaccained = pd.DataFrame(updated_df.loc[updated_df['total vaccined'] > 0])
usa_pre_df = pd.DataFrame(pre_veccaine.loc[pre_veccaine['location']=="United States"])
usa_pre_df.drop_duplicates()
usa_pre_df.to_csv("test")
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111)
ax.plot(pre_veccaine['date'],pre_veccaine['total cases'].where(pre_veccaine['location']=="Israel"),color='lightblue', linewidth=2)
ax.plot(usa_pre_df['date'],usa_pre_df['total cases'],color='red', linewidth=2)
plt.show()

