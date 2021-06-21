import pandas as pd
import os

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
updated_dataframe = pd.DataFrame({"location": location,"date":date,"new cases":new_cases,"total cases":total_cases,"new vaccined":new_vaccined,"total vaccined":total_vaccined,"population":population})
