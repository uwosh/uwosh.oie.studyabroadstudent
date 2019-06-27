$(document).ready(function() {
  if($('body').hasClass('template-edit') && $('body').hasClass('portaltype-oiestudyabroadparticipant')) {
    //Set up handlers and show/hide fields based on state.
    //Some frontend validation can be done here as well.
    var baseURL = $('body').attr('data-base-url');
    var utilURL = baseURL + '/edit-util';
    var baseWidgetSelector = '#formfield-form-widgets-';
    var baseInputSelector = '#form-widgets-';
  }
});
