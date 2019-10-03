import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib as plt
plt.style.use('fivethirtyeight')

df=pd.read_csv('C:/Users/annichen/Desktop/TC project/Intel1_beforeTTR_resample_bfill.csv')

temp_value=df['Temp03'].values
minute_value=list(range(len(temp_value)))
df['Minute']=minute_value

#Distinguish hot/warm/off phase
threshold_temp=500.0
normal_threshold_temp=323.0

df['Hot phase']= df['Temp03']> threshold_temp
df['Hot phase']=df['Hot phase']*1
df['Switch to hot phase']=df['Hot phase'].diff()

#Create two data frames
phase_hot=pd.DataFrame(df[df['Switch to hot phase']>0])
phase_N_hot=pd.DataFrame(df[df['Switch to hot phase']<0])

#Insert Start column
phase_hot['Start']=phase_hot.Minute
phase_N_hot['Start']=phase_N_hot.Minute

#Minute array
N_hot_minute=phase_N_hot['Minute'].values
hot_minute=phase_hot['Minute'].values

#reset index
phase_hot=phase_hot.reset_index(drop=True)
phase_N_hot=phase_N_hot.reset_index(drop=True)

#Insert End column
hot_start_time=float(phase_hot.loc[0,['Start']])
N_hot_start_time=float(phase_N_hot.loc[0,['Start']])

if hot_start_time < N_hot_start_time:
    phase_hot['End']=pd.Series(phase_N_hot['Start'])
    phase_N_hot['End']=phase_hot['Start'].shift(-1)
else:
    phase_hot['End']=phase_N_hot['Start'].shift(-1)
    phase_N_hot['End']=pd.Series(phase_hot['Start'])

#Time duration
phase_hot['Duration']=phase_hot['End']-phase_hot['Start']
phase_N_hot['Duration']=phase_N_hot['End']-phase_N_hot['Start']

print(phase_hot)
print("Hot phase duration time info: \n" +str(phase_hot['Duration'].describe()))
phase_hot.to_csv(r'C:/Users/annichen/Desktop/TC project/TTR_3 sensors/intel5/backfill nan data/intel5_woTTR_temp03_hot.csv')

#####################################################################################

df['Warm phase']=(df['Temp03']<threshold_temp) & (df['Temp03']>normal_threshold_temp)
df['Warm phase']=df['Warm phase']*1
df['Switch to warm phase']=df['Warm phase'].diff()

#Create two data frames
phase_warm=pd.DataFrame(df[df['Switch to warm phase']>0])
phase_N_warm=pd.DataFrame(df[df['Switch to warm phase']<0])

#Insert Start column
phase_warm['Start']=phase_warm.Minute
phase_N_warm['Start']=phase_N_warm.Minute

#Minute array
N_warm_minute=phase_N_warm['Minute'].values
warm_minute=phase_warm['Minute'].values

#reset index
phase_warm=phase_warm.reset_index(drop=True)
phase_N_warm=phase_N_warm.reset_index(drop=True)

#Insert End column
warm_start_time=float(phase_warm.loc[0,['Start']])
N_warm_start_time=float(phase_N_warm.loc[0,['Start']])

if warm_start_time < N_warm_start_time:
    phase_warm['End']=pd.Series(phase_N_warm['Start'])
    phase_N_warm['End']=phase_warm['Start'].shift(-1)
else:
    phase_warm['End']=phase_N_warm['Start'].shift(-1)
    phase_N_warm['End']=pd.Series(phase_warm['Start'])

#Time duration
phase_warm['Duration']=phase_warm['End']-phase_warm['Start']
phase_N_warm['Duration']=phase_N_warm['End']-phase_N_warm['Start']

print(phase_warm)
print("Warm phase info: \n" +str(phase_warm['Duration'].describe()))
phase_warm.to_csv(r'C:/Users/annichen/Desktop/TC project/TTR_3 sensors/intel5/backfill nan data/intel5_woTTR_temp03_warm.csv')
######################################################################################

df['Off phase']=(df['Temp03']< 323.0)
df['Off phase']=df['Off phase']*1
df['Switch to off phase']=df['Off phase'].diff()

#Create two data frames
phase_off=pd.DataFrame(df[df['Switch to off phase']>0])
phase_N_off=pd.DataFrame(df[df['Switch to off phase']<0])

#Insert Start column
phase_off['Start']=phase_off.Minute
phase_N_off['Start']=phase_N_off.Minute

#Minute array
N_off_minute=phase_N_off['Minute'].values
off_minute=phase_off['Minute'].values

#reset index
phase_off=phase_off.reset_index(drop=True)
phase_N_off=phase_N_off.reset_index(drop=True)

#Insert End column
off_start_time=float(phase_off.loc[0,['Start']])
N_off_start_time=float(phase_N_off.loc[0,['Start']])

if off_start_time < N_off_start_time:
    phase_off['End']=pd.Series(phase_N_off['Start'])
    phase_N_off['End']=phase_off['Start'].shift(-1)
else:
    phase_off['End']=phase_N_off['Start'].shift(-1)
    phase_N_off['End']=pd.Series(phase_off['Start'])

#Time duration
phase_off['Duration']=phase_off['End']-phase_off['Start']
phase_N_off['Duration']=phase_N_off['End']-phase_N_off['Start']

print(phase_off)
phase_off.to_csv(r'C:/Users/annichen/Desktop/TC project/TTR_3 sensors/intel5/backfill nan data/intel5_woTTR_temp03_off.csv')
print(df)
df.to_csv(r'C:/Users/annichen/Desktop/TC project/TTR_3 sensors/intel5/backfill nan data/intel5_woTTR_temp03_df.csv')
##############################################################################################################