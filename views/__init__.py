from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
import json
from collections import OrderedDict
#import sqlahelper
from stemp_abw.forms import LayerSelectForm
from stemp_abw.app_settings import LAYER_METADATA, LAYER_DEFAULT_STYLES, LABELS
from stemp_abw.simulation import Simulation
from stemp_abw import results

from stemp_abw.views.detail_views import *
from stemp_abw.views.serial_views import *


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'
    layer_data = {}

    def __init__(self):
        super(MapView, self).__init__()
        self.prepare_layer_data()

        self.simulation = Simulation()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(self.layer_data)
        # context['label'] = self.label

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

        return context

    def post(self, request):
        print(request.POST)

        results = self.simulation.run()
        print(results)

        return HttpResponse(json.dumps({'hallo': 'test'}))

    def prepare_layer_data(self):

        # create layer list for AJAX data urls
        layer_list = {l:d['show'] for ls in LAYER_METADATA.values() for l, d in ls.items()}
        self.layer_data['layer_list'] = layer_list

        # create JSON for layer styles
        layer_style = {l:a['style'] for v in LAYER_METADATA.values() for l, a in v.items()}
        layer_style.update(LAYER_DEFAULT_STYLES)
        self.layer_data['layer_style'] = json.dumps(layer_style)

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
            layer_groups[grp]['layers'] = [LayerSelectForm(layers=layers['layers'])]

            #layer_groups[grp] = [LayerSelectForm(layers=layers)]
        self.layer_data['layer_groups'] = layer_groups


class SourcesView(TemplateView):
    template_name = 'stemp_abw/sources.html'


