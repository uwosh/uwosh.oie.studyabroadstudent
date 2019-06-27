require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ApplyFormComponent = R.createClass({
      getInitialState: function(){
        var el = document.getElementById('oie-apply-data');
        var encoded = el.getAttribute('oie-program-data');
        var programs = JSON.parse(window.atob(encoded));
        return {
          programs: programs
        }
      },
      render: function(){
        var applyFields = [];
        var fieldClass = 'oie-apply-field';
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
        var programOptions = [];
        for (var i=0;i<this.state.programs.length;i++) {
          var optionAttributes = {
            value: this.state.programs[i]['uid']
          }
          if (this.state.programs[i]['selected'] == true){
            optionAttributes['selected'] = true;
          }
          programOptions.push(D.option(optionAttributes, this.state.programs[i]['name']));
        }
        var programField = D.select({
          className: fieldClass,
          name: 'program'
        }, programOptions);
        applyFields.push(programField);
        applyFields.push(D.input({
          type: 'submit'
        }));
        var applyForm = D.div({
          id: 'oie-apply'
        }, [
          D.form({
            onSubmit: this.validate,
          }, applyFields)
        ]);
        return applyForm;
      },
      validate: function(){
        this.submit();
      },
      submit: function(event){
        var validationErrors = this.validate();
        if (validationErrors) {
          event.preventDefault();
        } else {
          next_url = document.getElementById();
          window.location.href = "http://";
        }
      }
  });

  R.render(R.createElement(ApplyFormComponent, {}), document.getElementById('oie-apply-component'));
});
