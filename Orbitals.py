import math

class Orbitals(object):
    def __init__(self, orbitalDistance):
        self.parent = None
        self.children = []


        #Arbitary north as 0
        self.angle = 0
        #Metres
        self.orbitalDistance = orbitalDistance
        #Seconds
        self.orbitalPeriod = self.kepler3(self.orbitalDistance)


    def update(self, timeSinceStart):
        # Advance time by correct amount of time (a delta t could introduce floating point probs)
        self.Angle = (timeSinceStart / self.orbitalPeriod) * math.pi * 2

        # Update all of our children
        for i in range(0, len(self.children)):
            self.children[i].Update(timeSinceStart)

    def addChild(self, c):
        c.Parent = self
        self.children.append(c)

    def removeChild(self, c):
        c.Parent = None
        self.children.remove(c)

    def kepler3(self, radius):
        '''
        Takes in the orbital distance in metres as per Kepler's Law of
        harmonies, T^2 / R^3  = 3 x 10^-19
        :return: orbital period in seconds
        '''
        return (math.sqrt(0.0000000000000000003 * (radius ** 3)))



class Star(Orbitals):
    def __init__(self):
        #Assume the star is at the centre of the system with a radius of 1
        Orbitals.__init__(self, 1)
        self.orbitalPeriod = 0
        self.name = None


    def generate(self):
        self.stellarClass = "G5"
        self.name = "Sol"


    def __str__(self):
        return ("The stars name is " + self.name)

class Planet(Orbitals):
    def __init__(self, orbitalDistance, name):
        Orbitals.__init__(self, orbitalDistance)
        self.name = name

    def generate(self):
        pass

    def __str__(self):
        return("The planets name is " + self.name)



'''
t = Star()
t.generate()
print(t.orbitalPeriod / (360 * 24 * 3600))
print(t.name)
'''