from ant import Ant
import matplotlib.pyplot as plt
import random

# Setting figure size
plt.figure(figsize=(5,5))

# To make our graph animated/interactable
plt.ion()

# objects of all ants
ant1 = Ant("Mark", 0, 1, color='magenta')
ant2 = Ant("Moris", 0, 2, color='blue')
ant3 = Ant("James", 0, 3, color='green')
ant4 = Ant("Amla", 0, 4, color='red')
ant5 = Ant("Clarke", 0, 5, color='cyan')
ant6 = Ant("Finch", 0, 6, color='yellow')
ant7 = Ant("Warner", 0, 7, color='black')
ant8 = Ant("Kolhi", 0, 8, color='red')
ant9 = Ant("Dhoni", 0, 9, color='magenta')
ant10 = Ant("Gayle", 0, 10, color='green')

# list of ants
all_ants= [ant1, ant2, ant3, ant4, ant5, ant6, ant7, ant8, ant9, ant10]

# width of board
width = 10

# loop to draw initial position of ants
for ant in all_ants:
    ant.draw()

    
win = False
# loop will run till someone wins
while not win:
    plt.xlim(0, len(all_ants)+1)
    plt.xticks(range(width+1))
    plt.yticks(range(len(all_ants)+1))
    plt.show()
    plt.pause(0.5)
    plt.cla()
    # loop for each ant
    for ant in all_ants:
        ant.move(random.choice(range(1,4)), width)
        ant.draw()
        # breaking loop if any ant won
        if ant.at_edge(width):
            print("Winner:", ant.name)
            win = True
            break
