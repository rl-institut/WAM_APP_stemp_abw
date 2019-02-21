from django import forms

from .widgets import LayerSelectWidget, SliderWidget, SwitchWidget


class LayerGroupForm(forms.Form):
    """Form for layer group"""

    def __init__(self, cat_name=None, layers=None, *args, **kwargs):
        if layers is None:
            raise ValueError('No layers given. '
                             'Please add some in layers.cfg.')
        if cat_name is None:
            raise ValueError('No category name specified.')

        super(LayerGroupForm, self).__init__(*args, **kwargs)

        for name, data in layers.items():
            self.fields[name] = forms.TypedChoiceField(
                label='',
                coerce=lambda x: bool(int(x)),
                widget=LayerSelectWidget(
                    attrs={'id': 'cb_{grp}_{name}'.format(grp=cat_name,
                                                          name=name),
                           'category': cat_name,
                           'name': name,
                           'title': data['title'],
                           'text': data['text'],
                           'color': data['style']['fillColor'],
                           'geom_type': data['geom_type'],
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
                    label='',
                    widget=SliderWidget(
                        attrs={'id': 'sl_{}'.format(name),
                               'name': name,
                               'title': f'{data["title"]} [{data["unit"]}]',
                               'text': data['text'],
                               'min': data['min'],
                               'max': data['max'],
                               'from': data['value'],
                               'step': data['step']
                               }
                    ),
                    required = False
                )
            elif data['type'] == 'bool':
                self.fields[name] = forms.TypedChoiceField(
                    label='',
                    coerce=lambda x: bool(int(x)),
                    widget=SwitchWidget(
                        attrs={'id': 'cb_{}'.format(name),
                               'name': name,
                               'title': data['title'],
                               'text': data['text'],
                               'checked': True if data['value'] == '1' else False
                               }
                    ),
                    required = False
                )
            else:
                raise TypeError(
                    f'Unknown value for "type" in esys_components.cfg at {name}')
