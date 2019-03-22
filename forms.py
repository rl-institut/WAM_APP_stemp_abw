from django import forms
from .widgets import LayerSelectWidget, SliderWidget, SwitchWidget

from stemp_abw.models import Scenario


class LayerGroupForm(forms.Form):
    """Form for layer group (regional info)"""

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
                rep = {1: 'Kein',
                       2: 'Verhältnis 1:1'}
                attrs = {'id': 'sl_{}'.format(name),
                         'name': name,
                         'cell_style': '',
                         'title': f'{data["title"]} [{data["unit"]}]',
                         'text': data['text'],
                         'min': data['min'],
                         'max': data['max'],
                         'from': data['value'],
                         'step': data['step'],
                         'grid_num': data['grid_count'],
                         'disable': True if data.get('disable') == '1' else False
                         }
                # If slider is wind, add dropdown data.
                # It is required to provide data via widget as a new <select>
                # element cannot be added to the slider list
                if attrs.get('id') == 'sl_wind':
                    attrs['dropdown'] = ['<option value="{id}">{val}</option>'
                                             .format(id=c[0], val=c[1])
                                         for c in rep.items()]
                self.fields[name] = forms.FloatField(
                    label='',
                    widget=SliderWidget(attrs=attrs),
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


class AreaGroupForm(forms.Form):
    """Form for layer group (variable layers)"""

    def __init__(self, components=None, *args, **kwargs):
        if components is None:
            raise ValueError('No areas given. '
                             'Please add some in esys_areas.cfg.')
        super(AreaGroupForm, self).__init__(*args, **kwargs)

        for name, data in components.items():
            if data['type'] == 'range':
                self.fields[name] = forms.FloatField(
                    label='',
                    widget=SliderWidget(
                        attrs={'id': 'sl_{}'.format(name),
                               'name': name,
                               'cell_style': 'margin-bottom: 1.5rem;',
                               'title': f'{data["title"]} [{data["unit"]}]',
                               'text': data['text'],
                               'min': data['min'],
                               'max': data['max'],
                               'from': data['value'],
                               'step': data['step'],
                               'grid_num': data['grid_count'],
                               'disable': True if data.get('disable') == '1' else False
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
                               'class': 'esys',
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
                    f'Unknown value for "type" in esys_areas.cfg at {name}')


class ScenarioDropdownForm(forms.Form):
    """Form for scneario dropdown menu (predefined scenarios only)"""

    def __init__(self, *args, **kwargs):
        super(ScenarioDropdownForm, self).__init__(*args, **kwargs)

        self.fields['scn'] = forms.ChoiceField(
            choices=[(scn.id, str(scn))
                     for scn in Scenario.objects.filter(is_user_scenario=False)])
