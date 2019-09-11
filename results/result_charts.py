from django.utils.translation import gettext_lazy as _
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
            'title': {'text': str(_('Stromerzeugung'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}},
            'plotOptions': {'column': {'stacking': 'normal'}}
        },
        'data': pd.DataFrame(data=[{str(_('Windenergie')): 0,
                                    str(_('PV Freifläche')): 0,
                                    str(_('PV Dach')): 0,
                                    str(_('Wasserkraft')): 0,
                                    str(_('Biogas')): 0,
                                    str(_('Fossile Brennstoffe')): 0,
                                    str(_('Import')): 0},
                                   {str(_('Windenergie')): 0,
                                    str(_('PV Freifläche')): 0,
                                    str(_('PV Dach')): 0,
                                    str(_('Wasserkraft')): 0,
                                    str(_('Biogas')): 0,
                                    str(_('Fossile Brennstoffe')): 0,
                                    str(_('Import')): 0}
                                   ],
                             index=[str(_('Ihr Szenario')), str(_('Status quo'))])
    },
    {
        'container_id': 'hc_column_power_dem_both_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': str(_('Stromverbrauch'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}},
            'plotOptions': {'column': {'stacking': 'normal'}}
        },
        'data': pd.DataFrame(data=[{str(_('Haushalte')): 0,
                                    str(_('GHD')): 0,
                                    str(_('Industrie')): 0,
                                    str(_('Export')): 0},
                                   {str(_('Haushalte')): 0,
                                    str(_('GHD')): 0,
                                    str(_('Industrie')): 0,
                                    str(_('Export')): 0}
                                   ],
                             index=[str(_('Ihr Szenario')), str(_('Status quo'))])
    },
    {
        'container_id': 'hc_column_power_own_cons_both_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': str(_('Eigenversorgung Strom'))},
            'subtitle': {'text': str(_('in %'))},
            'yAxis': {'title': {'text': '%'}}
        },
        'data': pd.DataFrame(data=[{str(_('Bilanziell')): 0,
                                    str(_('Zeitgleich')): 0},
                                   {str(_('Bilanziell')): 0,
                                    str(_('Zeitgleich')): 0}
                                   ],
                             index=[str(_('Ihr Szenario')), str(_('Status quo'))])
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
            'title': {'text': str(_('Zusammensetzung Stromerzeugung (Dein Szenario)'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}}
        },
        'data': pd.DataFrame(data={'name': [str(_('Windenergie')),
                                            str(_('PV Freifläche')),
                                            str(_('PV Dach')),
                                            str(_('Wasserkraft')),
                                            str(_('Biogas')),
                                            str(_('Fossile Brennstoffe')),
                                            str(_('Import'))],
                                   'y': [0] * 7}).reset_index().to_dict(orient='records')
    },
    {
        'container_id': 'hc_pie_power_production_sq_scn',
        'type': 'pie',
        'setup_labels': {
            'title': {'text': str(_('Zusammensetzung Stromerzeugung (Status quo)'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}}
        },
        'data': pd.DataFrame(data={'name': [str(_('Windenergie')),
                                            str(_('PV Freifläche')),
                                            str(_('PV Dach')),
                                            str(_('Wasserkraft')),
                                            str(_('Biogas')),
                                            str(_('Fossile Brennstoffe')),
                                            str(_('Import'))],
                                   'y': [0] * 7}).reset_index().to_dict(orient='records')
    },
    {
        'container_id': 'hc_column_power_prod_m_user_scn',
        'type': 'column',
        'setup_labels': {
            'title': {'text': str(_('Monatliche Stromerzeugung aus EE (Dein Szenario)'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}}

        },
        'data': pd.DataFrame(data={str(_('Windenergie')): [0 for _ in MONTH_LABELS],
                                   str(_('PV')): [0 for _ in MONTH_LABELS]},
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
            'title': {'text': str(_('Energieverbrauch (Strom)'))},
            'subtitle': {'text': str(_('in GWh'))},
            'yAxis': {'title': {'text': str(_('GWh'))}}
        },
        'data': pd.DataFrame(data=[{str(_('Haushalte')): 0,
                                    str(_('GHD')): 0,
                                    str(_('Industrie')): 0,
                                    str(_('Export')): 0},
                                   {str(_('Haushalte')): 0,
                                    str(_('GHD')): 0,
                                    str(_('Industrie')): 0,
                                    str(_('Export')): 0}
                                   ],
                             index=[str(_('Ihr Szenario')), str(_('Status quo'))])
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
            'title': {'text': str(_('Windenergie Erzeugung'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
        },
        'data': {str(_('Windenergie')): [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0, 5],
                 str(_('Windenergie2')): [8, 3, 3, 6, 2, 2, 1, 5, 5, 8, 7, 5]}
    },
    {
        'container_id': 'hc_res_pv_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': str(_('Photovoltaik Erzeugung'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
        },
        'data': {'PV': [1, 2, 3, 4, 5, 4, 3, 2, 1, 8, 0, 5]}
    },
    {
        'container_id': 'hc_res_bio_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': str(_('Bioenergie Erzeugung'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
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
            'title': {'text': str(_('Erzeugung'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': str(_('Bedarf'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': str(_('Erneuerbare Energien'))},
            'subtitle': {'text': str(_('in GW'))},
            'yAxis': {'title': {'text': str(_('GW'))}}
        },
        # 'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    }
]
results_charts_tab5_viz = [results.ResultChart(
    setup_labels=l['setup_labels'],
    type='column').visualize() for l in results_charts_tab5]