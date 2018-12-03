from django import forms

from .widgets import LayerSelectWidget


class LayerSelectForm(forms.Form):
    """Form for layer group"""

    def __init__(self, layers=None, *args, **kwargs):
        if layers is None:
            raise ValueError('No layers given. '
                             'Please add some in layers.cfg.')
        super(LayerSelectForm, self).__init__(*args, **kwargs)

        for name, data in layers.items():
            self.fields[name] = forms.TypedChoiceField(
                #label = 'Layer {}'.format(name),
                label = '',
                # choices = (
                #     (1, "Yes"),
                #     (0, "No")
                # ),
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
                #initial = 1,
                required = False
            )
