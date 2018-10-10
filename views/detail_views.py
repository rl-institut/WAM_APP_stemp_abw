import stemp_abw.models as models
from django.views.generic import DetailView


####################
### Detail Views ### for popups
####################
class SubstDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.HvMvSubst
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(SubstDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some substation content'

        return context


class OsmPowerGenDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.OsmPowerGen
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(OsmPowerGenDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some generator content'

        return context


class RpAbwBoundDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RpAbwBound
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RpAbwBoundDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegMunDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegMun
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegMunDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegPrioAreaResDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaRes
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaResDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegWaterProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegWaterProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegWaterProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegBirdProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegBirdProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegBirdProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegBirdProtAreaB200DetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegBirdProtAreaB200
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegBirdProtAreaB200DetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegNatureProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegNatureProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegNatureProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegLandscProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegLandscProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegLandscProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegResidAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegResidArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegResidAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegResidAreaB500DetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegResidAreaB500
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegResidAreaB500DetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegPrioAreaFloodProtDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaFloodProt
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaFloodProtDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegPrioAreaCultDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaCult
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaCultDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegForestDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegForest
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegForestDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegFFHProtAreaDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegFFHProtArea
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegFFHProtAreaDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegResidAreaB1000DetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegResidAreaB1000
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegResidAreaB1000DetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class GenWECDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.GenWEC
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(GenWECDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegPrioAreaWECDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegPrioAreaWEC
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegPrioAreaWECDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegDeadZoneHardDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegDeadZoneHard
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegDeadZoneHardDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context


class RegDeadZoneSoftDetailView(DetailView):
    template_name = 'stemp_abw/layer_popup.html'
    model = models.RegDeadZoneSoft
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super(RegDeadZoneSoftDetailView, self).get_context_data(**kwargs)

        # TODO: Load more context from LAYER_METADATA, e.g. label & description
        context['bla'] = 'Some Planungsregion content'

        return context

