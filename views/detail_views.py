import stemp_abw.models as models
from django.views.generic import DetailView



class MasterDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    context_object_name = 'obj'


    def get_context_data(self, **kwargs):
        context = super(MasterDetailView, self).get_context_data(**kwargs)
    
        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some substation content'
    
        return context

####################
### Detail Views ### for popups
####################
class SubstDetailView(MasterDetailView):
    model = models.HvMvSubst


class OsmPowerGenDetailView(MasterDetailView):
    model = models.OsmPowerGen


class RpAbwBoundDetailView(MasterDetailView):
    model = models.RpAbwBound


class RegMunDetailView(MasterDetailView):
    model = models.RegMun


class RegMunPopDensityDetailView(MasterDetailView):
    model = models.RegMunPopDensity
    template_name = 'stemp_abw/layer_popup_reg_mun_pop_density.html'


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
