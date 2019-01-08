from utils.highcharts import Highchart, RLI_THEME


class HCStemp(Highchart):
    setup = {}

    def __init__(self, data=None, **kwargs):
        super(HCStemp, self).__init__(data,
                                      theme=RLI_THEME,
                                      setup=self.setup,
                                      **kwargs)


class HCTimeseries(HCStemp):
    setup = {
        'chart': {
            'type': 'line',
            'backgroundColor': '#EBF2FA',
            'height': str(int(9 / 16 * 100)) + '%' # 16:9 ratio
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
