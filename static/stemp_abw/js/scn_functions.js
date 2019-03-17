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

function updateScenarioControls(scn_name, scn_desc, controls, apply) {
  // Sliders
  var esys_sliders = $('.irs-hidden-input').get();
  for (var index in esys_sliders) {
    var slider = $('#' + esys_sliders[index].id).data("ionRangeSlider");
    var slider_vals_old = slider.options;
    var slider_val = controls[esys_sliders[index].id];

    // Set values
    if (apply === true) {
      slider.update({
        from: slider_val
        //min: 0
        //max: 10,
        //from_min: 1,
        //from_max: 9,
        //from_shadow: true,
        //to_shadow: true
      });
    } else {
      slider.update(slider_vals_old);
    }

    // add marker
    var marks = [[slider_val, scn_name, scn_desc]];
    addMarks(slider.result.slider, slider.options.min, slider.options.max, marks);
  };
  
  // Switches
  var esys_switches = $('.switch-input.esys').get();
  for (var index in esys_switches) {
    id = esys_switches[index].id;
    $('#' + id).prop('checked', controls[id]);
  };
};

// slider markers
function convertToPercent(num, min, max) {
  var percent = (num - min) / (max - min) * 100;
  return percent;
}

function addMarks($slider, min, max, marks) {
  var html = '';
  var left = 0;
  var i;

  for (i = 0; i < marks.length; i++) {
    left = convertToPercent(marks[i][0], min, max);
    html += '<div title="' + marks[i][2] + '"><div class="mark" style="left: ' + left + '%"></div><div class="mark--text" style="left: calc(' + left + '% + 1rem - (10rem/2))">' + marks[i][1] + '</div></div>';
  }

  $slider.append(html);
}

function changeScenarioControl(data) {
  console.log(data.from);
  /*
  var from_max = $(this).attr("from_max");
  var from_min = $(this).attr("from_min");
  if (data.from == from_max) {
    console.log('max erreicht');
  } else if (data.from == from_min) {
    console.log('min erreicht');
  }
  */
}
