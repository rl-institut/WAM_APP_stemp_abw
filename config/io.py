from collections import OrderedDict
import json
from stemp_abw.forms import LayerGroupForm, ComponentGroupForm

from stemp_abw.app_settings import LAYER_METADATA, LAYER_DEFAULT_STYLES, \
    ESYS_COMPONENTS_METADATA, LABELS


def prepare_layer_data():
    layer_data = {}

    # create layer list for AJAX data urls
    layer_list = {l: d['show'] for ls in LAYER_METADATA.values() for l, d in ls.items()}
    layer_data['layer_list'] = layer_list

    # create JSON for layer styles
    layer_style = {l: a['style'] for v in LAYER_METADATA.values() for l, a in v.items()}
    layer_style.update(LAYER_DEFAULT_STYLES)
    layer_data['layer_style'] = json.dumps(layer_style)

    # create JSON for choropleth layers
    choropleth_data = {l: a['choropleth'] for v in LAYER_METADATA.values() for l, a in v.items() if 'choropleth' in a}
    layer_data['choropleth_data'] = json.dumps(choropleth_data)

    # update layer and layer group labels using labels config
    layer_metadata = OrderedDict()
    for (grp, layers) in LAYER_METADATA.items():
        layer_metadata.update({grp: {'layers': layers}})
        layer_metadata[grp]['title'] = LABELS['layer_groups'][grp]['title']
        layer_metadata[grp]['text'] = LABELS['layer_groups'][grp]['text']
        for l, v in layers.items():
            layer_metadata[grp]['layers'][l]['title'] = LABELS['layers'][l]['title']
            layer_metadata[grp]['layers'][l]['text'] = LABELS['layers'][l]['text']

    # create layer groups for layer menu using layers config
    layer_groups = layer_metadata.copy()
    for grp, layers in layer_metadata.items():
        layer_groups[grp]['layers'] = LayerGroupForm(layers=layers['layers'])
    layer_data['layer_groups'] = layer_groups

    return layer_data


def prepare_component_data():
    component_data = {}
    # update component and component group labels using labels config
    comp_metadata = OrderedDict()
    for (grp, comps) in ESYS_COMPONENTS_METADATA.items():
        comp_metadata.update({grp: {'comps': comps}})
        comp_metadata[grp]['title'] = LABELS['component_groups'][grp]['title']
        comp_metadata[grp]['text'] = LABELS['component_groups'][grp]['text']
        for l, v in comps.items():
            comp_metadata[grp]['comps'][l]['title'] = LABELS['components'][l]['title']
            comp_metadata[grp]['comps'][l]['text'] = LABELS['components'][l]['text']

    # create component groups for esys menu using components config
    comp_groups = comp_metadata.copy()
    for grp, comps in comp_groups.items():
        comp_groups[grp]['comps'] = ComponentGroupForm(components=comps['comps'])
    component_data['comp_groups'] = comp_groups

    return component_data


def prepare_label_data():
    return {'panels': LABELS['panels']}
