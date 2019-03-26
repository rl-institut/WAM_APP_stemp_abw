import stemp_abw.models as models
from djgeojson.views import GeoJSONLayerView


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


###################
# ESys area views #
###################
# TODO: Replace with dynamic classes
class REPotentialAreas1Data(GeoJSONLayerView):
    model = models.REPotentialAreas1
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class REPotentialAreas2Data(GeoJSONLayerView):
    model = models.REPotentialAreas2
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5

class REPotentialAreas3Data(GeoJSONLayerView):
    model = models.REPotentialAreas3
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class REPotentialAreas4Data(GeoJSONLayerView):
    model = models.REPotentialAreas4
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5

class REPotentialAreas5Data(GeoJSONLayerView):
    model = models.REPotentialAreas5
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5


class REPotentialAreas6Data(GeoJSONLayerView):
    model = models.REPotentialAreas6
    properties = ['name']
    srid = 4326
    geometry_field = 'geom'
    precision = 5
