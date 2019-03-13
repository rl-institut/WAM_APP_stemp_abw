from collections import OrderedDict
from stemp_abw import results


# TODO: Temp stuff for WS
# Used in results as placeholder charts
labels1 = OrderedDict((
    ('Windenergie Erzeugung', ['Wind']),
    ('Photovoltaik Erzeugung', ['PV']),
    ('Bioenergie Erzeugung', ['Biomasse', 'Biogas'])
))
visualizations1 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                   for t, c in labels1.items()]

# TODO: Temp stuff for WS
# Used in results as placeholder charts
labels2 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations2 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                   for t, c in labels2.items()]

# TODO: Temp stuff for WS
# Used in popups as placeholder charts
labels3 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations3 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                   for t, c in labels3.items()]
