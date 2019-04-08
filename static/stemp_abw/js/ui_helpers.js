// Remote controlled tooltips

/**********************************/
/*** Remote controlled tooltip ***/
/**********************************/
/*
Notes:
* The rc triggers must be
  * either members of class ".rc-tooltip-trigger" and have an id
    following the pattern "rc-tooltip-trigger-XXX" where XXX is an unique no
    (fired via click event listener)
  * or members of class ".rc-tooltip-trigger-override"
    (for elements which the tooltip is fired externally since they cannot have
    an "rc-tooltip-trigger-XXX" id)
  This is necessary for the click event listener to hide all tooltips except for
  those which are members of one of these 2 classes (see below).
* The remote controlled tooltip must have the id "rc-tooltip-XXX" where XXX is
  the id used by the trigger above.
*/

// Listen to remote controlled (rc) tooltip actions using id.
$('.rc-tooltip-trigger').click( function () {
  var ctr = $(this).attr('id').substring(19);
  $('#rc-tooltip-' + ctr).foundation('show');
});
// Add listener to hide tooltips if the clicked element isn't a tooltip trigger (document)
document.addEventListener("click", function(event) {
  var element_class = $(event.target).attr('class');
	if (element_class != 'rc-tooltip-trigger' && element_class != 'rc-tooltip-trigger-override') {
	  $('.tooltip').foundation().hide();
	};
});
// Add listener to hide tooltips if the clicked element isn't a tooltip trigger (tabs in offcanvas menu)
$('.tabs-title').click( function(event) {
  var element_class = $(event.target).attr('class');
	if (element_class != 'rc-tooltip-trigger' && element_class != 'rc-tooltip-trigger-override') {
	  $('.tooltip').foundation().hide();
	};
});

/***************************/
/*** Highlight panel tab ***/
/***************************/
/*
Notes:
* A panel tab (left menu) can be highlighted using its id (e.g. 'tabsAreas')
* The highlighting is disabled as soon as it's clicked
*/

// Highlight panel tab (left menu)
function highlightPanelTab (tab_id) {
  if (!$('#' + tab_id).is('.is-active')) {
    $('#' + tab_id  + ' > a').addClass('tab-highlighted');
  }
}
// Remove panel tab highlight on click
$('.tabs-title').click( function () {
  $('#' + $(this).attr('id') + ' > a').removeClass('tab-highlighted');
});

/**********************/
/*** Open panel tab ***/
/**********************/
function openAreaTab() {
  // open/collapse tab content
  $('#deeplinked-tabs').foundation('_openTab', $('#panel-areas'));
  $('#deeplinked-tabs').foundation('_collapseTab', $('#panel-energy')); // activate/deactivate tab highlight

  // remove special tab highlight
  $('#tabsAreas > a').removeClass('tab-highlighted');

  $("#tabsEnergy").toggleClass("is-active");
  $("#tabsAreas").toggleClass("is-active");
}

$('.openAreaTab').on('click', openAreaTab);

function openEnergyTab() {
  // open/collapse tab content
  $('#deeplinked-tabs').foundation('_openTab', $('#panel-energy'));
  $('#deeplinked-tabs').foundation('_collapseTab', $('#panel-areas')); // activate/deactivate tab highlight

  // remove special tab highlight
  $('#tabsEnergy > a').removeClass('tab-highlighted');

  $("#tabsEnergy").toggleClass("is-active");
  $("#tabsAreas").toggleClass("is-active");
}

$('#openEnergyTab').on('click', openEnergyTab);



//$('.switch-tab-trigger').click( function () {
//  var ctr = $(this).attr('id').substring(19);
//  $('#rc-tooltip-' + ctr).foundation('show');
//});
//
//function switchToPanelTab (tab_id) {
//  jquery__WEBPACK_IMPORTED_MODULE_0___default()('#openTabExample').on('click', openTab);
//}
//
//$('.tabs-title').click( function () {
//  $('#' + $(this).attr('id') + ' > a').removeClass('tab-highlighted');
//});