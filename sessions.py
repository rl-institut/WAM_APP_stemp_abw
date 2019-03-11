import json

from stemp_abw.models import Scenario


class UserSession(object):
    def __init__(self):
        self.scenarios = self.init_default_scenarios()
        self.simulation = Simulation()

    def init_default_scenarios(self):
        scns = Scenario.objects.filter(is_user_scenario=False).all()
        return {scn.id: scn for scn in scns}


class Simulation(object):
    def __init__(self):
        self.esys = None
