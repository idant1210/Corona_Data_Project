  
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


def plot_frequent_elements(df, df_in_params):
    i=0
    fig, axes= plt.subplots(1, 3, figsize=(20,5)) 
    for indexs in df_in_params.index :
        
        sr = get_frequent_elements(df , df_in_params["col_name"][indexs], df_in_params["num_top_elements"][indexs])
        one_dim_plot(sr , df_in_params ["plot_type"][indexs] , axes[i])
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
