# -*- coding: utf-8 -*-

from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.supermodel import model
from plone.namedfile import field
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, month_vocabulary, \
    dayofmonth_vocabulary, room_type_vocabulary, smoking_vocabulary, semester_vocabulary, student_type_vocabulary, \
    bus_vocabulary, fly_vocabulary, orientation_conflict_vocabulary, hold_vocabulary, aware_vocabulary, \
    load_or_overload, replacement_costs, paid_by, rate_or_lump_sum


class ILearningObjectiveRowSchema(Interface):
    learning_objective = schema.TextLine(title=u"Enter one objective per row. Click on the \'+\' to add a row.")


class IOIEStudyAbroadProgram(Interface):

    title = schema.TextLine(
        title=_(u'Program Title'),
        description=_(u'The full Program Title will be displayed in all OIE print and on-line marketing and in all official OIE program-related materials.  To avoid confusion and increase "brand" awareness for your program, consistently use this program name in full, exactly as it appears here, in your print and electronic media.  Do not include country or city names in this field.'),
        required=True,
    )

    description = RichText(
        title=_(u'Description'),
        description=_(u'This is the description that will be used to promote your program.  Your description should capture the purpose of your program, include an overview of what students will be engaged in while abroad/away, and capture students’ interest! '),
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html',),
        required=False,
    )

    cooperating_partners = schema.List(
        title=_(u'Cooperating Partners'),
        description=_(u''),
        required=False,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner')
    )

    model.fieldset(
        'comments_fieldset',
        label=_(u"Comments"),
        fields=['comments_all', 'comments_oie_leaders', 'comments_oie_all' ]
    )

    comments_all = schema.Text(
        title=_(u'Public Comments'),
        description=_(u'Comments entered here are visible by all system users.'),
        required=False,
    )

    comments_oie_leaders = schema.Text(
        title=_(u'Comments for OIE leadership'),
        description=_(u'Comments entered here are visible by the OIE Program Manager, Program Liaison, Program Leaders/Co-leaders and site administrators.'),
        required=False,
    )

    comments_oie_all = schema.Text(
        title=_(u'Comments for all OIE users'),
        description=_(u'Comments entered here are visible by all OIE professional staff.'),
        required=False,
    )

    model.fieldset(
        'program_code_fieldset',
        label=_(u"Program Code"),
        fields=['calendar_year', 'term', 'college_or_unit', 'countries', 'program_code',]
    )

    calendar_year = schema.Choice(
        title=_(u'Calendar Year'),
        description=_(u'Use the year during which the program runs; this is not the year that is associated with the term of study.  For example, a January interim program running from Jan 2-28, 2017 will be associated with "2017".   A program running Dec 28, 2016-Jan 28, 2017 will also be associated with "2017".'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.calendar_year',
        required=True,
    )

    term = schema.Choice(
        title=_(u'Term'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.term',
    )

    college_or_unit = schema.Choice(
        title=_(u'College or Unit'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.college_or_unit',
    )

    countries = schema.List(
        title=_(u'Country or Countries'),
        description=_(u''),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries')
    )

    program_code = schema.TextLine(
        title=_(u'Program Code'),
        description=_(u'(auto-generated)'),
        required=True,
        default=_(u'will be auto-generated'),
        readonly=True
    )

    model.fieldset(
        'academic_program_fieldset',
        label=_(u"Academic Program"),
        fields=[]
    )

    sponsoring_unit_or_department = schema.List(
        title=_(u'Sponsoring Unit or Department'),
        description=_(u'Select all that apply.'),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.sponsoring_unit_or_department'),
    )

    program_type = schema.Choice(
        title=_(u'Program Type'),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_type',
    )

    program_component = schema.Choice(
        title=_(u'Program Component'),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_component',
    )

    widget(
        'learning_objectives',
        DataGridFieldFactory,
    )
    learning_objectives = schema.List(
        title=_(u'Learning Objectives'),
        description=_(u'State the learning objectives for this program.  Include only one learning objective per text field. These learning objectives will be included in end-of-program assessment and may be used to support Higher Learning Commission and other accreditation processes.'),
        required=False,
        value_type=DictRow(title=u"learning objective row", schema=ILearningObjectiveRowSchema)
    )

    equipment_and_space = schema.Choice(
        title=_(u'Equipment & Space'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.equipment_and_space',
    )

    equipment_and_space_needs = RichText(
        title=_(u'Equipment & Space details'),
        description=_(u'if needed'),
        required=False,
    )

    guest_lectures = schema.Choice(
        title=_(u'Guest Lectures'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.guest_lectures',
    )

    initial_draft_program_schedule = field.NamedFile(
        title=_(u'Initial Draft Program Schedule'),
        description=_(u'Complete the OIE itinerary form and upload here.'),
        required=False,
    )

    syllabus_and_supporting_docs = field.NamedFile(
        title=_(u'Syllabus & Other Supporting Documents'),
        description=_(u'Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel.'),
        required=False,
    )

    min_credits_earned = schema.Choice(
        title=_(u'Minimum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.credits',
    )

    max_credits_earned = schema.Choice(
        title=_(u'Maximum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.credits',
    )

    language_of_study = schema.List(
        title=_(u'Language of Study'),
        description=_(u'Select all that apply.  Contact the Office of International Education to add a language (abroad@uwosh.edu).'),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.language'),
    )

    model.fieldset(
        'compensation',
        label=_(u"Compensation"),
        fields=['load_or_overload', 'replacement_costs', 'paid_by', 'rate_or_lump_sum', 'lump_sum_amount'],
    ),

    load_or_overload = schema.Choice(
        title=_(u'Load or Overload'),
        description=_(u'Choose whether payment is part of load or is overload'),
        required=True,
        vocabulary=load_or_overload,
    )

    replacement_costs = schema.Choice(
        title=_(u'Replacement Costs'),
        description=_(u'Are replacement costs due to the College?'),
        required=True,
        vocabulary=replacement_costs,
    )

    paid_by = schema.Choice(
        title=_(u'Costs are paid by'),
        description=_(u'Choose who pays'),
        required=True,
        vocabulary=paid_by,
    )

    rate_or_lump_sum = schema.Choice(
        title=_(u'Payment Rate or Lump Sum'),
        description=_(u'Choose a payment rate or lump sum'),
        required=True,
        vocabulary=rate_or_lump_sum,
    )

    lump_sum_amount = schema.TextLine(
        title=_(u'Lump sum amount'),
        description=_(u'Enter the lump sum to be paid'),
        required=False,
    )

    model.fieldset(
        'program_dates_fieldset',
        label=_(u"Program Dates"),
        fields=['first_day_of_spring_semester_classes', 'last_day_of_spring_semester_classes',
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
              'winter_interim_spring_payment_deadline_1', 'winter_interim_spring_payment_deadline_2']
    )

    first_day_of_spring_semester_classes = schema.Date(
        title=u'First day of Spring Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_spring_semester_classes = schema.Date(
        title=u'Last day of Spring Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_spring_interim_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_spring_interim_classes = schema.Date(
        title=u'Last day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_spring_graduation_date = schema.Date(
        title=u'official spring graduation date',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_summer_i_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_summer_i_classes = schema.Date(
        title=u'Last day of Summer I Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_summer_ii_classes = schema.Date(
        title=u'First day of Summer II Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_summer_ii_classes = schema.Date(
        title=u'Last day of Summer II Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_summer_graduation_date = schema.Date(
        title=u'Official Summer Graduation Date',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_fall_semester_classes = schema.Date(
        title=u'First day of Fall Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_fall_semester_classes = schema.Date(
        title=u'Last day of Fall Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_winter_interim_classes = schema.Date(
        title=u'First day of Winter Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_winter_interim_classes = schema.Date(
        title=u'Last day of Winter Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_fall_graduation_date = schema.Date(
        title=u'Official Fall Graduation Date',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_in_person_orientation = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester In-person Orientation',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_semester_participant_orientation_deadline = schema.Date(
        title=u'Winter Interim & Spring Semester Participant Orientation Deadline',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_semester_in_person_orientation = schema.Date(
        title=u'Winter Interim & Spring Semester In-person Orientation',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title=u'Spring Interim Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    sunmmer_payment_deadline_2 = schema.Date(
        title=u'Sunmmer Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title=u'Fall Semester Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 1',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )



#"Syllabus & Other Supporting Documents
#Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel."
#"Number of Credits to be Earned by Each Applicant
#Minimum
#Maximum"
#"Language of Study
#Select all that apply.  Contact the Office of International Education to add a language (abroad@uwosh.edu)."
#"Cooperating Partners
#Only entities listed on the UW System Preferred Provider List or academic institutions with a current affiliation agreement with UWO may be selected here.  All other cooperating partners must be selected by following UW System procurement policies."

