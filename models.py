from django.db import models
# from djgeojson.fields import PointField
from django.contrib.gis.db import models as geomodels
# from geoalchemy2.types import Geometry
from stemp_abw import oep_models
from stemp_abw.app_settings import LABELS
import sqlahelper


# class MapLayers(models.Model):
#     model_label = models.CharField(max_length=20)
#     caption = models.CharField(max_length=50)
#     description = models.CharField(max_length=100)

####################
### Layer models ###
####################

class LayerModel(models.Model):

    @property
    def name(self):
        raise NotImplementedError

    # TODO: This can be chucked away?
    @property
    def popup_content(self):
        #return '<p>'+self.name+'</p>'
        return 'popup/'

    class Meta:
        abstract = True

    def __str__(self):
        return '{name} Objekt ({pk_name}={pk})'.format(
            name=LABELS['layers'][self.name]['title'],
            pk_name=self._meta.pk.name,
            pk=self.pk)


# TODO: This model is for testing puorposes only, to be removed!
class HvMvSubst(LayerModel):
    name = 'subst'
    geom = geomodels.PointField(srid=4326, null=True)
    subst_id = models.IntegerField()

    # @property
    # def popup_content(self):
    #     return '<p>{text}</p>'.format(
    #         text='Substation ' + str(self.subst_id))

    # def get_data(self):
    #     session = sqlahelper.get_session()
    #     query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
    #     data = query.all()


class RpAbwBound(LayerModel):
    name = 'rpabw'
    geom = geomodels.MultiLineStringField(srid=4326, null=True)

    # @property
    # def popup_content(self):
    #     return '<p>{text}</p>'.format(
    #         text='PR ABW Grenze des Planungsraumes')


class RegMun(LayerModel):
    name = 'reg_mun'
    ags = models.IntegerField(primary_key=True)
    geom = geomodels.MultiPolygonField(srid=3035)
    gen = models.CharField(max_length=254)
    pop_km2 = models.FloatField(null=True)


class RegMunPopDensity(RegMun):
    """This is a proxy model for RegMun which got same relations to the DB
    table but changes the model name. This is needed to load the appropriate
    DetailView when clicking on a map feature (serialized property in the data
    view).
    See Also: https://github.com/rl-institut/WAM_APP_stemp_abw/issues/2
    """
    name = 'reg_mun_pop_density'

    class Meta:
        proxy = True


class RegWaterProtArea(LayerModel):
    name = 'reg_water_prot_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    gebietsnam = models.CharField(max_length=254, null=True)
    gebietsnum = models.CharField(max_length=254, null=True)
    rechtsgrun = models.CharField(max_length=254, null=True)
    schutzzone = models.CharField(max_length=254, null=True)
    erfassungs = models.CharField(max_length=254, null=True)
    amtsblatt = models.CharField(max_length=254, null=True)


class RegBirdProtArea(LayerModel):
    name = 'reg_bird_prot_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    gebietsnam = models.CharField(max_length=254, null=True)
    gebietsnum = models.CharField(max_length=254, null=True)
    rechtsgrun = models.CharField(max_length=254, null=True)
    erfassungs = models.CharField(max_length=254, null=True)
    info_konta = models.CharField(max_length=254, null=True)


class RegBirdProtAreaB200(LayerModel):
    name = 'reg_bird_prot_area_b200'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegNatureProtArea(LayerModel):
    name = 'reg_nature_prot_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    gebietsnam = models.CharField(max_length=254, null=True)
    gebietsnum = models.CharField(max_length=254, null=True)
    rechtsgrun = models.CharField(max_length=254, null=True)
    schutzzone = models.CharField(max_length=254, null=True)
    erfassungs = models.CharField(max_length=254, null=True)
    info_konta = models.CharField(max_length=254, null=True)


class RegLandscProtAreaParts(LayerModel):
    name = 'reg_landsc_prot_area_parts'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    gebietsnam = models.CharField(max_length=254, null=True)
    gebietsnum = models.CharField(max_length=254, null=True)
    rechtsgrun = models.CharField(max_length=254, null=True)
    erfassungs = models.CharField(max_length=254, null=True)


class RegResidArea(LayerModel):
    name = 'reg_resid_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegResidAreaB500(LayerModel):
    name = 'reg_resid_area_b500'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaFloodProt(LayerModel):
    name = 'reg_prio_area_flood_prot'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    bemerkunge = models.CharField(max_length=254, null=True)
    bezeich_2 = models.CharField(max_length=254, null=True)
    bezeich_3 = models.CharField(max_length=254, null=True)


class RegPrioAreaCult(LayerModel):
    name = 'reg_prio_area_cult'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    bezeich_2 = models.CharField(max_length=254, null=True)


class RegForest(LayerModel):
    name = 'reg_forest'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegFFHProtArea(LayerModel):
    name = 'reg_ffh_prot_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    gebietsnam = models.CharField(max_length=254, null=True)
    gebietsnum = models.CharField(max_length=254, null=True)
    rechtsgrun = models.CharField(max_length=254, null=True)
    erfassungs = models.CharField(max_length=254, null=True)
    info_konta = models.CharField(max_length=254, null=True)


class RegResidAreaB1000(LayerModel):
    name = 'reg_resid_area_b1000'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaWEC(LayerModel):
    name = 'reg_prio_area_wec'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    bezeich_2 = models.CharField(max_length=254, null=True)
    bezeich_3 = models.CharField(max_length=254, null=True)


class GenWEC(LayerModel):
    name = 'gen_wec'
    geom = geomodels.MultiPointField(srid=3035, null=True)


class RegDeadZoneHard(LayerModel):
    name = 'reg_dead_zone_hard'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegDeadZoneSoft(LayerModel):
    name = 'reg_dead_zone_soft'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


# TODO: New layers below -> insert data into DB!

class RegFFHProtAreaB(LayerModel):
    name = 'reg_ffh_prot_area_b'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegLandscProtArea(LayerModel):
    name = 'reg_landsc_prot_area'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegNaturePark(LayerModel):
    name = 'reg_nature_park'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegBioReserve(LayerModel):
    name = 'reg_bio_reserve'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegRetentAreaEcosys(LayerModel):
    name = 'reg_retent_area_ecosys'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaNature(LayerModel):
    name = 'reg_prio_area_nature'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegNatureMonum(LayerModel):
    name = 'reg_nature_monum'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaWater(LayerModel):
    name = 'reg_prio_area_water'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaAgri(LayerModel):
    name = 'reg_prio_area_agri'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegRetentAreaAgri(LayerModel):
    name = 'reg_retent_area_agri'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegPrioAreaRes(LayerModel):
    name = 'reg_prio_area_res'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)
    bezeich_2 = models.CharField(max_length=254, null=True)
    bezeich_3 = models.CharField(max_length=254, null=True)


class RegInfrasRailway(LayerModel):
    name = 'reg_infras_railway'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegInfrasRoad(LayerModel):
    name = 'reg_infras_road'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegInfrasHvgrid(LayerModel):
    name = 'reg_infras_hvgrid'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class RegInfrasAviation(LayerModel):
    name = 'reg_infras_aviation'
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


# ###################
# ### Data models ###
# ###################
# The following tables contain initial data only, data that result from
# adjustments in the tool are not saved to these tables.

class MunData(models.Model):
    """Statistical data of municipalities

    Attributes
    ----------
    ags :
        Municipality key (Amtlicher Gemeindeschlüssel),
        refers to :class:`stemp_abw.models.RegMun`
    area :
        Total area in square kilometers

    pop_2011 :
        Population (2011) according to Zensus
    pop_2017 :
        Population (2017) according to GV-ISys
    pop_2030 :
        Population (2030) forecast according to MLV Sachsen-Anhalt
    pop_2050 :
        Population (2050), linearly extrapolated using 2017 and 2030

    gen_count_wind :
        Count of wind turbines
    gen_count_pv_roof_small :
        Count of small (<=30 kVA) roof-mounted PV systems
    gen_count_pv_roof_large :
        Count of large (>30 kVA, <=300 kVA) roof-mounted PV systems
    gen_count_pv_ground :
        Count of ground-mounted PV systems (>300 kVA)
    gen_count_hydro :
        Count of run-of-river systems
    gen_count_bio :
        Count of biogas/biomass systems
    gen_count_steam_turbine :
        Count of steam turbines
    gen_count_combined_cycle :
        Count of combined cycle systems
    gen_count_sewage_landfill_gas :
        Count of sewage/landfill gas systems
    gen_count_storage :
        Count of storages

    gen_capacity_wind :
        Total nominal power of wind turbines in MVA
    gen_capacity_pv_roof_small :
        Total nominal power of small roof-mounted PV systems in MW
    gen_capacity_pv_roof_large :
        Total nominal power of large roof-mounted PV systems in MW
    gen_capacity_pv_ground :
        Total nominal power of ground-mounted PV systems in MW
    gen_capacity_hydro :
        Total nominal power of run-of-river systems  in MW
    gen_capacity_bio :
        Total nominal power of biogas/biomass PV systems  in MW
    gen_capacity_steam_turbine :
        Total nominal power of steam turbine systems in MW
    gen_capacity_combined_cycle :
        Total nominal power of combined cycle systems in MW
    gen_capacity_sewage_landfill_gas :
        Total nominal power of sewage/landfill gas systems in MW
    gen_capacity_storage :
        Total storage capacity of storages in MWh

    gen_el_energy_wind :
        Annual el. energy fed in by wind turbines in MWh
    gen_el_energy_pv_roof :
        Annual el. energy fed in by roof-mounted PV systems in MWh
    gen_el_energy_pv_ground:
        Annual el. energy fed in by ground-mounted PV systems in MWh
    gen_el_energy_hydro :
        Annual el. energy fed in by run-of-river systems in MWh

    dem_el_capacity_hh :
        El. peak demand of households in MW
    dem_el_capacity_rca :
        El. peak demand of retail, commercial and agricultural sector in MW
    dem_el_capacity_ind :
        El. peak demand of industry in MW
    dem_th_capacity_hh :
        Heat peak demand of households in MW
    dem_th_capacity_rca :
        Heat peak demand of retail, commercial and agricultural sector in MW
    dem_th_capacity_ind :
        Heat peak demand of industry in MW

    dem_el_energy_hh :
        Annual el. energy consumed by households in MWh
    dem_el_energy_rca :
        Annual el. energy consumed by retail, commercial and agricultural
        sector in MWh
    dem_el_energy_ind :
        Annual el. energy consumed by industry in MWh
    dem_th_energy_hh :
        Annual heat consumed by households in MWh
    dem_th_energy_rca :
        Annual heat consumed by retail, commercial and agricultural sector in
        MWh
    dem_th_energy_ind :
        Annual heat consumed by industry in MWh
    """
    """"""
    ags = models.OneToOneField(RegMun, primary_key=True, on_delete=models.DO_NOTHING)
    area = models.FloatField(null=True)

    pop_2011 = models.IntegerField(null=True)
    pop_2017 = models.IntegerField(null=True)
    pop_2030 = models.IntegerField(null=True)
    pop_2050 = models.IntegerField(null=True)
    
    gen_count_wind = models.FloatField(null=True)
    gen_count_pv_roof_small = models.FloatField(null=True)
    gen_count_pv_roof_large = models.FloatField(null=True)
    gen_count_pv_ground = models.FloatField(null=True)
    gen_count_hydro = models.FloatField(null=True)
    gen_count_bio = models.FloatField(null=True)
    gen_count_steam_turbine = models.FloatField(null=True)
    gen_count_combined_cycle = models.FloatField(null=True)
    gen_count_sewage_landfill_gas = models.FloatField(null=True)
    gen_count_storage = models.FloatField(null=True)

    gen_capacity_wind = models.FloatField(null=True)
    gen_capacity_pv_roof_small = models.FloatField(null=True)
    gen_capacity_pv_roof_large = models.FloatField(null=True)
    gen_capacity_pv_ground = models.FloatField(null=True)
    gen_capacity_hydro = models.FloatField(null=True)
    gen_capacity_bio = models.FloatField(null=True)
    gen_capacity_steam_turbine = models.FloatField(null=True)
    gen_capacity_combined_cycle = models.FloatField(null=True)
    gen_capacity_sewage_landfill_gas = models.FloatField(null=True)
    gen_capacity_storage = models.FloatField(null=True)

    gen_el_energy_wind = models.FloatField(null=True)
    gen_el_energy_pv_roof = models.FloatField(null=True)
    gen_el_energy_pv_ground = models.FloatField(null=True)
    gen_el_energy_hydro = models.FloatField(null=True)

    dem_el_capacity_hh = models.FloatField(null=True)
    dem_el_capacity_rca = models.FloatField(null=True)
    dem_el_capacity_ind = models.FloatField(null=True)
    dem_th_capacity_hh = models.FloatField(null=True)
    dem_th_capacity_rca = models.FloatField(null=True)
    dem_th_capacity_ind = models.FloatField(null=True)

    dem_el_energy_hh = models.FloatField(null=True)
    dem_el_energy_rca = models.FloatField(null=True)
    dem_el_energy_ind = models.FloatField(null=True)
    dem_th_energy_hh = models.FloatField(null=True)
    dem_th_energy_rca = models.FloatField(null=True)
    dem_th_energy_ind = models.FloatField(null=True)


class FeedinTs(models.Model):
    """Renewable feedin timeseries (normalized)

    Attributes
    ----------
    id : DB id
    timestamp : timestamp
    ags : Municipality key (Amtlicher Gemeindeschlüssel)
        refers to :class:`stemp_abw.models.RegMun`
    pv_ground : Photovoltaics (ground-mounted systems)
    pv_roof : Photovoltaics (roof-mounted systems)
    hydro : Run-of-river plants
    wind_sq : Wind turbines (status quo)
    wind_fs : Wind turbines (future scenarios)
    """
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(db_index=True)
    ags = models.ForeignKey(RegMun, on_delete=models.DO_NOTHING)
    pv_ground = models.FloatField(blank=True, null=True)
    pv_roof = models.FloatField(blank=True, null=True)
    hydro = models.FloatField(blank=True, null=True)
    wind_sq = models.FloatField(blank=True, null=True)
    wind_fs = models.FloatField(blank=True, null=True)


class Powerplant(models.Model):
    """Power plants (status quo)

    Attributes
    ----------
    id : DB id
    ags : Municipality key (Amtlicher Gemeindeschlüssel)
        refers to :class:`stemp_abw.models.RegMun`
    capacity : Nominal power in MVA
    chp : indicates if plant is of type CHP (combined heat and power)
    com_month : Month of commissioning
    com_year : Year of commissioning
    comment : Comment
    decom_month : Month of decommissioning
    decom_year : Year of decommissioning
    efficiency : Efficiency
    energy_source_level_1 : Renewable or conventional
    energy_source_level_2 : Indicates energy source
    energy_source_level_3 : More specific energy source
    geometry : Geometry, SRID: EPSG:4326 (WGS84)
    technology : Technology
    thermal_capacity : Nominal thermal nominal power, if applicable
    coastdat2 : No. of weather cell of coastdat2
    capacity_in : Capacity of inflow
    federal_state : Abbreviation of federal state name (2 letters according to ISO 3166-2:DE)

    Notes
    -----
    Most of the attributes correspond to the OPSD dataset, some were added by reegis.
    """
    id = models.BigIntegerField(primary_key=True)
    ags = models.ForeignKey(RegMun, on_delete=models.DO_NOTHING)
    capacity = models.FloatField(blank=True, null=True)
    chp = models.TextField(blank=True, null=True)
    com_month = models.FloatField(blank=True, null=True)
    com_year = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    decom_month = models.BigIntegerField(blank=True, null=True)
    decom_year = models.BigIntegerField(blank=True, null=True)
    efficiency = models.FloatField(blank=True, null=True)
    energy_source_level_1 = models.TextField(blank=True, null=True)
    energy_source_level_2 = models.TextField(blank=True, null=True)
    energy_source_level_3 = models.TextField(blank=True, null=True)
    geometry = geomodels.PointField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    technology = models.TextField(blank=True, null=True)
    thermal_capacity = models.FloatField(blank=True, null=True)
    coastdat2 = models.FloatField(blank=True, null=True)
    capacity_in = models.FloatField(blank=True, null=True)
    federal_state = models.TextField(blank=True, null=True)
