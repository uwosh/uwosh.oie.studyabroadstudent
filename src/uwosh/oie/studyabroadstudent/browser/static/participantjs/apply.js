require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  const D = R.DOM;

  const ApplyFormComponent = R.createClass({
    getInitialState: function(){
      const globalStatusMessageElement = document.getElementById('global_statusmessage');
      const fakeElement = document.createElement('span');
      fakeElement.id = 'fake-element';
      return {
        loginUrl: null,
        registerUrl: null,
        isLoggedIn: false,
        programTitle: null,
        globalStatusMessageElement,
        emptyDiv: Array.from(globalStatusMessageElement.children).reverse()[0],
        loggedOutMessage: fakeElement,
        loggedInMessage: fakeElement,
        componentMounted: false,
      };
    },

    getLoggedOutMessage: function() {
      const messageBody = `You must log in with your UWosh login or a Study Abroad site account
       if you already have one, or register below.`;
      return this.createMessage('Warning', messageBody, 'logged-out-message');
    },

    componentDidMount: async function(){
      const loginDataUrl = window.location.href.replace('apply', '@@express-interest-data');
      const response = await fetch(loginDataUrl)
      const loginData = await response.json();
      this.setState(loginData);
      this.setState({
        loggedInMessage: this.getLoggedInMessage(),
        loggedOutMessage: this.getLoggedOutMessage(),
        componentMounted: true,
      });
    },


    getLoggedInMessage: function() {
      const messageBody = `You are logged in as ${this.state.userFullName}.
        This will be the account your application will be associated with.`;
      return this.createMessage('Info', messageBody, 'logged-in-message');
    },

    createMessage: function(messageType, messageBody, messageClass) {
      const message = document.createElement('dl');
      message.innerHTML = `<dt>${messageType}</dt>
        <dd>${messageBody}</dd>`;
      message.className = `portalMessage ${messageType.toLowerCase()} ${messageClass}`;
      return message;
    },


    rederLoginAndRegisterButtons: function() {
        const loginButton = D.button(
          {
            onClick: this.login,
            type: 'button',
            className: 'btn btn-primary login-button'
          },
          'Log In',
        );
        const registerButton = D.button(
          {
            onClick: this.register,
            type: 'button',
            className: 'btn btn-secondary register-button'
          },
          'Sign Up',
        );
        return D.div(
          {
            className: 'buttons'
          },
          [
            loginButton,
            registerButton,
          ],
        )
    },

    render: function(){
      this.renderMessages();
      return this.state.isLoggedIn ?
        this.renderSubmitForm() :
        this.rederLoginAndRegisterButtons();
    },

    login: function(){
        window.location = this.state.loginUrl;
    },
    register: function(){
        window.location = this.state.registerUrl;
    },

    setLoginStatusMessage: function() {
      const { isLoggedIn } = this.state;
      const incorrectSelector = `logged-${ isLoggedIn ? 'out' : 'in' }-message`;
      const correctSelector = `logged-${ isLoggedIn ? 'in' : 'out' }-message`;
      const incorrectElement = document.querySelector(incorrectSelector);
      const correctElement = document.querySelector(correctSelector);
      const message = this.state[`logged${ isLoggedIn ? 'In' : 'Out' }Message`];
      incorrectElement?.remove();
      if(!correctElement && message){
        document.querySelector('#fake-element')?.remove();
        this.state.globalStatusMessageElement.insertBefore(
          message,
          this.state.emptyDiv,
        );
      }
    },


    renderMessages: function(){
      this.setLoginStatusMessage();
    },

    rederEmptyElement: function() {
      return D.div();
    },

    renderSubmitForm: function(){
      const fieldClass = 'form-control oie-apply-field';

      const directions = D.div(
        {
          id: 'oie-apply-data',
        },
        [
          'To open an application for ',
          D.strong({},this.state.programTitle),
          ', submit the simple form below.',
        ]
      );
      const firstNameLabel = D.label({
        className: 'label',
        for: 'first-name',
      },'First Name');
      const firstNameField = D.input({
        className: fieldClass,
        id: 'first-name',
        type: 'text',
        name: 'first',
        placeholder: 'First Name',
        required: true,
      });
      const lastNameLabel = D.label({
        className: 'label',
        for: 'last-name',
      },'Last Name');
      const lastNameField = D.input({
        className: fieldClass,
        id: 'last-name',
        type: 'text',
        name: 'last',
        placeholder: 'Last Name',
        required: true,
      });
      const emailLabel = D.label({
        className: 'label',
        for: 'email',
      },'Email address (Uwosh email address preferred)');
      const emailField = D.input({
        className: fieldClass,
        type: 'email',
        name: 'email',
        id: 'email',
        placeholder: 'Email Address',
        required: true,
      });
      const submitButton = D.input({
        type: 'submit',
        className: 'btn btn-primary apply-button'
      });
      const applyFields = [
        directions,
        firstNameLabel,
        firstNameField,
        lastNameLabel,
        lastNameField,
        emailLabel,
        emailField,
        submitButton,
      ]
      const applyForm = D.div(
        {
          id: 'oie-apply'
        },
        D.form(
          {
            action: this.state.createdUrl,
            method: 'post',
            onSubmit: this.submit,
            id: 'express-interest-form',
          },
          applyFields,
        ),
      );
      return applyForm;
    },

    validate: function(event){
      return true;
    },

    submit: function(event){
      if ( this.validate(event) !== true) {
        event.preventDefault();
      }
    },

  });

  R.render(R.createElement(ApplyFormComponent, {}), document.getElementById('oie-apply-component'));
});
