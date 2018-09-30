from django.forms.widgets import CheckboxInput


class LayerSelectWidget(CheckboxInput):
    template_name = 'widgets/layer_select.html'

    # def __init__(self, attrs=None):
    #     super(CheckboxInput, self).__init__(attrs)
