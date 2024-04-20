import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ucl data related
#Players With Atleast One Goal In Group stage
def teams_goals_comp_hist_per_season(df):
    Players_With_Atleast_OneGoal = df[df["Gls"]>1][["Player","Gls"]]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(Players_With_Atleast_OneGoal.Player, Players_With_Atleast_OneGoal.Gls, color='red')
    #ax.set_facecolor('black')
    ax.set_title("Goals in G/S of UEFA UCL 2020-21", fontsize=40)
    ax.set_xlabel("Players", fontsize=30)
    ax.set_ylabel("Number Of Goals", fontsize=25)
    ax.tick_params(labelrotation=90)
    plt.show()

def ucl_player_goals_and_assist_comp_hist_per_season(shots):
    """

    :param shots:
    """
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


def single_player_stats_chart(df):
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