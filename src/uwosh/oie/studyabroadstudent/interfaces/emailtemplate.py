# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.directives import form
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIEProgramEmailTemplate(Interface):
    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Template Title'),
        required=True,
        default=_(u'will be auto-generated on save'),
    )
    transition = schema.Choice(
        title=_(u'Transition Name'),
        description=_(u'Transition that it will send an email on.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_transition',  # noqa
        required=True,
    )
    sendEmail = schema.Bool(
        title=_(u'Send Email on Transition'),
        description=_(u'Choose whether to send an email on this transition'),
    )
    sendEmailOnFailure = schema.Bool(
        title=_(u'Send Email on Transition Failure Only?'),
        description=_(u'Choose whether to send an email on transition '
                      u'failure only.'),
    )
    ccUsers = schema.TextLine(
        title=_(u'CC email addresses'),
        description=_(u'Enter each full email address, separated by a comma '
                      u'if there is more than one'),
        default=_(u'oie@uwosh.edu'),
    )
    emailText = RichText(
        title=_(u'Email Text'),
        description=_(u'Text that will display in the email body.'),
        default_mime_type='text/html',
        allowed_mime_types=('text/plain', 'text/html'),
        required=True,
    )
    send_to_actor = schema.Bool(
        title=_(u'Send Email To the user who triggered this transition'),
        description=_(u'Should the user who triggered this transition recieve an email?'),  # noqa
    )
    send_to_program_leader = schema.Bool(
        title=_(u'Send Email To Program Leader on Transition'),
        description=_(u'Should the program leader recieve an email when their application goes through this transition?'),  # noqa
    )


class IOIEParticipantEmailTemplate(IOIEProgramEmailTemplate):
    transition = schema.Choice(
        title=_(u'Transition Name'),
        description=_(u'Transition that it will send an email on.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.participant_transition',  # noqa
        required=True,
    )

    send_to_participant = schema.Bool(
        title=_(u'Send Email To Participant/Application on Transition'),
        description=_(u'Should the participant/applicant recieve an email when their application goes through this transition?'),  # noqa
    )
