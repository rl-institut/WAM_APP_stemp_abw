from collections import OrderedDict
from stemp_abw import results


# TODO: Temp stuff for WS
# LineChart: used in results as placeholder charts
labels1 = OrderedDict((
    ('Windenergie Erzeugung', ['Wind']),
    ('Photovoltaik Erzeugung', ['PV']),
    ('Bioenergie Erzeugung', ['Biomasse', 'Biogas'])
))
visualizations1 = [results.ResultAnalysisVisualization(title=t, captions=c, type='line').visualize()
                   for t, c in labels1.items()]

# TODO: Temp stuff for WS
# LineChart: used in results as placeholder charts
labels2 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations2 = [results.ResultAnalysisVisualization(title=t, captions=c, type='line').visualize()
                   for t, c in labels2.items()]

# TODO: Temp stuff for WS
# LineChart: used in popups as placeholder charts
labels3 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations3 = [results.ResultAnalysisVisualization(title=t, captions=c, type='line').visualize()
                   for t, c in labels3.items()]


# TODO: Temp stuff for WS
# PieChart: used in popups as placeholder charts
labels4 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations4 = [results.ResultAnalysisVisualization(title=t, captions=c, type='pie').visualize()
                   for t, c in labels4.items()]
