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
    ags = models.OneToOneField(RegMun, primary_key=True, on_delete=models.DO_NOTHING)
    area = models.FloatField(null=True)

    pop_2011 = models.FloatField(null=True)
    pop_2017 = models.FloatField(null=True)
    pop_2030 = models.FloatField(null=True)
    pop_2050 = models.FloatField(null=True)
    
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

    dem_el_energy_hh = models.FloatField(null=True)
    dem_el_energy_rca = models.FloatField(null=True)
    dem_el_energy_ind = models.FloatField(null=True)
    dem_th_energy_hh = models.FloatField(null=True)
    dem_th_energy_rca = models.FloatField(null=True)
    dem_th_energy_ind = models.FloatField(null=True)


class FeedinTs(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(db_index=True)
    ags = models.ForeignKey(RegMun, on_delete=models.DO_NOTHING)
    pv_ground = models.FloatField(blank=True, null=True)
    pv_roof = models.FloatField(blank=True, null=True)
    hydro = models.FloatField(blank=True, null=True)
    wind_sq = models.FloatField(blank=True, null=True)
    wind_fs = models.FloatField(blank=True, null=True)


class Powerplant(models.Model):
    """Power plants (status quo)"""
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
