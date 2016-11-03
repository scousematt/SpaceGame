import Orbitals
import random
import math


class StarSystem(Orbitals.Orbitals):
    def __init__(self, orbitalDistance, angle, name):
        Orbitals.Orbitals.__init__(self, orbitalDistance)
        self.angle = angle
        self.orbitalPeriod = 1   #A static Galaxy
        self.name = name
        self.maxOrbitalDistance = None




    def generate(self):

        #Star
        myStar = Orbitals.Star(self.name)
        myStar.generate()
        myPlanet = None

        self.addChild(myStar)


        #Assume 5 planets - TODO randomise this
        numPlanets = random.randint(3, 14)
        print(numPlanets)

        #Planets

        suffix =['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv']
        for i in range(0, numPlanets):
            orbitalDistance = 150000000000 + i * 40000000000

            myPlanet = Orbitals.Planet(orbitalDistance, " ".join( (self.name, suffix[i]) ) )
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
