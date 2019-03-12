//TODO: Move other controls here too

// Update scenario list in esys panel
function updateScenarioList(scenarios) {
  var select_scn_frm = $('#select-scn-frm');
  // Refresh list
  var current_value = select_scn_frm.val();
  select_scn_frm.find('option').remove();
  for (var index in scenarios) {
      select_scn_frm.append($('<option>', {
        value: index,
        text: scenarios[index]
      }));
  };
  // Reset selected value
  $(select_scn_frm).val(current_value);
};

function updateScenarioControls(scn_data, mode) {
  var esys_sliders = $('.irs-hidden-input').get();
  //console.log(esys_sliders);
  
  // Sliders
  for (var index in esys_sliders) {
    var slider = $('#' + esys_sliders[index].id).data("ionRangeSlider");
    slider.reset();
    if (mode == 'marker') {
      console.log('marker');
      //var marks = [[50, 'Status Quo', 'text for tooltip 1']];
      //var toolTipText = 'Example of text for tooltip';
      //addMarks(data.slider, data.min, data.max, marks);
    } else if (mode == 'apply') {
      slider.update({
        from: 50
        //min: 0
        //max: 10,
        //from_min: 1,
        //from_max: 9,
        //from_shadow: true,
        //to_shadow: true
      });
    }
  };
  
  // Switches
  // TBD
};
