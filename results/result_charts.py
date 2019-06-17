from stemp_abw.results import results
from stemp_abw.app_settings import MONTH_LABELS
import pandas as pd


####################
### Result Tab 1 ###
####################

results_charts_tab1 = [
    {
        'container_id': 'hc_column_power_prod_both_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': 'Stromerzeugung'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}},
            'plotOptions': {'column': {'stacking': 'normal'}}
        },
        'data': pd.DataFrame(data=[{'Windenergie': 0,
                                    'PV Freifläche': 0,
                                    'PV Dach': 0,
                                    'Wasserkraft': 0,
                                    'Biogas': 0,
                                    'Fossile Brennstoffe': 0,
                                    'Import': 0},
                                   {'Windenergie': 0,
                                    'PV Freifläche': 0,
                                    'PV Dach': 0,
                                    'Wasserkraft': 0,
                                    'Biogas': 0,
                                    'Fossile Brennstoffe': 0,
                                    'Import': 0}
                                   ],
                             index=['Ihr Szenario', 'Status quo'])
    },
    {
        'container_id': 'hc_column_power_dem_both_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': 'Stromverbrauch'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}},
            'plotOptions': {'column': {'stacking': 'normal'}}
        },
        'data': pd.DataFrame(data=[{'Haushalte': 0,
                                    'GHD': 0,
                                    'Industrie': 0,
                                    'Export': 0},
                                   {'Haushalte': 0,
                                    'GHD': 0,
                                    'Industrie': 0,
                                    'Export': 0}
                                   ],
                             index=['Ihr Szenario', 'Status quo'])
    },
    {
        'container_id': 'hc_column_power_own_cons_both_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': 'Eigenversorgung Strom (bilanziell)'},
            'subtitle': {'text': 'in %'},
            'yAxis': {'title': {'text': '%'}}
        },
        'data': pd.DataFrame(data=[{'Eigenversorgung': 0},
                                   {'Eigenversorgung': 0}
                                   ],
                             index=['Ihr Szenario', 'Status quo'])
    }
]

results_charts_tab1_viz = [results.ResultChart(
    setup_labels=chart['setup_labels'],
    type=chart['type'],
    data=chart['data']).visualize(renderTo=chart['container_id'])
                           for chart in results_charts_tab1]

####################
### Result Tab 2 ###
####################

results_charts_tab2 = [
    {
        'container_id': 'hc_pie_power_production_user_scn',
        'type': 'pie',
        'setup_labels': {
            'title': {'text': 'Zusammensetzung Stromerzeugung (Dein Szenario)'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}
        },
        'data': pd.DataFrame(data={'name': ['Windenergie',
                                            'PV Freifläche',
                                            'PV Dach',
                                            'Wasserkraft',
                                            'Biogas',
                                            'Fossile Brennstoffe',
                                            'Import'],
                                   'y': [0] * 7}).reset_index().to_dict(orient='records')
    },
    {
        'container_id': 'hc_pie_power_production_sq_scn',
        'type': 'pie',
        'setup_labels': {
            'title': {'text': 'Zusammensetzung Stromerzeugung (Status quo)'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}
        },
        'data': pd.DataFrame(data={'name': ['Windenergie',
                                            'PV Freifläche',
                                            'PV Dach',
                                            'Wasserkraft',
                                            'Biogas',
                                            'Fossile Brennstoffe',
                                            'Import'],
                                   'y': [0] * 7}).reset_index().to_dict(orient='records')
    },
    {
        'container_id': 'hc_column_power_prod_m_user_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': 'Monatliche Stromerzeugung aus EE (Dein Szenario)'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}

        },
        'data': pd.DataFrame(data={'Windenergie': [0 for _ in MONTH_LABELS],
                                   'PV': [0 for _ in MONTH_LABELS]},
                             index=MONTH_LABELS)
    },
]

results_charts_tab2_viz = [results.ResultChart(
    setup_labels=chart['setup_labels'],
    type=chart['type'],
    data=chart['data']).visualize(renderTo=chart['container_id'])
                           for chart in results_charts_tab2]

####################
### Result Tab 3 ###
####################

results_charts_tab3 = [
    {
        'container_id': 'hc_column_power_dem_both_scn2',
        'type': 'column',
        'setup_labels': {
            'title': {'text': 'Energieverbrauch (Strom)'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}
        },
        'data': pd.DataFrame(data=[{'Haushalte': 0,
                                    'GHD': 0,
                                    'Industrie': 0,
                                    'Export': 0},
                                   {'Haushalte': 0,
                                    'GHD': 0,
                                    'Industrie': 0,
                                    'Export': 0}
                                   ],
                             index=['Ihr Szenario', 'Status quo'])
    },
]

results_charts_tab3_viz = [results.ResultChart(
    setup_labels=chart['setup_labels'],
    type=chart['type'],
    data=chart['data']).visualize(renderTo=chart['container_id'])
                           for chart in results_charts_tab3]

####################
### Result Tab 4 ###
####################

results_charts_tab4 = [
    {
        'container_id': 'hc_res_wind_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Windenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data': {'Windenergie': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0, 5],
                 'Windenergie2': [8, 3, 3, 6, 2, 2, 1, 5, 5, 8, 7, 5]}
    },
    {
        'container_id': 'hc_res_pv_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Photovoltaik Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data': {'PV': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0, 5]}
    },
    {
        'container_id': 'hc_res_bio_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Bioenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data': {'Bio': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0, 5]}
    }
]

results_charts_tab4_viz = [results.ResultChart(
    setup_labels=chart['setup_labels'],
    type=chart['type'],
    data=pd.DataFrame(data=chart['data'],
                      index=MONTH_LABELS)).visualize(renderTo=chart['container_id'])
                           for chart in results_charts_tab4]



# StackedGroupedColumnChart: used in popups as placeholder charts
results_charts_tab5 = [
    {
        'setup_labels': {
            'title': {'text': 'Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': 'Bedarf'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': 'Erneuerbare Energien'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    }
]
results_charts_tab5_viz = [results.ResultChart(
    setup_labels=l['setup_labels'],
    type='column').visualize() for l in results_charts_tab5]