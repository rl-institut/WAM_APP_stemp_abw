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
        showErrorPopup();
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
        showErrorPopup();
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

  // show simulation spinner
  $('#loader-text').text('Simuliere...');
  $('#loader-detail-text').text('');
  toggleSpinnerVisibility();

  //element.prop("disabled", true);
  //$('#simulation-save-btn').show();

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
          showErrorPopup();
      }
  }).done(function(returned_data){
      //updateSimProgressBar(25);
      console.log(returned_data);

      // hide simulation spinner
      toggleSpinnerVisibility();

      // reload results if simulation was triggered from result panel
      if ($('#panel-results').hasClass('is-collapsed')) {
        getSimulationResults();
      }
  });
};

//// Control simulation
//function checkForSimulationResults() {
//  console.log('checking for results...');
//
//  $.ajax({
//      url : '/stemp_abw/app/',
//      type : "POST",
//      data : {action: 'check_results',
//              data: '',
//              csrfmiddlewaretoken: csrf_token},
//      success: function(page) {
//          console.log('success');
//      },
//      error: function(page) {
//          console.log('error');
//      }
//  }).done(function(returned_data){
//      if (returned_data === 'none') {
//          console.log(Highcharts.charts);
//
//          for (var hc_ctr = 0; hc_ctr < 11; hc_ctr++) {
//              idx=$("#hc_" + hc_ctr.toString()).data('highchartsChart');
//              Highcharts.charts[idx].showLoading('Daten noch nicht verfügbar,</br>bitte Simulation starten..');
//          };
//      } else {
//          data = JSON.parse(returned_data);
//          console.log(data)
//      };
//      getSimulationResults();
//  });
//};

// Load simulation results from serial view
function getSimulationResults() {
    $.ajax({
        url: '/stemp_abw/results/',
        type : "GET",
        success: function(data) {
            idx=parseInt($("#hc_res_wind_time")[0].getAttribute('data-highcharts-chart'))
            idx2=parseInt($("#hc_res_summary_scn")[0].getAttribute('data-highcharts-chart'))
            idx3=parseInt($("#hc_res_summary_sq")[0].getAttribute('data-highcharts-chart'))
            if (data == null) {
                Highcharts.charts[idx].showLoading('Das Szenario wurde verändert.</br>Für Ergebnisse bitte Simulation starten.');
                Highcharts.charts[idx2].showLoading('Das Szenario wurde verändert.</br>Für Ergebnisse bitte Simulation starten.');
            } else {
                Highcharts.charts[idx].series[0].setData(data['hc_res_wind_time']);
                Highcharts.charts[idx].hideLoading();
                Highcharts.charts[idx2].series[0].setData(data['hc_res_summary_scn']);
                Highcharts.charts[idx2].hideLoading();
                Highcharts.charts[idx3].series[0].setData(data['hc_res_summary_sq']);
            };
        },
        error: function(page) {
            console.log('error');
            showErrorPopup();
        },
        cache: false
    });
}
