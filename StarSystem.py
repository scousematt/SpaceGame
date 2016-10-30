import Orbitals


class StarSystem(Orbitals.Orbitals):
    def __init__(self, orbitalDistance, angle):
        Orbitals.Orbitals.__init__(self, orbitalDistance)
        self.angle = angle
        self.orbitalPeriod = 0   #A static Galaxy
        self.name = None




    def generate(self):

        #Star
        myStar = Orbitals.Star()
        myStar.generate()
        self.name = myStar.name
        self.addChild(myStar)


        #Assume 5 planets - TODO randomise this
        numPlanets = 5


        #Planets
        for i in range(0, numPlanets):
            orbitalDistance = i * 25000000000
            myPlanet = Orbitals.Planet(orbitalDistance, self.name + " " + str(i + 1))
            self.addChild(myPlanet)
            #print(myPlanet)


        #A check on generation
        for item in self.children:
            print(item)


#A little test

mySystem = StarSystem(10000000, 25)
mySystem.generate()
