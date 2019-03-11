import json

from stemp_abw.models import Scenario


class UserSession(object):
    def __init__(self):
        self.simulation = Simulation()

    @property
    def scenarios(self):
        return {scn.id: scn
                for scn in Scenario.objects.filter(
                    is_user_scenario=False).all()
                }


class Simulation(object):
    def __init__(self):
        self.esys = None
