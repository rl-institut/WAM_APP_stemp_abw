
class UserSession(object):
    def __init__(self):
        self.scenarios = []
        self.simulation = Simulation()
        self.highcharts_temp = None


class Simulation(object):
    def __init__(self):
        self.esys = None