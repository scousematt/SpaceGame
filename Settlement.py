def interp(x):
    '''Return temperature given a latitude input -90 -> 90'''
    latitudes = [90, 60, 30, 18, 0, -18, -30, -60, -90]
    temperatures = [-60, -40, -10, -3, 0, -3, -10, -40, -60]
    for i, latitude in enumerate(latitudes):
        if latitude < x:
            dx = (x - latitude) / (latitudes[i - 1] - latitude)
            return (int(temperatures[i] - (dx * (temperatures[i] - temperatures[i - 1]))))


class Settlement(object):
    def __init__(self, faction, planet, latitude, population=30000):
        self.faction = faction
        self.planet = planet
        self.star = self.planet
        self.latitude = latitude
        self.meanTemp = interp(self.latitude)
        '''The temperature depends on the atmosphere rather than the solar energy hitting the
        surface. Also, does the planet temperature need to be here. should be in Orbitals.'''
        self.population = population

    def update(self):
        return ()
        # increase / decrease population
        # process existing builds for the time


s = Settlement('Welsh', 'Mars', 32, 1000000)
print(getattr(s, 'meanTemp'))