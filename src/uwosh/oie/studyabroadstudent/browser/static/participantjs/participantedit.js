$(document).ready(function() {
  if($('body').hasClass('template-edit') && $('body').hasClass('portaltype-oiestudyabroadparticipant')) {
    var baseURL = $('body').attr('data-base-url');
    var utilURL = baseURL + '/edit-util';
    var baseWidgetSelector = '#formfield-form-widgets-';
    var baseInputSelector = '#form-widgets-';
    var util_data = {};

    function populateDates() {
      var deadlineMarkup = '';
      var moment = require('moment');
      for(var i=0;i<util_data.paymentDeadlines.length;i++){
        deadlineMarkup+='<br>';
        var date = moment(util_data.paymentDeadlines[i].date).format("MMM Do YY");
        deadlineMarkup+=util_data.paymentDeadlines[i].label+': '+date;
      }
      $(baseWidgetSelector + 'paymentDeadlines').prepend(deadlineMarkup);
      deadlineMarkup = '';
      for(var i=0;i<util_data.orientationDeadlines.length;i++){
        deadlineMarkup+='<br>';
        var date = moment(util_data.orientationDeadlines[i].date).format("MMM Do YY");
        deadlineMarkup+=util_data.orientationDeadlines[i].label+': '+date;
      }
      $(baseWidgetSelector + 'orientationDeadline').prepend(deadlineMarkup);
    }

    function handleInterview() {
      if (util_data.individualInterview.toLowerCase() != 'yes') {
        $(baseWidgetSelector + 'interviewDate').hide();
      }
    }

    $.ajax(utilURL, {
      success: function(data) {
        util_data = JSON.parse(data);
        populateDates();
        handleInterview();
      }
    });
  }
});
