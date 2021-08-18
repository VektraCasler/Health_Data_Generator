#%%
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

#%%
myDF = pd.read_csv('OUTPUT/data_verification.csv')
print(myDF.head())

#%%
myDF['AGE'].hist(bins=20)

# %%
censusDF = pd.read_csv('miscellaneous/2010_census_ages.csv')
print(censusDF.head())

# %%
my_index = censusDF['AGE']
ax1 = censusDF['BOTH'].plot.bar()
ax2 = censusDF['MALE'].plot.bar()
ax3 = censusDF['FEMALE'].plot.bar()

# %%
sns.histplot(data=myDF['AGE'])

# %%
ax = sns.barplot(data=censusDF['BOTH'])
# %%
plt.bar(x=censusDF['AGE'], height=censusDF['BOTH'], width=4, align='center', color='khaki')
plt.bar(x=censusDF['AGE'], height=censusDF['FEMALE'], width=2, align='edge', color='pink')
plt.bar(x=censusDF['AGE'], height=censusDF['MALE'], width=-2, align='edge', color='lightsteelblue')
matplotlib.axes.Axes()

# %%
