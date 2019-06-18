from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, View
from djgeojson.views import GeoJSONLayerView, GeoJSONResponseMixin

import stemp_abw.models as models
from wam.settings import SESSION_DATA


#########################
### GeoJSONLayerViews ###
#########################
class RpAbwBoundData(GeoJSONLayerView):
    model = models.RpAbwBound
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegMunData(GeoJSONLayerView):
    model = models.RegMun
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegMunPopData(GeoJSONLayerView):
    model = models.RegMunPop
    properties = [
        'name',
        'gen',
        'pop',
        'pop_region'
    ]


class RegMunPopDensityData(GeoJSONLayerView):
    model = models.RegMunPopDensity
    properties = [
        'name',
        'gen',
        'pop_density',
        'pop_density_region'
    ]


class RegMunEnergyReElDemShareData(GeoJSONLayerView):
    model = models.RegMunEnergyReElDemShare
    properties = [
        'name',
        'gen',
        'energy_re_el_dem_share',
        'energy_re_el_dem_share_region'
    ]


class RegMunGenEnergyReData(GeoJSONLayerView):
    model = models.RegMunGenEnergyRe
    properties = [
        'name',
        'gen',
        'gen_energy_re',
        'gen_energy_re_region'
    ]


class RegMunGenEnergyRePerCapitaData(GeoJSONLayerView):
    model = models.RegMunGenEnergyRePerCapita
    properties = [
        'name',
        'gen',
        'gen_energy_re_per_capita',
        'gen_energy_re_per_capita_region'
    ]


class RegMunGenEnergyReDensityData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDensity
    properties = [
        'name',
        'gen',
        'gen_energy_re_density',
        'gen_energy_re_density_region'
    ]


class RegMunGenCapReData(GeoJSONLayerView):
    model = models.RegMunGenCapRe
    properties = [
        'name',
        'gen',
        'gen_cap_re',
        'gen_cap_re_region'
    ]


class RegMunGenCapReDensityData(GeoJSONLayerView):
    model = models.RegMunGenCapReDensity
    properties = [
        'name',
        'gen',
        'gen_cap_re_density',
        'gen_cap_re_density_region'
    ]


class RegMunGenCountWindDensityData(GeoJSONLayerView):
    model = models.RegMunGenCountWindDensity
    properties = [
        'name',
        'gen',
        'gen_count_wind_density',
        'gen_count_wind_density_region'
    ]


class RegMunDemElEnergyData(GeoJSONLayerView):
    model = models.RegMunDemElEnergy
    properties = [
        'name',
        'gen',
        'dem_el_energy',
        'dem_el_energy_region'
    ]


class RegMunDemElEnergyPerCapitaData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyPerCapita
    properties = [
        'name',
        'gen',
        'dem_el_energy_per_capita'
    ]


class RegMunDemThEnergyData(GeoJSONLayerView):
    model = models.RegMunDemThEnergy
    properties = [
        'name',
        'gen',
        'dem_th_energy'
    ]


class RegMunDemThEnergyPerCapitaData(GeoJSONLayerView):
    model = models.RegMunDemThEnergyPerCapita
    properties = [
        'name',
        'gen',
        'dem_th_energy_per_capita'
    ]


class RegWaterProtAreaData(GeoJSONLayerView):
    model = models.RegWaterProtArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaData(GeoJSONLayerView):
    model = models.RegBirdProtArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBirdProtAreaB200Data(GeoJSONLayerView):
    model = models.RegBirdProtAreaB200
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureProtAreaData(GeoJSONLayerView):
    model = models.RegNatureProtArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegLandscProtAreaPartsData(GeoJSONLayerView):
    model = models.RegLandscProtAreaParts
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegResidAreaData(GeoJSONLayerView):
    model = models.RegResidArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegResidAreaB500Data(GeoJSONLayerView):
    model = models.RegResidAreaB500
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaFloodProtData(GeoJSONLayerView):
    model = models.RegPrioAreaFloodProt
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaCultData(GeoJSONLayerView):
    model = models.RegPrioAreaCult
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegForestData(GeoJSONLayerView):
    model = models.RegForest
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegFFHProtAreaData(GeoJSONLayerView):
    model = models.RegFFHProtArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegResidAreaB1000Data(GeoJSONLayerView):
    model = models.RegResidAreaB1000
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 4


class RegPrioAreaWECData(GeoJSONLayerView):
    model = models.RegPrioAreaWEC
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class GenWECData(GeoJSONLayerView):
    model = models.GenWEC
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class GenPVGroundData(GeoJSONLayerView):
    model = models.GenPVGround
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegDeadZoneHardData(GeoJSONLayerView):
    model = models.RegDeadZoneHard
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegDeadZoneSoftData(GeoJSONLayerView):
    model = models.RegDeadZoneSoft
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegFFHProtAreaBData(GeoJSONLayerView):
    model = models.RegFFHProtAreaB
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegLandscProtAreaData(GeoJSONLayerView):
    model = models.RegLandscProtArea
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureParkData(GeoJSONLayerView):
    model = models.RegNaturePark
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegBioReserveData(GeoJSONLayerView):
    model = models.RegBioReserve
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegRetentAreaEcosysData(GeoJSONLayerView):
    model = models.RegRetentAreaEcosys
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaNatureData(GeoJSONLayerView):
    model = models.RegPrioAreaNature
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegNatureMonumData(GeoJSONLayerView):
    model = models.RegNatureMonum
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaWaterData(GeoJSONLayerView):
    model = models.RegPrioAreaWater
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaAgriData(GeoJSONLayerView):
    model = models.RegPrioAreaAgri
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegRetentAreaAgriData(GeoJSONLayerView):
    model = models.RegRetentAreaAgri
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegPrioAreaResData(GeoJSONLayerView):
    model = models.RegPrioAreaRes
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasRailwayData(GeoJSONLayerView):
    model = models.RegInfrasRailway
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasRoadData(GeoJSONLayerView):
    model = models.RegInfrasRoad
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasHvgridData(GeoJSONLayerView):
    model = models.RegInfrasHvgrid
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class RegInfrasAviationData(GeoJSONLayerView):
    model = models.RegInfrasAviation
    properties = ['name']
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
        return super(GeoJSONSingleDatasetLayerView, self) \
            .render_to_response(context, **response_kwargs)


class REPotentialAreasData(GeoJSONSingleDatasetLayerView):
    model = models.REPotentialAreas
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


########################
# Results serial views #
########################
class SimulationStatus(View):
    model = None

    @staticmethod
    @never_cache
    def get(request):
        session = SESSION_DATA.get_session(request)
        results = session.simulation.results
        return JsonResponse({'sim_status': results.status}, safe=True)


class ResultChartsData(View):
    model = None

    @staticmethod
    @never_cache
    def get(request):
        session = SESSION_DATA.get_session(request)
        results = session.simulation.results
        return JsonResponse(results.get_result_charts_data(), safe=True)


class RegMunEnergyReElDemShareResultData(GeoJSONLayerView):
    model = models.RegMunEnergyReElDemShareResult
    properties = [
        'name',
        'gen',
        'energy_re_el_dem_share_result'
    ]


class RegMunGenEnergyReResultData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReResult
    properties = [
        'name',
        'gen',
        'gen_energy_re_result'
    ]


class RegMunGenEnergyReDensityResultData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDensityResult
    properties = [
        'name',
        'gen',
        'gen_energy_re_density_result'
    ]


class RegMunGenCapReResultData(GeoJSONLayerView):
    model = models.RegMunGenCapReResult
    properties = [
        'name',
        'gen',
        'gen_cap_re_result'
    ]


class RegMunGenCapReDensityResultData(GeoJSONLayerView):
    model = models.RegMunGenCapReDensityResult
    properties = [
        'name',
        'gen',
        'gen_cap_re_density_result'
    ]


class RegMunGenCountWindDensityResultData(GeoJSONLayerView):
    model = models.RegMunGenCountWindDensityResult
    properties = [
        'name',
        'gen',
        'gen_count_wind_density_result'
    ]


class RegMunDemElEnergyResultData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyResult
    properties = [
        'name',
        'gen',
        'dem_el_energy_result'
    ]


class RegMunDemElEnergyPerCapitaResultData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyPerCapitaResult
    properties = [
        'name',
        'gen',
        'dem_el_energy_per_capita_result'
    ]


################################
# Results serial views (DELTA) #
################################

class RegMunEnergyReElDemShareResultDeltaData(GeoJSONLayerView):
    model = models.RegMunEnergyReElDemShareDeltaResult
    properties = [
        'name',
        'gen',
        'energy_re_el_dem_share_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunGenEnergyReResultDeltaData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDeltaResult
    properties = [
        'name',
        'gen',
        'gen_energy_re_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunGenEnergyReDensityResultDeltaData(GeoJSONLayerView):
    model = models.RegMunGenEnergyReDensityDeltaResult
    properties = [
        'name',
        'gen',
        'gen_energy_re_density_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunGenCapReResultDeltaData(GeoJSONLayerView):
    model = models.RegMunGenCapReDeltaResult
    properties = [
        'name',
        'gen',
        'gen_cap_re_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunGenCapReDensityResultDeltaData(GeoJSONLayerView):
    model = models.RegMunGenCapReDensityDeltaResult
    properties = [
        'name',
        'gen',
        'gen_cap_re_density_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunGenCountWindDensityResultDeltaData(GeoJSONLayerView):
    model = models.RegMunGenCountWindDensityDeltaResult
    properties = [
        'name',
        'gen',
        'gen_count_wind_density_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunDemElEnergyResultDeltaData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyDeltaResult
    properties = [
        'name',
        'gen',
        'dem_el_energy_result_delta'
    ]
    geometry_field = 'geom_centroid'


class RegMunDemElEnergyPerCapitaResultDeltaData(GeoJSONLayerView):
    model = models.RegMunDemElEnergyPerCapitaDeltaResult
    properties = [
        'name',
        'gen',
        'dem_el_energy_per_capita_result_delta'
    ]
    geometry_field = 'geom_centroid'
