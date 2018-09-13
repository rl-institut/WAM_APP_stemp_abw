
# from collections import defaultdict, OrderedDict, ChainMap
from sqlalchemy import Column, VARCHAR, BIGINT, JSON, Float, Integer, Text, SmallInteger, BigInteger
# from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from geoalchemy2.types import Geometry

from sqlalchemy.ext.declarative import declarative_base
import sqlahelper
#from stemp_abw import app_settings


# SCHEMA = 'sandbox'
SCHEMA = 'sandbox'

Base = declarative_base()


class WnAbwEgoDpHvmvSubstation(Base):
    __tablename__ = 'wn_abw_ego_dp_hvmv_substation'
    __table_args__ = {'schema': SCHEMA}

    version = Column(Text, nullable=False)
    subst_id = Column(Integer, primary_key=True)
    lon = Column(Float(53))
    lat = Column(Float(53))
    point = Column(Geometry('POINT', 4326))
    polygon = Column(Geometry)
    voltage = Column(Text)
    power_type = Column(Text)
    substation = Column(Text)
    osm_id = Column(Text)
    osm_www = Column(Text)
    frequency = Column(Text)
    subst_name = Column(Text)
    ref = Column(Text)
    operator = Column(Text)
    dbahn = Column(Text)
    status = Column(SmallInteger)
    otg_id = Column(BigInteger)
    ags_0 = Column(Text)
    geom = Column(Geometry('POINT', 3035), index=True)
