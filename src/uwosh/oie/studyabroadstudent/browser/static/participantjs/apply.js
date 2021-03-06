require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ApplyFormComponent = R.createClass({
      getInitialState: function(){
        return {}
      },
      render: function(){
        var applyFields = [];
        var fieldClass = 'form-control oie-apply-field';
        var firstNameField = D.input({
          className: fieldClass,
          type: 'text',
          name: 'first',
          placeholder: 'First Name'
        });
        applyFields.push(firstNameField);
        var lastNameField = D.input({
          className: fieldClass,
          type: 'text',
          name: 'last',
          placeholder: 'Last Name'
        });
        applyFields.push(lastNameField);
        var emailField = D.input({
          className: fieldClass,
          type: 'text',
          name: 'email',
          placeholder: 'Email Address (Use university address if possible)'
        });
        applyFields.push(emailField);
        applyFields.push(D.input({
          type: 'submit',
          className: 'btn btn-primary apply-button'
        }));
        var createURL = $('body').attr('data-base-url') + '/submit'
        var applyForm = D.div({
          id: 'oie-apply'
        }, [
          D.form({
            action: createURL,
            method: 'post',
            onSubmit: this.submit,
          }, applyFields)
        ]);
        return applyForm;
      },
      validate: function(){
        return true;
      },
      submit: function(event){
        var validated = this.validate();
        if (validated !== true) {
          event.preventDefault();
        }
      }
  });

  R.render(R.createElement(ApplyFormComponent, {}), document.getElementById('oie-apply-component'));
});
