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

#   ____                                             _
#  / ___|___  _ __ ___  _ __   ___  _ __   ___ _ __ | |_ ___
# | |   / _ \| '_ ` _ \| '_ \ / _ \| '_ \ / _ \ '_ \| __/ __|
# | |__| (_) | | | | | | |_) | (_) | | | |  __/ | | | |_\__ \
#  \____\___/|_| |_| |_| .__/ \___/|_| |_|\___|_| |_|\__|___/
#                      |_|
#
# A list of things that vessels can have
class Ship(Vessel):
    def __init__(self, name, speed, cost):
        Vessel.__init__(self, name, speed, cost)
        pass

    def add_engine(self, engine):
        self.engine = engine
        engine.owner = self

    def add_active_sensor(self, active_sensor):
        self.active_sensor = active_sensor
        active_sensor.owner = self

    def add_passive_sensor(self, passive_sensor):
        self.passive_sensor = passive_sensor
        passive_sensor.owner = self


    def add_thermal_sensor(self, thermal_sensor):
        self.thermal_sensor = thermal_sensor
        thermal_sensor.owner = self

    def add_hull(self, hull):
        self.hull = hull
        hull.owner = self

    def add_firecontrol(self, firecontrol):
        self.firecontrol = firecontrol
        firecontrol.owner = self

    def add_weapon(self, weapon):
        self.weapon = weapon
        weapon.owner = self

class Engine:
    def __init__(self):
        self.owner = None

class ActiveSensor:
    def __init__(self):
        self.owner = None

class PassiveSensor:
    def __init__(self):
        self.owner = None

class ThermalSensor:
    def __init__(self):
        self.owner = None

class Hull:
    def __init__(self):
        self.owner = None

class FireControl:
    def __init__(self):
        self.owner = None

class Weapon:
    def __init__(self):
        self.owner = None






if __name__ == '__main__':
    s1 = Vessel('Witch', 10, 100)
    print(s1.getCoords())
    s1.update(10)
    print(s1.getCoords())