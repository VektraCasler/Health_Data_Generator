#%%
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

#%%
myDF = pd.read_csv('OUTPUT/person_list.csv')
myDF.head()

ages = myDF['AGE']
age_cats = [0] * 25

for x in ages:
    age_cats[(x // 5)] += 1

ages_male = myDF[myDF['SEX'] == 'Male']
ages_male = ages_male['AGE']
age_cats_male = [0] * 25

for x in ages_male:
    age_cats_male[(x // 5)] += 1

ages_female = myDF[myDF['SEX'] == 'Female']
ages_female = ages_female['AGE']
age_cats_female = [0] * 25

for x in ages_female:
    age_cats_female[(x // 5)] += 1

with open('OUTPUT/my_data_ages.csv', 'w') as file_output:

    file_output.write('AGE,BOTH,MALE,FEMALE\n')

    for x in range(20):
        string_out = '{},{},{},{}\n'.format((x*5), age_cats[x], age_cats_male[x], age_cats_female[x])
        file_output.write(string_out)

# %%
censusDF = pd.read_csv('miscellaneous/2010_census_ages.csv')
mydataDF = pd.read_csv('OUTPUT/my_data_ages.csv')

# %%
my_index = censusDF['AGE']

plt.bar(x=censusDF['AGE'], height=censusDF['BOTH'], width=4, align='center', color='khaki')
plt.bar(x=censusDF['AGE'], height=censusDF['FEMALE'], width=2, align='edge', color='pink')
plt.bar(x=censusDF['AGE'], height=censusDF['MALE'], width=-2, align='edge', color='lightsteelblue')
plt.savefig('OUTPUT/age_graph_census.png')

# %%
my_index = mydataDF['AGE']

plt.bar(x=mydataDF['AGE'], height=mydataDF['BOTH'], width=4, align='center', color='khaki')
plt.bar(x=mydataDF['AGE'], height=mydataDF['FEMALE'], width=2, align='edge', color='pink')
plt.bar(x=mydataDF['AGE'], height=mydataDF['MALE'], width=-2, align='edge', color='lightsteelblue')
plt.savefig('OUTPUT/age_graph_mydata.png')

# %%
import folium
map = folium.Map(location=[38, -95],zoom_start=4)
map

# %%
