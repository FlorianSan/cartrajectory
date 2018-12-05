"""Interactive airport simulation.

This module defines the interactions with the simulation"""


SHORTCUTS = """Shortcuts:
n: next time step
b: last time step
q: close window"""


class Simulation:
    """The simulation state, with the following attributes:
    - airport: airport.Airport (the airport)
    - flights: traffic.Flight list (the traffic)
    - t: int (current time step)"""

    def __init__(self):

        self.t = 0


    def set_time(self, t):
        """set_time(int): set the current time to 't'"""
        self.t = t


    def increment_time(self, dt):
        """increment_time(int): increases the current time step by 'dt'
        (dt might be negative)"""
        self.set_time(self.t + dt)
