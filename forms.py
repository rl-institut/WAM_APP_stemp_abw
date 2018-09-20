from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Fieldset
#from crispy_forms.bootstrap import Field as bField


class LayerForm(forms.Form):

    # cbs = {name: forms.TypedChoiceField(
    #     label = 'Layer {}'.format(name),
    #     choices = (
    #         (1, "Yes"),
    #         (0, "No")
    #     ),
    #     coerce = lambda x: bool(int(x)),
    #     widget = forms.CheckboxInput,
    #     initial = '1',
    #     required = False,
    #     help_text='helptext',
    # )
    #        for name in LAYERS}


    # name = forms.TypedChoiceField(
    #     label = 'Substation label',
    #     choices = (
    #         (1, "Yes"),
    #         (0, "No")
    #     ),
    #     coerce = lambda x: bool(int(x)),
    #     widget = forms.CheckboxInput,
    #     initial = '1',
    #     required = False,
    #     #help_text='helptext',
    # )

    def __init__(self, layers=None, *args, **kwargs):
        if layers is None:
            raise ValueError('No layers given. Please add some in app_settings.')
        super(LayerForm, self).__init__(*args, **kwargs)

        for name in layers:
            self.fields[name] = forms.TypedChoiceField(
                                    label = 'Layer {}'.format(name),
                                    choices = (
                                        (1, "Yes"),
                                        (0, "No")
                                    ),
                                    coerce = lambda x: bool(int(x)),
                                    widget = forms.CheckboxInput,
                                    initial = '1',
                                    required = False,
                                    #help_text='helptext',
                                )

        self.helper = FormHelper()
        #self.helper.form_class = 'switch tiny'
        #self.helper.form_class = 'form-horizontal'
        #self.helper.field_class = 'col-lg-8'
        #LAYERS2 = LAYERS + ('name',)
        #self.helper.field_class = 'switch-input toggle-button'

        #x = (Field('name'), Field('name'))
        self.helper.layout = Layout(
            Div(*tuple(Field(name,
                             #css_class='bla',
                             id='cb_{}'.format(name),
                             )
                       for name in layers),
                #css_class='switch tiny'
                )
        )
        #self.helper[0:2].wrap(Field, css_class='switch-input toggle-button')
        #self.helper.all().wrap(Div, css_class="hello")
        #self.helper[0:2].wrap_together(Div, css_class="hello")
        # self.helper.layout = Layout(
        #     #*x
        #     *tuple(Field(name) for name in LAYERS)
        #     #Fieldset('Legend', 'name', 'name'),
        #      # for name in self.cbs.keys():
        #      #     Field(name, css_class='exampleSwitch1')
        #     #Field('name', css_class='exampleSwitch1'),
        #     #PrependedText('name', 'prepended text'),
        #
        #     # HTML("""
        #     #         <p>We use notes to get better</p>
        #     #     """),
        #     #Div('bla')
        #
        # )