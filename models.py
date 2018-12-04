from django.db import models
# from djgeojson.fields import PointField
from django.contrib.gis.db import models as geomodels
# from geoalchemy2.types import Geometry
from stemp_abw import oep_models
import sqlahelper


# class MapLayers(models.Model):
#     model_label = models.CharField(max_length=20)
#     caption = models.CharField(max_length=50)
#     description = models.CharField(max_length=100)

####################
### Layer models ###
####################

class LayerModel(models.Model):

    class Meta:
        abstract = True

    @property
    def name(self):
        raise NotImplementedError

    # TODO: This can be chucked away?
    @property
    def popup_content(self):
        #return '<p>'+self.name+'</p>'
        return 'popup/'


# TODO: This model is for testing puorposes only, to be removed!
class HvMvSubst(LayerModel):
    name = 'subst'
    geom = geomodels.PointField(srid=4326, null=True)
    subst_id = models.IntegerField()

    objects = geomodels.Manager()

    # @property
    # def popup_content(self):
    #     return '<p>{text}</p>'.format(
    #         text='Substation ' + str(self.subst_id))

    def __unicode__(self):
        return 'subst {}'.format(self.subst_id)

    # def get_data(self):
    #     session = sqlahelper.get_session()
    #     query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
    #     data = query.all()


class OsmPowerGen(LayerModel):
    name = 'gen'
    geom = geomodels.PointField(srid=4326, null=True)
    subst_id = models.IntegerField()
    osm_id = models.IntegerField()

    objects = geomodels.Manager()

    # @property
    # def popup_content(self):
    #     return '<p>{text}</p>'.format(
    #         text='Generator ' + str(self.osm_id))

    def __unicode__(self):
        return 'gen {}'.format(self.osm_id)


class RpAbwBound(LayerModel):
    name = 'rpabw'
    geom = geomodels.MultiLineStringField(srid=4326, null=True)

    # @property
    # def popup_content(self):
    #     return '<p>{text}</p>'.format(
    #         text='PR ABW Grenze des Planungsraumes')

    def __unicode__(self):
        return 'PR ABW Grenze des Planungsraumes'


class RegMun(LayerModel):
    name = 'reg_mun'
    ags = models.IntegerField(primary_key=True)
    geom = geomodels.MultiPolygonField(srid=3035)
    gen = models.CharField(max_length=254)
    pop_km2 = models.FloatField(null=True)


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
