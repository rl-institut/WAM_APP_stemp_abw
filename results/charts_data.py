from stemp_abw.results import results

# TODO: Temp stuff for WS
# LineChart: used in results as placeholder charts



# TODO: Temp stuff for WS
# LineChart: used in results as placeholder charts
labels2 = [
    {
        'setup_labels': {
            'title': {'text': 'Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Strom', 'Wärme']
    },
    {
        'setup_labels': {
            'title': {'text': 'Bedarf'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Strom', 'Wärme']
    },
    {
        'setup_labels': {
            'title': {'text': 'Erneuerbare Energien'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Wind', 'Solar']
    }
]
visualizations2 = [results.ResultAnalysisVisualization(
    setup_labels=l['setup_labels'],
    data_labels=l['data_labels'],
    type='line').visualize() for l in labels2]


# TODO: Temp stuff for WS
# StackedGroupedColumnChart: used in popups as placeholder charts
labels5 = [
    {
        'setup_labels': {
            'title': {'text': 'Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': 'Bedarf'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    },
    {
        'setup_labels': {
            'title': {'text': 'Erneuerbare Energien'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Anhalt', 'Bitterfeld', 'Wolfen', 'Dessau', 'Zerbst']
    }
]
visualizations5 = [results.ResultAnalysisVisualization(
    setup_labels=l['setup_labels'],
    data_labels=l['data_labels'],
    type='column').visualize() for l in labels5]


####################
### Result Tab 1 ###
####################

results_charts_tab1 = [
    {
        'container_id': 'hc_res_summary_scn',
        'type': 'pie',
        'setup_labels': {
            'title': {'text': 'Ihr Szenario'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}
        },
        'data_labels': ['Strom', 'Wärme']
    },
    {
        'container_id': 'hc_res_summary_sq',
        'type': 'pie',
        'setup_labels': {
            'title': {'text': 'Status quo'},
            'subtitle': {'text': 'in GWh'},
            'yAxis': {'title': {'text': 'GWh'}}
        },
        'data_labels': ['Strom', 'Wärme']
    }
]

#CONTAINER_LIST = [l['container_id'] for l in labels_res_summary]

results_charts_tab1_viz = [results.ResultAnalysisVisualization(
    setup_labels=chart['setup_labels'],
    data_labels=chart['data_labels'],
    type=chart['type']).visualize(renderTo=chart['container_id'])
                   for chart in results_charts_tab1]


####################
### Result Tab 2 ###
####################

results_charts_tab2 = [
    {
        'container_id': 'hc_res_wind_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Windenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Wind']
    },
    {
        'container_id': 'hc_res_pv_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Photovoltaik Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['PV']
    },
    {
        'container_id': 'hc_res_bio_time',
        'type': 'line',
        'setup_labels': {
            'title': {'text': 'Bioenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Biomasse', 'Biogas']
    }
]

results_charts_tab2_viz = [results.ResultAnalysisVisualization(
    setup_labels=chart['setup_labels'],
    data_labels=chart['data_labels'],
    type=chart['type']).visualize(renderTo=chart['container_id'])
                   for chart in results_charts_tab2]
