
from plone import api
from uwosh.oie.studyabroadstudent.exceptions import StateError
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant, IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.interfaces.directives import (
    REQUIRED_IN_STATE_KEY,
    REQUIRED_VALUE_IN_STATE_KEY,
)
from uwosh.oie.studyabroadstudent.utils import get_object_from_uid

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
    """Find all fields that must have values before we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    requiredFields = []
    missingValues = []

    required_in_state = interface.queryTaggedValue(REQUIRED_IN_STATE_KEY)
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
            message = f"The field '{field_title}' is required for state '{new_state_id}' but has no value"
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
    """Find all fields that must have specific values before we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    missingValues = []

    requiredValueFields = []
    required_value_in_state = interface.queryTaggedValue(REQUIRED_VALUE_IN_STATE_KEY)
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
            message = (
                f"The field '{field_title}' is required to have the value '{must_be}' "
                f"for state '{new_state_id}' but has the value '{value}'"
            )
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

    emailTemplate = getEmailMessageTemplate(state_change, interface)

    if not emailTemplate:
        message = f'Not sending transition email for transition {state_change.transition.id}.'
        question = 'Was the Email Template created?'
        logger.info(f'{message} {question}')
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

    mSubj = f'Your {update_text[interface]} Update (UW Oshkosh Office of International Education)'

    state_msg = None
    if old_state_id != new_state_id:
        state_msg = f"Its state has changed from '{old_state_id}' to '{new_state_id}'.\n\n"

    transition_message = f'Sending email for transition {state_change.transition.id} to {mTo}'
    subject_message = f"subject '{mSubj}'"
    email_template_message = "emailTemplate = '{emailTemplate}'"
    logger.info(f'{transition_message}, {subject_message}, {email_template_message}')
    mMsg = f'{assembleEmailMessage(object, emailTemplate)}\n\n{state_msg}'

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
    workflow_tool = api.portal.get_tool('portal_workflow')

    memberid = workflow_tool.getInfoFor(object, 'actor')  # noqa
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
            except (AttributeError, ValueError):
                logger.info("Can't get participant email")

    if emailTemplate.send_to_actor:
        actor = getActor(object)
        if actor['email']:
            addresses.append(actor['email'])

    if emailTemplate.send_to_program_leader:
        try:
            leader_id = object.program_leader
            leader = get_object_from_uid(leader_id)
            if leader.Title != '*Nobody':
                addresses.append(leader.email)
        except (AttributeError, ValueError):
            logger.info("Can't get program leader email")

    addresses.extend([addr.strip() for addr in emailTemplate.ccUsers.split(',')])

    return addresses


def assembleEmailMessage(object, emailTemplate):
    workflow_tool = api.portal.get_tool('portal_workflow')
    return f"""

Your UW Oshkosh Office of International Education study abroad program has been updated.

{emailTemplate.emailText.output}

You can view your application here: {object.absolute_url()}

Comment: {workflow_tool.getInfoFor(object, 'comments')}
"""


def getAssembledErrorMessage(errorMessage):
    if errorMessage:

        message = ''
        for key in errorMessage.keys():
            message += f'\n\n Section: {key}\n'
            for error in errorMessage[key]:
                message += f'Field: {error["field"]},\tExplanation: {error["message"]}\n'

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
            # TODO need template for chair/dean reviews and to send the message here # noqa: T000


special_program_transitions = {
    'submit-to-dean': (chair_dean_review, None),
    'submit-to-chair': (chair_dean_review, None),
}

special_participant_transitions = {}

special_transitions = {
    IOIEStudyAbroadProgram: special_program_transitions,
    IOIEStudyAbroadParticipant: special_participant_transitions,
}
