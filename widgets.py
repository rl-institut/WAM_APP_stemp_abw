from django.forms.widgets import CheckboxInput, NumberInput


class LayerSelectWidget(CheckboxInput):
    template_name = 'widgets/layer_select.html'

    # def __init__(self, attrs=None):
    #     super(CheckboxInput, self).__init__(attrs)


class SliderWidget(NumberInput):
    input_type = 'number'
    template_name = 'widgets/esys_component.html'

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