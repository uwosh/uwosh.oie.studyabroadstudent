from datetime import timedelta
from plone import api
from plone.app.dexterity.behaviors.constrains import DISABLED
from plone.app.uuid.utils import uuidToObject
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from uwosh.oie.studyabroadstudent.constants import DURATIONS, SPECIAL_DAYS
from zope.component import getUtility
from uwosh.oie.studyabroadstudent.constants import STATES_FOR_DISPLAYING_PROGRAMS


def get_full_camelcase_name(o):
    full_name = f'{o.firstName} {o.middleName or ""} {o.lastName}'
    return full_name.replace('  ', ' ')


def get_full_snakecase_name(o):
    full_name = f'{o.first_name} {o.middle_name or ""} {o.last_name}'
    return full_name.replace('  ', ' ')


def set_application_title(o):
    o.title = f'{get_full_camelcase_name(o)} {o.programName} {o.programYear}'


def get_list_item(brain):
    return f'<li><a href="{brain.getURL()}">{brain.Title}</a></li>'


def get_unordered_list(brains):
    list_items = [get_list_item(b) for b in brains]
    return '<ul>' + ''.join(list_items) + '</ul>'


###############################################################
def application_created(o, event):
    set_application_title(o)
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)


def application_modified(o, event):
    set_application_title(o)


###############################################################
def _update_insurance_end_date(o, event):
    arrival = o.arrivalInWisconsinDate
    start = o.arrivalAtDestinationAndInsuranceStartDate
    if arrival and start:
        duration = arrival - start
        for d in DURATIONS:
            delta = timedelta(days=d)
            if duration <= delta:
                o.insuranceEndDate = start + delta
                break


def _update_term_based_dates(o, event):
    # copy these dates based on the term selected
    #   - STEP I, II, III, IV application deadlines
    #   - request for proposal deadlines
    #   - application deadline
    #
    term = o.term
    year = uuidToObject(o.calendar_year)
    prefix = term[2:].lower().replace(' ', '_')
    suffix = ''.join([
        first_letter
        for first_letter in
        map(lambda x: x[0], prefix.split('_'))
    ])

    if o.step_1_and_2_application_deadline is None:
        o.step_1_and_2_application_deadline = getattr(
            year,
            f'step_1_and_2_application_deadline_{suffix}',
            None)
    if o.step_3_application_deadline is None:
        o.step_3_application_deadline = getattr(
            year,
            f'step_3_application_deadline_{suffix}',
            None)
    if o.step_4_application_deadline is None:
        o.step_4_application_deadline = getattr(
            year,
            f'step_4_application_deadline_{suffix}',
            None)
    if o.request_for_proposal_due_date is None:
        o.request_for_proposal_due_date = getattr(
            year,
            f'{prefix}_request_for_proposals_deadline_date',
            None)
    if o.application_deadline is None:
        o.application_deadline = getattr(
            year,
            f'{prefix}_application_deadline',
            None)

def _update_contained_object_fields(o, event):
    # update fields that show contained objects
    # and related 'add object' link fields
    update_course_field(o)
    update_add_course_link(o)
    update_health_document_field(o)
    update_add_health_document_link(o)
    update_transition_field(o)
    update_add_transition_link(o)

def program_created(o, event):
    # set the program code
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = f'{calendar_year[2:4]}{o.term[0]}{o.college_or_unit[0]}'
    for c in o.countries:
        program_code += c[0:3].upper()
    if o.program_code != program_code:
        o.program_code = program_code
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)
    # copy all dates from selected calendar year into the new Program object
    for special_day in SPECIAL_DAYS:
        setattr(o, special_day, getattr(calendar_year_obj, special_day))
    _update_contained_object_fields(o, event)
    _update_term_based_dates(o, event)
    _update_insurance_end_date(o, event)

def program_transitioned(o, event):
    if event.new_state.id not in STATES_FOR_DISPLAYING_PROGRAMS:
        return
    program_title = o.title
    if program_title:
        programs = api.portal.get_registry_record('oiestudyabroadstudent.programs', default=[])
        if program_title not in programs:
            api.portal.set_registry_record(
                'oiestudyabroadstudent.programs',
                tuple(
                    sorted({
                        *programs,
                        program_title,
                    })
                )
            )



def program_added(program, event):
    # doesn't work in the IObjectCreatedEvent
    # fix which types can be contained in a Program
    aspect = ISelectableConstrainTypes(program)
    aspect.setConstrainTypesMode(DISABLED)
    portal = api.portal.get()
    api.content.move(program, portal['programs'])


def program_modified(o, event):
    # update the program code if needed
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    if o.program_code != program_code:
        o.program_code = program_code
    _update_contained_object_fields(o, event)
    _update_term_based_dates(o, event)
    _update_insurance_end_date(o, event)



###############################################################
def calendar_year_created(calendar_year, event):
    portal = api.portal.get()
    api.content.move(calendar_year, portal['years'])


###############################################################
def contact_created(o, event):
    o.title = get_full_snakecase_name(o)
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)


def contact_modified(o, event):
    contact_created(o, event)


###############################################################
def _participant_update(participant, event, event_type=None):
    program_uid = participant.programName
    if program_uid:
        program = uuidToObject(program_uid)
        if program:
            question_changed_str = 'This answer requires review because the question has changed: '
            programName = program.title
            program_assigned_or_changed = False
            if event_type == 'created':
                program_assigned_or_changed = True
            else:
                if event_type == 'updated' and getattr(
                    event, 'descriptions', None,
                ):
                    for evt_description in event.descriptions:
                        if 'programName' in evt_description.attributes:
                            program_assigned_or_changed = True
                            break
            if program_assigned_or_changed:
                for index in range(1, 6):
                    # copy questions from program object
                    setattr(
                        participant,
                        f'applicant_question_text{index}',
                        getattr(program, f'applicantQuestion{index}', None),
                    )
                    # if needed, mark the answer as being potentially out of date
                    answer = getattr(participant, f'applicant_question_answer{index}', None)
                    if answer and not answer.startswith(question_changed_str):
                        setattr(
                            participant,
                            f'applicant_question_answer{index}',
                            question_changed_str + answer,
                        )
            year_obj = uuidToObject(program.calendar_year)
            programYear = year_obj.title
            participant.title = f'{get_full_camelcase_name(participant)} {programName} {programYear}'


def participant_created(participant, event):
    _participant_update(participant, event, event_type='created')
    if not getattr(participant, 'title', None):
        first_name = f'{getattr(participant, "firstName", "first")}'
        last_name = f'{getattr(participant, "lastName", "last")}'
        title = f'{first_name} {last_name}'
        participant.title = title
    if not getattr(participant, 'id', None):
        normalizer = getUtility(IIDNormalizer)
        participant.id = normalizer.normalize(participant.title)


def participant_modified(participant, event):
    _participant_update(participant, event, event_type='updated')


###############################################################
def liaison_created(o, event):
    o.title = get_full_snakecase_name(o)


def liaison_modified(o, event):
    liaison_created(o, event)


###############################################################
def update_course_field(o):
    brains = api.content.find(
        context=o,
        portal_type='OIECourse',
        sort_on='sortable_title',
        sort_order='ascending',
    )
    o.courses = get_unordered_list(brains)


def update_add_course_link(o):
    richtext = f'<a href="{o.absolute_url()}/++add++OIECourse" target="_blank">Add a course</a>'
    if o.add_course_link != richtext:
        o.add_course_link = richtext


def course_added(o, event):
    # update containing Program's course field which lists contained courses
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_course_field(parent)


def course_created(o, event):
    if o.title != o.course:
        o.title = o.course
        o.reindexObject()
    # update containing Program's course field which lists contained courses
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_course_field(parent)
            update_add_course_link(parent)


def course_modified(o, event):
    course_created(o, event)


###############################################################


def emailtemplate_created(o, event):
    computed_title = o.transition
    if o.title != computed_title:
        o.title = computed_title
        o.reindexObject()


def emailtemplate_modified(o, event):
    emailtemplate_created(o, event)


###############################################################
def update_transition_field(o):
    brains = api.content.find(
        context=o,
        portal_type='OIETransition',
        sort_on='sortable_title',
        sort_order='ascending',
    )
    o.travelDatesTransitionsAndDestinations = get_unordered_list(brains)


def update_add_transition_link(o):
    richtext = f'<a href="{o.absolute_url()}/++add++OIETransition" target="_blank">Add a transition</a>'
    if o.add_transition_link != richtext:
        o.add_transition_link = richtext


def transition_added(o, event):
    # update containing Program's travelDatesTransitionsAndDestinations field
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_transition_field(parent)
            update_add_transition_link(parent)


def transition_created(o, event):
    new_title = f'{o.transitionDate} {o.destinationCity}'
    if o.title != new_title:
        o.title = new_title
    # update containing Program's travelDatesTransitionsAndDestinations field
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_transition_field(parent)
            update_add_transition_link(parent)


def transition_modified(o, event):
    transition_created(o, event)


###############################################################
def update_health_document_field(o):
    brains = api.content.find(
        context=o,
        portal_type='OIEHealthSafetySecurityDocument',
        sort_on='sortable_title',
        sort_order='ascending',
    )
    o.health_safety_security_documents = get_unordered_list(brains)


def update_add_health_document_link(o):
    richtext = (
        f'<a href="{o.absolute_url()}/++add++OIEHealthSafetySecurityDocument" '
        'target="_blank">Add the OIE Risk Assessment and health, safety and security documents</a>'
    )
    if o.add_health_document_link != richtext:
        o.add_health_document_link = richtext


def health_document_added(o, event):
    # update containing Program's health documents field
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_health_document_field(parent)


def health_document_created(o, event):
    if getattr(o.file, 'filename', None):
        filename = o.file.filename
    else:
        filename = o.file.name
    if o.title != filename:
        o.title = filename
        o.reindexObject()
    # update containing Program's health_documents field
    if getattr(o, 'aq_parent', None):
        parent = o.aq_parent
        if parent.portal_type == 'OIEStudyAbroadProgram':
            update_health_document_field(parent)
            update_add_health_document_link(parent)


def health_document_modified(o, event):
    health_document_created(o, event)


###############################################################
def program_leader_created(o, event):
    o.title = get_full_snakecase_name(o)


def program_leader_modified(o, event):
    program_leader_created(o, event)
