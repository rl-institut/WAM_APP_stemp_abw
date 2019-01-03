from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, render
import json
from collections import OrderedDict
#import sqlahelper
from stemp_abw.forms import LayerGroupForm, ComponentGroupForm

from stemp_abw.app_settings import LAYER_METADATA, LAYER_DEFAULT_STYLES, \
    ESYS_COMPONENTS_METADATA, LABELS
from stemp_abw.simulation.bookkeeping import simulate_energysystem
from stemp_abw import results

from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *
from utils.widgets import InfoButton
from wam.settings import SESSION_DATA
import os
import stemp_abw


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


class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'

    def __init__(self):
        super(MapView, self).__init__()

        #self.simulation = Simulation()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(self.prepare_layer_data())
        context.update(self.prepare_component_data())
        context.update(self.prepare_label_data())

        # TODO: Temp stuff for WS
        labels1 = OrderedDict((
            ('Windenergie Erzeugung', ['Wind']),
            ('Photovoltaik Erzeugung', ['PV']),
            ('Bioenergie Erzeugung', ['Biomasse', 'Biogas'])
        ))
        visualizations1 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                          for t, c in labels1.items()]
        labels2 = {'Erzeugung': ['Strom', 'Wärme'],
                  'Bedarf': ['Strom', 'Wärme'],
                  'Erneuerbare Energien': ['Wind', 'Solar']
                  }
        visualizations2 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                          for t, c in labels2.items()]
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
        SESSION_DATA.start_session(request)
        session = SESSION_DATA.get_session(request)

        context = self.get_context_data()
        return self.render_to_response(context)

    @check_session
    def post(self, request, session):
        print(request.POST)

        result, param_result = simulate_energysystem()

        print('Results:', results)
        print('Params:', param_result)

        return HttpResponse(json.dumps({'hallo': 'test'}))

    @staticmethod
    def prepare_layer_data():

        layer_data = {}

        # create layer list for AJAX data urls
        layer_list = {l:d['show'] for ls in LAYER_METADATA.values() for l, d in ls.items()}
        layer_data['layer_list'] = layer_list

        # create JSON for layer styles
        layer_style = {l:a['style'] for v in LAYER_METADATA.values() for l, a in v.items()}
        layer_style.update(LAYER_DEFAULT_STYLES)
        layer_data['layer_style'] = json.dumps(layer_style)

        # update layer and layer group labels using labels config
        layer_metadata = OrderedDict()
        for (grp, layers) in LAYER_METADATA.items():
            layer_metadata.update({grp: {'layers': layers}})
            layer_metadata[grp]['title'] = LABELS['layer_groups'][grp]['title']
            layer_metadata[grp]['text'] = LABELS['layer_groups'][grp]['text']
            for l, v in layers.items():
                layer_metadata[grp]['layers'][l]['title'] = LABELS['layers'][l]['title']
                layer_metadata[grp]['layers'][l]['text'] = LABELS['layers'][l]['text']

        # create layer groups for layer menu using layers config
        layer_groups = layer_metadata.copy()
        for grp, layers in layer_metadata.items():
            layer_groups[grp]['layers'] = LayerGroupForm(layers=layers['layers'])
        layer_data['layer_groups'] = layer_groups

        return layer_data

    @staticmethod
    def prepare_component_data():

        component_data = {}
        # update component and component group labels using labels config
        comp_metadata = OrderedDict()
        for (grp, comps) in ESYS_COMPONENTS_METADATA.items():
            comp_metadata.update({grp: {'comps': comps}})
            comp_metadata[grp]['title'] = LABELS['component_groups'][grp]['title']
            comp_metadata[grp]['text'] = LABELS['component_groups'][grp]['text']
            for l, v in comps.items():
                comp_metadata[grp]['comps'][l]['title'] = LABELS['components'][l]['title']
                comp_metadata[grp]['comps'][l]['text'] = LABELS['components'][l]['text']

        # create component groups for esys menu using components config
        comp_groups = comp_metadata.copy()
        for grp, comps in comp_groups.items():
            comp_groups[grp]['comps'] = ComponentGroupForm(components=comps['comps'])
        component_data['comp_groups'] = comp_groups

        return component_data

    @staticmethod
    def prepare_label_data():
        return {'panels':  LABELS['panels']}


class SourcesView(TemplateView):
    template_name = 'stemp_abw/sources.html'
