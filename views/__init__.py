from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, render
import json

from stemp_abw.config import io

from stemp_abw.models import Scenario

from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *
from stemp_abw.results.result_charts import results_charts_tab1_viz, results_charts_tab2_viz, visualizations2, visualizations5

from utils.widgets import InfoButton
from wam.settings import SESSION_DATA
from stemp_abw.sessions import UserSession
from stemp_abw.app_settings import RE_POT_LAYER_ID_LIST

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

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        # prepare layer data and move result layers to separate context var
        layer_data = io.prepare_layer_data()
        layer_data['layer_list'] = {layer: data
                                    for layer, data in layer_data['layer_list'].items()
                                    if data['cat'] != 'results'}
        layer_data['layer_list_results'] = {layer: data
                                            for layer, data in layer_data['layer_list'].items()
                                            if data['cat'] == 'results'}
        context.update(layer_data)

        context.update(io.prepare_component_data())
        context.update(io.prepare_scenario_data())
        context.update(io.prepare_label_data())
        context['re_pot_layer_id_list'] = RE_POT_LAYER_ID_LIST

        # TODO: Temp stuff for WS
        context['results_charts_tab2_viz'] = results_charts_tab2_viz
        context['visualizations2'] = visualizations2
        context['results_charts_tab1_viz'] = results_charts_tab1_viz
        context['visualizations5'] = visualizations5

        # Trial: new info button
        # TODO: Move
        file = os.path.join(os.path.dirname(stemp_abw.__file__), 'config', 'text', 'test.md')
        f = open(file, 'r', encoding='utf-8')
        context['info'] = InfoButton(text=f.read(),
                                     tooltip='tooltip hahaha',
                                     is_markdown=True,
                                     ionicon_type='ion-information-circled',
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
            ret_data = json.dumps(ret_data)
        
        # apply scenario (trigger: scn button) -> set as user scenario
        elif action == 'apply_scenario':
            scn_id = int(data)
            scn = session.scenarios[scn_id]
            ret_data = {'scenario': {'name': scn.name,
                                     'desc': scn.description,
                                     'data': scn.data.data},
                        'controls': session.get_control_values(scn)
                        }
            ret_data = json.dumps(ret_data)
            session.set_user_scenario(scn_id=scn_id)
            session.simulation.results.is_up_to_date = False   # set results to outdated

        # change scenario/control value (trigger: control)
        elif action == 'update_scenario':
            print(json.loads(data))
            sl_wind_repower_pot = session.update_scenario_data(
                ctrl_data=json.loads(data))
            ret_data = {'sl_wind_repower_pot': sl_wind_repower_pot}
            ret_data = json.dumps(ret_data)
            session.simulation.results.is_up_to_date = False   # set results to outdated

        # start simulation (trigger: sim button)
        elif action == 'simulate':
            session.simulation.create_esys()
            session.simulation.load_or_simulate()

            ret_data = 'simulation successful'

        # # check if there are resuls for current scenario
        # # (trigger: open results panel)
        # elif action == 'check_results':
        #     if session.simulation.results is None:
        #         ret_data = 'none'
        #     else:
        #         ret_data = json.dumps({'results': 'found'})

        return HttpResponse(ret_data)


class SourcesView(TemplateView):
    template_name = 'stemp_abw/sources.html'
