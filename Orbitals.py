import math
import random


# -------------------------------------------- CONSTANTS -------------------------------

starClass = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
starColor = ['dodger blue', 'light sky blue', 'white', 'light yellow',
                  'yellow', 'orange', 'red']
starHowCommon = [0.00003, 0.12503, 0.75003, 3.78003, 11.28003, 23.28003, 100]
starChancePlanet = [0, 4, 10, 50, 60, 60, 60]


# In earth masses
solarMasses = [[16, 25], [2.1, 16], [1.4, 2.1], [1.04, 1.4], [0.8, 1.04], [0.45, 0.8], [0.08, 0.45]]

solarMass = 1.989 * 10 ** 30

def getStarTypeIndex():
    '''
    Uses the constant list starHowCommon and a random number to decide on an index for the other stat type
     lists.
    :return: The index of starClass, starColor
    '''
    t = random.random() * 100
    for i, j in enumerate(starHowCommon):
        if t <= j:
            return(i)

def getStarMass(c):
    '''Takes in the index of both starClass and starColor which will be the same and
    returns the mass in units - solar mass'''
    return solarMasses[c][0] + (random.random() * (solarMasses[c][1] - solarMasses[c][0]))

class Orbitals(object):
    def __init__(self, orbitalDistance):

        self.parent = None
        self.children = []

        self.currentTime = 1534562334
        self.name = None
        #Arbitary north as 0
        self.angle = 0
        #Metres
        self.orbitalDistance = orbitalDistance
        self.orbitalPeriod = 100000



    def update(self, timeSinceStart):
        # Advance time by correct amount of time (a delta t could introduce floating point probs)
        self.currentTime += timeSinceStart
        self.angle = (self.currentTime / self.orbitalPeriod) * math.pi * 2
        # Update all of our children
        for i in range(0, len(self.children)):
            self.children[i].update(timeSinceStart)

    def addChild(self, c):
        c.parent = self
        self.children.append(c)

    def removeChild(self, c):
        c.parent = None
        self.children.remove(c)

    def getCoords(self):
        return(math.sin(self.angle) * self.orbitalDistance,
               math.cos(self.angle) * self.orbitalDistance)


    def kepler3(self, radius, mass):
        '''
        Takes in the orbital distance in metres as per Kepler's Law of
        harmonies, T^2 / R^3  = 3 x 10^-19 and the mass of the body being orbited
        :return: orbital period in seconds
        '''
        G = 6.67408 * 10 ** -11
        return (math.sqrt((4 * math.pi**2/ (G * mass)) * radius ** 3))




class Star(Orbitals):
    def __init__(self, name):
        #Assume the star is at the centre of the system with a radius of 1
        Orbitals.__init__(self, 1)
        self.orbitalPeriod = 1
        t = getStarTypeIndex()
        self.name = name
        self.mass = solarMass * getStarMass(t)
        self.stellarClass = starClass[t]
        self.stellarColor = starColor[t]
        self.orbitalPeriod = self.kepler3(self.orbitalDistance, self.mass)
        self.chanceOfPlanet = starChancePlanet[t]


class Planet(Orbitals):
    def __init__(self, orbitalDistance, name, pType, pMass, moons):
        Orbitals.__init__(self, orbitalDistance)
        self.name = name
        self.planetType = pType
        self.mass = pMass
        self.moons = moons
        self.angle = (random.randrange(360) / 360) * 2 * math.pi


    def generate(self):
        #Note, parents and childen are not set during __init__.
        self.orbitalPeriod = self.kepler3(self.orbitalDistance, self.parent.children[0].mass)

class Moon(Orbitals):
    def __init__(self, orbitalDistance, name, mMass, pOrb):
        Orbitals.__init__(self, orbitalDistance)
        self.name = name
        self.moonMass = mMass
        self.planet_orbited = pOrb
        self.orbitalPeriod = self.kepler3(self.orbitalDistance, self.planet_orbited.mass )