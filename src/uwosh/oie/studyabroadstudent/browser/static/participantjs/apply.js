require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ApplyFormComponent = R.createClass({
      getInitialState: function(){
      },
      render: function(){
        var applyForm = D.div({
          id: 'oie-apply'
        }, [
          D.form({
            onSubmit: this.submit,
          }, [
            D.input({
              type: 'submit'
            }, 'Begin')
          ])
        ])
      },
      validate: function(){

      },
      submit: function(event){
        var validationErrors = this.validate();
        if (validationErrors) {
          event.preventDefault();
        } else {
          next_url = document.getElementById()
          window.location.href = "http://";
        }
      }
  });

  R.render(R.createElement(ProgramSearchComponent, {}), document.getElementById('oie-apply-component'));
});
