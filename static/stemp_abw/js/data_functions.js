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
  } else if (element_id == 'init-sq-scn') {
    console.log('init sq scn');
    action = 'init_sq_scenario';
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
    var scn_data = JSON.parse(returned_data);
    if (element_id == 'select-scn-frm') {
      //console.log(scn_data);
      updateScenarioList(scn_data['scenario_list']);
      updateScenarioControls(scn_data['scenario']['name'],
                             scn_data['scenario']['desc'],
                             scn_data['controls'],
                             false);
    } else if (element_id == 'apply-scn-btn' || element_id == 'init-sq-scn') {
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
  $('#loader-text').html('<i class="icon ion-coffee"></i> Simuliere...');
  $('#loader-detail-text').text('(max. 1 Minute)');
  toggleSpinnerVisibility();

  //element.prop("disabled", true);
  //$('#simulation-save-btn').show();

  $.ajax({
    url: '/stemp_abw/app/',
    type: "POST",
    data: {
      action: 'simulate',
      data: '',
      csrfmiddlewaretoken: csrf_token
    },
    success: function (page) {
      console.log('simulation success');
      console.log('hidding result layers and legends');
      hideResultLayers();
      if (simulation_info.hidden === false) {
        simulation_info.hidden = true;
      }
      console.log('calling result_map_init ...');
      window.result_map_init(window.maps);
    },
    error: function (page) {
      console.log('error');
      showErrorPopup();
    }
  }).done(function (returned_data) {

      // hide simulation spinner
      toggleSpinnerVisibility();

      // reload results if simulation was triggered from result panel
      if ($('#panel-results').hasClass('is-collapsed')) {
        getSimulationResults();
      } else {
        if (!$('#panel-results').hasClass('is-active')) {
          $('#rc-tooltip-results-available').foundation('show');
          highlightPanelTab('tabsResults');
        }
      }
  });
};

// Load simulation results from serial view
function getSimulationResults() {
    // Check if simulation results are up-to-date
    $.ajax({
        url: '/stemp_abw/sim_status.data',
        type : "GET",
        success: function(data) {
            // get indices of chart (needed since HC increments on reload)
            idx1=parseInt($("#hc_column_power_prod_both_scn")[0].getAttribute('data-highcharts-chart'))
            idx2=parseInt($("#hc_column_power_dem_both_scn")[0].getAttribute('data-highcharts-chart'))
            idx3=parseInt($("#hc_column_power_own_cons_both_scn")[0].getAttribute('data-highcharts-chart'))
            idx4=parseInt($("#hc_pie_power_production_user_scn")[0].getAttribute('data-highcharts-chart'))
            idx5=parseInt($("#hc_pie_power_production_sq_scn")[0].getAttribute('data-highcharts-chart'))
            idx6=parseInt($("#hc_column_power_prod_m_user_scn")[0].getAttribute('data-highcharts-chart'))
            idx7=parseInt($("#hc_res_wind_time")[0].getAttribute('data-highcharts-chart'))

            const hc_idx_array = [idx1, idx2, idx3, idx4, idx5, idx6, idx7]

            // Check if results are not outdated
            if (data['sim_status'] == 'init' || data['sim_status'] == 'up_to_date') {
                $.ajax({
                    url: '/stemp_abw/result_charts.data',
                    type : "GET",
                    success: function(data) {

                        while(Highcharts.charts[idx1].series.length > 0)
                            Highcharts.charts[idx1].series[0].remove(true);
                        for (var i = 0; i < data['hc_column_power_prod_both_scn'].length; i++) {
                            Highcharts.charts[idx1].addSeries(data['hc_column_power_prod_both_scn'][i]);
                        }
                        while(Highcharts.charts[idx2].series.length > 0)
                            Highcharts.charts[idx2].series[0].remove(true);
                        for (var i = 0; i < data['hc_column_power_dem_both_scn'].length; i++) {
                            Highcharts.charts[idx2].addSeries(data['hc_column_power_dem_both_scn'][i]);
                        }
                        while(Highcharts.charts[idx3].series.length > 0)
                            Highcharts.charts[idx3].series[0].remove(true);
                        for (var i = 0; i < data['hc_column_power_own_cons_both_scn'].length; i++) {
                            Highcharts.charts[idx3].addSeries(data['hc_column_power_own_cons_both_scn'][i]);
                        }

                        //Highcharts.charts[idx3].series[0].setData(data['hc_column_power_own_cons_both_scn']);
                        Highcharts.charts[idx4].series[0].setData(data['hc_pie_power_production_user_scn']);
                        Highcharts.charts[idx5].series[0].setData(data['hc_pie_power_production_sq_scn']);

                        while(Highcharts.charts[idx6].series.length > 0)
                            Highcharts.charts[idx6].series[0].remove(true);
                        for (var i = 0; i < data['hc_column_power_prod_m_user_scn'].length; i++) {
                            Highcharts.charts[idx6].addSeries(data['hc_column_power_prod_m_user_scn'][i]);
                        }

                        Highcharts.charts[idx7].series[0].setData(data['hc_res_wind_time']);

                        // Hide loading text
                        hc_idx_array.forEach(function (item, index) {
                            Highcharts.charts[item].hideLoading();
                        });

                    },
                    error: function(page) {
                        console.log('error');
                        showErrorPopup();
                    },
                    cache: false
                });
            } else if (data['sim_status'] == 'outdated') {
                // Show loading text
                hc_idx_array.forEach(function (item, index) {
                    Highcharts.charts[item].showLoading('Das Szenario wurde verändert.</br>Für Ergebnisse bitte Simulation starten.');
                });
            };
        },
        error: function(page) {
            console.log('error');
            showErrorPopup();
        },
    });
}
