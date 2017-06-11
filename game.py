'''
This module is where all of the global project variables are going to be encountered, stored and accessed.

Variables will be set up when the main.py is run.
'''


top_menu = None

galaxy = None
current_time = 0
current_system = 0


def update_time(dt):
    current_time += dt
