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

