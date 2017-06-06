import random
import math
import game

'''
A settlement is any place on or around a body upon which citizens are based.

Mining Colony
Military Base
Planetary sensor

All facilities will requires a population and infrastructure, hence will be a settlement.


What about Babylon 5 strucures - All they need is a place within current_system.children as type<construct>


'''


def interp(x):
    '''Return temperature given a latitude input -90 -> 90'''
    latitudes = [90, 60, 30, 18, 0, -18, -30, -60, -90]
    temperatures = [-60, -40, -10, -3, 0, -3, -10, -40, -60]
    for i, latitude in enumerate(latitudes):
        if latitude < x:
            dx = (x - latitude) / (latitudes[i - 1] - latitude)
            return (int(temperatures[i] - (dx * (temperatures[i] - temperatures[i - 1]))))


class Settlement(object):
    def __init__(self, faction, planet, population):
        self.faction = faction
        self.planet = planet
        self.star = self.planet
        self.latitude = random.randint(-90, 90)
        self.meanTemp = interp(self.latitude)
        '''The temperature depends on the atmosphere rather than the solar energy hitting the
        surface. Also, does the planet temperature need to be here. should be in Orbitals.'''
        self.population = population

    def update(self):
        return ()
        # increase / decrease population
        # process existing builds for the time


class Player_Homeworld(Settlement):
    def __init__(self, faction, planet, population):
        Settlement.__init__(faction, planet, population)
        self.faction = 'player'
        self.population = population

        self.temperature = -20 + 40 * math.cos(self.latitude * 3.142 / 180)
