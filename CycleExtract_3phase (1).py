import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib as plt
plt.style.use('fivethirtyeight')

df=pd.read_csv('C:/Users/annichen/Desktop/TC project/Gutter Temp performance comparation with TTR/intel5_noTTR_0619_resample.csv')

temp_value=df['Temp1'].values
minute_value=list(range(len(temp_value)))
df['Minute']=minute_value

del df['Temp2']
#Distinguish hot/warm/off phase
threshold_temp=500.0
normal_threshold_temp=343.0

above_hot_threshold=temp_value>threshold_temp
df['Hot phase']=above_hot_threshold*1
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
phase_hot.to_csv(r'C:/Users/annichen/Desktop/TC project/Gutter Temp performance comparation with TTR/intel5_noTTR_0619_temp1_hot.csv')
#####################################################################################

df['Warm phase']=(df['Temp1']<threshold_temp) & (df['Temp1']>normal_threshold_temp)
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
phase_warm.to_csv(r'C:/Users/annichen/Desktop/TC project/Gutter Temp performance comparation with TTR/intel5_noTTR_0619_temp1_warm.csv')
######################################################################################

df['Off phase']=(df['Temp1']< 343.0)
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
phase_off.to_csv(r'C:/Users/annichen/Desktop/TC project/Gutter Temp performance comparation with TTR/intel5_noTTR_0619_temp1_off.csv')
print(df)
df.to_csv(r'C:/Users/annichen/Desktop/TC project/Gutter Temp performance comparation with TTR/intel5_noTTR_0619_temp1_df.csv')
#####################################################################################

#Duration in each phase
from pandas import Series
a=phase_hot['Duration']
b=phase_warm['Duration']
c=phase_off['Duration']
a=Series(a)
b=Series(b)
C=Series(c)
#Hot/Warm TC median
print(a.value_counts().head())
print(b.value_counts().head())

#plot-OVERALL performance in Duration vs TC counts
bins=np.linspace(0,1000,1000)
pyplot.hist(a,bins,alpha=0.6,label='Hot Phase Duration Time',color='#ff6666')
pyplot.hist(b,bins,alpha=0.6,label='Warm Phase Duration Time',color='#ffcc99')
pyplot.hist(c,bins,alpha=0.6,label='Off Phase Duration Time',color='#66b3ff')
pyplot.title('Duration Time in each phase(minute) vs Counts of each Thermal Cycling')
pyplot.xlabel('Time Duration(Min)')
pyplot.ylabel('Thermal Cycle Counts')
pyplot.legend(loc='upper right')
pyplot.xlim(0,1000)
pyplot.ylim(0,30)
pyplot.show()

#plot- hot phase TC duration vs TC count

import matplotlib.pyplot as plt
import numpy as np
fig=plt.figure()
ax1=fig.add_subplot(3,1,1)
bins_hot=np.arange(0, max(a)+20,20.0)
n_hot,edgeBin_hot,patches_hot=plt.hist(a,bins=bins_hot,color='#ff6666',alpha=0.5)
plt.xticks(bins_hot)
y_hot=np.array(list(n_hot))
for g,f in zip(bins_hot,y_hot):
    plt.text(g+9, f, str(int(f)), ha = 'center', va = 'bottom',color='#ff6666')

plt.title("Thermal Cycle in Hot Phase per time",fontsize=12)
pyplot.ylabel('Thermal Cycle(Counts)',fontsize=12)

#plot-warm phase TC duration vs TC count
ax2=fig.add_subplot(3,1,2)
bins_warm=np.arange(0, max(b)+100,100)
n_warm,edgeBin_warm,patches_warm=plt.hist(b,bins=bins_warm,color='#ffcc99',alpha=0.5)
y_warm=np.array(list(n_warm))
for g,f in zip(bins_warm,y_warm):
    plt.text(g+60, f, str(int(f)), ha = 'center', va = 'bottom',color='#ffcc99')
plt.title("Thermal Cycle in Warm Phase per time",fontsize=12)
plt.xticks(bins_warm)
pyplot.ylabel('Thermal Cycle Counts',fontsize=12)

#plot-off phase TC duration vs TC count
ax3=fig.add_subplot(3,1,3)
bins_off=np.arange(0, max(c)+200, 200.0)
n_off,edgeBin_off,patches_off=plt.hist(c,bins=bins_off,color='#66b3ff',alpha=0.5)
y_off=np.array(list(n_off))
for g,f in zip(bins_off,y_off):
    plt.text(g+50, f, str(int(f)), ha = 'center', va = 'bottom',color='#66b3ff')
plt.title("Thermal Cycle in Off Phase per time",fontsize=12)
plt.xticks(bins_off)
pyplot.xlabel('Time Duration(Min)')
pyplot.ylabel('Thermal Cycle Counts',fontsize=12)

pyplot.show()

#plot- time duration vs TC count with KDE(PDF)
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(13,10),dpi=80)
sns.distplot(a, hist=True, kde=True, bins=int(600/5),kde_kws={'linewidth': 4})
sns.distplot(b, hist=True, kde=True, bins=int(100/5),color='red',kde_kws={'linewidth': 4})
plt.xlim(0,600)
plt.ylim(0,0.045)
plt.title('Probability density plot of thermal cycle in hot/warm phases')
plt.legend()
plt.show()

#plot-duration vs TC count with KDE(PDF)in each phase
sns.distplot(a, hist=True, kde=True, bins=int(600/5),kde_kws={'linewidth': 4})
plt.xlabel('Hot Phase Time Duration(Min)')
plt.ylabel('Density')
plt.show()

sns.distplot(b, hist=True, kde=True, bins=int(100/5),color='red',kde_kws={'linewidth': 4})
plt.xlabel('Warm Phase Time Duration(Min)')
plt.ylabel('Density')
plt.xlim(0,600)
plt.show()

#Time to Get Donut
Hot_count=phase_hot['Duration'].count()
Warm_count=phase_warm['Duration'].count()
Off_count=phase_off['Duration'].count()
Hot_sum_duration_time=phase_hot['Duration'].sum()
Warm_sum_duration_time=phase_warm['Duration'].sum()
Off_sum_duration_time=phase_off['Duration'].sum()
print("The counts of thermal cycling in each phases: \n in hot:"+ str(Hot_count)+" in warm:" +str(Warm_count)+" in off:"+ str(Off_count)+".")
print("The sum of duration time of thermal cycling in each phases: \n in hot:"+ str(Hot_sum_duration_time)+" in warm:" +str(Warm_sum_duration_time)+" in off:"+ str(Off_sum_duration_time)+".")
#Donut chart in the probability percentile with 3phase in counts (counts)
fig=plt.figure()
ax1=fig.add_subplot(2,1,1)
labels=['Hot','Warm','Off']
sizes=[Hot_count,Warm_count,Off_count]
colors=['#ff6666', '#ffcc99', '#66b3ff']
my_circle=plt.Circle((0,0), 0.7, color='white')
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title("Thermal cycle of each phases by counts")
p1=plt.gcf()
p1.gca().add_artist(my_circle)
p1.patch.set_facecolor('white')

#Donut chart in the probability percentile with 3phase in duration time (sum(duration time ))
ax2=fig.add_subplot(2,1,2)
labels=['Hot','Warm','Off']
sizes=[Hot_sum_duration_time,Warm_sum_duration_time,Off_sum_duration_time]
colors=['#ff6666', '#ffcc99', '#66b3ff']
my_circle=plt.Circle((0,0), 0.7, color='white')
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title("Thermal cycle of each phases in minute")
p2=plt.gcf()
p2.gca().add_artist(my_circle)
p2.patch.set_facecolor('white')
plt.show()

#Donut chart in the probability percentile in hot phase
import matplotlib as mpl
mpl.rcParams['font.size'] = 7.0

phase_hot[['Duration']]=phase_hot[['Duration']].astype(float)
labels_hot = ['[0-15]','[15-30]','[30-45]','[45-60]','[60-75]', '[75-90]', '[90-105]', '[105-120]', '[120-135]',
               '[135-150]' , '[150-165]', '[165-180]', '[180-195]', '[195-210]', '[210-225]', '[225+]']
sizes_hot = [len(phase_hot[(phase_hot.Duration >=0) & (phase_hot.Duration <15)]),
             len(phase_hot[(phase_hot.Duration >=15) & (phase_hot.Duration <30)]),
             len(phase_hot[(phase_hot.Duration >=30) & (phase_hot.Duration <45)]),
             len(phase_hot[(phase_hot.Duration >=45) & (phase_hot.Duration <60)]),
             len(phase_hot[(phase_hot.Duration >=60) & (phase_hot.Duration <75)]),
             len(phase_hot[(phase_hot.Duration >=75) & (phase_hot.Duration <90)]),
             len(phase_hot[(phase_hot.Duration >=90) & (phase_hot.Duration <105)]),
             len(phase_hot[(phase_hot.Duration >=105) & (phase_hot.Duration <120)]),
             len(phase_hot[(phase_hot.Duration >=120) & (phase_hot.Duration <135)]),
             len(phase_hot[(phase_hot.Duration >=135) & (phase_hot.Duration <150)]),
             len(phase_hot[(phase_hot.Duration >=150) & (phase_hot.Duration <165)]),
             len(phase_hot[(phase_hot.Duration >=165) & (phase_hot.Duration <180)]),
             len(phase_hot[(phase_hot.Duration >=180) & (phase_hot.Duration <195)]),
             len(phase_hot[(phase_hot.Duration >=195) & (phase_hot.Duration <210)]),
             len(phase_hot[(phase_hot.Duration >=210) & (phase_hot.Duration <225)]),
             len(phase_hot[(phase_hot.Duration >=225) & (phase_hot.Duration <1000)])
             ]
colors_hot=['#7a0000','#8d0000','#a10000','#b40000','#c80000','#dc0000','#ef0000','#ff0404','#ff2b2b','#ff3f3f',
            '#ff5252','#ff6666','#ff7a7a','#ff8d8d','#ffb4b4','#ffb4b4']

hot_zip=zip(labels_hot,sizes_hot,colors_hot)
hot_zip=[t for t in hot_zip if 0 not in t]
labels_hot,sizes_hot,colors_hot=zip(*hot_zip)

hot= plt.pie(sizes_hot, labels=labels_hot,
             colors=colors_hot,radius=0.9,
             startangle=0, labeldistance=1.05,
             pctdistance=0.7,autopct='%1.1f%%')

centre_circle = plt.Circle((0, 0), 0.7, color='white', linewidth=0)
plt.title("Thermal cycle performance in Hot phase")

fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.patch.set_facecolor('white')
plt.axis('equal')
plt.tight_layout()
plt.show()
#Donut chart in the probability percentile in warm phase

phase_warm[['Duration']]=phase_warm[['Duration']].astype(float)
labels_warm= ['[0-100]','[100-200]','[200-300]','[300-400]','[500-600]','[600-700]','[700-800]','[800-900]',\
              '[900-1000]','[1000-1100]','[1100-1200]','[1200-1300]','[1300+]']
sizes_warm= [len(phase_warm[(phase_warm.Duration >=0) & (phase_warm.Duration <100)]),
             len(phase_warm[(phase_warm.Duration >=100) & (phase_warm.Duration <200)]),
             len(phase_warm[(phase_warm.Duration >=200) & (phase_warm.Duration <300)]),
             len(phase_warm[(phase_warm.Duration >=300) & (phase_warm.Duration <400)]),
             len(phase_warm[(phase_warm.Duration >=400) & (phase_warm.Duration <500)]),
             len(phase_warm[(phase_warm.Duration >=500) & (phase_warm.Duration <600)]),
             len(phase_warm[(phase_warm.Duration >=600) & (phase_warm.Duration <700)]),
             len(phase_warm[(phase_warm.Duration >=700) & (phase_warm.Duration <800)]),
             len(phase_warm[(phase_warm.Duration >=800) & (phase_warm.Duration <900)]),
             len(phase_warm[(phase_warm.Duration >=900) & (phase_warm.Duration <1000)]),
             len(phase_warm[(phase_warm.Duration >=1000) & (phase_warm.Duration <1100)]),
             len(phase_warm[(phase_warm.Duration >=1100) & (phase_warm.Duration <1200)]),
             len(phase_warm[(phase_warm.Duration >=1200) & (phase_warm.Duration <1300)]),
             len(phase_warm[(phase_warm.Duration >=1300) & (phase_warm.Duration <50000)])
             ]
colors_warm=['#fb7e00','#ffcc99','#ffc285','#ffe0c0','#ffb872','#ffaf5e','#ffa54b','#ff9b37','#ff9123','#ff8710',\
             '#e77400','#d46a00','#c06000']

warm_zip=zip(labels_warm,sizes_warm,colors_warm)
warm_zip=[t for t in warm_zip if 0 not in t]
labels_warm,sizes_warm,colors_warm=zip(*warm_zip)

warm = plt.pie(sizes_warm, labels=labels_warm,
               colors=colors_warm, radius=0.9,
               startangle=0, labeldistance=1.05,
               pctdistance=0.7,autopct='%1.1f%%')

centre_circle = plt.Circle((0, 0), 0.7, color='white', linewidth=0)
plt.title("Thermal cycle performance in Warm phase")
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.patch.set_facecolor('white')
plt.axis('equal')
plt.tight_layout()
plt.show()

#Donut chart in the probability percentile in off phase
phase_off[['Duration']]=phase_off[['Duration']].astype(float)
labels_off= ['[0-200]','[200-400]','[400-600]','[600-800]','[800-1000]','[1000-1200]','[1200-1400]','[1400-1600]',
              '[1600-1800]','[1800-2000]','[2000-2200]','[2200-2400]','[2400-2600]','[2600-2800]','[2800-3000]',
              '[3000-3200]','[3200-3400]', '[3400-3600]', '[3600-3800]', '[3800-4000]', '[4000-4200]', '[4200-4400]',
              '[4400-4600]','[4600-4800]', '[4800-5000]', '[5000-5200]', '[5200-5400]', '[5400-5600]', '[5600+]']
sizes_off= [ len(phase_off[(phase_off.Duration >=0) & (phase_off.Duration <200)]),
             len(phase_off[(phase_off.Duration >=200) & (phase_off.Duration <400)]),
             len(phase_off[(phase_off.Duration >=400) & (phase_off.Duration <600)]),
             len(phase_off[(phase_off.Duration >=600) & (phase_off.Duration <800)]),
             len(phase_off[(phase_off.Duration >=800) & (phase_off.Duration <1000)]),
             len(phase_off[(phase_off.Duration >=1000) & (phase_off.Duration <1200)]),
             len(phase_off[(phase_off.Duration >=1200) & (phase_off.Duration <1400)]),
             len(phase_off[(phase_off.Duration >=1400) & (phase_off.Duration <1600)]),
             len(phase_off[(phase_off.Duration >=1600) & (phase_off.Duration <1800)]),
             len(phase_off[(phase_off.Duration >=1800) & (phase_off.Duration <2000)]),
             len(phase_off[(phase_off.Duration >=2000) & (phase_off.Duration <2200)]),
             len(phase_off[(phase_off.Duration >=2200) & (phase_off.Duration <2400)]),
             len(phase_off[(phase_off.Duration >=2400) & (phase_off.Duration <2600)]),
             len(phase_off[(phase_off.Duration >=2600) & (phase_off.Duration <2800)]),
             len(phase_off[(phase_off.Duration >=2800) & (phase_off.Duration <3000)]),
             len(phase_off[(phase_off.Duration >=3000) & (phase_off.Duration <3200)]),
             len(phase_off[(phase_off.Duration >=3200) & (phase_off.Duration <3400)]),
             len(phase_off[(phase_off.Duration >=3400) & (phase_off.Duration <3600)]),
             len(phase_off[(phase_off.Duration >=3600) & (phase_off.Duration <3800)]),
             len(phase_off[(phase_off.Duration >=3800) & (phase_off.Duration <4000)]),
             len(phase_off[(phase_off.Duration >=4000) & (phase_off.Duration <4200)]),
             len(phase_off[(phase_off.Duration >=4200) & (phase_off.Duration <4400)]),
             len(phase_off[(phase_off.Duration >=4400) & (phase_off.Duration <4600)]),
             len(phase_off[(phase_off.Duration >=4600) & (phase_off.Duration <4800)]),
             len(phase_off[(phase_off.Duration >=4800) & (phase_off.Duration <5000)]),
             len(phase_off[(phase_off.Duration >=5000) & (phase_off.Duration <5200)]),
             len(phase_off[(phase_off.Duration >=5200) & (phase_off.Duration <5400)]),
             len(phase_off[(phase_off.Duration >=5400) & (phase_off.Duration <5600)]),
             len(phase_off[(phase_off.Duration >=5600) & (phase_off.Duration <100000000000)])]
colors_off=['#dcedff','#c8e4ff','#b4daff','#a1d0ff','#8dc6ff','#7abdff','#66b3ff','#52a9ff','#3fa0ff','#2b96ff',\
            '#188cff','#0482ff','#0078ef','#006fdc','#0065c8','#005bb4','#0051a1','#00478d','#003d7a','#003366',\
            '#002952','#00203f','#1ac6ff','#33ccff','#4dd3ff','#66d9ff','#80dfff','#99e6ff','#66ffd9']

off_zip=zip(labels_off,sizes_off,colors_off)
off_zip=[t for t in off_zip if 0 not in t]
labels_off,sizes_off,colors_off=zip(*off_zip)

off = plt.pie(sizes_off,radius=0.9,colors=colors_off,
              startangle=0, labeldistance=1.05,labels=labels_off,
              pctdistance=0.7,autopct='%1.1f%%')

centre_circle = plt.Circle((0, 0), 0.7, color='white', linewidth=0)
plt.title("Thermal cycle performance in Off phase")
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.patch.set_facecolor('white')
plt.axis('equal')
plt.tight_layout()
plt.show()

#do the pass/fail percentage comparation with the ideally condition
#need default ideal condition to do binary classification

#distribution, get the line plot number
#can do KDE on TSMC6/7? and plot together on the same chart

#compare with diff temp sensors- see the each distribution

#think about why the TC extraction is important? can bring what assistance to the team
#the value of my work: creative, technical, valuable to team






