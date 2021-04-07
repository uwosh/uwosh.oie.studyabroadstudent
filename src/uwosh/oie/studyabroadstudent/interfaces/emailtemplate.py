from plone.app.textfield import RichText
from plone.autoform.directives import mode
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIEProgramEmailTemplate(Interface):
    mode(title='hidden')
    title = schema.TextLine(
        title=_('Template Title'),
        required=True,
        default=_('will be auto-generated on save'),
    )
    transition = schema.Choice(
        title=_('Transition Name'),
        description=_('Transition that it will send an email on.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_transition',
        required=True,
    )
    sendEmail = schema.Bool(
        title=_('Send Email on Transition'),
        description=_('Choose whether to send an email on this transition'),
    )
    sendEmailOnFailure = schema.Bool(
        title=_('Send Email on Transition Failure Only?'),
        description=_('Choose whether to send an email on transition failure only.'),
    )
    ccUsers = schema.TextLine(
        title=_('CC email addresses'),
        description=_('Enter each full email address, separated by a comma if there is more than one'),
        default=_('oie@uwosh.edu'),
    )
    emailText = RichText(
        title=_('Email Text'),
        description=_('Text that will display in the email body.'),
        default_mime_type='text/html',
        allowed_mime_types=('text/plain', 'text/html'),
        required=True,
    )
    send_to_actor = schema.Bool(
        title=_('Send Email To the user who triggered this transition'),
        description=_('Should the user who triggered this transition recieve an email?'),
    )
    send_to_program_leader = schema.Bool(
        title=_('Send Email To Program Leader on Transition'),
        description=_(
            'Should the program leader recieve an email when their '
            'application goes through this transition?'
        ),
    )


class IOIEParticipantEmailTemplate(IOIEProgramEmailTemplate):
    transition = schema.Choice(
        title=_('Transition Name'),
        description=_('Transition that it will send an email on.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.participant_transition',
        required=True,
    )

    send_to_participant = schema.Bool(
        title=_('Send Email To Participant/Application on Transition'),
        description=_(
            'Should the participant/applicant recieve an email when their '
            'application goes through this transition?'
        ),
    )
