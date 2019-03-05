import stemp_abw.models as models
from django.views.generic import DetailView
from stemp_abw.app_settings import LABELS


class MasterDetailView(DetailView):
    template_name = 'stemp_abw/popups/base_layer_popup.html'
    context_object_name = 'obj'


    def get_context_data(self, **kwargs):
        context = super(MasterDetailView, self).get_context_data(**kwargs)

        context['title'] = LABELS['layers'][self.model.name]['title']
        context['text'] = LABELS['layers'][self.model.name]['text']
    
        return context

####################
### Detail Views ### for popups
####################
class RpAbwBoundDetailView(MasterDetailView):
    model = models.RpAbwBound


class RegMunDetailView(MasterDetailView):
    model = models.RegMun


class RegMunPopDetailView(MasterDetailView):
    model = models.RegMunPop
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_pop.html'


class RegMunPopDensityDetailView(MasterDetailView):
    model = models.RegMunPopDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun_pop_density.html'


class RegMunEnergyReElDemShareDetailView(MasterDetailView):
    model = models.RegMunEnergyReElDemShare
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenEnergyReDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRe
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenEnergyRePerCapitaDetailView(MasterDetailView):
    model = models.RegMunGenEnergyRePerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenEnergyReDensityDetailView(MasterDetailView):
    model = models.RegMunGenEnergyReDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenCapReDetailView(MasterDetailView):
    model = models.RegMunGenCapRe
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenCapReDensityDetailView(MasterDetailView):
    model = models.RegMunGenCapReDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunGenCountWindDensityDetailView(MasterDetailView):
    model = models.RegMunGenCountWindDensity
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunDemElEnergyDetailView(MasterDetailView):
    model = models.RegMunDemElEnergy
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunDemElEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemElEnergyPerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunDemThEnergyDetailView(MasterDetailView):
    model = models.RegMunDemThEnergy
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


class RegMunDemThEnergyPerCapitaDetailView(MasterDetailView):
    model = models.RegMunDemThEnergyPerCapita
    template_name = 'stemp_abw/popups/layer_popup_reg_mun.html'


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
