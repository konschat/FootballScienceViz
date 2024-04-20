import pandas as pd
import numpy as np
from math import pi
import matplotlib.pyplot as plt
#%matplotlib inline

def createRadar(team, data, Scenario):
    print('the data', data.loc[:, Scenario].values[0])
    data = data.loc[:, Scenario].values[0].tolist()

    print('Scenario ', type(Scenario), Scenario)
    num_categories = len(Scenario)

    # Calculate angle values for each category
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
    angles += angles[:1]
    data += data[:1]

    # Create the radar plot
    plt.figure(figsize=(6, 6))
    plt.polar(angles, data, marker='o')
    plt.fill(angles, data, 'b', alpha=0.1)
    plt.xticks(angles[:-1], Scenario)
    plt.title(team)
    plt.show()

def createRadar2(data1, data2, team_home, team_against, Scenario):
    # Number of categories
    num_categories = len(Scenario)
    data1 = data1.loc[:, Scenario].values[0].tolist()
    data2 = data2.loc[:, Scenario].values[0].tolist()

    # Calculate angle values for each category
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
    angles += angles[:1]
    data1 += data1[:1]
    data2 += data2[:1]

    # Create the subplots for two radar plots side by side
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), subplot_kw={'polar': True})

    # Plot the first radar plot
    ax.plot(angles, data1, marker='o', label=team_home)
    ax.fill(angles, data1, 'b', alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(Scenario)
    ax.set_title(team_home)
    ax.legend()

    # Plot the second radar plot
    ax.plot(angles, data2, marker='o', label=team_against)
    ax.fill(angles, data2, 'r', alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(Scenario)
    ax.set_title(team_against)
    ax.legend()

    # Adjust spacing between subplots
    plt.tight_layout()
    # Show the radar plots
    plt.show()

def team_aggregation():

    katikati = 0

    return katikati

dataset = pd.read_csv('data/Advanced.csv')
print(dataset.head(100))
print(dataset.shape)

nan_count = dataset.isna().sum().sum()
null_count = dataset.isnull().sum().sum()
total_missing = nan_count + null_count
print('Number of null values:', null_count)
print('Number of missing values:', total_missing)

# Against --> Our team
# Oppose --> Opponent
columns_list = list(dataset.columns)
teams = set(list(dataset.Team))
seasons = set(list(dataset['Season']))

# Scenarios here #
Attacking = ['goals', 'xG', 'xA', 'xGChain', 'xGBuildup'] # 'shots', 'key_passes'
Defending = ['goals_Against', 'xG_Against', 'xA_Against', 'xGChain_Against', 'xGBuildup_Against'] # 'shots_Against', 'key_passes_Against',
AttPossesion = ['key_passes', 'xA', 'xGChain', 'xGBuildup']
DfPossesion = ['key_passes_Against', 'xA_Against', 'xGChain_Against', 'xGBuildup_Against']
Possesion = ['key_passes', 'key_passes_Against', 'xA', 'xA_Against', 'xGChain', 'xGChain_Against', 'xGBuildup', 'xGBuildup_Against']
AllScenarios = [Attacking, Defending, AttPossesion, DfPossesion, Possesion]
##################

Liverpool_H_A_df = dataset.loc[(dataset['Team'] == 'Liverpool') & (dataset['TeamAgainst'] == 'Chelsea') & (dataset['Season'] == 2021)]
Chelsea_H_A_df = dataset.loc[(dataset['Team'] == 'Chelsea') & (dataset['TeamAgainst'] == 'Liverpool') & (dataset['Season'] == 2021)]

Team_season_df = dataset.loc[(dataset['Team'] == 'Liverpool') & (dataset['Season'] == 2021)]
TeamAgainst_season_df = dataset.loc[(dataset['TeamAgainst'] == 'Chelsea') & (dataset['Season'] == 2021)]

# Team_season_df.agg({'A' : ['sum', 'min'], 'B' : ['min', 'max']})

print('the data : ', Liverpool_H_A_df[Liverpool_H_A_df['Side'] == 'h'])

# createRadar("Liverpool", Liverpool_H_A_df[Liverpool_H_A_df['Side'] == 'h'], Attacking)
for Scenario in AllScenarios:
    createRadar2(Liverpool_H_A_df[Liverpool_H_A_df['Side'] == 'h'], Chelsea_H_A_df[Chelsea_H_A_df['Side'] == 'a'], "Liverpool", "Chelsea", Scenario)
# createRadar("Dybala",[24,91,86,81,67,85])


# Sample the highest goal scorers
teams_Goals_per_season = dataset.groupby(['Team', 'Season']).agg(total_goals= ('goals', 'sum')).reset_index()

print(teams_Goals_per_season.columns)
season_2016 = teams_Goals_per_season[teams_Goals_per_season['Season'] == 2016]


# teams_2016 = high_Goals[dataset["Season"] == 2016]['Team']
# goals_per_team_2016 = dataset[dataset["Season"] == 2016]['goals']


# Highest Number Of Goals EPL 2016
# with markerline deriving from plt.stem
plt.figure(figsize=(20, 10))
plt.stem(season_2016['Team'], season_2016["total_goals"])
plt.ylim(0, 100)
plt.xticks(season_2016['Team'],rotation='vertical')
plt.stem(season_2016["total_goals"])
(markerline, stemlines, baseline) = plt.stem(season_2016['Team'], season_2016["total_goals"])
plt.setp(baseline, visible=False)
plt.xlabel('Players', fontsize=25)
plt.ylabel('Shots', fontsize=25)
plt.title('Highest Number Of Goals EPL 2016', fontsize=20)
plt.show()


# Group the data by season and calculate total goals scored and conceded
goal_trends_per_year = dataset.groupby(['Season', 'Team'])[['goals', 'goals_Against']].sum().reset_index()

filtered_dataset = dataset[dataset['Team'].isin(list(dataset.Team))]
goal_trends = filtered_dataset.groupby('Season')[['goals']].sum().reset_index()
goals_Against_trends = filtered_dataset.groupby('Season')[['goals_Against']].sum().reset_index()

thisisit = goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['Team']
thistheothershit = goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['goals']

# Create a figure and axis
plt.figure(figsize=(12, 6))

# Plot goals scored and goals conceded
plt.plot(goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['Team'], goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['goals'], label='Goals Scored', marker='o')
plt.plot(goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['Team'], goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['goals_Against'], label='Goals Conceded', marker='o')

plt.xlabel('Teams')
plt.ylabel('Total Goals', rotation=45)
plt.title('Goal Trends in Season 2020')
plt.legend()
plt.grid(True)

# Customize x and y ticks
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.yticks(range(0, 100, 5))  # Set custom y-axis ticks (adjust as needed)

plt.show()


# Create a line plot for goal trends
plt.figure(figsize=(12, 6))
plt.plot(goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['Team'], goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['goals'], label='Goals Scored', marker='o') #, rotation=90)
plt.plot(goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['Team'], goal_trends_per_year[goal_trends_per_year['Season'] == 2020]['goals_Against'], label='Goals Conceded', marker='o') #, rotation=90)
plt.xlabel('Season 2020')
plt.ylabel('Total Goals', rotation = 45)
plt.title('Goal Trends Over the Years')
plt.legend()
plt.grid(True)
plt.show()


# Create a scatter plot for xG vs. actual goals
plt.figure(figsize=(10, 8))
plt.scatter(dataset['xG'], dataset['goals'], alpha=0.5)
plt.xlabel('xG (Expected Goals)')
plt.ylabel('Actual Goals Scored')
plt.title('xG vs. Actual Goals')
plt.grid(True)
plt.show()
