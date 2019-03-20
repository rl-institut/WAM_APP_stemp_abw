from utils.highcharts import Highchart


class HCStemp(Highchart):
    setup = {}

    def __init__(self, data=None, setup_labels=None, **kwargs):
        super(HCStemp, self).__init__(**kwargs)
        self.set_dict_options(self.setup)
        self.set_dict_options(setup_labels)
        if data is not None:
            series_type = self.setup.get('chart').get('type')
            self.add_pandas_data_set(data=data,
                                     series_type=series_type,
                                     **kwargs)


class HCTimeseries(HCStemp):
    setup = {
        'chart': {
            'type': 'line',
            'backgroundColor': 'rgba(255, 255, 255, 0.0)',
            'height': str(int(9 / 16 * 100)) + '%',  # 16:9 ratio
        },
        'xAxis': {
            'type': 'datetime'
        },
        'yAxis': {
            'min': 0
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
    }


class HCPiechart(HCStemp):
    setup = {
        'chart': {
            'type': 'pie',
            'backgroundColor': 'rgba(255, 255, 255, 0.0)',
            'height': str(int(9 / 16 * 100)) + '%',
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': False,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.y}<br>({point.percentage:.1f} %)',
                }
            }
        },
        'tooltip': {
            'headerFormat': None,
            'pointFormat': '{point.name}: <b>{point.percentage:.1f}%</b>'
        }
    }


class HCStackedColumn(HCStemp):
    setup = {
        'chart': {
            'type': 'column',
            'height': str(int(9 / 16 * 100)) + '%',
        },
        'yAxis': {
            'min': 0
        },
        'tooltip': {
            'headerFormat': '<b>{point.x}</b><br/>',
            'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': False
                }
            }
        }
    }
