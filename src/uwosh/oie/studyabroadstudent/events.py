from plone import api
from plone.app.uuid.utils import uuidToObject
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone.app.dexterity.behaviors.constrains import DISABLED
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


def application_created(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)
    o.reindexObject()


def application_modified(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)


def program_created(o, event):
    # set the program code
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    o.program_code = program_code
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)
    # copy all the dates from selected calendar year into the new Program object
    for d in ['first_day_of_spring_semester_classes', 'last_day_of_spring_semester_classes',
              'first_day_of_spring_interim_classes', 'last_day_of_spring_interim_classes',
              'official_spring_graduation_date', 'first_day_of_summer_i_classes', 'last_day_of_summer_i_classes',
              'first_day_of_summer_ii_classes', 'last_day_of_summer_ii_classes',
              'official_summer_graduation_date', 'first_day_of_fall_semester_classes',
              'last_day_of_fall_semester_classes', 'first_day_of_winter_interim_classes',
              'last_day_of_winter_interim_classes', 'official_fall_graduation_date',
              'spring_interim_summer_fall_semester_participant_orientation_deadline',
              'spring_interim_summer_fall_semester_in_person_orientation',
              'winter_interim_spring_semester_participant_orientation_deadline',
              'winter_interim_spring_semester_in_person_orientation',
              'spring_interim_summer_fall_semester_payment_deadline_1', 'spring_interim_payment_deadline_2',
              'sunmmer_payment_deadline_2', 'fall_semester_payment_deadline_2',
              'winter_interim_spring_payment_deadline_1', 'winter_interim_spring_payment_deadline_2']:
        setattr(o, d, getattr(calendar_year_obj, d))
    o.reindexObject()


def program_added(o, event):
    # doesn't work in the IObjectCreatedEvent
    # fix which types can be contained in a Program
    aspect = ISelectableConstrainTypes(o)
    # immediately_addable = ['Event', 'File', 'Folder', 'Image', 'Link', 'News Item', 'Document']
    # import pdb;pdb.set_trace()
    # aspect.setImmediatelyAddableTypes(immediately_addable)
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
    # update course field
    brains = api.content.find(
        context=o,
        portal_type='OIECourse',
        sort_on='sortable_title',
        sort_order='ascending',
    )
    richtext = u'<ul>'
    for b in brains:
        richtext += '<li><a href="%s">%s</a></li>' % (b.getURL(), b.getObject().course)
    richtext += u'</ul>'
    if o.courses != richtext:
        o.courses = richtext


def contact_created(o, event):
    if o.middle_name and o.middle_name.strip() != '':
        o.title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)
    else:
        o.title = '%s %s' % (o.first_name, o.last_name)
    if not o.id:
        normalizer = getUtility(IIDNormalizer)
        o.id = normalizer.normalize(o.title)
    o.reindexObject()


def contact_modified(o, event):
    contact_created(o, event)


def participant_created(o, event):
    program_uid = o.programName
    if program_uid:
        program = uuidToObject(program_uid)
        if program:
            programName = program.title
            # copy questions from program object
            o.applicant_question_text1 = program.applicantQuestion1
            o.applicant_question_text2 = program.applicantQuestion2
            o.applicant_question_text3 = program.applicantQuestion3
            o.applicant_question_text4 = program.applicantQuestion4
            o.applicant_question_text5 = program.applicantQuestion5
            year_obj = uuidToObject(program.calendar_year)
            programYear = year_obj.title
            if o.middle_name and o.middle_name.strip() != '':
                o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, programName, programYear)
            else:
                o.title = '%s %s %s %s' % (o.firstName, o.lastName, programName, programYear)
            if not o.id:
                normalizer = getUtility(IIDNormalizer)
                o.id = normalizer.normalize(o.title)
    o.reindexObject()

def participant_modified(o, event):
    program_uid = o.programName
    if program_uid:
        program = uuidToObject(program_uid)
        if program:
            programName = program.title
            year_obj = uuidToObject(program.calendar_year)
            programYear = year_obj.title
            if o.middle_name and o.middle_name.strip() != '':
                o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, programName, programYear)
            else:
                o.title = '%s %s %s %s' % (o.firstName, o.lastName, programName, programYear)

def liaison_created(o, event):
    if o.middle_name and o.middle_name.strip() != '':
        title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)
    else:
        title = '%s %s' % (o.first_name, o.last_name)
    if o.title != title:
        o.title = title
        o.reindexObject()

def liaison_modified(o, event):
    liaison_created(o, event)

def course_created(o, event):
    if o.title != o.course:
        o.title = o.course
        o.reindexObject()

def course_modified(o, event):
    course_created(o, event)

def program_leader_created(o, event):
    if o.middle_name and o.middle_name.strip() != '':
        title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)
    else:
        title = '%s %s' % (o.first_name, o.last_name)
    if o.title != title:
        o.title = title
        o.reindexObject()

def program_leader_modified(o, event):
    program_leader_created(o, event)


