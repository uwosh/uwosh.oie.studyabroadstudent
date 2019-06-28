# -*- coding: utf-8 -*-

from plone import api
from uwosh.oie.studyabroadstudent.exceptions import StateError
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_IN_STATE_KEY  # noqa
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_VALUE_IN_STATE_KEY  # noqa
from zLOG import ERROR
from zLOG import INFO
from zLOG import LOG


DEFAULT_NOTIFICATION_EMAIL_ADDRESS = 'kyle.arthurs+oie@wildcardcorp.com'
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
    check_for_required_values_by_state(state_change)
    check_for_required_specific_values_by_state(state_change)
    transition = state_change.transition.id
    if transition in special_transitions[interface]:
        special_transitions[interface][transition][PRE](state_change)


def post_transition(state_change, **kw):
    interface = get_interface_from_state_change(state_change)
    afterTransition(state_change)
    sendTransitionMessage(state_change)
    transition = state_change.transition.id
    if transition in special_transitions[interface]:
        if special_transitions[interface][transition][POST]:
            special_transitions[interface][transition][POST](state_change)


def afterTransition(state_change):
    pass


def check_for_required_values_by_state(state_change):
    """Find all fields that must have values before
       we can move into the new state"""
    obj = state_change.object
    interface = get_interface_from_state_change(state_change)
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
            message = "The field '%s' is required for state '%s' but has no value" % (field_title, new_state_id)  # noqa
            LOG('check_for_required_values_by_state', ERROR, message)
            missingValues.append(
                {
                    'expected': 'N/A',
                    'current_value': value,
                    'field': field_title,
                    'message': 'You are missing this required field',
                },
            )
            raise StateError(message)


def check_for_required_specific_values_by_state(state_change):
    """Find all fields that must have specific values before
       we can move into the new state"""
    obj = state_change.object
    interface = get_interface_from_state_change(state_change)
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
            message = "The field '%s' is required to have the value '%s' for state '%s' but has the value '%s'" % (field_title, must_be, new_state_id, value)  # noqa
            LOG('check_for_required_values_by_state', ERROR, message)
            missingValues.append(
                {
                    'expected': must_be,
                    'current_value': value,
                    'field': field_title,
                    'message': 'This field does not have the required value',
                },
            )
            raise StateError(message)

    sendTransitionMessage(object, state_change)


def sendTransitionMessage(state_change, cc=[]):

    emailTemplate = getEmailMessageTemplate(state_change)  # noqa

    if not emailTemplate:
        LOG('sendTransitionMessage', INFO,
            "Not sending transition email for transition %s" % (  # noqa
            state_change.transition.id))
        return

    portal = api.portal.get()
    wftool = api.portal.get_tool('portal_workflow')

    object = state_change.object

    old_state_id = state_change.old_state.id
    new_state_id = state_change.new_state.id

    reviewer = getReviewerInfo(object)

    mTo = getToAddresses(object, emailTemplate, cc)
    mFrom = reviewer['email']

    # If the owner is performing action, this will prevent them from sending an email to themselves  # noqa
    if mFrom in mTo:
        mFrom = DEFAULT_NOTIFICATION_EMAIL_ADDRESS

    mSubj = 'Your {0} update (UW Oshkosh Office of International Education)'  # noqa

    state_msg = None
    if old_state_id != new_state_id:
        state_msg = "Its state has changed from '" + old_state_id + "' to '" + new_state_id + "'.\n\n"  # noqa

    LOG('sendTransitionMessage', INFO,
        "Sending transition email for transition %s to %s, subject '%s', emailTemplate = '%s'" % (  # noqa
        state_change.transition.id, mTo, mSubj, emailTemplate))  # noqa
    mMsg = assembleEmailMessage(object, wftool, emailTemplate)

    portal.MailHost.secureSend(mMsg, mTo, mFrom, mSubj)


def getEmailMessageTemplate(state_change):
    email_types = {
        IOIEStudyAbroadProgram: 'OIEProgramEmailTemplate',
        IOIEStudyAbroadParticipant: 'OIEParticipantEmailTemplate',
    }
    interface = get_interface_from_state_change(state_change)
    template_type = email_types[interface]
    templates = state_change.object.queryCatalog({
        'portal_type': template_type,
        'transition': state_change.transition.id,
        'sort_on': 'modified',
    })  # this query only for objects within this program container?
    template = None
    if templates:
        template = templates[0].getObject()  # using last modified
    return template


def getCreatorInfo(object):
    creator = object.Creator()
    member = api.user.get(creator)

    return {
        'member': member,
        'id': member.getId(),
        'fullname': member.getProperty('fullname', 'Fullname missing'),
        'email': member.getProperty('email', None),
    }


def getReviewerInfo(object):
    pmtool = api.portal.get_tool('portal_membership')
    wftool = api.portal.get_tool('portal_workflow')

    actorid = wftool.getInfoFor(object, 'actor')  # noqa
    actor = pmtool.getMemberById(actorid)  # noqa

    reviewer = {
        'member': actor,
        'id': actor.getId(),
        'fullname': actor.getProperty('fullname', 'Fullname missing'),
        'email': actor.getProperty('email', None),
    }

    return reviewer


# cc will be faculty on that transition
def getToAddresses(object, emailTemplate, cc=[]):
    addresses = []

    # student email
    # addresses.append(application.getEmail())

    # if emailTemplate:
    #    # custom specified emails sent
    #    addresses.extend(emailTemplate.getFormattedCCAddresses())

    if cc is not None:
        addresses.extend(cc)

    return addresses


def assembleEmailMessage(object, wftool, emailTemplate):
    # Name: %s
    # Program Name: %s
    # Program Year: %s

    mMsg = """

Your UW Oshkosh Office of International Education study abroad program has been updated.

%s

You can view your program here: %s

Comment: %s

""" % (  # noqa
        # application.getFirstName() + ' ' + application.getLastName(),
        # application.getProgramNameAsString(),
        # application.getProgramYear(),
        emailTemplate.getFormattedEmailText(),
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
    pass


special_program_transitions = {
    'submit-to-dean': (chair_dean_review, None),
    'submit-to-chair': (chair_dean_review, None),
}

special_participant_transitions = {}

special_transitions = {
    IOIEStudyAbroadProgram: special_program_transitions,
    IOIEStudyAbroadParticipant: special_participant_transitions,
}
