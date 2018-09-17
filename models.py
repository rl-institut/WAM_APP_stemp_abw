from django.db import models
# from djgeojson.fields import PointField
from django.contrib.gis.db import models as geomodels
# from geoalchemy2.types import Geometry
from stemp_abw import oep_models
import sqlahelper


class HvMvSubst(models.Model):
    geom = geomodels.PointField(srid=4326, null=True)
    subst_id = models.IntegerField()

    objects = geomodels.Manager()
    name = 'xxxxxxxxxx'

    @property
    def popup_content(self):
        return '<p>{text}</p>'.format(
            text='Substation ' + str(self.subst_id))

    def __unicode__(self):
        return 'subst {}'.format(self.subst_id)

    # def get_data(self):
    #     session = sqlahelper.get_session()
    #     query = session.query(oep_models.WnAbwEgoDpHvmvSubstation)
    #     data = query.all()
