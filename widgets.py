from django.forms.widgets import CheckboxInput, NumberInput
from django.utils.safestring import mark_safe

from utils.widgets import CustomWidget


class LayerSelectWidget(CheckboxInput):
    template_name = 'widgets/layer_switch.html'

    # def __init__(self, attrs=None):
    #     super(CheckboxInput, self).__init__(attrs)


class SliderWidget(NumberInput):
    # Caution: As worksround, the slider was renamed as there's a template in
    # stemp app with the same name.
    # For details see https://github.com/rl-institut/WAM/issues/12
    template_name = 'widgets/slider_abw.html'

    # def __init__(self, step_size=1, attrs=None):
    #     super(SliderWidget, self).__init__(attrs)
    #     self.step_size = step_size
    #
    # def __get_precision(self):
    #     try:
    #         return len(str(self.step_size).split('.')[1])
    #     except IndexError:
    #         return 0
    #
    # def get_context(self, name, value, attrs):
    #     context = super(SliderWidget, self).get_context(name, value, attrs)
    #     context['widget']['step_size'] = self.step_size
    #     #context['widget']['precision'] = self.__get_precision()
    #     return context


class SwitchWidget(NumberInput):
    template_name = 'widgets/switch.html'


class ResultsWidget(CustomWidget):
    template_name = 'stemp_abw/results_full.html'

    def __init__(self, visualizations1, visualizations2):
        self.visualizations1 = visualizations1
        self.visualizations2 = visualizations2

    def get_context(self):
        return {
            'visualizations1': self.visualizations1,
            'visualizations2': self.visualizations2
        }

    def media(self):
        # Join all vis arrays
        vis_all = self.visualizations1 + self.visualizations2
        html = (
            "$('#btnExpand').on('click', function(e) {"
                "if ($('#panel-results').hasClass('is-collapsed')) {"
                    "setTimeout(function(){" +
                    '\n'.join([vis.media() for vis in vis_all]) +
                    "; }, 750);"
            "}});"
        )
        return mark_safe(html)
