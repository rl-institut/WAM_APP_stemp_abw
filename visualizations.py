from utils.highcharts import Highchart


class HCStemp(Highchart):
    setup = {}

    def __init__(self, data=None, title='New Highchart', **kwargs):
        super(HCStemp, self).__init__(**kwargs)
        self.set_dict_options(self.setup)
        self.set_options('title', {'text': title})
        if data is not None:
            self.add_pandas_data_set(data)


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
