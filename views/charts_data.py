from collections import OrderedDict
from stemp_abw import results


# TODO: Temp stuff for WS
labels1 = OrderedDict((
    ('Windenergie Erzeugung', ['Wind']),
    ('Photovoltaik Erzeugung', ['PV']),
    ('Bioenergie Erzeugung', ['Biomasse', 'Biogas'])
))
visualizations1 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                   for t, c in labels1.items()]


labels2 = {'Erzeugung': ['Strom', 'Wärme'],
           'Bedarf': ['Strom', 'Wärme'],
           'Erneuerbare Energien': ['Wind', 'Solar']
           }
visualizations2 = [results.ResultAnalysisVisualization(title=t, captions=c).visualize()
                   for t, c in labels2.items()]



reg_mun_detail_js = """
    console.log("For a fistful of codelines, I will show RegMun's JS!");
    setTimeout(function() {
        $(function () {
            Highcharts.setOptions({"global": {}, "lang": {}});
            var option = {
                "chart": {"renderTo": "hc_test_1", "type": "line", "backgroundColor": "#EBF2FA"},
                "colors": ["#fc8e65", "#55aae5", "#7fadb7", "#fce288", "#f69c3a", "#c28e5e", "#a27b82", "#797097"],
                "credits": {"enabled": false},
                "drilldown": {},
                "exporting": {},
                "labels": {},
                "legend": {
                    "itemStyle": {"font": "1rem Trebuchet MS, Verdana, sans-serif", "color": "black"},
                    "itemHoverStyle": {"color": "gray"},
                    "layout": "vertical",
                    "align": "right",
                    "verticalAlign": "middle"
                },
                "loading": {},
                "navigation": {},
                "pane": {},
                "plotOptions": {},
                "series": {},
                "subtitle": {
                    "style": {"color": "#666", "font": "bold 12px Verdana, sans-serif"},
                    "text": "in GW"
                },
                "title": {
                    "text": "Gemeinden",
                    "style": {"color": "#002E4F", "font": "bold 1.2rem Verdana, sans-serif"}
                },
                "tooltip": {},
                "xAxis": {
                    "type": "datetime",
                    "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                },
                "yAxis": {"min": 0, "title": {"text": "GW"}}
            };
            var chart = new Highcharts.Chart(option);
            var data = [{
                "data": [6.39, 4.03, 0.9, 4.15, 9.18, 3.15, 7.27, 3.46, 3.19, 1.65, 7.07, 4.95],
                "type": "column",
                "name": "Wind"
            }];
            var dataLen = data.length;
            for (var ix = 0; ix < dataLen; ix++) {
                chart.addSeries(data[ix]);
                }
        });
    }, 500);
"""

reg_mun_pop_detail_js = """
    console.log("For a fistful of codelines, I will show RegMunPopDensity's JS!");
    setTimeout(function() {
        $(function () {
            Highcharts.setOptions({"global": {}, "lang": {}});
            var option = {
                "chart": {"renderTo": "hc_test_2", "type": "line", "backgroundColor": "#EBF2FA"},
                "colors": ["#fc8e65", "#55aae5", "#7fadb7", "#fce288", "#f69c3a", "#c28e5e", "#a27b82", "#797097"],
                "credits": {"enabled": false},
                "drilldown": {},
                "exporting": {},
                "labels": {},
                "legend": {
                    "itemStyle": {"font": "1rem Trebuchet MS, Verdana, sans-serif", "color": "black"},
                    "itemHoverStyle": {"color": "gray"},
                    "layout": "vertical",
                    "align": "right",
                    "verticalAlign": "middle"
                },
                "loading": {},
                "navigation": {},
                "pane": {},
                "plotOptions": {},
                "series": {},
                "subtitle": {
                    "style": {"color": "#666", "font": "bold 12px Verdana, sans-serif"},
                    "text": "in GW"
                },
                "title": {
                    "text": "EinwohnerInnen",
                    "style": {"color": "#002E4F", "font": "bold 1.2rem Verdana, sans-serif"}
                },
                "tooltip": {},
                "xAxis": {
                    "type": "datetime",
                    "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                },
                "yAxis": {"min": 0, "title": {"text": "GW"}}
            };
            var chart = new Highcharts.Chart(option);
            var data = [{
                "data": [3.56, 1.95, 8.62, 7.99, 6.31, 0.2, 3.33, 2.6, 2.21, 7.52, 2.89, 2.54],
                "type": "column",
                "name": "Biomasse"
            }, {
                "data": [3.04, 3.8, 9.97, 3.33, 3.04, 5.24, 4.67, 0.38, 9.11, 0.8, 1.8, 9.21],
                "type": "column",
                "name": "Biogas"
            }];
            var dataLen = data.length;
            for (var ix = 0; ix < dataLen; ix++) {
                chart.addSeries(data[ix]);
            }
        });
    }, 500);
"""

reg_mun_pop_density_detail_js = """
    console.log("For a fistful of codelines, I will show RegMunPop's JS!");
    setTimeout(function() {
        $(function () {
            Highcharts.setOptions({"global": {}, "lang": {}});
            var option = {
                "chart": {"renderTo": "hc_test_3", "type": "line", "backgroundColor": "#EBF2FA"},
                "colors": ["#fc8e65", "#55aae5", "#7fadb7", "#fce288", "#f69c3a", "#c28e5e", "#a27b82", "#797097"],
                "credits": {"enabled": false},
                "drilldown": {},
                "exporting": {},
                "labels": {},
                "legend": {
                    "itemStyle": {"font": "1rem Trebuchet MS, Verdana, sans-serif", "color": "black"},
                    "itemHoverStyle": {"color": "gray"},
                    "layout": "vertical",
                    "align": "right",
                    "verticalAlign": "middle"
                },
                "loading": {},
                "navigation": {},
                "pane": {},
                "plotOptions": {},
                "series": {},
                "subtitle": {
                    "style": {"color": "#666", "font": "bold 12px Verdana, sans-serif"},
                    "text": "in GW"
                },
                "title": {
                    "text": "Bevölkerungsdichte",
                    "style": {"color": "#002E4F", "font": "bold 1.2rem Verdana, sans-serif"}
                },
                "tooltip": {},
                "xAxis": {
                    "type": "datetime",
                    "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                },
                "yAxis": {"min": 0, "title": {"text": "GW"}}
            };
            var chart = new Highcharts.Chart(option);
            var data = [{
                "data": [3.73, 7.41, 3.51, 6.08, 1.0, 6.39, 6.03, 8.05, 8.74, 2.76, 2.48, 5.01],
                "type": "column",
                "name": "PV"
            }];
            var dataLen = data.length;
            for (var ix = 0; ix < dataLen; ix++) {
                chart.addSeries(data[ix]);
            }
        });
    }, 500);
"""