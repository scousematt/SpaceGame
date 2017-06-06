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

        '''
        Do I add a list of settlements here, and how do I reference them? A unique ID when created?

        Do I add a new class, Factions, which controls species traits and its settlements and ships? I like the idea of that



        So we are looking at something like...

        self.generate_factions()
            generate_species()
                'Human'
                generate_nation()
                    'UK'
                    generate_settlement()
                        'London'
                    'France'
                        'Paris'
                'Vulcan'
                    'Vulcan'
                        'Vulcan City'


        '''

        self.generate()


    def generate(self):
        numberOfStars = 11
        #with open('res/data/stardata.txt') as f:
        #   for line in F:
        #       print(line.rstrip('\r\n'))
        #no need to close
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




