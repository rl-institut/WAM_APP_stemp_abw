from django.views.generic import TemplateView, DetailView
from djgeojson.views import GeoJSONLayerView
from django import forms
import sqlahelper
from stemp_abw import oep_models
from .oep_models import WnAbwEgoDpHvmvSubstation
from .models import HvMvSubst, OsmPowerGen, RpAbwBound
from .forms import LayerSelectForm
from .widgets import LayerSelectWidget
from .app_settings import LAYER_METADATA,LAYER_DEFAULT_STYLES
from django.core import serializers
import json
from collections import OrderedDict


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


# def map(request):
#     #question = get_object_or_404(Question, pk=question_id)
#
#     session = sqlahelper.get_session()
#     query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
#     data = query.all()
#     # for id, row in data.iterrows():
#     #     HvMvSubstation(
#     #         subst_id=row['subst_id'],
#     #         geom=row['geom']
#     #     )#.save()
#
#     return render(request, 'stemp_abw/map.html', {'data': data}, )

class SubstData(GeoJSONLayerView):
    model = HvMvSubst
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'


class OsmPowerGenData(GeoJSONLayerView):
    model = OsmPowerGen
    properties = ['popup_content']
    srid = 4326
    geometry_field = 'geom'


class RpAbwBoundData(GeoJSONLayerView):
    model = RpAbwBound
    properties = ['popup_content']
    srid = 4326
    geometry_field = 'geom'
    precision = 5   # float
    #simplify = 0.02  # generalization


class MapView(TemplateView):
    template_name = 'stemp_abw/map.html'
    layer_data = {}

    def __init__(self):
        super(MapView, self).__init__()
        self.prepare_layer_data()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(self.layer_data)
        # context['label'] = self.label

        return context

    def prepare_layer_data(self):

        #groups = {grp:{lay for lay in lays.keys()} for grp, lays in LAYER_METADATA.items()}

        # create layer list for AJAX data urls
        layer_list = [l for v in LAYER_METADATA.values() for l in v.keys()]
        self.layer_data['layer_list'] = layer_list

        # create JSON for layer styles
        layer_style = {l:a['style'] for v in LAYER_METADATA.values() for l, a in v.items()}
        layer_style.update(LAYER_DEFAULT_STYLES)
        self.layer_data['layer_style'] = json.dumps(layer_style)

        # create layer groups for layer menu
        layer_groups = OrderedDict()
        for grp, layers in LAYER_METADATA.items():
            layer_groups[grp] = [LayerSelectForm(layers=[l for l in layers.keys()])]
        self.layer_data['layer_groups'] = layer_groups


    # def get_data(self):
    #     return 'result'


    # class Meta:
    #
    #     model = MushroomSpot
    #model = WnAbwEgoDpHvmvSubstation

    # session = sqlahelper.get_session()
    # query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
    # data = query.all()
    # for id, row in data.iterrows():
    #     HvMvSubstation(
    #         subst_id=row['subst_id'],
    #         geom=row['geom']
    #     )#.save()


class HvMvSubstDetailView(DetailView):
    template_name = 'stemp_abw/subst_detail.html'
    model = HvMvSubst
    context_object_name = 'subst'


class HvMvSubstView(TemplateView):
    template_name = 'stemp_abw/subst.html'
    model = HvMvSubst
    context_object_name = 'subst'

    #queryset = qs_results

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['data'] = HvMvSubst.objects.all()
    #     return context
