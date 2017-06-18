import game
import Orbitals
import math

class Vessel(Orbitals.Orbitals):
    def __init__(self, name, speed, cost):
        '''
        what will all vessels have
        '''
        self.name = name
        self.speed = speed    # km/s
        self.cost = cost
        self.color = 'green'   #friendly
        self.heading = 45
        self.heading_rad = self.heading * game.PI / 180
        self.angle = 225
        self.orbitalDistance = 500000000000

        game.all_vessels.append(self)

    def update(self, dt):
        x, y = self.getCoords()
        x += math.sin(self.heading_rad) * dt * self.speed
        y += math.cos(self.heading_rad) * dt * self.speed

        # So 0, 0 is the centre of the system - star location
        self.angle = math.atan(x/y)
        self.orbitalDistance = ((x * x) + (y * y)) ** 0.5

if __name__ == '__main__':
    s1 = Vessel('Witch', 10, 100)
    print(s1.getCoords())
    s1.update(10)
    print(s1.getCoords())