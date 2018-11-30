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
