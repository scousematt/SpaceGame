import math
import Orbitals
import StarSystem
import random


class Galaxy(object):
    '''
    The Galaxy class is a master class from which all stars, planets, moons etc are derived
    '''

    def __init__(self):
        self.systems = []
        self.systemNames = []
        self.generate()

    def generate(self):
        numberOfStars = 11
        f = open('res/data/stardata.txt')
        starNames = []
        for line in f:
            starNames.append(line.rstrip('\r\n'))

        f.close()

        for i in range(0, numberOfStars):
            orbDis = random.randrange(10) * 10000000
            angle = 3.1415927 * random.randrange(359)/360
            c = random.randrange(len(starNames) - 1)
            name = starNames[c]
            starNames.remove(name)

            #add to systemNames so we can do an index search when selecting a system
            self.systemNames.append(name)
            #Add to list of objects
            self.systems.append(StarSystem.StarSystem(orbDis, angle, name))

        #print(self.systems)




    def loadFromFile(self):
        pass




