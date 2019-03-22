# This file contains helpers for recurrent processes

import os
import json
import hashlib
from uuid import UUID
from shapely.wkt import loads as wkt_loads
from geoalchemy2 import Geometry, WKTElement
from django.core.wsgi import get_wsgi_application


kopy_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
os.chdir(kopy_path)

os.environ['DJANGO_DATABASE'] = 'default'
os.environ['DJANGO_SETTINGS_MODULE'] = 'wam.settings'
application = get_wsgi_application()

from stemp_abw.dataio.load_static import load_mun_data
from stemp_abw.models import \
    Scenario, ScenarioData, REPotentialAreas, RepoweringScenario


def insert_status_quo_scenario():
    # def create_wkt_element(geom):
    #     return WKTElement(geom, srid=3035)

    mun_data = load_mun_data()

    # test RE area object
    repot_area_params = {'repot_area_params': 0}
    repot_mun_data = {'repot_mun_data': 0}
    mpoly_wkt = 'MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))'
    repot_areas_obj = REPotentialAreas.objects.create(area_params=json.dumps(repot_area_params),
                                                      mun_data=json.dumps(repot_mun_data),
                                                      geom=mpoly_wkt)

    # prepare scenario data
    mun_data.rename(columns={'pop_2017': 'pop'}, inplace=True)
    mun_data_cols = ['dem_el_energy_hh', 'dem_el_energy_ind',
                     'dem_el_energy_rca', 'dem_th_energy_hh',
                     'dem_th_energy_hh_efh', 'dem_th_energy_hh_mfh',
                     'dem_th_energy_rca',
                     'gen_capacity_bio', 'gen_capacity_combined_cycle',
                     'gen_capacity_hydro', 'gen_capacity_pv_ground',
                     'gen_capacity_pv_roof_large', 'gen_capacity_pv_roof_small',
                     'gen_capacity_sewage_landfill_gas', 'gen_capacity_steam_turbine',
                     'gen_capacity_storage', 'gen_capacity_wind',
                     'gen_count_bio', 'gen_count_combined_cycle',
                     'gen_count_hydro', 'gen_count_pv_ground',
                     'gen_count_pv_roof_large', 'gen_count_pv_roof_small',
                     'gen_count_sewage_landfill_gas', 'gen_count_steam_turbine',
                     'gen_count_wind',
                     'gen_el_energy_hydro', 'gen_el_energy_pv_ground',
                     'gen_el_energy_pv_roof', 'gen_el_energy_wind',
                     'pop'
                     ]
    mun_data_filtered = mun_data[mun_data_cols].round(decimals=1)
    global_params = {'resid_save_el': 0, 'crt_save_el': 0, 'battery': 0,
                     'dsm_resid': 0, 'emobility': 0, 'resid_save_th': 0,
                     'crt_save_th': 0, 'resid_pth': 0, 'crt_pth': 0,
                     'dist_resid': 1000, 'use_forest': False,
                     'use_ffh_areas': False, 'use_cult_areas': False,
                     'repowering_scn': 0}
    region_data = mun_data_filtered.sum(axis=0).round(decimals=1).to_dict()
    region_data.update(global_params)
    scn_data = json.dumps(
        {
            'reg_params': global_params,
            'mun_data': mun_data_filtered.to_dict(orient='index')
        },
        sort_keys=True
    )
    uuid = UUID(hashlib.md5(scn_data.encode('utf-8')).hexdigest())

    scn_data_obj = ScenarioData.objects.create(data=scn_data,
                                               data_uuid=uuid)

    repowering_scenario = RepoweringScenario.objects.get(name='Kein Repowering')

    print('Scenario data hash UUID:', uuid)

    scn = Scenario.objects.create(name='Status quo',
                                  description='Dieses Szenario enthält den aktuellen Zustand '
                                              'der Energieversorgung und Flächennutzung in '
                                              'der Region.',
                                  is_user_scenario=False,
                                  data=scn_data_obj,
                                  re_potential_areas=repot_areas_obj,
                                  repowering_scenario=repowering_scenario)
    scn = Scenario.objects.create(name='Status quo 2',
                                  description='Dieses Szenario enthält den aktuellen Zustand '
                                              'der Energieversorgung und Flächennutzung in '
                                              'der Region.',
                                  is_user_scenario=False,
                                  data=scn_data_obj,
                                  re_potential_areas=repot_areas_obj,
                                  repowering_scenario=repowering_scenario)


def insert_repowering_scenarios():

    # insert no-repowering-scenario
    RepoweringScenario.objects.create(id=0,
                                      name='Kein Repowering',
                                      description='Es wird kein Repowering vorgenommen.',
                                      data=None)

    # insert 1:1 scenario
    mun_data = load_mun_data()[['gen_count_wind', 'gen_capacity_wind']]
    mun_data['gen_count_wind'] = mun_data['gen_count_wind'].astype(int)
    mun_data['gen_capacity_wind'] = (mun_data['gen_count_wind'] * 4.2).round(decimals=1)

    scn = {
        'name': '1:1-Repowering',
        'description': 'Standorttreues Repowering aller heute in Betrieb '
                       'befindlichen Altanlagen durch eine neue Anlage.',
        'data': json.dumps(mun_data.to_dict(orient='index'), sort_keys=True)
    }

    RepoweringScenario.objects.create(**scn)

# def insert_potential_areas():
#     # test RE area object
#     repot_area_params = {'repot_area_params': 0}
#     repot_mun_data = {'repot_mun_data': 0}
#     mpoly_wkt = 'MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))'
#     repot_areas_obj = REPotentialAreas.objects.create(area_params=json.dumps(repot_area_params),
#                                                       mun_data=json.dumps(repot_mun_data),
#                                                       geom=mpoly_wkt)

insert_status_quo_scenario()
#insert_repowering_scenarios()
#insert_potential_areas()
