'''
This module is where all of the global project variables are going to be encountered, stored and accessed.

Variables will be set up when the main.py is run.
'''
PI = 3.1415927

top_menu = None

galaxy = None
all_vessels = []



current_time = 0
current_system = 0


def update_time(dt):
    global current_time, all_vessels

    current_time += dt
    for ship in all_vessels:
        ship.update(dt)
        print(ship.name)


def deg2rad(theta):
    return theta * PI / 180

def rad2deg(theta):
    return theta * 180 / PI