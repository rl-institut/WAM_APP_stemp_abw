from stemp_abw import results


# TODO: Temp stuff for WS
# LineChart: used in results as placeholder charts
labels1 = [
    {
        'setup_labels': {
            'title': {'text': 'Windenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Wind']
    },
    {
        'setup_labels': {
            'title': {'text': 'Photovoltaik Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['PV']
    },
    {
        'setup_labels': {
            'title': {'text': 'Bioenergie Erzeugung'},
            'subtitle': {'text': 'in GW'},
            'yAxis': {'title': {'text': 'GW'}}
        },
        'data_labels': ['Biomasse', 'Biogas']
    }
]
visualizations1 = [results.ResultAnalysisVisualization(
    setup_labels=l['setup_labels'],
    data_labels=l['data_labels'],
    type='line').visualize() for l in labels1]


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
# PieChart: used in popups as placeholder charts
labels4 = [
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
visualizations4 = [results.ResultAnalysisVisualization(
    setup_labels=l['setup_labels'],
    data_labels=l['data_labels'],
    type='pie').visualize() for l in labels4]


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
