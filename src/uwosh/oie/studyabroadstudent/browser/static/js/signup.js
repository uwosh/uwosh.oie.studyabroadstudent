require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  const D = R.DOM;
  const renderElement = document.getElementById('oie-signup-component');

  const SignupFormComponent = R.createClass({
      getInitialState: function(){
        return {
          signupEndpoint: ''
        };
      },


 componentDidMount: async function(){
      const { signupSubmissionUrl } = renderElement.dataset;
      // const loginDataUrl = window.location.href.replace('apply', '@@express-interest-data');
      // const response = await fetch(loginDataUrl)
      // const loginData = await response.json();
      this.setState({
        signupSubmissionUrl,
        passwordElements: null,
      });
    },

// <!-- Password field -->
// Password: <input type="password" value="FakePSW" id="myInput">

// <!-- An element to toggle between password visibility -->
// <input type="checkbox" onclick="myFunction()">Show Password

    togglePasswordVisibility: function() {
      const newType = this.state.passwordElements[0].type === 'text' ? 'password' : 'text';
      this.state.passwordElements.forEach(element => element.type = newType);
    },
      render: function(){
        const loginButton = D.button(
          {
            type: 'button',
            className: 'btn btn-primary login-button'
          },
          'Log in',
        );
        return D.div(
          {
            id: 'oie-login-check'
          },
          D.form(
            {
              action: this.state.loginUrl,
              query: {came_from: this.state.cameFrom},
              method: 'get',
              onSubmit: this.submit,
              id: 'login-check-form',
            },
            [
              message,
              ...(this.state.isLoggedIn ? [] : [loginButton]),
              skipLoginButton,
            ],
          ),
        );
      },


      validate: function(event){
        return true;
      },

      submit: function(event){
        if ( this.validate(event) !== true) {
          event.preventDefault();
        }
      }
  });

  R.render(R.createElement(SignupFormComponent, {}), renderElement);
});
