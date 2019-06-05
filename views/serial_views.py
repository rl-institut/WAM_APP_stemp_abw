import stemp_abw.models as models
from django.views.generic import DetailView, View
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from djgeojson.views import GeoJSONLayerView, GeoJSONResponseMixin
from wam.settings import SESSION_DATA


#########################
### GeoJSONLayerViews ###
#########################
class RpAbwBoundData(GeoJSONLayerView):
    model = models.RpAbwBound
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegMunData(GeoJSONLayerView):
    model = models.RegMun
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegMunPopData(GeoJSONLayerView):
    model = models.RegMunPop
    properties = ['popup_content',
                  'name',
                  'gen',
                  'pop']


class RegMunPopDensityData(GeoJSONLayerView):
    model = models.RegMunPopDensity
    properties = ['popup_content',
                  'name',
                  'gen',
                  'pop_density']


class RegMunEnergyReElDemShareData(GeoJSONLayerView):
    model = models.RegMunEnergyReElDemShare
    properties = ['popup_content',
                  'name',
                  'gen',
                  'energy_re_el_dem_share']


class RegMunGenEnergyReData(GeoJSONLayerView):
    model = models.RegMunGenEnergyRe
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_energy_re']


class RegMunGenEnergyRePerCapitaData(GeoJSONLayerView):
    model = models.RegMunGenEnergyRePerCapita
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_energy_re_per_capita']


class RegMunGenEnergyReDensityData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDensity
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_energy_re_density']


class RegMunGenCapReData(GeoJSONLayerView):
    model = models.RegMunGenCapRe
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_cap_re']


class RegMunGenCapReDensityData(GeoJSONLayerView):
    model = models.RegMunGenCapReDensity
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_cap_re_density']


class RegMunGenCountWindDensityData(GeoJSONLayerView):
    model = models.RegMunGenCountWindDensity
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_count_wind_density']


class RegMunDemElEnergyData(GeoJSONLayerView):
    model = models.RegMunDemElEnergy
    properties = ['popup_content',
                  'name',
                  'gen',
                  'dem_el_energy']


class RegMunDemElEnergyPerCapitaData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyPerCapita
    properties = ['popup_content',
                  'name',
                  'gen',
                  'dem_el_energy_per_capita']


class RegMunDemThEnergyData(GeoJSONLayerView):
    model = models.RegMunDemThEnergy
    properties = ['popup_content',
                  'name',
                  'gen',
                  'dem_th_energy']


class RegMunDemThEnergyPerCapitaData(GeoJSONLayerView):
    model = models.RegMunDemThEnergyPerCapita
    properties = ['popup_content',
                  'name',
                  'gen',
                  'dem_th_energy_per_capita']


class RegWaterProtAreaData(GeoJSONLayerView):
    model = models.RegWaterProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaData(GeoJSONLayerView):
    model = models.RegBirdProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaB200Data(GeoJSONLayerView):
    model = models.RegBirdProtAreaB200
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureProtAreaData(GeoJSONLayerView):
    model = models.RegNatureProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegLandscProtAreaPartsData(GeoJSONLayerView):
    model = models.RegLandscProtAreaParts
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegResidAreaData(GeoJSONLayerView):
    model = models.RegResidArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegResidAreaB500Data(GeoJSONLayerView):
    model = models.RegResidAreaB500
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaFloodProtData(GeoJSONLayerView):
    model = models.RegPrioAreaFloodProt
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaCultData(GeoJSONLayerView):
    model = models.RegPrioAreaCult
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegForestData(GeoJSONLayerView):
    model = models.RegForest
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegFFHProtAreaData(GeoJSONLayerView):
    model = models.RegFFHProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegResidAreaB1000Data(GeoJSONLayerView):
    model = models.RegResidAreaB1000
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaWECData(GeoJSONLayerView):
    model = models.RegPrioAreaWEC
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class GenWECData(GeoJSONLayerView):
    model = models.GenWEC
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class GenPVGroundData(GeoJSONLayerView):
    model = models.GenPVGround
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegDeadZoneHardData(GeoJSONLayerView):
    model = models.RegDeadZoneHard
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegDeadZoneSoftData(GeoJSONLayerView):
    model = models.RegDeadZoneSoft
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegFFHProtAreaBData(GeoJSONLayerView):
    model = models.RegFFHProtAreaB
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegLandscProtAreaData(GeoJSONLayerView):
    model = models.RegLandscProtArea
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureParkData(GeoJSONLayerView):
    model = models.RegNaturePark
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBioReserveData(GeoJSONLayerView):
    model = models.RegBioReserve
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegRetentAreaEcosysData(GeoJSONLayerView):
    model = models.RegRetentAreaEcosys
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaNatureData(GeoJSONLayerView):
    model = models.RegPrioAreaNature
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureMonumData(GeoJSONLayerView):
    model = models.RegNatureMonum
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaWaterData(GeoJSONLayerView):
    model = models.RegPrioAreaWater
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaAgriData(GeoJSONLayerView):
    model = models.RegPrioAreaAgri
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegRetentAreaAgriData(GeoJSONLayerView):
    model = models.RegRetentAreaAgri
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaResData(GeoJSONLayerView):
    model = models.RegPrioAreaRes
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasRailwayData(GeoJSONLayerView):
    model = models.RegInfrasRailway
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasRoadData(GeoJSONLayerView):
    model = models.RegInfrasRoad
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasHvgridData(GeoJSONLayerView):
    model = models.RegInfrasHvgrid
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasAviationData(GeoJSONLayerView):
    model = models.RegInfrasAviation
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


###############################
# GeoJSON serial detail views #
###############################

class GeoJSONSingleDatasetLayerView(GeoJSONResponseMixin, DetailView):
    """View for single objects of djgeojson's GeoJSON response

    Modified version of GeoJSONResponseMixin - filter queryset before creating
    GeoJSON response.
    """
    def render_to_response(self, context, **response_kwargs):
        self.queryset = self.model.objects.filter(id=context['object'].id)
        return super(GeoJSONSingleDatasetLayerView, self)\
            .render_to_response(context, **response_kwargs)


class REPotentialAreasData(GeoJSONSingleDatasetLayerView):
    model = models.REPotentialAreas
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


########################
# Results serial views #
########################

class ResultChartsData(View):
    model = None

    @staticmethod
    @never_cache
    def get(request):
        session = SESSION_DATA.get_session(request)
        results = session.simulation.results
        if results.is_up_to_date:
            return JsonResponse(results.get_panel_results(), safe=True)
        else:
            return JsonResponse(None, safe=False)


# TODO: Remove/alter after test
class RegMunPopResultData(GeoJSONLayerView):
    model = models.RegMunPopResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'pop_result']


# TODO: Remove/alter after test
class RegMunPopDensityResultData(GeoJSONLayerView):
    model = models.RegMunPopDensityResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'pop_density_result']


class RegMunEnergyReElDemShareResultData(GeoJSONLayerView):
    model = models.RegMunEnergyReElDemShareResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'energy_re_el_dem_share_result']

class RegMunGenEnergyReResultData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_energy_re_result']


class RegMunGenEnergyReDensityResultData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDensityResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_energy_re_density_result']


class RegMunGenCapReResultData(GeoJSONLayerView):
    model = models.RegMunGenCapReResult
    properties = ['popup_content',
                  'name',
                  'gen',
                  'gen_cap_re_result']