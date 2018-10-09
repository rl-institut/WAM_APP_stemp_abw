from utils.highcharts import Highchart, RLI_THEME


class HCStemp(Highchart):
    setup = {}

    def __init__(self, data, title):
        self.setup['title']['text'] = title
        super(HCStemp, self).__init__(data, theme=RLI_THEME, setup=self.setup, style=self.style)


class HCTimeseries(HCStemp):
    style = 'line'
    setup = {
        'chart': {
            'type': 'line',
            'backgroundColor': '#EBF2FA',
            #'width': '100%',
            'height': str(int(9 / 16 * 100)) + '%' # 16:9 ratio
            #'borderColor': '#002E4F',
            #'borderWidth': 3
        },
        'title': {
            'text': '',
        },
        'subtitle': {
            'text': 'in GW'
        },
        'xAxis': {
            'type': 'datetime'
        },
        'yAxis': {
            'min': 0,
            'title': {'text': 'GW'}
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
    }

class HCCosts(HCStemp):
    setup = {
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': 'Wärmekosten',
        },
        'subtitle': {
            'text': 'Cent pro Kilowattstunde'
        },
        'xAxis': {
            'categories': ['BHKW', 'PV + Wärmepumpe', 'Ölheizung', 'Gasheizung']
        },
        'yAxis': {
            'min': 0,
            'title': {'text': ''},
            'stackLabels': {
                'enabled': True,
                'style': {
                    'fontWeight': 'bold',
                    'color': "(Highcharts.theme && Highcharts.theme.textColor) || 'gray'"
                }
            }
        },
        'tooltip': {
            'headerFormat': '<b>{point.x}</b><br/>',
            'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True,
                    'color': "(Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'"
                }
            }
        },
    }
