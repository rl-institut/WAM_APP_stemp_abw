from django.utils.translation import gettext_lazy as _
import pandas as pd
import stemp_abw.models as models
from django.views.generic import DetailView
from meta.models import Source
from stemp_abw.app_settings import labels, layer_region_metadata, \
    layer_result_metadata, layer_areas_metadata
from stemp_abw.visualizations import highcharts
from wam.settings import SESSION_DATA


class MasterDetailView(DetailView):
    mode = None
    template_name = 'stemp_abw/popups/base_layer_popup.html'
    context_object_name = 'layer'

    def get_source_data(self, metadata, app_name):
        """
        This method takes a metadata ConfigObj and returns a list
        with 0 OR n-amount of Source objects, if primary keys (PK)s
        of sources records in database are provided in ConfigObj object.
        Values in the metadata config file should correspond to PKs
        as list of values (1,2,3,...n). if the sole value 0 is provided
        in the metadata config file then the returned list is empty.

        Parameters
        ----------
        metadata : :obj:`ConfigObj`
        app_name : :obj:`str`

        Returns
        -------
        :obj:`list` of :obj:`wam.meta.models.Source`
            List with 0 OR n-amount of Source objects.
        """
        for layer_group in metadata.values():
            for layer in layer_group.values():
                if layer['model'] == self.model.name:
                    sources = []

                    # convert sources to list type if it's a string
                    # (happens if there's only 1 source)
                    if isinstance(layer['sources'], str):
                        layer['sources'] = [layer['sources']]

                    for source in layer['sources']:
                        if source == '0':
                            break
                        else:
                            sources.append(Source.objects
                                           .filter(app_name=app_name)
                                           .get(pk=source))
                    return sources
                else:
                    pass

    def get_context_data(self, **kwargs):
        context = super(MasterDetailView, self).get_context_data(**kwargs)

        _labels = labels()
        context['title'] = _labels['layers'][self.model.name]['title']
        context['text'] = _labels['layers'][self.model.name]['text']

        # Get app_name from request
        app_name = self.request.resolver_match.app_name
        # Gather all layer metadata ConfigObj objects
        layers_metadata = [layer_region_metadata(),
                           layer_result_metadata(),
                           layer_areas_metadata()]
        # Put sources PKs into context
        for layer_metadata in layers_metadata:
            source_layer_metadata = self.get_source_data(layer_metadata,
                                                         app_name)
            if source_layer_metadata is not None:
                context['sources'] = source_layer_metadata

        return context

    def chart_session_store(self, context):
        # Backup current HC to session if view for html is requested,
        # load from session if subsequent view for js is requested.
        session = SESSION_DATA.get_session(self.request)
        if session.highcharts_temp is None:
            context['chart'] = self.build_chart()
            session.highcharts_temp = context['chart']
        else:
            context['chart'] = session.highcharts_temp
            session.highcharts_temp = None


###########################
# Detail Views for popups #
###########################
class RpAbwBoundDetailView(MasterDetailView):
    model = models.RpAbwBound


class RegMunDetailView(MasterDetailView):
    model = models.RegMun


class RegMunPopDetailView(MasterDetailView):
    model = models.RegMunPop
    template_name = 'stemp_abw/popups/pop.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunPopDetailView, self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        pop_2017 = mun_data.pop_2017
        pop_2030 = mun_data.pop_2030
        pop_2050 = mun_data.pop_2050
        index = ['2017', '2030', '2050']
        data = pd.DataFrame(index=index,
                            data={str(_('Personen')): [pop_2017, pop_2030, pop_2050]})
        setup_labels = {
            'title': {'text': str(_('Bevölkerungsentwicklung'))},
            'subtitle': {'text': str(_('Prognose'))},
            'yAxis': {'title': {'text': str(_('Personen'))}}
        }
        chart = highcharts.HCTimeseries(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunPopDensityDetailView(MasterDetailView):
    model = models.RegMunPopDensity
    template_name = 'stemp_abw/popups/pop_density.html'


class RegMunEnergyReElDemShareDetailView(MasterDetailView):
    model = models.RegMunEnergyReElDemShare
    template_name = 'stemp_abw/popups/energy_re_el_dem_share.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunEnergyReElDemShareDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        reg_mun_dem_el_energy = models.RegMunDemElEnergy.objects.get(
            pk=self.kwargs['pk'])
        wind = round(((mun_data.gen_el_energy_wind / 1e3) /
                      reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_roof = round(((mun_data.gen_el_energy_pv_roof / 1e3) /
                         reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_ground = round(((mun_data.gen_el_energy_pv_ground / 1e3) /
                           reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        hydro = round(((mun_data.gen_el_energy_hydro / 1e3) /
                       reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        bio = round(((mun_data.gen_el_energy_bio / 1e3) /
                       reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        data = pd.DataFrame(data={
            'EE-Träger': {str(_('Wind')): wind, str(_('PV Dach')): pv_roof,
                          str(_('PV Freifläche')): pv_ground, str(_('Wasserkraft')): hydro,
                          str(_('Bioenergie')): bio}})
        setup_labels = {
            'title': {'text': str(_('EE-Erzeugung'))},
            'subtitle': {'text': str(_('in Prozent zum Strombedarf'))},
            'yAxis': {'title': {'text': str(_('Prozent'))}},
            'tooltip': {
                'pointFormat': str(_('Bedarf')) + ': {point.y:.1f} %'
            }
        }
        chart = highcharts.HCStackedColumn(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenEnergyReDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRe
    template_name = 'stemp_abw/popups/gen_energy_re.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / 1e3), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / 1e3), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / 1e3), 1)
        hydro = round((mun_data.gen_el_energy_hydro / 1e3), 1)
        bio = round((mun_data.gen_el_energy_bio / 1e3), 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Gewonnene Energie aus EE'))},
            'subtitle': {'text': str(_('nach Quelle'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                GWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenEnergyRePerCapitaDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRePerCapita
    template_name = 'stemp_abw/popups/gen_energy_re_per_capita.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyRePerCapitaDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / mun_data.pop_2017), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / mun_data.pop_2017), 1)
        pv_ground = round(
            (mun_data.gen_el_energy_pv_ground / mun_data.pop_2017), 1)
        hydro = round((mun_data.gen_el_energy_hydro / mun_data.pop_2017), 1)
        bio = round((mun_data.gen_el_energy_bio / mun_data.pop_2017), 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Gewonnene Energie aus EE'))},
            'subtitle': {'text': str(_('je EinwohnerIn'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenEnergyReDensityDetailView(MasterDetailView):
    model = models.RegMunGenEnergyReDensity
    template_name = 'stemp_abw/popups/gen_energy_re_density.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReDensityDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / mun_data.area), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / mun_data.area), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / mun_data.area), 1)
        hydro = round((mun_data.gen_el_energy_hydro / mun_data.area), 1)
        bio = round((mun_data.gen_el_energy_bio / mun_data.area), 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Gewonnene Energie aus EE'))},
            'subtitle': {'text': str(_('je km²'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCapReDetailView(MasterDetailView):
    model = models.RegMunGenCapRe
    template_name = 'stemp_abw/popups/gen_cap_re.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenCapReDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round(mun_data.gen_capacity_wind, 1)
        pv_roof = round(mun_data.gen_capacity_pv_roof_large, 1)
        pv_ground = round(mun_data.gen_capacity_pv_ground, 1)
        hydro = round(mun_data.gen_capacity_hydro, 1)
        bio = round(mun_data.gen_capacity_bio, 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach, groß')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Installierte Leistung EE'))},
            'subtitle': {'text': str(_('nach Quelle'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MW<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MW<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCapReDensityDetailView(MasterDetailView):
    model = models.RegMunGenCapReDensity
    template_name = 'stemp_abw/popups/gen_cap_re_density.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenCapReDensityDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_capacity_wind / mun_data.area), 2)
        pv_roof = round((mun_data.gen_capacity_pv_roof_large / mun_data.area),
                        2)
        pv_ground = round((mun_data.gen_capacity_pv_ground / mun_data.area), 2)
        hydro = round((mun_data.gen_capacity_hydro / mun_data.area), 2)
        bio = round((mun_data.gen_capacity_bio / mun_data.area), 2)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach, groß')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Installierte Leistung EE'))},
            'subtitle': {'text': str(_('je km²'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MW<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MW<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCountWindDensityDetailView(MasterDetailView):
    model = models.RegMunGenCountWindDensity
    template_name = 'stemp_abw/popups/gen_count_wind_density.html'


class RegMunDemElEnergyDetailView(MasterDetailView):
    model = models.RegMunDemElEnergy
    template_name = 'stemp_abw/popups/dem_el_energy.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemElEnergyDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_el_energy_hh / 1e3), 1)
        rca = round((mun_data.dem_el_energy_rca / 1e3), 1)
        ind = round((mun_data.dem_el_energy_ind / 1e3), 1)
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.')), str(_('Industrie'))],
            'y': [hh, rca, ind]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Strombedarf'))},
            'subtitle': {'text': str(_('nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                GWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunDemElEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemElEnergyPerCapita
    template_name = 'stemp_abw/popups/dem_el_energy_per_capita.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemElEnergyPerCapitaDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_el_energy_hh * 1000 / mun_data.pop_2017))
        rca = round((mun_data.dem_el_energy_rca * 1000 / mun_data.pop_2017))
        ind = round((mun_data.dem_el_energy_ind * 1000 / mun_data.pop_2017))
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.')), str(_('Industrie'))],
            'y': [hh, rca, ind]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Strombedarf'))},
            'subtitle': {'text': str(_('je EinwohnerIn nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        KWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                KWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunDemThEnergyDetailView(MasterDetailView):
    model = models.RegMunDemThEnergy
    template_name = 'stemp_abw/popups/dem_th_energy.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemThEnergyDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_th_energy_hh / 1e3), 1)
        rca = round((mun_data.dem_th_energy_rca / 1e3), 1)
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.'))],
            'y': [hh, rca]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_(' Wärmebedarf'))},
            'subtitle': {'text': str(_('nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                GWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunDemThEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemThEnergyPerCapita
    template_name = 'stemp_abw/popups/dem_th_energy_per_capita.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemThEnergyPerCapitaDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_th_energy_hh * 1000 / mun_data.pop_2017))
        rca = round((mun_data.dem_th_energy_rca * 1000 / mun_data.pop_2017))
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.'))],
            'y': [hh, rca]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Wärmebedarf'))},
            'subtitle': {'text': str(_('je EinwohnerIn nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        KWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                KWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegWaterProtAreaDetailView(MasterDetailView):
    model = models.RegWaterProtArea


class RegBirdProtAreaDetailView(MasterDetailView):
    model = models.RegBirdProtArea


class RegBirdProtAreaB200DetailView(MasterDetailView):
    model = models.RegBirdProtAreaB200


class RegNatureProtAreaDetailView(MasterDetailView):
    model = models.RegNatureProtArea


class RegLandscProtAreaPartsDetailView(MasterDetailView):
    model = models.RegLandscProtAreaParts


class RegResidAreaDetailView(MasterDetailView):
    model = models.RegResidArea


class RegResidAreaB500DetailView(MasterDetailView):
    model = models.RegResidAreaB500


class RegPrioAreaFloodProtDetailView(MasterDetailView):
    model = models.RegPrioAreaFloodProt


class RegSurfaceWaterDetailView(MasterDetailView):
    model = models.RegSurfaceWater


class RegPrioAreaCultDetailView(MasterDetailView):
    model = models.RegPrioAreaCult


class RegForestDetailView(MasterDetailView):
    model = models.RegForest


class RegFFHProtAreaDetailView(MasterDetailView):
    model = models.RegFFHProtArea


class RegResidAreaB1000DetailView(MasterDetailView):
    model = models.RegResidAreaB1000


class GenWECDetailView(MasterDetailView):
    model = models.GenWEC


class GenPVGroundDetailView(MasterDetailView):
    model = models.GenPVGround


class RegPrioAreaWECDetailView(MasterDetailView):
    model = models.RegPrioAreaWEC


class RegDeadZoneHardDetailView(MasterDetailView):
    model = models.RegDeadZoneHard


class RegDeadZoneSoftDetailView(MasterDetailView):
    model = models.RegDeadZoneSoft


class RegFFHProtAreaBDetailView(MasterDetailView):
    model = models.RegFFHProtAreaB


class RegLandscProtAreaDetailView(MasterDetailView):
    model = models.RegLandscProtArea


class RegNatureParkDetailView(MasterDetailView):
    model = models.RegNaturePark


class RegBioReserveDetailView(MasterDetailView):
    model = models.RegBioReserve


class RegRetentAreaEcosysDetailView(MasterDetailView):
    model = models.RegRetentAreaEcosys


class RegPrioAreaNatureDetailView(MasterDetailView):
    model = models.RegPrioAreaNature


class RegNatureMonumDetailView(MasterDetailView):
    model = models.RegNatureMonum


class RegPrioAreaWaterDetailView(MasterDetailView):
    model = models.RegPrioAreaWater


class RegPrioAreaAgriDetailView(MasterDetailView):
    model = models.RegPrioAreaAgri


class RegRetentAreaAgriDetailView(MasterDetailView):
    model = models.RegRetentAreaAgri


class RegPrioAreaResDetailView(MasterDetailView):
    model = models.RegPrioAreaRes


class RegInfrasRailwayDetailView(MasterDetailView):
    model = models.RegInfrasRailway


class RegInfrasRoadDetailView(MasterDetailView):
    model = models.RegInfrasRoad


class RegInfrasHvgridDetailView(MasterDetailView):
    model = models.RegInfrasHvgrid


class RegInfrasAviationDetailView(MasterDetailView):
    model = models.RegInfrasAviation


#######################
# RESULT DETAIL VIEWS #
#######################
class RegMunEnergyReElDemShareResultDetailView(MasterDetailView):
    model = models.RegMunEnergyReElDemShareResult
    template_name = 'stemp_abw/popups/result_energy_re_el_dem_share.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunEnergyReElDemShareResultDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        reg_mun_dem_el_energy = models.RegMunEnergyReElDemShareResult.objects.get(
            pk=self.kwargs['pk'])
        wind = round(((mun_data.gen_el_energy_wind / 1e3) /
                      reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_roof = round(((mun_data.gen_el_energy_pv_roof / 1e3) /
                         reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        pv_ground = round(((mun_data.gen_el_energy_pv_ground / 1e3) /
                           reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        hydro = round(((mun_data.gen_el_energy_hydro / 1e3) /
                       reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        bio = round(((mun_data.gen_el_energy_bio / 1e3) /
                     reg_mun_dem_el_energy.dem_el_energy) * 100, 1)
        data = pd.DataFrame(data={
            'EE-Träger': {str(_('Wind')): wind, str(_('PV Dach')): pv_roof,
                          str(_('PV Freifläche')): pv_ground, str(_('Wasserkraft')): hydro,
                          str(_('Bioenergie')): bio}})
        setup_labels = {
            'title': {'text': str(_('Ergebnis: EE-Erzeugung'))},
            'subtitle': {'text': str(_('in Prozent zum Strombedarf'))},
            'yAxis': {'title': {'text': str(_('Prozent'))}},
            'tooltip': {
                'pointFormat': str(_('Bedarf: {point.stackTotal} %'))
            }
        }
        chart = highcharts.HCStackedColumn(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenEnergyReResultDetailView(MasterDetailView):
    model = models.RegMunGenEnergyReResult
    template_name = 'stemp_abw/popups/result_gen_energy_re.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReResultDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / 1e3), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / 1e3), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / 1e3), 1)
        hydro = round((mun_data.gen_el_energy_hydro / 1e3), 1)
        bio = round((mun_data.gen_el_energy_bio / 1e3), 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Gewonnene Energie aus EE'))},
            'subtitle': {'text': str(_('nach Quelle'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                GWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenEnergyReDensityResultDetailView(MasterDetailView):
    model = models.RegMunGenEnergyReDensityResult
    template_name = 'stemp_abw/popups/result_gen_energy_re_density.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenEnergyReDensityResultDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_el_energy_wind / mun_data.area), 1)
        pv_roof = round((mun_data.gen_el_energy_pv_roof / mun_data.area), 1)
        pv_ground = round((mun_data.gen_el_energy_pv_ground / mun_data.area), 1)
        hydro = round((mun_data.gen_el_energy_hydro / mun_data.area), 1)
        bio = round((mun_data.gen_el_energy_bio / mun_data.area), 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach')), str(_('PV Freifläche')), str(_('Wasserkraft'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Gewonnene Energie aus EE'))},
            'subtitle': {'text': str(_('je km²'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCapReResultDetailView(MasterDetailView):
    model = models.RegMunGenCapReResult
    template_name = 'stemp_abw/popups/result_gen_cap_re.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenCapReResultDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round(mun_data.gen_capacity_wind, 1)
        pv_roof = round(mun_data.gen_capacity_pv_roof_large, 1)
        pv_ground = round(mun_data.gen_capacity_pv_ground, 1)
        hydro = round(mun_data.gen_capacity_hydro, 1)
        bio = round(mun_data.gen_capacity_bio, 1)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach, groß')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Installierte Leistung EE'))},
            'subtitle': {'text': str(_('nach Quelle'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MW<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MW<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCapReDensityResultDetailView(MasterDetailView):
    model = models.RegMunGenCapReDensityResult
    template_name = 'stemp_abw/popups/result_gen_cap_re_density.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunGenCapReDensityResultDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        wind = round((mun_data.gen_capacity_wind / mun_data.area), 2)
        pv_roof = round((mun_data.gen_capacity_pv_roof_large / mun_data.area),
                        2)
        pv_ground = round((mun_data.gen_capacity_pv_ground / mun_data.area), 2)
        hydro = round((mun_data.gen_capacity_hydro / mun_data.area), 2)
        bio = round((mun_data.gen_capacity_bio / mun_data.area), 2)
        data = pd.DataFrame({
            'name': [str(_('Wind')), str(_('PV Dach, groß')), str(_('PV Freifläche')),
                     str(_('Wasserkraft')), str(_('Bioenergie'))],
            'y': [wind, pv_roof, pv_ground, hydro, bio]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Installierte Leistung EE'))},
            'subtitle': {'text': str(_('je km²'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        MW<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                MW<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunGenCountWindDensityResultDetailView(MasterDetailView):
    model = models.RegMunGenCountWindDensityResult
    template_name = 'stemp_abw/popups/result_gen_count_wind_density.html'


class RegMunDemElEnergyResultDetailView(MasterDetailView):
    model = models.RegMunDemElEnergyResult
    template_name = 'stemp_abw/popups/result_dem_el_energy.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemElEnergyResultDetailView, self).get_context_data(
            **kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_el_energy_hh / 1e3), 1)
        rca = round((mun_data.dem_el_energy_rca / 1e3), 1)
        ind = round((mun_data.dem_el_energy_ind / 1e3), 1)
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.')), str(_('Industrie'))],
            'y': [hh, rca, ind]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Strombedarf'))},
            'subtitle': {'text': str(_('nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        GWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                GWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart


class RegMunDemElEnergyPerCapitaResultDetailView(MasterDetailView):
    model = models.RegMunDemElEnergyPerCapitaResult
    template_name = 'stemp_abw/popups/result_dem_el_energy_per_capita.html'

    def get_context_data(self, **kwargs):
        context = super(RegMunDemElEnergyPerCapitaResultDetailView,
                        self).get_context_data(**kwargs)
        self.chart_session_store(context)

        return context

    def build_chart(self):
        mun_data = models.MunData.objects.get(pk=self.kwargs['pk'])
        hh = round((mun_data.dem_el_energy_hh * 1000 / mun_data.pop_2017))
        rca = round((mun_data.dem_el_energy_rca * 1000 / mun_data.pop_2017))
        ind = round((mun_data.dem_el_energy_ind * 1000 / mun_data.pop_2017))
        data = pd.DataFrame({
            'name': [str(_('Haushalte')), str(_('GHD und Landw.')), str(_('Industrie'))],
            'y': [hh, rca, ind]
        })
        data.set_index('name', inplace=True)
        # Convert data to appropriate format for pie chart
        data = data.reset_index().to_dict(orient='records')
        setup_labels = {
            'title': {'text': str(_('Ergebnis: Strombedarf'))},
            'subtitle': {'text': str(_('je EinwohnerIn nach Verbrauchergruppe'))},
            'plotOptions': {
                'pie': {
                    'dataLabels': {
                        'format': '<b>{point.name}</b>: {point.y} \
                        KWh<br>({point.percentage:.1f} %)',
                    }
                }
            },
            'tooltip': {
                'pointFormat': '<b>{point.name}</b>: {point.y} \
                KWh<br>({point.percentage:.1f} %)'
            }
        }
        chart = highcharts.HCPiechart(
            data=data,
            setup_labels=setup_labels,
            style='display: inline-block',
            theme='popups'
        )
        return chart
