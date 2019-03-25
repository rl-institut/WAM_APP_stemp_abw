// Remote controlled tooltips

/*
Notes:
* The rc triggers must be members of class ".rc-tooltip-trigger" and have an id
  following the pattern "rc-tooltip-trigger-XXX" where XXX is an unique no.
* The remote controlled tooltip must have the id "rc-tooltip-XXX" where XXX is
  the id used by the trigger above.
*/

// Listen to remote controlled (rc) tooltip actions.
$('.rc-tooltip-trigger').click( function () {
  var ctr = $(this).attr('id').substring(19);
  $('#rc-tooltip-' + ctr).foundation('show');
});
// Add listener to hide tooltips if the clicked element isn't a tooltip trigger
document.addEventListener("click", function(event) {
	if ($(event.target).attr('class') != 'rc-tooltip-trigger') {
	  $('.tooltip').foundation().hide();
	};
});
