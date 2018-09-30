from django import forms

from .widgets import LayerSelectWidget


class LayerSelectForm(forms.Form):

    def __init__(self, layers=None, *args, **kwargs):
        if layers is None:
            raise ValueError('No layers given. Please add some in app_settings.')
        super(LayerSelectForm, self).__init__(*args, **kwargs)

        for name in layers:
            self.fields[name] = forms.TypedChoiceField(
                                    label = 'Layer {}'.format(name),
                                    choices = (
                                        (1, "Yes"),
                                        (0, "No")
                                    ),
                                    coerce = lambda x: bool(int(x)),
                                    widget=LayerSelectWidget(
                                        attrs={'id': 'cb_{}'.format(name),
                                               'label': 'Layer {}'.format(name),
                                               'name': name}
                                    ),
                                    initial = '1',
                                    required = False
                                )
