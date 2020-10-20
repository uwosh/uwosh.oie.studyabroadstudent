# -*- coding: utf-8 -*-

from plone import api
from uwosh.oie.studyabroadstudent.exceptions import StateError
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_IN_STATE_KEY  # noqa : E501
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_VALUE_IN_STATE_KEY  # noqa : E501

import logging


logger = logging.getLogger(__name__)


DEFAULT_NOTIFICATION_FROM_ADDRESS = 'brian.duncan+oie@wildcardcorp.com'
PRE = 0
POST = 1


def get_interface_from_state_change(state_change):
    obj = state_change.object
    if IOIEStudyAbroadProgram.providedBy(obj):
        return IOIEStudyAbroadProgram
    elif IOIEStudyAbroadParticipant.providedBy(obj):
        return IOIEStudyAbroadParticipant
    return None


def pre_transition(state_change, **kw):
    interface = get_interface_from_state_change(state_change)
    check_for_required_values_by_state(state_change, interface)
    check_for_required_specific_values_by_state(state_change, interface)
    transition = state_change.transition.id
    if transition in special_transitions[interface]:
        if special_transitions[interface][transition][PRE]:
            special_transitions[interface][transition][PRE](state_change)


def post_transition(state_change, **kw):
    interface = get_interface_from_state_change(state_change)
    # afterTransition(state_change, interface)
    sendTransitionMessage(state_change, interface)
    transition = state_change.transition.id
    if transition in special_transitions[interface]:
        if special_transitions[interface][transition][POST]:
            special_transitions[interface][transition][POST](state_change)


def afterTransition(state_change, interface):
    pass


def check_for_required_values_by_state(state_change, interface):
    """Find all fields that must have values before
       we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    requiredFields = []
    missingValues = []

    required_in_state = interface.queryTaggedValue(REQUIRED_IN_STATE_KEY)  # noqa
    if required_in_state:
        required_fields = required_in_state.keys()
    else:
        return

    for f in required_fields:
        state = required_in_state[f]
        if new_state_id == state:
            requiredFields.append(f)

    for f in requiredFields:
        value = getattr(obj, f, None)
        field = interface.get(f)
        field_title = field.title
        if not value:
            message = "The field '{}' is required for state '{}' but has no value".format(field_title, new_state_id)  # noqa : E501
            logger.error(message)
            missingValues.append(
                {
                    'expected': 'N/A',
                    'current_value': value,
                    'field': field_title,
                    'message': 'You are missing this required field',
                },
            )
            raise StateError(message)


def check_for_required_specific_values_by_state(state_change, interface):
    """Find all fields that must have specific values before
       we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    missingValues = []

    requiredValueFields = []
    required_value_in_state = interface.queryTaggedValue(REQUIRED_VALUE_IN_STATE_KEY)  # noqa
    if required_value_in_state:
        required_value_fields = required_value_in_state.keys()
    else:
        return

    for f in required_value_fields:
        if isinstance(required_value_in_state[f][0], tuple):
            for must_be, state in required_value_in_state[f]:
                if new_state_id == state:
                    requiredValueFields.append([f, must_be])
        else:
            must_be, state = required_value_in_state[f]
            if new_state_id == state:
                requiredValueFields.append([f, must_be])

    for f, must_be in requiredValueFields:
        value = getattr(obj, f, None)
        field = interface.get(f)
        field_title = field.title
        if isinstance(must_be, str):
            # e.g., to handle DateTimes
            value = str(value)
        if value != must_be:
            message = "The field '{}' is required to have the value '{}' for state '{}' but has the value '{}'".format(field_title, must_be, new_state_id, value)  # noqa : E501
            logger.error(message)
            missingValues.append(
                {
                    'expected': must_be,
                    'current_value': value,
                    'field': field_title,
                    'message': 'This field does not have the required value',
                },
            )
            raise StateError(message)

    sendTransitionMessage(state_change, interface)


def sendTransitionMessage(state_change, interface):

    emailTemplate = getEmailMessageTemplate(state_change, interface)  # noqa

    if not emailTemplate:
        message = 'Not sending transition email for transition {}.'.format(state_change.transition.id)  # noqa : E501
        question = 'Was the Email Template created?'
        logger.info('{} {}'.format(message, question))
        return

    object = state_change.object

    old_state_id = state_change.old_state.id
    new_state_id = state_change.new_state.id

    mTo = getToAddresses(object, emailTemplate)
    mFrom = DEFAULT_NOTIFICATION_FROM_ADDRESS  # use site settings 'From' address? # noqa

    update_text = {
        IOIEStudyAbroadProgram: 'Study Abroad Program',
        IOIEStudyAbroadParticipant: 'Study Abroad Participant Application',
    }

    mSubj = 'Your {} Update (UW Oshkosh Office of International Education)'.format(update_text[interface])  # noqa : E501

    state_msg = None
    if old_state_id != new_state_id:
        state_msg = "Its state has changed from '{}' to '{}'.\n\n".format(old_state_id, new_state_id)  # noqa : E501

    transition_message= "Sending email for transition {} to {}".format(state_change.transition.id, mTo)  # noqa : E501
    subject_message = "subject '{mSubj}'"
    email_template_message = "emailTemplate = '{emailTemplate}'"
    logger.info('{}, {}, {}'.format(transition_message,subject_message,email_template_message))  # noqa : E501
    mMsg = '{}\n\n{}'.format(assembleEmailMessage(object, emailTemplate), state_msg)

    mail_host = api.portal.get_tool(name='MailHost')
    mail_host.send(mMsg, mTo, mFrom, mSubj)


def getEmailMessageTemplate(state_change, interface):
    email_types = {
        IOIEStudyAbroadProgram: 'OIEProgramEmailTemplate',
        IOIEStudyAbroadParticipant: 'OIEParticipantEmailTemplate',
    }
    template_type = email_types[interface]
    catalog = api.portal.get_tool('portal_catalog')
    try:
        templates = catalog({
            'portal_type': template_type,
            'transition': state_change.transition.id,
            'sort_on': 'modified',
        })
    except AssertionError:  # occurs when templates not created yet
        return None
    template = None
    if templates:
        template = templates[0].getObject()  # using last modified
    return template


def getActor(object):
    pmtool = api.portal.get_tool('portal_membership')
    wftool = api.portal.get_tool('portal_workflow')

    memberid = wftool.getInfoFor(object, 'actor')  # noqa
    member = pmtool.getMemberById(memberid)  # noqa

    actor = {
        'member': member,
        'id': member.getId(),
        'fullname': member.getProperty('fullname', 'Fullname missing'),
        'email': member.getProperty('email', None),
    }

    return actor


def getToAddresses(object, emailTemplate):
    addresses = []

    if IOIEStudyAbroadParticipant.providedBy(object):
        if emailTemplate.send_to_participant:
            try:
                addresses.append(object.email)
            except Exception:
                logger.info("Can't get participant email")

    if emailTemplate.send_to_actor:
        actor = getActor(object)
        if actor['email']:
            addresses.append(actor['email'])

    if emailTemplate.send_to_program_leader:
        try:
            leader_id = object.program_leader
            leader = api.content.get(UID=leader_id)
            if leader.Title != '*Nobody':
                addresses.append(leader.email)
        except Exception:
            logger.info("Can't get program leader email")

    addresses.extend([addr.strip() for addr in emailTemplate.ccUsers.split(',')])  # noqa

    return addresses


def assembleEmailMessage(object, emailTemplate):
    # Name: %s
    # Program Name: %s
    # Program Year: %s

    wftool = api.portal.get_tool('portal_workflow')

    mMsg = """

Your UW Oshkosh Office of International Education study abroad program has been updated.

%s

You can view your program here: %s

Comment: %s
""" % (  # noqa
        # application.getFirstName() + ' ' + application.getLastName(),
        # application.getProgramNameAsString(),
        # application.getProgramYear(),
        emailTemplate.emailText,
        object.absolute_url(),
        wftool.getInfoFor(object, 'comments'),  # noqa
        # getAssembledErrorMessage(onFailure),
    )

    return mMsg


def getAssembledErrorMessage(errorMessage):
    if errorMessage:

        message = ''
        for key in errorMessage.keys():
            message += '\n\n Section: ' + key + '\n'
            for error in errorMessage[key]:
                message += 'Field: ' \
                           + error['field'] \
                           + ',\tExplanation: ' \
                           + error['message'] \
                           + '\n'

        return message

    else:
        return ''


def chair_dean_review(state_change):
    addresses = []
    if state_change.transition.id == 'submit-to-dean':
        reviewers_field = state_change.object.dean_emails
    else:  # submit-to-chair
        reviewers_field = state_change.object.chair_emails
    if reviewers_field:
        for reviewer in reviewers_field:
            email = reviewer.get('reviewer_email_row', None)
            if email:
                addresses.append(email)
            # TODO need template for chair/dean reviews and to send the message here # noqa


special_program_transitions = {
    'submit-to-dean': (chair_dean_review, None),
    'submit-to-chair': (chair_dean_review, None),
}

special_participant_transitions = {}

special_transitions = {
    IOIEStudyAbroadProgram: special_program_transitions,
    IOIEStudyAbroadParticipant: special_participant_transitions,
}
