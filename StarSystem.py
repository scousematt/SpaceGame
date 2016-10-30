import Orbitals
import random
import math


class StarSystem(Orbitals.Orbitals):
    def __init__(self, orbitalDistance, angle):
        Orbitals.Orbitals.__init__(self, orbitalDistance)
        self.angle = angle
        self.orbitalPeriod = 1   #A static Galaxy
        self.name = None
        self.maxOrbitalDistance = None




    def generate(self):

        #Star
        myStar = Orbitals.Star()
        myStar.generate()
        self.name = myStar.name
        self.addChild(myStar)


        #Assume 5 planets - TODO randomise this
        numPlanets = random.randint(3, 14)
        print(numPlanets)

        #Planets
        for i in range(0, numPlanets):
            orbitalDistance = 150000000000 + i * 40000000000

            myPlanet = Orbitals.Planet(orbitalDistance, self.name + " " + str(i + 1))
            myPlanet.angle = (random.randrange(360) / 360) * 2 * math.pi

            self.addChild(myPlanet)
            print(myPlanet)

        #last object in system
        self.maxOrbitalDistance = myPlanet.orbitalDistance * 3

        self.update(10)



        #A check on generation
        # for item in self.children:
        #     print(item)


#A little test
#
# mySystem = StarSystem(10000000, 25)
# mySystem.generate()
# print(mySystem.children[1].angle)
# mySystem.update(55000000)
# print(mySystem.children[1].angle)
# print(mySystem.children[1].orbitalPeriod)
#
# mySystem.update(55000000)
# print(mySystem.children[1].angle)
