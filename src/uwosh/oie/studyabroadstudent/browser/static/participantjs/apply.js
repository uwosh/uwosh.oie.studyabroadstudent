require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react', // FIX THIS!!!!!!
], function(R) {
  const D = R.DOM;

  const ApplyFormComponent = R.createClass({
    getInitialState: function(){
      const globalStatusMessageElement = document.getElementById('global_statusmessage');
      return {
        loginUrl: null,
        isLoggedIn: false,
        programTitle: null,
        globalStatusMessageElement,
        emptyDiv: Array.from(globalStatusMessageElement.children).reverse()[0],
        signupMessage: null,
        loggedOutMessage: null,
        loggedInMessage: null,
        componentMounted: false,
      }
    },

    getLoggedOutMessage: function() {
      const messageBody = `You aren't logged in.
        If you have a UWosh general account or a Study Abroad site account,
        <a href="${this.state.loginUrl}">click here</a> to log in and continue.`;
      return this.createMessage('Warning', messageBody, 'logged-out-message');
    },

    getSignupMessage: function() {
      console.log('this.state')
      console.log(this.state)
      const messageBody = `If you don't already have a UWosh general account or a Study Abroad site account,
        <a href="${this.state.signupUrl}">click here</a> to create one now`;
      return this.createMessage('Info', messageBody, 'signup-message');
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

    componentDidMount: async function(){
      const loginDataUrl = window.location.href.replace('apply', '@@express-interest-data');
      const response = await fetch(loginDataUrl)
      const loginData = await response.json();
      this.setState(loginData);
      this.setState({
        loggedOutMessage: this.getLoggedOutMessage(),
        signupMessage: this.getSignupMessage(),
        componentMounted: true,
      });
    },

    render: function(){
      return this.state.isLoggedIn ?
      this.renderSubmitForm() :
      this.renderMessages();
    },

    login: function(){
        window.location = this.state.loginUrl;
    },
    signup: function(){
        window.location = this.state.signupUrl;
    },

    renderLoginMessage: function() {
      const shouldRender = (
        this.state.loggedOutMessage &&
        !document.querySelector('.logged-out-message')
      )
      if(shouldRender){
        this.state.globalStatusMessageElement.insertBefore(
          this.state.loggedOutMessage,
          this.state.emptyDiv,
          );
        }
      },

    renderSignUpMessage: function() {
      const shouldRender = (
        this.state.signupMessage &&
        !document.querySelector('.signup-message')
      )
      if(shouldRender){
        this.state.globalStatusMessageElement.insertBefore(
          this.state.signupMessage,
          this.state.emptyDiv,
        );
      }
    },

    renderMessages: function(){
      console.log(this.state)
      this.renderLoginMessage();
      this.renderSignUpMessage();
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
      },'First Name');
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
      console.log(this.state)
    },

  });

  R.render(R.createElement(ApplyFormComponent, {}), document.getElementById('oie-apply-component'));
});
