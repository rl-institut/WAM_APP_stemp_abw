import os
from django import forms
from .widgets import LayerSelectWidget, SliderWidget, EsysSwitchWidget
from stemp_abw.models import Scenario
from stemp_abw.app_settings import get_language_or_fallback

# do not execute when on RTD (reqd for API docs):
if 'READTHEDOCS' not in os.environ:
    from stemp_abw.dataio.load_static import load_repowering_scenarios
    REPOWERING_SCENARIOS = load_repowering_scenarios()


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
                attrs = {'id': 'sl_{}'.format(name),
                         'name': name,
                         'cell_style': '',
                         'title': f'{data["title"]} [{data["unit"]}]',
                         'text': data['text'],
                         'text2': data.get('text2'),
                         'popup': data.get('popup'),
                         'icon': data.get('icon'),
                         'min': data['min'],
                         'max': data['max'],
                         'from': data['value'],
                         'step': data['step'],
                         'grid_num': data['grid_count'],
                         'disable': True if data.get('disable') == '1' else False,
                         'extra_classes': ''
                         }
                # If slider is wind, add dropdown data.
                # It is required to provide data via widget as a new <select>
                # element cannot be added to the slider list
                lang = get_language_or_fallback().lower()[:2]
                if attrs.get('id') == 'sl_wind':
                    attrs['dropdown'] = []
                    for c in REPOWERING_SCENARIOS:
                        if lang == 'de':
                            opt = '<option value="{id}">{val}</option>'\
                                .format(id=c.id, val=c.name_de)
                        elif lang == 'en':
                            opt = '<option value="{id}">{val}</option>'\
                                .format(id=c.id, val=c.name_en)
                        else:
                            opt = '<option value="{id}">{val}</option>'\
                                .format(id=c.id, val=c.name_de)
                        attrs['dropdown'].append(opt)

                self.fields[name] = forms.FloatField(
                    label='',
                    widget=SliderWidget(attrs=attrs),
                    required = False
                )
            elif data['type'] == 'bool':
                self.fields[name] = forms.TypedChoiceField(
                    label='',
                    coerce=lambda x: bool(int(x)),
                    widget=EsysSwitchWidget(
                        attrs={'id': 'cb_{}'.format(name),
                               'name': name,
                               'title': data['title'],
                               'text': data['text'],
                               'text2': data.get('text2'),
                               'popup': data.get('popup'),
                               'icon': data.get('icon'),
                               'checked': True if data['value'] == '1' else False
                               }
                    ),
                    required = False
                )
            else:
                raise ValueError(
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
                               'popup': data.get('popup'),
                               'icon': data.get('icon'),
                               'min': data['min'],
                               'max': data['max'],
                               'from': data['value'],
                               'step': data['step'],
                               'grid_num': data['grid_count'],
                               'disable': True if data.get('disable') == '1' else False,
                               'extra_classes': 'rc-tooltip-trigger-override'
                               }
                    ),
                    required = False
                )
            elif data['type'] == 'bool':
                self.fields[name] = forms.TypedChoiceField(
                    label='',
                    coerce=lambda x: bool(int(x)),
                    widget=EsysSwitchWidget(
                        attrs={'id': 'cb_{}'.format(name),
                               'class': 'esys',
                               'name': name,
                               'title': data['title'],
                               'text': data['text'],
                               'popup': data.get('popup'),
                               'icon': data.get('icon'),
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
