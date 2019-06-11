import random
from uuid import uuid4

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from stemp_abw.app_settings import LABELS


# class MapLayers(models.Model):
#     model_label = models.CharField(max_length=20)
#     caption = models.CharField(max_length=50)
#     description = models.CharField(max_length=100)

#############################
# Layer models (status quo) #
#############################

class LayerModel(models.Model):

    class Meta:
        abstract = True

    @property
    def name(self):
        raise NotImplementedError

    def __str__(self):
        return '{name} Objekt ({pk_name}={pk})'.format(
            name=LABELS['layers'][self.name]['title'],
            pk_name=self._meta.pk.name,
            pk=self.pk)


class RpAbwBound(LayerModel):
    name = 'rpabw'
    geom = geomodels.MultiLineStringField(srid=4326, null=True)


class RegMun(LayerModel):
    name = 'reg_mun'
    ags = models.IntegerField(primary_key=True)
    geom = geomodels.MultiPolygonField(srid=3035)
    geom_centroid = geomodels.PointField(srid=3035, null=True)
    gen = models.CharField(max_length=254)


class RegMunPop(RegMun):
    """This is a proxy model for RegMun which got same relations to the DB
    table but changes the model name. This is needed to load the appropriate
    DetailView when clicking on a map feature (serialized property in the data
    view).
    - See Also: https://github.com/rl-institut/WAM_APP_stemp_abw/issues/2
    - All other model classes which heir from RegMun work like this.
    """
    name = 'reg_mun_pop'

    class Meta:
        proxy = True

    @property
    def pop(self):
        return self.mundata.pop_2017

    @property
    def pop_region(self):
        pop_region = 0
        for pop_mun in MunData.objects.values('pop_2017'):
            pop_region += pop_mun['pop_2017']
        return pop_region


class RegMunPopDensity(RegMun):
    name = 'reg_mun_pop_density'

    class Meta:
        proxy = True

    @property
    def pop_density(self):
        return round(self.mundata.pop_2017 / self.mundata.area)

    @property
    def pop_density_region(self):
        pop_region = 0
        for pop_mun in MunData.objects.values('pop_2017'):
            pop_region += pop_mun['pop_2017']
        area_region = 0
        for area_mun in MunData.objects.values('area'):
            area_region += area_mun['area']
        return round(pop_region / area_region)


class RegMunGenEnergyRe(RegMun):
    name = 'reg_mun_gen_energy_re'

    class Meta:
        proxy = True

    @property
    def gen_energy_re(self):
        return round((self.mundata.gen_el_energy_wind +
                      self.mundata.gen_el_energy_pv_roof +
                      self.mundata.gen_el_energy_pv_ground +
                      self.mundata.gen_el_energy_hydro) / 1e3)

    @property
    def gen_energy_re_region(self):
        gen_energy_re_region = 0
        for wind_mun in MunData.objects.values('gen_el_energy_wind'):
            gen_energy_re_region += wind_mun['gen_el_energy_wind']
        for roof_mun in MunData.objects.values('gen_el_energy_pv_roof'):
            gen_energy_re_region += roof_mun['gen_el_energy_pv_roof']
        for pv_ground_mun in MunData.objects.values('gen_el_energy_pv_ground'):
            gen_energy_re_region += pv_ground_mun['gen_el_energy_pv_ground']
        for hydro_mun in MunData.objects.values('gen_el_energy_hydro'):
            gen_energy_re_region += hydro_mun['gen_el_energy_hydro']
        return round(gen_energy_re_region / 1e3)


class RegMunDemElEnergy(RegMun):
    name = 'reg_mun_dem_el_energy'

    class Meta:
        proxy = True

    @property
    def dem_el_energy(self):
        return round((self.mundata.dem_el_energy_hh +
                      self.mundata.dem_el_energy_rca +
                      self.mundata.dem_el_energy_ind) / 1e3)


class RegMunEnergyReElDemShare(RegMunGenEnergyRe, RegMunDemElEnergy):
    name = 'reg_mun_energy_re_el_dem_share'

    class Meta:
        proxy = True

    @property
    def energy_re_el_dem_share(self):
        return round(self.gen_energy_re / self.dem_el_energy * 100)


class RegMunGenEnergyRePerCapita(RegMunGenEnergyRe):
    name = 'reg_mun_gen_energy_re_per_capita'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_per_capita(self):
        return round(self.gen_energy_re * 1e3 / self.mundata.pop_2017, 1)


class RegMunGenEnergyReDensity(RegMunGenEnergyRe):
    name = 'reg_mun_gen_energy_re_density'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_density(self):
        return round(self.gen_energy_re * 1e3 / self.mundata.area, 1)


class RegMunGenCapRe(RegMun):
    name = 'reg_mun_gen_cap_re'

    class Meta:
        proxy = True

    @property
    def gen_cap_re(self):
        return round(self.mundata.gen_capacity_wind +
                     self.mundata.gen_capacity_pv_roof_large +
                     self.mundata.gen_capacity_pv_ground +
                     self.mundata.gen_capacity_hydro +
                     self.mundata.gen_capacity_bio)


class RegMunGenCapReDensity(RegMunGenCapRe):
    name = 'reg_mun_gen_cap_re_density'

    class Meta:
        proxy = True

    @property
    def gen_cap_re_density(self):
        return round(self.gen_cap_re / self.mundata.area, 2)


class RegMunGenCountWindDensity(RegMun):
    name = 'reg_mun_gen_count_wind_density'

    class Meta:
        proxy = True

    @property
    def gen_count_wind_density(self):
        return round(self.mundata.gen_count_wind / self.mundata.area, 2)


class RegMunDemElEnergyPerCapita(RegMunDemElEnergy):
    name = 'reg_mun_dem_el_energy_per_capita'

    class Meta:
        proxy = True

    @property
    def dem_el_energy_per_capita(self):
        return round(self.dem_el_energy * 1e6 / self.mundata.pop_2017)


class RegMunDemThEnergy(RegMun):
    name = 'reg_mun_dem_th_energy'

    class Meta:
        proxy = True

    @property
    def dem_th_energy(self):
        return round((self.mundata.dem_th_energy_hh +
                      self.mundata.dem_th_energy_rca) / 1e3)


class RegMunDemThEnergyPerCapita(RegMunDemThEnergy):
    name = 'reg_mun_dem_th_energy_per_capita'

    class Meta:
        proxy = True

    @property
    def dem_th_energy_per_capita(self):
        return round(self.dem_th_energy * 1e6 / self.mundata.pop_2017)


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

class GenPVGround(LayerModel):
    name = 'gen_pv_ground'
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


##########################
# Layer models (results) #
##########################
# TODO: Alter extended classes to result classes
class RegMunEnergyReElDemShareResult(RegMunGenEnergyRe, RegMunDemElEnergy):
    name = 'reg_mun_energy_re_el_dem_share_result'

    class Meta:
        proxy = True

    @property
    def energy_re_el_dem_share_result(self):
        return round(self.gen_energy_re / self.dem_el_energy * 100)


# TODO: Alter extended class to result class
class RegMunGenEnergyReResult(RegMun):
    name = 'reg_mun_gen_energy_re_result'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_result(self):
        return round((self.mundata.gen_el_energy_wind +
                      self.mundata.gen_el_energy_pv_roof +
                      self.mundata.gen_el_energy_pv_ground +
                      self.mundata.gen_el_energy_hydro) / 1e3)


# TODO: Alter extended class to result class
class RegMunGenEnergyReDensityResult(RegMunGenEnergyRe):
    name = 'reg_mun_gen_energy_re_density_result'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_density_result(self):
        return round(self.gen_energy_re * 1e3 / self.mundata.area, 1)


# TODO: Alter extended class to result class
class RegMunGenCapReResult(RegMun):
    name = 'reg_mun_gen_cap_re_result'

    class Meta:
        proxy = True

    @property
    def gen_cap_re_result(self):
        return round(self.mundata.gen_capacity_wind +
                     self.mundata.gen_capacity_pv_roof_large +
                     self.mundata.gen_capacity_pv_ground +
                     self.mundata.gen_capacity_hydro +
                     self.mundata.gen_capacity_bio)


# TODO: Alter extended class to result class
class RegMunGenCapReDensityResult(RegMunGenCapRe):
    name = 'reg_mun_gen_cap_re_density_result'

    class Meta:
        proxy = True

    @property
    def gen_cap_re_density_result(self):
        return round(self.gen_cap_re / self.mundata.area, 2)


# TODO: Alter extended class to result class
class RegMunGenCountWindDensityResult(RegMun):
    name = 'reg_mun_gen_count_wind_density_result'

    class Meta:
        proxy = True

    @property
    def gen_count_wind_density_result(self):
        return round(self.mundata.gen_count_wind / self.mundata.area, 2)


# TODO: Alter extended class to result class
class RegMunDemElEnergyResult(RegMun):
    name = 'reg_mun_dem_el_energy_result'

    class Meta:
        proxy = True

    @property
    def dem_el_energy_result(self):
        return round((self.mundata.dem_el_energy_hh +
                      self.mundata.dem_el_energy_rca +
                      self.mundata.dem_el_energy_ind) / 1e3)


# TODO: Alter extended class to result class
class RegMunDemElEnergyPerCapitaResult(RegMunDemElEnergy):
    name = 'reg_mun_dem_el_energy_per_capita_result'

    class Meta:
        proxy = True

    @property
    def dem_el_energy_per_capita_result(self):
        return round(self.dem_el_energy * 1e6 / self.mundata.pop_2017)


################################
# Layer models (results DELTA) #
################################
# TODO: This is a test delta layer
class RegMunEnergyReElDemShareDeltaResult(RegMun):
    name = 'reg_mun_energy_re_el_dem_share_result_delta'

    class Meta:
        proxy = True

    @property
    def energy_re_el_dem_share_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunGenEnergyReDeltaResult(RegMun):
    name = 'reg_mun_gen_energy_re_result_delta'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunGenEnergyReDensityDeltaResult(RegMun):
    name = 'reg_mun_gen_energy_re_density_result_delta'

    class Meta:
        proxy = True

    @property
    def gen_energy_re_density_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunGenCapReDeltaResult(RegMun):
    name = 'reg_mun_gen_cap_re_result_delta'

    class Meta:
        proxy = True

    @property
    def gen_cap_re_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunGenCapReDensityDeltaResult(RegMun):
    name = 'reg_mun_gen_cap_re_density_result_delta'

    class Meta:
        proxy = True

    @property
    def gen_cap_re_density_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunGenCountWindDensityDeltaResult(RegMun):
    name = 'reg_mun_gen_count_wind_density_result_delta'

    class Meta:
        proxy = True

    @property
    def gen_count_wind_density_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunDemElEnergyDeltaResult(RegMun):
    name = 'reg_mun_dem_el_energy_result_delta'

    class Meta:
        proxy = True

    @property
    def dem_el_energy_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


# TODO: This is a test delta layer
class RegMunDemElEnergyPerCapitaDeltaResult(RegMun):
    name = 'reg_mun_dem_el_energy_per_capita_result_delta'

    class Meta:
        proxy = True

    @property
    def dem_el_energy_per_capita_result_delta(self):
        return str(random.randrange(-100, 100, 1)) + '%'


###############
# Data models #
###############
# The following tables contain initial data only, data that result from
# adjustments in the tool are not saved to these tables.

class MunData(models.Model):
    """Statistical data of municipalities (status quo)

    Attributes
    ----------
    ags :
        Municipality key (Amtlicher Gemeindeschlüssel),
        refers to :class:`stemp_abw.models.RegMun`
    area :
        Total area in km^2

    pop_2011 :
        Population (2011) according to Zensus
    pop_2017 :
        Population (2017) according to GV-ISys
    pop_2030 :
        Population (2030) forecast according to MLV Sachsen-Anhalt
    pop_2050 :
        Population (2050), linearly extrapolated using 2017 and 2030
    total_living_space :
        Total living space (Wohnfläche) in m^2

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

    dem_el_peak_load_hh :
        El. peak demand of households in MW
    dem_el_peak_load_rca :
        El. peak demand of retail, commercial and agricultural sector (GHD)
        in MW
    dem_el_peak_load_ind :
        El. peak demand of industry in MW
    dem_el_energy_hh :
        Annual el. energy consumed by households in MWh
    dem_el_energy_rca :
        Annual el. energy consumed by retail, commercial and agricultural
        sector (GHD) in MWh
    dem_el_energy_ind :
        Annual el. energy consumed by industry in MWh

    dem_th_peak_load_hh :
        Heat peak demand of households in MW
    dem_th_peak_load_rca :
        Heat peak demand of retail, commercial and agricultural sector (GHD)
        in MW
    dem_th_peak_load_ind :
        Heat peak demand of industry in MW
    dem_th_energy_hh :
        Annual heat consumed by households in MWh
    dem_th_energy_hh_efh :
        Annual heat consumed by single-family households (Einfamilienhäuser)
        in MWh
    dem_th_energy_hh_mfh :
        Annual heat consumed by multi-family households (Mehrfamilienhäuser)
        in MWh
    dem_th_energy_hh_efh_spec :
        Annual heat consumed by single-family households (Einfamilienhäuser),
        area-specific in kWh/m^2
    dem_th_energy_hh_mfh_spec :
        Annual heat consumed by multi-family households (Mehrfamilienhäuser),
        area-specific in kWh/m^2
    dem_th_energy_rca :
        Annual heat consumed by retail, commercial and agricultural sector
        (GHD) in MWh
    dem_th_energy_ind :
        Annual heat consumed by industry in MWh

    dem_th_energy_hh_per_capita :
        Annual heat demand of households per capita in MWh
    dem_th_energy_total_per_capita :
        Annual heat demand of households, retail, commercial and agricultural
        sector per capita in MWh

    reg_prio_area_wec_area :
        Area sum of priority areas (parts) in ha
    reg_prio_area_wec_count :
        Count of priority area (parts)
    """
    """"""
    ags = models.OneToOneField(RegMun, primary_key=True, on_delete=models.DO_NOTHING)
    area = models.FloatField(null=True)

    pop_2011 = models.IntegerField(null=True)
    pop_2017 = models.IntegerField(null=True)
    pop_2030 = models.IntegerField(null=True)
    pop_2050 = models.IntegerField(null=True)
    total_living_space = models.FloatField(null=True)
    
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

    dem_el_peak_load_hh = models.FloatField(null=True)
    dem_el_peak_load_rca = models.FloatField(null=True)
    dem_el_peak_load_ind = models.FloatField(null=True)
    dem_el_energy_hh = models.FloatField(null=True)
    dem_el_energy_rca = models.FloatField(null=True)
    dem_el_energy_ind = models.FloatField(null=True)

    dem_th_peak_load_hh = models.FloatField(null=True)
    dem_th_peak_load_rca = models.FloatField(null=True)
    dem_th_peak_load_ind = models.FloatField(null=True)
    dem_th_energy_hh = models.FloatField(null=True)
    dem_th_energy_hh_efh = models.FloatField(null=True)
    dem_th_energy_hh_mfh = models.FloatField(null=True)
    dem_th_energy_hh_efh_spec = models.FloatField(null=True)
    dem_th_energy_hh_mfh_spec = models.FloatField(null=True)
    dem_th_energy_rca = models.FloatField(null=True)
    dem_th_energy_ind = models.FloatField(null=True)

    dem_th_energy_hh_per_capita = models.FloatField(null=True)
    dem_th_energy_total_per_capita = models.FloatField(null=True)

    reg_prio_area_wec_area = models.FloatField(null=True)
    reg_prio_area_wec_count = models.IntegerField(null=True)


class FeedinTs(models.Model):
    """Renewable feedin timeseries (normalized, hourly)

    Attributes
    ----------
    id :
        DB id
    timestamp :
        timestamp
    ags :
        Municipality key (Amtlicher Gemeindeschlüssel),
        refers to :class:`stemp_abw.models.RegMun`
    pv_ground :
        Photovoltaics (ground-mounted systems)
    pv_roof :
        Photovoltaics (roof-mounted systems)
    hydro :
        Run-of-river plants
    wind_sq :
        Wind turbines (status quo)
    wind_fs :
        Wind turbines (future scenarios)

    Notes
    -----
    Timeseries are stored per timestep and ags -> one dataset is uniquely
    identified by timestamp and municipality's ags.
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
    id :
        DB id
    ags :
        Municipality key (Amtlicher Gemeindeschlüssel),
        refers to :class:`stemp_abw.models.RegMun`
    capacity :
        Nominal power in MW
    chp :
        Indicates if plant is of type CHP (combined heat and power)
    com_month :
        Month of commissioning
    com_year :
        Year of commissioning
    comment :
        Comment
    decom_month :
        Month of decommissioning
    decom_year :
        Year of decommissioning
    efficiency :
        Efficiency
    energy_source_level_1 :
        Indicates if renewable or conventional
    energy_source_level_2 :
        Indicates energy source
    energy_source_level_3 :
        More specific energy source
    geometry : Geometry
        SRID: EPSG:4326 (WGS84)
    technology :
        Technology
    thermal_capacity :
        Nominal thermal nominal power, if applicable
    coastdat2 :
        No. of coastdat2 weather cell (reegis)
    capacity_in :
        Capacity of inflow
    federal_state :
        Abbreviation of federal state name (2 letters according to ISO
        3166-2:DE)

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


class DemandTs(models.Model):
    """Demand timeseries (hourly)

    Attributes
    ----------
    id :
        DB id
    timestamp :
        timestamp
    ags :
        Municipality key (Amtlicher Gemeindeschlüssel),
        refers to :class:`stemp_abw.models.RegMun`
    el_hh :
        El. demand of households
    el_rca :
        El. demand of retail, commercial and agricultural sector (GHD)
    el_ind :
        El. demand of industry
    th_hh_efh :
        Heat demand of households in single-family houses (Einfamilienhäuser),
        absolute, in MW
    th_hh_mfh :
        Heat demand of households in multi-family houses (Mehrfamilienhäuser),
        absolute, in MW
    th_hh_efh_spec :
        Heat demand of households in single-family houses (Einfamilienhäuser),
        area-specific in kWh/m^2
    th_hh_mfh_spec :
        Heat demand of households in multi-family houses (Mehrfamilienhäuser),
        area-specific in kWh/m^2
    th_rca :
        Heat demand of retail, commercial and agricultural sector (GHD) in MW
    th_ind :
        Heat demand of industry in MW

    Notes
    -----
    Timeseries are stored per timestep and ags -> one dataset is uniquely
    identified by timestamp and municipality's ags.
    """
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(db_index=True)
    ags = models.ForeignKey(RegMun, on_delete=models.DO_NOTHING)

    el_hh = models.FloatField(blank=True, null=True)
    el_rca = models.FloatField(blank=True, null=True)
    el_ind = models.FloatField(blank=True, null=True)
    th_hh_efh = models.FloatField(blank=True, null=True)
    th_hh_mfh = models.FloatField(blank=True, null=True)
    th_hh_efh_spec = models.FloatField(blank=True, null=True)
    th_hh_mfh_spec = models.FloatField(blank=True, null=True)
    th_rca = models.FloatField(blank=True, null=True)
    th_ind = models.FloatField(blank=True, null=True)


# class Emission(models.Model):
#     """Emissions of technologies in kg/MWh"""
#     technology = models.CharField(max_length=254, null=True)
#     emissions_fix = models.FloatField()
#     emissions_variable = models.FloatField()
#
# class Costs(models.Model):
#     """Costs of technologies in €/MWh"""
#     technology = models.CharField(max_length=254, null=True)
#     costs_fix = models.FloatField()
#     costs_variable = models.FloatField()


class RepoweringScenario(models.Model):
    """Repowering scenario

    TODO: Add doctring
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True)
    data = JSONField(default=None, null=True)


class REPotentialAreas(models.Model):
    """Potential areas for renewable plants

    Attributes
    ----------
    id :
        DB id
    area_params :
        TODO: Define format
        App settings for usable areas (area panel)
    mun_data :
        TODO: Define format
        Available potentials (per technology)
        TO BE SPECIFIED
    geom : Geometry
        SRID: EPSG:3035 (ETRS89/LAEA)
    """
    name = 're_pot_areas'

    id = models.BigAutoField(primary_key=True)
    area_params = JSONField(default=None, null=True)
    mun_data = JSONField(default=None, null=True)
    geom = geomodels.MultiPolygonField(srid=3035, null=True)


class SimulationResults(models.Model):
    """Results of a scenario simulation

    Attributes
    ----------
    id :
        DB id
    data : json
        Result data, format as defined <HERE>
    """
    id = models.BigAutoField(primary_key=True)
    data = JSONField()

    def __str__(self):
        return self.data


class ScenarioData(models.Model):
    """Scenario data

    Attributes
    ----------
    id :
        DB id
    data : json
        TODO: Define format
        Scenario data, format as defined <HERE>
    data_uuid :
        UUID for scenario data to quickly compare settings to avoid blowing
        up postgreSQL
    """
    id = models.BigAutoField(primary_key=True)
    data = JSONField()
    data_uuid = models.UUIDField(default=uuid4, editable=False,
                                 unique=True, null=False)

    def __str__(self):
        return self.data


class Scenario(models.Model):
    """Scenario (energy system configuration)

    Attributes
    ----------
    id :
        DB id
    created : DateTime
        Timestamp of creation
    name : String
        Name of scenario
    is_user_scenario : Bool
        True, if scenario was created by a user (default)
    data :
        Reference to ScenarioData
    results :
        Reference to SimulationResults
    re_potential_areas :
        Reference to REPotentialAreas
    repowering_scenario :
        Reference to RepoweringScenario
    """
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True)
    is_user_scenario = models.BooleanField(default=True)
    data = models.ForeignKey(ScenarioData, on_delete=models.DO_NOTHING)
    results = models.ForeignKey(SimulationResults, on_delete=models.DO_NOTHING,
                                null=True, default=None)
    re_potential_areas = models.ForeignKey(REPotentialAreas,
                                           on_delete=models.DO_NOTHING)
    repowering_scenario = models.ForeignKey(RepoweringScenario,
                                            on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'
