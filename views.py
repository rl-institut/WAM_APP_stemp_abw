from django.views.generic import TemplateView, DetailView
from djgeojson.views import GeoJSONLayerView
import sqlahelper
from stemp_abw import oep_models
from .oep_models import WnAbwEgoDpHvmvSubstation
from .models import HvMvSubst


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

class MapData(GeoJSONLayerView):
    model = HvMvSubst
    properties = ['popup_content', 'name']
    srid = 4326


class MapView(TemplateView):
    label = 'Substations'
    template_name = 'stemp_abw/map.html'
    context_object_name = 'subst'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['label'] = self.label
        return context


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

# class MapNew(TemplateView):
#     template_name = 'stemp_abw/map2.html'

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
