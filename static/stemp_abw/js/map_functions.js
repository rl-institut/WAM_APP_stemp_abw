// Get color and step values as associated array
function getColorValues(schema, min, max, step, reverse) {

  // Convert to floats
  min = parseFloat(min);
  max = parseFloat(max);
  step = parseFloat(step);

  // Get number if digits to round resulting range values below
  var numberOfDigits = Math.ceil(Math.log(step + 1) / Math.LN10);

  // Get the sum of steps by step (interval)
  var sumSteps = parseInt((max - min) / step);

  // Get dividable interval step from steps
  // This is necessary, if "((max - min) / step)" produced rest
  var stepInterval = (max - min) / sumSteps;

  // Get colors for schema
  var colors = chroma.scale(schema).colors(sumSteps + 1);

  // Reverse colors if reverse value is true
  if (reverse == "true") {
    colors = colors.reverse();
  }

  // Combine colors and values of step intervals
  var colorsAndStepValues = {};
  colorsAndStepValues['values'] = [];
  var base = min;
  for (var i = 0; i < colors.length; i++) {
    colorsAndStepValues['values'][parseFloat(base)] = colors[i];
    base = parseFloat(
        (parseFloat(base) + stepInterval).toFixed(numberOfDigits)
    );
  }

  // Add max value
  colorsAndStepValues['max'] = max;

  return colorsAndStepValues;
}

// Get explicit color value from associated array and
// supplied averaged value
function getColor(colorVals, averagedValue) {
  for (var stepVal in colorVals['values']) {
    if (averagedValue <= stepVal) {
      return colorVals['values'][stepVal];
    }
    // Check if averageValue exceeds max value.
    if (averagedValue > colorVals['max']) {
      return colorVals['values'][colorVals['max']];
    }
  }
  // No color found - return '#FFFFFF'.
  // This should never happen.
  return '#FFFFFF';
}

// feature: click style
function execClickAction(e) {
  var style = getLayerStyle("_click");
  var layer = e.target;
  layer.setStyle(style);

  // load popup content from detail view
  console.log(layer.feature.properties.name);
  var url = "../popup/" + layer.feature.properties.name + "/"
      + String(layer.feature.id) + "/"
  console.log(url);
  $.get(url, function (data) {
    layer.setPopupContent(data);
    if (data.indexOf('id="hc_') !== -1) {
      var url_js = "../popupjs/" + layer.feature.properties.name + "/"
          + String(layer.feature.id) + "/"
      $.get(url_js, function (data) {
        setTimeout(function () {
          eval(data);
        }, 250);
      });
    }
  });

  // center map to clicked location, consider viewport size and panel area
  var new_center = layer._map.project(e.latlng);
  var map_size = layer._map.getSize();
  new_center.y -= map_size.y / 4; // find the height of the popup container, divide by 2, subtract from the Y axis of marker location
  new_center.x -= map_size.x / 8;
  layer._map.panTo(layer._map.unproject(new_center), {duration: 1.5}); // pan to new center
}

// feature: mousover style
function setHighlightFeatureStyle(e) {
  var style = getLayerStyle("_highlight");
  var layer = e.target;
  layer.setStyle(style);
}

// feature: normal style
function setNormalFeatureStyle(layerName, feature) {
  return function _(e) {
    var style = getLayerStyle(layerName, feature);
    var layer = e.target;
    layer.setStyle(style);
  };
}

// bind popups for each feature and define event actions
function onEachFeature(layerName) {
  return function (feature, layer) {
    // popup style
    var customPopup =
        {
          'maxWidth': '500',
          'className': 'custom_popup'
        }
    if (feature.properties) {
      layer.bindPopup('', customPopup);
    }
    layer.on({
      click: execClickAction,
      mouseover: setHighlightFeatureStyle,
      mouseout: setNormalFeatureStyle(layerName, feature)
    });
  };
}

// TEMP FUNCTION TO PREVENT RESULT LAYER POPUPS
function onEachFeatureNoPopup(layerName) {
  return function (feature, layer) {
    layer.on({
      mouseover: setHighlightFeatureStyle,
      mouseout: setNormalFeatureStyle(layerName, feature)
    });
  };
}

function pointToLayer(feature, latlng) {
  var marker = L.circleMarker(latlng)
  return marker;
}

// Create layer style from style_data json obj
// if it does not exist, use default
function getLayerStyle(name, feature) {
  if (choropleth_data.hasOwnProperty(name)) {
    var column = choropleth_data[name].data_column;
    var schema = choropleth_data[name].color_schema;
    var min = choropleth_data[name].min;
    var max = choropleth_data[name].max;
    var step = choropleth_data[name].step;
    var reverse = choropleth_data[name].reverse;
    var colorVals = getColorValues(schema, min, max, step, reverse);
    var fill = getColor(colorVals, feature.properties[column]);
    return {
      fillColor: fill,
      weight: style_data[name].weight,
      opacity: style_data[name].opacity,
      color: style_data[name].color,
      fillOpacity: style_data[name].fillOpacity,
    };
  } else if (style_data.hasOwnProperty(name)) {
    return style_data[name];
  } else {
    return style_data._default;
  }
}

// Control layer visibility via checkboxes (region layers)
$('.switch-input-layer-select-region, .switch-input-layer-select-results').click(function () {
  var id = $(this).attr('id');

  // Individual layers switches
  l = layers[id.replace(/cb_(region|results)_/, '')];
  console.log("Adding OR removing from lmap: " + lmap);
  if (this.checked) lmap.addLayer(l);
  else lmap.removeLayer(l);
});

// Control layer visibility via checkboxes (areas layers)
$('.switch-input-layer-select-areas').click(function () {
  var id = $(this).attr('id');

  // Master switch for all layers
  if (id == "cb_all_areas_layers") {
    for (var l in layers) {
      if (layers.hasOwnProperty(l) && layers_cat[l] == 'areas') {
        if (this.checked) lmap.addLayer(layers[l]);
        else lmap.removeLayer(layers[l]);
      }
      $('.switch-input-layer-select-areas').prop('checked', this.checked);
    }
  }

  // Individual layers switches
  else {
    l = layers[id.replace('cb_areas_', '')];
    if (this.checked) lmap.addLayer(l);
    else lmap.removeLayer(l);
  }
  ;
});


// Region layers: control legend visibility via checkboxes
$('.switch-input-layer-select-region, .switch-input-layer-select-results').click(function () {
  var id = $(this).attr('id');

  // Master switch for all legends
  // (CURRENTLY DISABLED AS ONLY REGION LAYER LIST CONTAINS CHORO MAPS)
  /*
  if (id == "cb_all_areas_layers") {
    for (var l in legends) {
      if (legends.hasOwnProperty(l)) {
        lmap.removeControl(legends[l]);
      }
    $('.switch-input-layer-select').prop('checked', this.checked);
    }
  }
  */

  // Individual legend switches
  //else {
  id = id.replace(/cb_(region|results)_/, '');
  for (var l in legends) {
    if (l !== id && choropleth_data.hasOwnProperty(id)) {
      if (this.checked) {
        lmap.removeLayer(layers[l]);
        lmap.removeControl(legends[l]);
        var el = document.querySelector('#cb_region_' + l + ', ' + '#cb_results_' + l);
        el.checked = false;
      }
    } else if (l === id) {
      l = legends[id];
      if (this.checked) l.addTo(lmap);
      else lmap.removeControl(l);
    }
  }
  //}
});

// temp for RE pot layer control
function addRePotAreaLayer() {
  // Remove all layers
  removeRePotAreaLayers();

  // Get controls' status
  sl_val = Math.round($('#sl_dist_resid').data("ionRangeSlider").result.from);
  sw_val = $('#cb_use_forest').prop('checked');

  // TODO: add mapping from properties to layer

  // Add needed layer
  if (sl_val == 1000) {
    if (sw_val == false) {
      lmap.addLayer(layers_re_pot['1']);
      wec_count = 179;
    } else {
      lmap.addLayer(layers_re_pot['2']);
      wec_count = 345;
    }
  } else if (sl_val == 1500) {
    if (sw_val == false) {
      lmap.addLayer(layers_re_pot['3']);
      wec_count = 37;
    } else {
      lmap.addLayer(layers_re_pot['4']);
      wec_count = 128;
    }
  } else if (sl_val == 500) {
    if (sw_val == false) {
      lmap.addLayer(layers_re_pot['5']);
      wec_count = 439;
    } else {
      lmap.addLayer(layers_re_pot['6']);
      wec_count = 738;
    }
  }

  $('#sl_wind').data("ionRangeSlider").update({
    max: Math.round(wec_count * 4.2)
  });

  // post wind slider value, this is needed as the slider value is adjusted
  // by area controls in free repowering scn but not updated in backend scenario,
  // cf. https://github.com/rl-institut/WAM_APP_stemp_abw/issues/106
  if ($('#dd_repowering').prop('value') == -1) {
    ctrlScenarioPost('sl_wind', $('#sl_wind').data("ionRangeSlider").result.from);
  }

}

// Remove all RE pot layers
function removeRePotAreaLayers() {
  for (var l in layers_re_pot) {
    lmap.removeLayer(layers_re_pot[l]);
  }
}

// Lock result switches if results are null
var result_panel = document.querySelector('#panel-results fieldset');
var result_switches = result_panel.querySelectorAll('.switch-input-layer-select-results');
var simulation_info = document.getElementById('simulation-info');


function resultDependentSwitchLocker() {
  console.log('Fired: resultDependentSwitchLocker (), ' + Date.now());
  // Reset switch override if given
  // Check if results == null, and add switch override
  $.ajax({
    url: '/stemp_abw/sim_status.data',
    type: "GET",
    success: function (data) {
      console.log('Ajax success fired: resultDependentSwitchLocker (), ' + Date.now())
      if (data['sim_status'] != 'up_to_date') {
        if (simulation_info.hidden === true) {
          simulation_info.hidden = false;
        }
        result_switches.forEach(function (currentValue) {
              currentValue.setAttribute('disabled', '');
            }
        );
      } else {
        result_switches.forEach(function (currentValue) {
              if (currentValue.hasAttribute('disabled')) {
                currentValue.removeAttribute('disabled');
              }
            }
        );
      }
    },
    error: function (page) {
      console.log('error');
      showErrorPopup();
    },
    cache: false
  });
}

result_panel.onmouseenter = resultDependentSwitchLocker;


// Hide result layers, if user goes to region, areas or energy panel
function hideResultLayers() {
  console.log('In panel: ' + this.id);
  result_switches.forEach(function (currentValue) {
      if (currentValue.checked === true) {
        console.log('setting switch to false: ' + currentValue.id);
        currentValue.checked = false;
        var layer_to_remove = currentValue.id.replace('cb_results_', '');
        console.log('remove result layer of: ' + layer_to_remove);
        lmap.removeLayer(layers[layer_to_remove]);
        console.log('remove result layer of: ' + layer_to_remove);
        lmap.removeControl(legends[layer_to_remove]);
      }
    }
  );
};

var energy_panel_label = document.getElementById('panel-energy-label');
energy_panel_label.onclick = hideResultLayers;

var area_panel_label = document.getElementById('panel-areas-label');
area_panel_label.onclick = hideResultLayers;

var results_panel_label = document.getElementById('panel-results-label');
results_panel_label.onclick = resultDependentSwitchLocker;
