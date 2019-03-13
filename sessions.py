from uuid import uuid4

from stemp_abw.models import Scenario


class UserSession(object):
    def __init__(self):
        self.user_scenario = self.__init_user_scenario()
        self.simulation = Simulation()

    @property
    def scenarios(self):
        return {scn.id: scn
                for scn in Scenario.objects.filter(
                    is_user_scenario=False).all()
                }

    @staticmethod
    def __init_user_scenario():
        """Make a copy of status quo scenario for user scenario"""
        scn = Scenario.objects.get(name='Status quo')
        scn.name = 'User Scenario {uuid}'.format(uuid=str(uuid4()))
        scn.description = ''
        scn.id = None
        # scn.save()
        return scn
    

class Simulation(object):
    def __init__(self):
        self.esys = None
