import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/ucl.csv', encoding='latin-1')
# print(df)

df = df.drop(['Rk'], axis=1)
print(df)

# df converted to series
df.info()
df = df.fillna(0)
# Number of missing values in current datadrame
#print(df.isnull().sum())

# print(df)
print("Squad -- Player's Club\nGls -- Goals\nsh -- Shots Total\nSot -- Shots On Target\nSot% -- Shots On Target Percentage\nSh/90 -- Shots total per 90 minutes\nSot/90 -- Shots On target per 90 minutes\nG/Sh -- Goals Per Shot\nG/Sot -- Goals Per Shot On Target\nDist -- Average distance,in yards, from goal of all shots taken\nFK - Shots from free kicks\nPK -- Penalty Kicks Made\nPKatt -- Penalty Kicks Attempted\nxG -- Expected Goals\nnpxG -- Non-Penalty Expected Goals\nnpxG/Sh -- Non-Penalty Expected Goals per shot\nG-xG -- Goals minus Expected Goals\nnp:G-xG -- Non-Penalty Goals minus Non-Penalty Expected Goals")

# Sample the highest goal scorers
high_Goals = df[df['Gls'] == df['Gls'].max()]
print(high_Goals)

#Players With Atleast One Goal In Group stage
Players_With_Atleast_OneGoal = df[df["Gls"]>1][["Player","Gls"]]
fig, ax = plt.subplots(figsize=(20, 10))
ax.scatter(Players_With_Atleast_OneGoal.Player, Players_With_Atleast_OneGoal.Gls, color='red')
#ax.set_facecolor('black')
ax.set_title("Goals in G/S of UEFA UCL 2020-21", fontsize=40)
ax.set_xlabel("Players", fontsize=30)
ax.set_ylabel("Number Of Goals", fontsize=25)
ax.tick_params(labelrotation=90)
plt.show()

# Sample players with > than 10 shots
shots= df[df["Sh"]>10][["Player","Sh"]]
print(shots)

shots.sort_values(by=['Sh'], inplace=True, ascending=False)
print(shots)


# with markerline deriving from plt.stem
plt.figure(figsize=(20, 10))
plt.stem(shots.Player, shots.Sh)
plt.ylim(0, 30)
plt.xticks(shots.Player,rotation='vertical')
plt.stem(shots.Sh)
(markerline, stemlines, baseline) = plt.stem(shots.Player, shots.Sh)
plt.setp(baseline, visible=False)
plt.xlabel('Players', fontsize=25)
plt.ylabel('Shots', fontsize=25)
plt.title('Highest Number Of Shots In G/S (UEFA UCL 2020-21)', fontsize=20)
plt.show()


# individual Player Stats using the Radar Chart
label = np.array(['Gls', 'Sh', 'SoT', 'Sh/90', 'SoT/90', 'G/Sh','G/SoT'])
stats = df.loc[456,label].values
angles = np.linspace(0, 2*np.pi, len(label), endpoint=False)
# stats = np.concatenate((stats,[stats[0]]))
# angles = np.concatenate((angles,[angles[0]]))
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, 'o--', linewidth= 2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, label)
ax.set_title([df.loc[456,'Player']])
ax.grid(True)
plt.show()


label = np.array(['xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG'])
stats = df.loc[456,label].values
angles = np.linspace(0, 2*np.pi, len(label), endpoint=False)
# stats = np.concatenate((stats,[stats[0]]))
# angles = np.concatenate((angles,[angles[0]]))
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, '.--', linewidth= 2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, label)
ax.set_title([df.loc[456,'Player']])
ax.grid(True)
plt.show()


label = np.array(['Gls', 'Sh', 'SoT', 'Sh/90', 'SoT/90', 'G/Sh','G/SoT'])
stats = df.loc[417,label].values
angles = np.linspace(0, 2*np.pi, len(label), endpoint=False)
# stats = np.concatenate((stats,[stats[0]]))
# angles = np.concatenate((angles,[angles[0]]))
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, 'o--', linewidth= 2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, label)
ax.set_title([df.loc[417,'Player']])
ax.grid(True)
plt.show()