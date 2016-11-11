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

        pType = None    #'Rocky' or 'Gas Giant'
        pMass = 0 #This is in Earth Masses
        moons = 0 # number of moons

        #Star
        myStar = Orbitals.Star(self.name)

        myPlanet = None

        self.addChild(myStar)


        #Generate the number of planets

        #Assume 1000Mkm has largest gas giants
        gasGiantMassModifier = [(1 / math.sqrt(2 * math.pi)) * math.e ** (-0.5 * ((x / 6) ** 2)) * 2.5 for x in range(-10, 11)]
        #There are 20 planet 'electron shells'
        orbitShells = [0.07 * (i * 15) ** 2 + 25 for i in range(20)]
        chancePlanet = myStar.chanceOfPlanet
        planetNumber = 0

        #Planets
        suffix = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii',
                  'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'ix', 'xx']

        for i in range(0, 20):
            if random.randint(0, 100) < chancePlanet:
                orbitalDistance = orbitShells[i] + (orbitShells[i] * (random.randint(-7, 12)) / 100)
                planetNumber += 1
                if gasGiantMassModifier[i] + 0.25 > 1:
                    pType = 'Gas Giant'
                    pMass = gasGiantMassModifier[i] ** 3 * (255) + random.randint(0, 100)
                    moonChance = 500
                else:
                    pType='Rocky'
                    pMass=random.randint(1, 1000) / 1000 * 1.2 + 0.5
                    moonChance = 40
                moons = 0
                x = random.randint(0, 100)
                while x < moonChance:
                    moonChance -= x
                    moons += 1
                    x = random.randint(0, 100)
                #Create the planet object
                #print(" ".join(('Planet Number is', str(planetNumber))))
                myPlanet = Orbitals.Planet(orbitalDistance, " ".join( (self.name, suffix[planetNumber -1 ]) ),
                                           pType, pMass, moons )
                self.addChild(myPlanet)

        #last object in system
        self.maxOrbitalDistance = myPlanet.orbitalDistance * 3
        self.update(10)

    def getPlanetNames(self):
        '''
        Sends a type to self.getNamesFromChildren
        :return: A list of planet names
        '''
        return(self.getNamesFromChildren('<class \'Orbitals.Planet\'>'))
        #return([item for item in self.children if str(type(item)) == '<class \'Orbitals.Planet\'>'])


    def getNamesFromChildren(self, text):
        '''
        :param: text is the type e.g. 'Orbitals.planet'
        :return: A list of all the names within self.children of type(text)
        '''


        #return([item for item in self.children if str(type(item)) == text])
        output = []
        for item in self.children:
            if str(type(item)) == text:
                output.append(item.name)
        return(output)





