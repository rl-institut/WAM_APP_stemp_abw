from utils.highcharts import Highchart

#####################
# Custom RLI themes #
#####################
# (overwrite main WAM RLI theme in utils/highcharts.py)

# theme for result charts
RESULT_THEME = {
    'credits': {
        'enabled': False
    },
    'colors': [
        '#fc8e65', '#55aae5', '#7fadb7', '#fce288', '#f69c3a', '#c28e5e',
        '#a27b82', '#797097'
    ],
    'title': {
        'style': {
            'color': 'rgb(0, 46, 79)',
        }
    },
    'subtitle': {
        'style': {
            'color': 'rgb(0, 46, 79)',
        }
    },
    'lang': {
        'decimalPoint': ',',
        'thousandsSep': '.'
    },
    'legend': {
        'itemStyle': {
            'font': '1em Roboto, Arial, sans-serif',
        },
        'itemHoverStyle': {
            'color': 'rgb(80, 126, 159)'
        }
    },
    'plotOptions': {
        'series': {
            'dataLabels': {
                'enabled': True,
                'style': {
                    'fontWeight': None,
                    'textOutline': None
                }
            }
        }
    },
    'loading': {
        'labelStyle': {
            'fontWeight': 'bold',
            'position': 'relative'
        },
        'style': {
            'backgroundColor': '#EBF2FA',
            'opacity': 0.8
        }
    }
}

# theme for popup charts
POPUP_THEME = {
    'credits': {
        'enabled': False
    },
    'chart': {'height': str(int(9 / 16 * 100)) + '%'},  # 16:9 ratio
    'colors': [
        '#fc8e65', '#55aae5', '#7fadb7', '#fce288', '#f69c3a', '#c28e5e',
        '#a27b82', '#797097'
    ],
    'title': {
        'style': {
            'color': 'rgb(0, 46, 79)',
            'font': '1.17em Roboto, Arial, sans-serif',
            'font-weight': '300'
        }
    },
    'subtitle': {
        'style': {
            'color': 'rgb(0, 46, 79)',
            'font': '1em Roboto, Arial, sans-serif',
            'font-weight': '300'
        }
    },
    'lang': {
        'decimalPoint': ',',
        'thousandsSep': '.'
    },
    'legend': {
        'itemStyle': {
            'font': '1em Roboto, Arial, sans-serif',
            'color': 'rgb(0, 46, 79)',
            'font-weight': '300'
        },
        'itemHoverStyle': {
            'color': 'rgb(80, 126, 159)'
        }
    },
    'plotOptions': {
        'series': {
            'dataLabels': {
                'enabled': False,
                'style': {
                    'fontWeight': None,
                    'textOutline': None
                }
            }
        }
    }
}


class HCStemp(Highchart):
    setup = {}

    def __init__(self, theme='results', data=None, setup_labels=None, **kwargs):
        super(HCStemp, self).__init__(**kwargs)
        self.set_dict_options(self.setup)
        self.set_dict_options(setup_labels)
        if theme == 'results':
            self.set_dict_options(RESULT_THEME)
        elif theme == 'popups':
            self.set_dict_options(POPUP_THEME)
        if data is not None:
            series_type = self.setup.get('chart').get('type')
            self.add_pandas_data_set(data=data,
                                     series_type=series_type)


class HCTimeseries(HCStemp):
    setup = {
        'chart': {
            'type': 'line',
            'backgroundColor': 'rgba(255, 255, 255, 0.0)'
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
            'backgroundColor': 'rgba(255, 255, 255, 0.0)'
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': False,
                'cursor': 'pointer',
                'dataLabels': {
                    'format': '<b>{point.name}</b>: {point.y}<br>({point.percentage:.1f} %)',
                    },
                'showInLegend': True
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
            'backgroundColor': 'rgba(255, 255, 255, 0.0)'
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
