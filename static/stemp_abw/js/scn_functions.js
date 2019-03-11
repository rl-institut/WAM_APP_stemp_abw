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
