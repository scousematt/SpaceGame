import math

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
        #Seconds
        self.orbitalPeriod = self.kepler3(self.orbitalDistance)

    def update(self, timeSinceStart):
        # Advance time by correct amount of time (a delta t could introduce floating point probs)

        #print("Updating via Orbitals :" + self.name)
        self.currentTime += timeSinceStart

        self.angle = (self.currentTime / self.orbitalPeriod) * math.pi * 2





        # Update all of our children
        for i in range(0, len(self.children)):
            self.children[i].update(timeSinceStart)

    def addChild(self, c):
        c.Parent = self
        self.children.append(c)

    def removeChild(self, c):
        c.Parent = None
        self.children.remove(c)

    def getCoords(self):
        return(math.sin(self.angle) * self.orbitalDistance,
               math.cos(self.angle) * self.orbitalDistance,
               )


    def kepler3(self, radius):
        '''
        Takes in the orbital distance in metres as per Kepler's Law of
        harmonies, T^2 / R^3  = 3 x 10^-19
        :return: orbital period in seconds

        Extra solar planets are different

        time = math.sqrt((4 * math.pi**2/ (0.000000000067 * stellarMass)) * radius ** 3)
        '''
        #TODO stellarMass needs to be calculated for each star


        G = 6.67408 * 10 ** -11
        stellarMass = 1.989 * 10 ** 30

        return (math.sqrt((4 * math.pi**2/ (G * stellarMass)) * radius ** 3))




class Star(Orbitals):
    def __init__(self, name):
        #Assume the star is at the centre of the system with a radius of 1
        Orbitals.__init__(self, 1)
        self.orbitalPeriod = 1
        self.name = name
        #TODO self.stellarMass for kepler3(stellarMass)

    def generate(self):
        self.stellarClass = "G5"





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



#
# t = Planet(150000000000, "Earth")
# #t.generate()
# print(t.orbitalPeriod / (360 * 24 * 3600))
# print(t)
