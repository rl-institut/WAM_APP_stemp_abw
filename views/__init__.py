import os
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, render
import json

from stemp_abw.config.prepare_context import component_data, prepare_layer_data

# do not execute when on RTD (reqd for API docs):
if 'READTHEDOCS' not in os.environ:
    from stemp_abw.config.prepare_context import SCENARIO_DATA

from stemp_abw.config.prepare_texts import label_data, text_data
from stemp_abw.config.leaflet import LEAFLET_CONFIG
from stemp_abw.models import Scenario
from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *
from stemp_abw.results.result_charts import results_charts_tab1_viz,\
    results_charts_tab2_viz, results_charts_tab3_viz, results_charts_tab4_viz,\
    results_charts_tab5_viz

from wam.settings import SESSION_DATA
from stemp_abw.sessions import UserSession
from stemp_abw.app_settings import RE_POT_LAYER_ID_LIST


# TODO: use WAM's + Test it
def check_session(func):
    def func_wrapper(self, request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            return render(request, 'stemp_abw/session_not_found.html')
        return func(self, request, session=session, *args, **kwargs)
    return func_wrapper


def get_clean_session(request):
    """Checks for existing session

    Obtain it using WAM's :class:`wam.user_sessions.sessions.SessionData`
    and delete session data (instantiate
    :class:`stemp_abw.sessions.UserSession`).

    Parameters
    ----------
    request : :obj:`django.core.handlers.wsgi.WSGIRequest`
        Request
    """
    # get current session key
    session_key = request.session.session_key
    # get session (existing or new one if there's none)
    SESSION_DATA.start_session(request, UserSession)
    # if session existed before: delete session data
    if session_key is not None:
        SESSION_DATA.sessions['stemp_abw'][session_key] = UserSession()


class ContactView(TemplateView):
    template_name = 'stemp_abw/contact.html'


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
        layer_data = prepare_layer_data()
        layer_list_results = layer_data['layer_list']
        layer_data['layer_list'] = {layer: data
                                    for layer, data in layer_data['layer_list'].items()
                                    if data['cat'] != 'results'}
        layer_data['layer_list_results'] = {layer: data
                                            for layer, data in layer_list_results.items()
                                            if data['cat'] == 'results'}
        context.update(layer_data)

        context.update(component_data())
        context.update(SCENARIO_DATA)
        context.update(label_data())
        context.update(text_data())
        context['re_pot_layer_id_list'] = RE_POT_LAYER_ID_LIST

        context['results_charts_tab1_viz'] = results_charts_tab1_viz()
        context['results_charts_tab2_viz'] = results_charts_tab2_viz()
        context['results_charts_tab3_viz'] = results_charts_tab3_viz
        context['results_charts_tab4_viz'] = results_charts_tab4_viz
        context['results_charts_tab5_viz'] = results_charts_tab5_viz

        context['leaflet_config'] = LEAFLET_CONFIG

        context['redirect_to'] = '/stemp_abw/app/'

        return context

    def get(self, request, *args, **kwargs):
        # get clean session
        get_clean_session(request)

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
        elif action in ['apply_scenario', 'init_sq_scenario']:
            scn_id = int(data)
            scn = session.scenarios[scn_id]
            ret_data = {'scenario': {'name': scn.name,
                                     'desc': scn.description,
                                     'data': scn.data.data},
                        'controls': session.get_control_values(scn)
                        }
            ret_data = json.dumps(ret_data)
            session.set_user_scenario(scn_id=scn_id)
            # set results to outdated (if scn is not applied on startup)
            if action == 'apply_scenario':
                session.simulation.results.status = 'outdated'  # set results to outdated

        # change scenario/control value (trigger: control)
        elif action == 'update_scenario':
            print(json.loads(data))
            sl_wind_repower_pot = session.update_scenario_data(
                ctrl_data=json.loads(data))
            ret_data = {'sl_wind_repower_pot': sl_wind_repower_pot}
            ret_data = json.dumps(ret_data)
            session.simulation.results.status = 'outdated'  # set results to outdated

        # start simulation (trigger: sim button)
        elif action == 'simulate':
            session.simulation.create_esys()
            session.simulation.load_or_simulate()

            ret_data = 'simulation successful'

        return HttpResponse(ret_data)
