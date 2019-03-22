from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, render
import json
from collections import OrderedDict
#import sqlahelper

from stemp_abw.config import io
from stemp_abw import results

from stemp_abw.models import Scenario

from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *
from stemp_abw.charts_data import visualizations1, visualizations2

from utils.widgets import InfoButton
from wam.settings import SESSION_DATA
from stemp_abw.sessions import UserSession
import os
import stemp_abw

# TODO: use WAM's + Test it
def check_session(func):
    def func_wrapper(self, request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            return render(request, 'stemp_abw/session_not_found.html')
        return func(self, request, session=session, *args, **kwargs)
    return func_wrapper


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


class ImprintView(TemplateView):
    template_name = 'stemp_abw/imprint.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'stemp_abw/privacy_policy.html'
    

class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'

    def __init__(self):
        super(MapView, self).__init__()

        #self.simulation = Simulation()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(io.prepare_layer_data())
        context.update(io.prepare_component_data())
        context.update(io.prepare_scenario_data())
        context.update(io.prepare_label_data())

        # TODO: Temp stuff for WS
        context['visualizations1'] = visualizations1
        context['visualizations2'] = visualizations2

        # Trial: new info button
        # TODO: Move
        file = os.path.join(os.path.dirname(stemp_abw.__file__), 'config', 'text', 'test.md')
        f = open(file, 'r', encoding='utf-8')
        context['info'] = InfoButton(text=f.read(),
                                     tooltip='tooltip hahaha',
                                     is_markdown=True,
                                     ionicon_type='ion-help-circled',
                                     ionicon_size='medium')
        f.close()

        return context

    def get(self, request, *args, **kwargs):
        # Start session (if there's none):
        SESSION_DATA.start_session(request, UserSession)

        context = self.get_context_data()
        return self.render_to_response(context)

    @check_session
    def post(self, request, session):
        action = request.POST['action']
        data = request.POST['data']
        
        # get scnenario values (trigger: scenario dropdown)
        if action == 'select_scenario':
            scn = session.scenarios[int(data)]
            ret_data = {'scenario_list': dict(Scenario.objects.filter(
                is_user_scenario=False).values_list('id', 'name')),
                        'scenario': {'name': scn.name,
                                     'desc': scn.description,
                                     'data': scn.data.data},
                        'controls': session.get_control_values(scn)
                        }
        
        # apply scenario (trigger: scn button) -> set as user scenario
        elif action == 'apply_scenario':
            scn_id = int(data)
            scn = session.scenarios[scn_id]
            ret_data = {'scenario': {'name': scn.name,
                                     'desc': scn.description,
                                     'data': scn.data.data},
                        'controls': session.get_control_values(scn)
                        }
            session.set_user_scenario(scn_id=scn_id)

        # change scenario/control value (trigger: control)
        elif action == 'update_scenario':
            sl_wind_repower_pot = session.update_scenario_data(
                ctrl_data=json.loads(data))
            ret_data = {'sl_wind_repower_pot': sl_wind_repower_pot}

        # start simulation (trigger: sim button)
        elif action == 'simulate':
            session.simulation.create_esys()
            session.simulation.simulate()

            ret_data = {'simulation': 'successful'}

        return HttpResponse(json.dumps(ret_data))


class SourcesView(TemplateView):
    template_name = 'stemp_abw/sources.html'
