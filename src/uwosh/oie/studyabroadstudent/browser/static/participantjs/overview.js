require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ParticipantOverviewComponent = R.createClass({
      getInitialState: function(){
        },

  });

  R.render(R.createElement(ProgramSearchComponent, {}), document.getElementById('oie-overview-component'));
});
