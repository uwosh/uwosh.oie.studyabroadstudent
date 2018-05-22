# -*- coding: utf-8 -*-

from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface, implementer
from plone.supermodel import model
from plone.namedfile import field
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, \
    dayofmonth_vocabulary, hold_vocabulary, aware_vocabulary, program_cycle_vocabulary, seat_assignment_protocol, RegistryValueVocabulary
from plone.directives import form
from Products.CMFPlone.RegistrationTool import checkEmailAddress, EmailAddressInvalid
from zope.schema import ValidationError
from collective import dexteritytextindexer
from plone.formwidget.namedfile.widget import NamedFileFieldWidget
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import validate_email


class IOIECourse(Interface):
    form.mode(title="display")
    title = schema.TextLine(
        title=_(u'Course Title'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )
    course = schema.Choice(
        title=_(u'UW Oshkosh Course Subject & Number'),
        description=_(
            u'Add all courses associated with your program, including courses that will be taught partially at UW Oshkosh and partially while away on the program.  Do not include courses that will be taught entirely at UWO, even when these courses are offered in preparation for the program away.  Contact the OIE to add a course (abroad@uwosh.edu).'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.course'),
    )
    credits_earned = schema.Int(
        title=_(u'UW Oshkosh Credits Earned'),
        description=_(
            u'Enter the number of credits that participants will earn for each individual course.  If you are offering a course that can be taught for a range of credits on your program (e.g. 3-5 credits), you must enter the course into this system multiple times, giving the course a different credit value each time that you enter it.')
    )
    class_start_date = schema.Date(
        title=_(u'Class Start Date')
        # TODO Auto-generate the first day of the term in which this program runs from the calendar?????  Maybe this isn't possible.
    )
    class_end_date = schema.Date(
        title=_(u'Class End Date')
        # TODO If the "PeopleSoft Class End Date" is AFTER the Official Graduation Date, prompt the coursebuilder to complete the "Course End Date Extension Form".
    )
    min_credits = schema.Int(
        title=_(u'Course Prerequisites: minimum number of credits'),
        description=_(
            u'If this course requires a minimum number of completed credits prior to the course start date, indicate this here'),
        min=0,
        max=999
    )
    gpa = schema.Int(
        title=_(u'Course Prerequisites: GPA'),
        description=_(u'If this course requires a minimum GPA prior to the course start date, indicate this here.'),
        min=0,
        max=999
    )
    completed_courses = schema.Text(
        title=_(u'Course Prerequisites: completed courses'),
        description=_(
            u'If this course requires that other courses be completed, or that a particular grade be earned in an earlier course, prior to the course start date, indicate this here.')
    )
    program_of_study = schema.Choice(
        title=_(u'Course Prerequisites: program of study'),
        description=_(
            u'If this course requires admission to a particular program of study prior to the course start date, indicate this here.'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.program_of_study'),
    )
    instruction_provided_by_host = schema.Choice(
        title=_(u'Instruction Provided by Host?'),
        description=_(
            u'Select the name of the person who will teach the course, if the course is to be taught by a UW Oshkosh professor.  Select "host" when instruction is provided by a partner.  Do not select the name of the "instructor-of-record" at UW Oshkosh when instruction is provided by a partner.'),
        vocabulary=yes_no_none_vocabulary,
    )
    instruction_provided_by = schema.Choice(
        title=_(u'Instruction Provided by (if not host)'),
        description=_(
            u'Select the name of the person who will teach the course, if the course is to be taught by a UW Oshkosh professor.  Select "host" when instruction is provided by a partner.  Do not select the name of the "instructor-of-record" at UW Oshkosh when instruction is provided by a partner.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
        required=False,
    )
    course_enrollment_at = schema.Choice(
        title=_(u'Course Enrollment at'),
        description=_(
            u'Indicate the institution at which program participants will be enrolled for each individual course.'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.enrollment_institution'),
        required=True,
    )
    foreign_institution = schema.Choice(
        title=_(u'Foreign Institution Name'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner',
        required=True,
        # TODO Oshkosh must be the first option on this dropdown list
    )
    foreign_course_number = schema.Text(
        title=_(u'Foreign Course Number'),
        description=_(u'')
    )
    foreign_course_credits = schema.Int(
        title=_(u'Foreign Course Number of Credits'),
        description=_(u'max: 2 digits'),
        min=0,
        max=99,
    )
    foreign_course_review_date = schema.Date(
        title=_(u'Foreign Course Date of Most Recent Review'),
        description=_(u'')
    )
    foreign_course_reviewer_info = schema.TextLine(
        title=_(u'Foreign Course Reviewer Name, Title & College'),
        description=_(u'')
    )
    foreign_course_syllabus = field.NamedFile(
        title=_(u'Foreign Course Syllabus'),
        description=_(u'Upload the syllabus that corresponds to the most recent date of review'),
    )
    foreign_course_builder_email = schema.TextLine(
        title=_(u'PeopleSoft Course Builder'),
        description=_(
            u'Enter the email address of the person in your department who will build your course/s in PeopleSoft.  If instruction is provided by the host institution, with no concurrent enrollment at UWO, enter OIE@uwosh.edu into the email address field.'),
        constraint=validate_email,
        # TODO "A message should be generated to the course builder email addresses associated with each course.  Course builders should have access to all ""Course Subject & Number"" related fields and must have permission to edit greyed out fields in this section only.
        # TODO Course builders may request instructions on how to build study abroad/away sections in PeopleSoft by emailing OIE@uwosh.edu.  Course builders enter the data requested below; Financial Services uses this data to properly set tuition & fees for each course."
    )
    ps_course_id = schema.Int(
        title=_(u'PeopleSoft Course ID'),
        min=0,
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_class_id = schema.Int(
        title=_(u'PeopleSoft Class Number'),
        min=0,
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_section_id = schema.Int(
        title=_(u'PeopleSoft Course Section Number'),
        min=0,
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_section_letter = schema.TextLine(
        title=_(u'PeopleSoft Course Section Letter'),
        # TODO dropdown?
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_grade_by_date = schema.Date(
        title=_(u'PeopleSoft "grade by" date'),
        # TODO Autogenerate the "PeopleSoft 'grade by' date" by adding 5 calendar days to the "PeopleSoft Class End Date".
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    tuition_and_fees = schema.Choice(
        title=_(u'Tuition & Fees'),
        vocabulary=yes_no_none_vocabulary,
        # TODO vocabulary?
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    tuition_and_fees = schema.Choice(
        title=_(u'External Studies Courses'),
        description=_(u'Confirm that any External Studies Courses have been graded.'),
        vocabulary=yes_no_none_vocabulary,
        # TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
        # TODO This field must be associated with each Ext Studies Course listed in "Course Subject & Number".
    )
