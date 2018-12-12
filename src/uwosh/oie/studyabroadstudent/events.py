# -*- coding: utf-8 -*-
from plone import api
from plone.app.dexterity.behaviors.constrains import DISABLED
from plone.app.uuid.utils import uuidToObject
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from zope.component import getUtility


def application_created(o, event):
    title = '{firstName} {middleName} {lastName} {programName} {programYear}'\
        .format(
            firstName=o.firstName,
            middleName=o.middleName,
            lastName=o.lastName,
            programName=o.programName,
            programYear=o.programYear,
        )
    if o.title != title:
        o.title = title
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)


def application_modified(o, event):
    title = '{firstName} {middleName} {lastName} {programName} {programYear}'\
        .format(
            firstName=o.firstName,
            middleName=o.middleName,
            lastName=o.lastName,
            programName=o.programName,
            programYear=o.programYear,
        )
    if o.title != title:
        o.title = title


###############################################################
def program_created(o, event):
    # set the program code
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + \
                   (o.term)[0] + \
                   (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    if o.program_code != program_code:
        o.program_code = program_code
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)
    # copy all dates from selected calendar year into the new Program object
    for d in ['first_day_of_spring_semester_classes',
              'last_day_of_spring_semester_classes',
              'first_day_of_spring_interim_classes',
              'last_day_of_spring_interim_classes',
              'official_spring_graduation_date',
              'first_day_of_summer_i_classes', 'last_day_of_summer_i_classes',
              'first_day_of_summer_ii_classes',
              'last_day_of_summer_ii_classes',
              'official_summer_graduation_date',
              'first_day_of_fall_semester_classes',
              'last_day_of_fall_semester_classes',
              'first_day_of_winter_interim_classes',
              'last_day_of_winter_interim_classes',
              'official_fall_graduation_date',
              'spring_interim_summer_fall_semester_participant_orientation_deadline',  # noqa
              'spring_interim_summer_fall_semester_in_person_orientation',
              'winter_interim_spring_semester_participant_orientation_deadline',  # noqa
              'winter_interim_spring_semester_in_person_orientation',
              'spring_interim_summer_fall_semester_payment_deadline_1',
              'spring_interim_payment_deadline_2',
              'summer_payment_deadline_2', 'fall_semester_payment_deadline_2',
              'winter_interim_spring_payment_deadline_1',
              'winter_interim_spring_payment_deadline_2']:
        setattr(o, d, getattr(calendar_year_obj, d))


def program_added(o, event):
    # doesn't work in the IObjectCreatedEvent
    # fix which types can be contained in a Program
    aspect = ISelectableConstrainTypes(o)
    aspect.setConstrainTypesMode(DISABLED)


def program_modified(o, event):
    # update the program code if needed
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    if o.program_code != program_code:
        o.program_code = program_code
    # update fields that show contained objects
    # and related 'add object' link fields
    update_course_field(o)
    update_add_course_link(o)
    update_health_document_field(o)
    update_add_health_document_link(o)
    update_transition_field(o)
    update_add_transition_link(o)


###############################################################
def contact_created(o, event):
    if o.middle_name and o.middle_name.strip() != '':
        title = '{first_name} {middle_name} {last_name}'.format(
            first_name=o.first_name,
            middle_name=o.middle_name,
            last_name=o.last_name,
        )
    else:
        title = '{first_name} {last_name}'.format(
            first_name=o.first_name,
            last_name=o.last_name,
        )
    if o.title != title:
        o.title = title
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)


def contact_modified(o, event):
    contact_created(o, event)


###############################################################
def _participant_update(o, event, event_type=None):
    program_uid = o.programName
    if program_uid:
        program = uuidToObject(program_uid)
        if program:
            answer_changed_str = 'This answer requires review because '\
                                 'the question has changed: '
            programName = program.title
            if event_type == 'created':
                program_assigned_or_changed = True
            else:
                program_assigned_or_changed = False
            if event_type == 'updated' and getattr(
                event, 'descriptions', None,
            ):
                for evt_description in event.descriptions:
                    if 'programName' in evt_description.attributes:
                        program_assigned_or_changed = True
                        break
            if program_assigned_or_changed:
                # copy questions from program object
                o.applicant_question_text1 = program.applicantQuestion1
                o.applicant_question_text2 = program.applicantQuestion2
                o.applicant_question_text3 = program.applicantQuestion3
                o.applicant_question_text4 = program.applicantQuestion4
                o.applicant_question_text5 = program.applicantQuestion5
                # if needed, mark the answer as being potentially out of date
                if o.applicant_question_answer1 and not (
                    o.applicant_question_answer1.startswith(answer_changed_str)
                ):
                    o.applicant_question_answer1 = answer_changed_str + \
                                                   o.applicant_question_answer1
                if o.applicant_question_answer2 and not (
                    o.applicant_question_answer2.startswith(answer_changed_str)
                ):
                    o.applicant_question_answer2 = answer_changed_str + \
                                                   o.applicant_question_answer2
                if o.applicant_question_answer3 and not (
                    o.applicant_question_answer3.startswith(answer_changed_str)
                ):
                    o.applicant_question_answer3 = answer_changed_str + \
                                                   o.applicant_question_answer3
                if o.applicant_question_answer4 and not (
                    o.applicant_question_answer4.startswith(answer_changed_str)
                ):
                    o.applicant_question_answer4 = answer_changed_str + \
                                                   o.applicant_question_answer4
                if o.applicant_question_answer5 and not (
                    o.applicant_question_answer5.startswith(answer_changed_str)
                ):
                    o.applicant_question_answer5 = answer_changed_str + \
                                                   o.applicant_question_answer5
            year_obj = uuidToObject(program.calendar_year)
            programYear = year_obj.title
            if o.middleName and o.middleName.strip() != '':
                title = (
                    '{firstName} {middleName} {lastName} '
                    '{programName} {programYear}'.format(
                        firstName=o.firstName,
                        middleName=o.middleName,
                        lastName=o.lastName,
                        programName=programName,
                        programYear=programYear,
                    )
                )
            else:
                title = '{firstName} {lastName} {programName} {programYear}'.\
                    format(
                        firstName=o.firstName,
                        lastName=o.lastName,
                        programName=programName,
                        programYear=programYear,
                    )
            if o.title != title:
                o.title = title


def participant_created(o, event):
    _participant_update(o, event, event_type='created')
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)


def participant_modified(o, event):
    _participant_update(o, event, event_type='updated')


###############################################################
def liaison_created(o, event):
    if o.middle_name and o.middle_name.strip() != '':
        title = '{f} {m} {l}'.format(
            f=o.first_name,
            m=o.middle_name,
            l=o.last_name,
        )
    else:
        title = '{f} {l}'.format(
            f=o.first_name,
            l=o.last_name,
        )
    if o.title != title:
        o.title = title


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
    richtext = u'<ul>'
    for b in brains:
        richtext += '<li><a href="{url}">{title}</a></li>'.format(
            url=b.getURL(),
            title=b.Title,
        )
    richtext += u'</ul>'
    if o.courses != richtext:
        o.courses = richtext


def update_add_course_link(o):
    richtext = u'<a href="{url}/++add++OIECourse" target="_blank">Add a course</a>'.format(url=o.absolute_url())  # noqa
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
def update_transition_field(o):
    brains = api.content.find(
        context=o,
        portal_type='OIETransition',
        sort_on='sortable_title',
        sort_order='ascending',
    )
    richtext = u'<ul>'
    for b in brains:
        richtext += '<li><a href="{url}">{title}</a></li>'.format(
            url=b.getURL(),
            title=b.Title,
        )
    richtext += u'</ul>'
    if o.travelDatesTransitionsAndDestinations != richtext:
        o.travelDatesTransitionsAndDestinations = richtext


def update_add_transition_link(o):
    richtext = u'<a href="{url}/++add++OIETransition" target="_blank">Add a transition</a>'.format(url=o.absolute_url())  # noqa
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
    new_title = '{date} {city}'.format(
        date=o.transitionDate,
        city=o.destinationCity,
    )
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
    richtext = u'<ul>'
    for b in brains:
        richtext += '<li><a href="{url}">{title}</a></li>'.format(
            url=b.getURL(),
            title=b.Title,
        )
    richtext += u'</ul>'
    if o.health_safety_security_documents != richtext:
        o.health_safety_security_documents = richtext


def update_add_health_document_link(o):
    richtext = u'<a href="{url}/++add++OIEHealthSafetySecurityDocument" target="_blank">Add a health document</a>'.format(url=o.absolute_url())  # noqa
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
    if o.middle_name and o.middle_name.strip() != '':
        title = '{f} {m} {l}'.format(
            f=o.first_name,
            m=o.middle_name,
            l=o.last_name,
        )
    else:
        title = '{f} {l}'.format(f=o.first_name, l=o.last_name)
    if o.title != title:
        o.title = title


def program_leader_modified(o, event):
    program_leader_created(o, event)
