import stemp_abw.models as models
from djgeojson.views import GeoJSONLayerView


#########################
### GeoJSONLayerViews ###
#########################
class SubstData(GeoJSONLayerView):
    model = models.HvMvSubst
    # TODO: 'name' is used to load popup content in JS from view (build url).
    # TODO: Find smarter approach!
    properties = ['popup_content', 'name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


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


class RegMunStatsData(GeoJSONLayerView):
    model = models.RegMunStats
    properties = ['popup_content',
                  'name',
                  'gen',
                  'pop',
                  'pop_density',
                  'gen_capacity_re',
                  'gen_energy_re',
                  'gen_energy_re_per_capita',
                  'gen_energy_re_density',
                  'dem_el_energy',
                  'dem_el_energy_per_capita',
                  'dem_th_energy',
                  'dem_th_energy_per_capita',
                  'energy_re_el_dem_share']
    srid = 4326
    geometry_field = 'geom'
    precision = 3


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

