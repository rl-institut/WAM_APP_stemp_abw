# This file contains helpers for recurrent processes

import os
import json
import hashlib
from uuid import UUID
from django.core.wsgi import get_wsgi_application


kopy_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
os.chdir(kopy_path)

os.environ['DJANGO_DATABASE'] = 'default'
os.environ['DJANGO_SETTINGS_MODULE'] = 'wam.settings'
application = get_wsgi_application()

from stemp_abw.dataio.load_static import load_mun_data
from stemp_abw.models import \
    Scenario, ScenarioData, REPotentialAreas, RepoweringScenario, SimulationResults
from stemp_abw.sessions import UserSession
from stemp_abw.results.io import oemof_results_to_json


def insert_status_quo_scenario():
    # def create_wkt_element(geom):
    #     return WKTElement(geom, srid=3035)

    mun_data = load_mun_data()

    # # test RE area object
    # repot_area_params = {'repot_area_params': 0}
    # repot_mun_data = {'repot_mun_data': 0}
    # mpoly_wkt = 'MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))'
    # repot_areas_obj = REPotentialAreas.objects.create(area_params=json.dumps(repot_area_params),
    #                                                   mun_data=json.dumps(repot_mun_data),
    #                                                   geom=mpoly_wkt)

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

    # no RE potential area or repowering scenario for status quo
    re_potential_areas = REPotentialAreas.objects.get(id=0)
    repowering_scenario = RepoweringScenario.objects.get(id=0)

    print('Scenario data hash UUID:', uuid)

    scn = Scenario.objects.create(name='Status quo',
                                  description='Dieses Szenario enthält den aktuellen Zustand '
                                              'der Energieversorgung und Flächennutzung in '
                                              'der Region.',
                                  is_user_scenario=False,
                                  data=scn_data_obj,
                                  re_potential_areas=re_potential_areas,
                                  repowering_scenario=repowering_scenario)
    # scn = Scenario.objects.create(name='Status quo 2',
    #                               description='Dieses Szenario enthält den aktuellen Zustand '
    #                                           'der Energieversorgung und Flächennutzung in '
    #                                           'der Region.',
    #                               is_user_scenario=False,
    #                               data=scn_data_obj,
    #                               re_potential_areas=re_potential_areas,
    #                               repowering_scenario=repowering_scenario)


def insert_repowering_scenarios():
    # get data
    mun_data = load_mun_data()[['gen_count_wind', 'gen_capacity_wind']]
    mun_data['gen_count_wind'] = mun_data['gen_count_wind'].astype(int)

    # insert no-repowering-scenario
    scn = {
        'id': 0,
        'name': 'Kein Repowering/aktuell',
        'description': 'Es wird kein Repowering vorgenommen.',
        'data': json.dumps(mun_data.round(decimals=1).to_dict(orient='index'), sort_keys=True)
    }
    RepoweringScenario.objects.create(**scn)

    # insert 1:1 scenario
    mun_data['gen_capacity_wind'] = (mun_data['gen_count_wind'] * 4.2).round(decimals=1)

    scn = {
        'name': '1:1-Repowering',
        'description': 'Standorttreues Repowering aller heute in Betrieb '
                       'befindlichen Altanlagen durch eine neue Anlage, '
                       'sowohl innerhalb als auch außerhalb von '
                       'Vorranggebieten (VR/EG) für Windenergie.',
        'data': json.dumps(mun_data.to_dict(orient='index'), sort_keys=True)
    }
    RepoweringScenario.objects.create(**scn)

    # insert free scenario
    # TODO: Insert data
    scn = {
        'id': -1,
        'name': 'Freier Zubau',
        'description': 'In diesem Szenario können Windenergieanlagen unter '
                       'Verwendung zusätzlicher Potenzialflächen frei zugebaut '
                       'werden.',
        #'data': json.dumps(mun_data.to_dict(orient='index'), sort_keys=True
        'data': json.dumps({})
    }
    RepoweringScenario.objects.create(**scn)

# def insert_potential_areas():
#     # test RE area object
#     repot_area_params = {'repot_area_params': {'dist_resid': 1000,
#                                                'use_forest': False,
#                                                'use_ffh_areas': False,
#                                                'use_cult_areas': False}}
#     repot_mun_data = {'repot_mun_data': 0}
#     mpoly_wkt = 'MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))'
#     repot_areas_obj = REPotentialAreas.objects.create(area_params=json.dumps(repot_area_params),
#                                                       mun_data=json.dumps(repot_mun_data),
#                                                       geom=mpoly_wkt)


def insert_status_quo_results():
    # ACHTUNG: To make it work:
    # 1) Comment out in class Results:
    #        self.sq_results_raw, self.sq_param_results_raw = oemof_json_to_results(
    #        Scenario.objects.get(name='Status quo').results.data)
    # and set
    #   self.results_raw = None
    #   self.param_results_raw = None
    #
    # 2) Comment out result lookup:
    # # reverse lookup for scenario
    # if Scenario.objects.filter(data__data_uuid=user_scn_data_uuid).exists():
    #     print('Scenario results found, load from DB...')
    #     results_json = Scenario.objects.get(
    #         data__data_uuid=user_scn_data_uuid).results.data
    #     self.store_values(*oemof_json_to_results(results_json))
    # else:
    #     print('Scenario results not found, start simulation...')

    session = UserSession()
    session.simulation.create_esys()
    session.simulation.load_or_simulate()

    data = oemof_results_to_json(results=session.simulation.results.results_raw,
                                 param_results=session.simulation.results.param_results_raw)

    results = SimulationResults.objects.create(data=data)

    scn = Scenario.objects.get(name='Status quo')
    scn.results = results
    scn.save()


#insert_repowering_scenarios()
#insert_potential_areas()
#insert_status_quo_scenario()
#insert_status_quo_results()