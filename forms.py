from django import forms

from .widgets import LayerSelectWidget, SliderWidget

class LayerGroupForm(forms.Form):
    """Form for layer group"""

    def __init__(self, layers=None, *args, **kwargs):
        if layers is None:
            raise ValueError('No layers given. '
                             'Please add some in layers.cfg.')
        super(LayerGroupForm, self).__init__(*args, **kwargs)

        for name, data in layers.items():
            self.fields[name] = forms.TypedChoiceField(
                #label = 'Layer {}'.format(name),
                label = '',
                coerce = lambda x: bool(int(x)),
                widget=LayerSelectWidget(
                    attrs={'id': 'cb_{}'.format(name),
                           'title': data['title'],
                           'text': data['text'],
                           'color': data['style']['fillColor'],
                           'geom_type': data['geom_type'],
                           'name': name,
                           'checked': True if data['show'] == '1' else False
                           }
                ),
                required=False
            )


class ComponentGroupForm(forms.Form):
    """Form for esys components"""

    def __init__(self, components=None, *args, **kwargs):
        if components is None:
            raise ValueError('No components given. '
                             'Please add some in esys_components.cfg.')
        super(ComponentGroupForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper(self)
        # self.helper.template = 'forms/parameter_form.html'

        for name, data in components.items():
            if data['type'] == 'range':
                self.fields[name] = forms.FloatField(
                    label='sl_{}'.format(name),
                    widget=SliderWidget(
                        attrs={'id': 'sl_{}'.format(name),
                               'title': data['title'],
                               'text': data['text'],
                               'min': data['min'],
                               'max': data['max'],
                               'from': data['value'],
                               'step': data['step'],
                               #'name': name
                               }
                    ),
                    #initial = 1,
                    required = False
                )
