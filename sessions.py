
class UserSession(object):
    def __init__(self):
        self.scenarios = []
        self.simulation = Simulation()


class Simulation(object):
    def __init__(self):
        self.esys = None