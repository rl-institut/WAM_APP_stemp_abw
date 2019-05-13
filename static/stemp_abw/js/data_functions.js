// Control scenario select and apply
function ctrlScenario(element_id) {
  element = $('#' + element_id);
  var data = '';

  if (element_id == 'select-scn-frm') {
    console.log('change scn dropdown');
    action = 'select_scenario';
    data = element.val();
  } else if (element_id == 'apply-scn-btn') {
    console.log('apply scn btn');
    action = 'apply_scenario';
    data = $('#select-scn-frm').val();
  }

  $.ajax({
    url : '/stemp_abw/app/',
    type : "POST",
    data : {action: action,
            data: data,
            csrfmiddlewaretoken: csrf_token},
    success: function(page) {
        console.log('scn apply successful');
    },
    error: function(page) {
        console.log('error');
    }
  }).done(function(returned_data) {
    if (element_id == 'select-scn-frm') {
      var scn_data = JSON.parse(returned_data);
      //console.log(scn_data);
      updateScenarioList(scn_data['scenario_list']);
      updateScenarioControls(scn_data['scenario']['name'],
                             scn_data['scenario']['desc'],
                             scn_data['controls'],
                             false);
    } else if (element_id == 'apply-scn-btn') {
      var scn_data = JSON.parse(returned_data)
      //console.log(returned_data);
      updateScenarioControls(scn_data['scenario']['name'],
                             scn_data['scenario']['desc'],
                             scn_data['controls'],
                             true);
    }
  });
};

// Post scenario settings
function ctrlScenarioPost(element_id, data) {
  console.log(element_id + ': ' + data);
  $.ajax({
    url : '/stemp_abw/app/',
    type : "POST",
    data : {action: 'update_scenario',
            data: JSON.stringify({[element_id]: data}),
            csrfmiddlewaretoken: csrf_token},
    success: function(page) {
        //console.log('success');
    },
    error: function(page) {
        console.log('error');
    }
  }).done(function(returned_data) {
    data = JSON.parse(returned_data);
    if (element_id == 'dd_repowering') {
      updateScenarioControlRepDropdown(data['sl_wind_repower_pot']);
    }
  });
};

// Control simulation
function ctrlSimulate() {
  console.log('simulation started');
  //element.prop("disabled", true);
  //$('#simulation-save-btn').show();
  //jquery__WEBPACK_IMPORTED_MODULE_0___default()('.loader-wrapper').toggleClass("loader-wrapper--hide");
  //jquery__WEBPACK_IMPORTED_MODULE_0___default()('body').toggleClass("body--nopointer");

  $.ajax({
      url : '/stemp_abw/app/',
      type : "POST",
      data : {action: 'simulate',
              data: '',
              csrfmiddlewaretoken: csrf_token},
      success: function(page) {
          console.log('success');
      },
      error: function(page) {
          console.log('error');
      }
  }).done(function(returned_data){
      //updateSimProgressBar(25);
      console.log(returned_data);
  });
};

// Control simulation
function checkForSimulationResults() {
  console.log('checking for results...');

  $.ajax({
      url : '/stemp_abw/app/',
      type : "POST",
      data : {action: 'check_results',
              data: '',
              csrfmiddlewaretoken: csrf_token},
      success: function(page) {
          console.log('success');
      },
      error: function(page) {
          console.log('error');
      }
  }).done(function(returned_data){
      if (returned_data === 'none') {
          console.log(Highcharts.charts);

          for (var hc_ctr = 0; hc_ctr < 11; hc_ctr++) {
              idx=$("#hc_" + hc_ctr.toString()).data('highchartsChart');
              Highcharts.charts[idx].showLoading('Daten noch nicht verfügbar,</br>bitte Simulation starten..');
          };
      } else {
          data = JSON.parse(returned_data);
          console.log(data)
      };
  });
};

