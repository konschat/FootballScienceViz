import pandas as pd
from math import pi
import matplotlib.pyplot as plt
#%matplotlib inline

#Create a data frame from Messi and Ronaldo's 6 Ultimate Team data points from FIFA 18
Messi = {'Pace':89,'Shooting':90,'Passing':86,'Dribbling':95,'Defending':26,'Physical':61}
Ronaldo = {'Pace':90,'Shooting':93,'Passing':82,'Dribbling':90,'Defending':33,'Physical':80}

data = pd.DataFrame([Messi,Ronaldo], index = ["Messi","Ronaldo"])
print(data)

Attributes =list(data)
AttNo = len(Attributes)

values = data.iloc[1].tolist()
values += values[:1]
print(values)

angles = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
angles += angles[:1]

#Find the values and angles for Messi from the table
values2 = data.iloc[0].tolist()
values2 += values2 [:1]

angles2 = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
angles2 += angles2 [:1]

def createRadar(player, data):
    Attributes = ["Defending", "Dribbling", "Pace", "Passing", "Physical", "Shooting"]

    data += data[:1]

    angles = [n / 6 * 2 * pi for n in range(6)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], Attributes)
    ax.plot(angles, data)
    ax.fill(angles, data, 'blue', alpha=0.1)

    ax.set_title(player)
    plt.show()

def createRadar2(player, data, player2, data2):
    Attributes = ["Defending", "Dribbling", "Pace", "Passing", "Physical", "Shooting"]

    data += data[:1]
    data2 += data2[:1]

    angles = [n / 6 * 2 * pi for n in range(6)]
    angles += angles[:1]

    angles2 = [n / 6 * 2 * pi for n in range(6)]
    angles2 += angles2[:1]

    ax = plt.subplot(111, polar=True)

    # Create the chart as before, but with both Ronaldo's and Messi's angles/values
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], Attributes)

    ax.plot(angles, values)
    ax.fill(angles, values, 'teal', alpha=0.1)

    ax.plot(angles2, values2)
    ax.fill(angles2, values2, 'red', alpha=0.1)

    # Rather than use a title, individual text points are added
    plt.figtext(0.2, 0.9, player, color="teal")
    plt.figtext(0.2, 0.85, "v")
    plt.figtext(0.2, 0.8, player2, color="red")
    plt.show()

createRadar("Dybala",[24,91,86,81,67,85])

createRadar2("Henderson", [76,76,62,82,81,70],"Wilshere", [62,82,71,80,72,69])






createRadar("Dybala",[24,91,86,81,67,85])
