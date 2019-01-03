from django.apps import AppConfig
from wam import settings
from stemp_abw.sessions import SessionData


class StempAbwConfig(AppConfig):
    name = 'stemp_abw'
    settings.SESSION_DATA = SessionData()
