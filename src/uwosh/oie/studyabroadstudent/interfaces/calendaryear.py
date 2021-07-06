from datetime import date, datetime
from plone.autoform.directives import widget
from plone.supermodel import model
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.constants import DEADLINES
from uwosh.oie.studyabroadstudent.widgets import SundayStartDateWidget
from zope import schema
from zope.interface import Interface


class DeadlineHelper:
    @staticmethod
    def date_default_value():
        return date.today()

    @staticmethod
    def datetime_default_value():
        return datetime.today()

    @staticmethod
    def get_application_deadline_description(step, semester):
        deadline_info = DEADLINES[step]
        default_deadline = (
            f' The default student application deadline for {semester} programs is {deadline_info[semester]}.'
            if semester in deadline_info
            else ''
        )
        return f'{deadline_info["base_description"]}{default_deadline}'


class IOIECalendarYear(Interface):

    title = schema.TextLine(
        title=_('Calendar Year'),
        required=True,
    )

    widget('first_day_of_spring_semester_classes', SundayStartDateWidget)
    first_day_of_spring_semester_classes = schema.Date(
        title='First day of Spring Semester Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_spring_semester_classes', SundayStartDateWidget)
    last_day_of_spring_semester_classes = schema.Date(
        title='Last day of Spring Semester Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('first_day_of_spring_interim_classes', SundayStartDateWidget)
    first_day_of_spring_interim_classes = schema.Date(
        title='First day of Spring Interim Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_spring_interim_classes', SundayStartDateWidget)
    last_day_of_spring_interim_classes = schema.Date(
        title='Last day of Spring Interim Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('official_spring_graduation_date', SundayStartDateWidget)
    official_spring_graduation_date = schema.Date(
        title='Official spring graduation date',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('first_day_of_summer_i_classes', SundayStartDateWidget)
    first_day_of_summer_i_classes = schema.Date(
        title='First day of Summer I Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_summer_i_classes', SundayStartDateWidget)
    last_day_of_summer_i_classes = schema.Date(
        title='Last day of Summer I Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('first_day_of_summer_ii_classes', SundayStartDateWidget)
    first_day_of_summer_ii_classes = schema.Date(
        title='First day of Summer II Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_summer_ii_classes', SundayStartDateWidget)
    last_day_of_summer_ii_classes = schema.Date(
        title='Last day of Summer II Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('official_summer_graduation_date', SundayStartDateWidget)
    official_summer_graduation_date = schema.Date(
        title='Official Summer Graduation Date',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('first_day_of_fall_semester_classes', SundayStartDateWidget)
    first_day_of_fall_semester_classes = schema.Date(
        title='First day of Fall Semester Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_fall_semester_classes', SundayStartDateWidget)
    last_day_of_fall_semester_classes = schema.Date(
        title='Last day of Fall Semester Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('first_day_of_winter_interim_classes', SundayStartDateWidget)
    first_day_of_winter_interim_classes = schema.Date(
        title='First day of Winter Interim Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('last_day_of_winter_interim_classes', SundayStartDateWidget)
    last_day_of_winter_interim_classes = schema.Date(
        title='Last day of Winter Interim Classes',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('official_fall_graduation_date', SundayStartDateWidget)
    official_fall_graduation_date = schema.Date(
        title='Official Fall Graduation Date',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('summer_request_for_proposals_deadline_date', SundayStartDateWidget)
    summer_request_for_proposals_deadline_date = schema.Date(
        title='Summer Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )
    widget('fall_semester_request_for_proposals_deadline_date', SundayStartDateWidget)
    fall_semester_request_for_proposals_deadline_date = schema.Date(
        title='Fall Semester Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )
    widget('fall_interim_request_for_proposals_deadline_date', SundayStartDateWidget)
    fall_interim_request_for_proposals_deadline_date = schema.Date(
        title='Fall Interim Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )
    widget('spring_semester_request_for_proposals_deadline_date', SundayStartDateWidget)
    spring_semester_request_for_proposals_deadline_date = schema.Date(
        title='Spring Semester Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )
    widget('spring_break_request_for_proposals_deadline_date', SundayStartDateWidget)
    spring_break_request_for_proposals_deadline_date = schema.Date(
        title='Spring Break Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )
    widget('spring_interim_request_for_proposals_deadline_date', SundayStartDateWidget)
    spring_interim_request_for_proposals_deadline_date = schema.Date(
        title='Spring Interim Request for Proposals Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('summer_application_deadline', SundayStartDateWidget)
    summer_application_deadline = schema.Date(
        title='Summer Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('fall_semester_application_deadline', SundayStartDateWidget)
    fall_semester_application_deadline = schema.Date(
        title='Fall Semester Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('fall_interim_application_deadline', SundayStartDateWidget)
    fall_interim_application_deadline = schema.Date(
        title='Fall Interim Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('spring_semester_application_deadline', SundayStartDateWidget)
    spring_semester_application_deadline = schema.Date(
        title='Spring Semester Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('spring_break_application_deadline', SundayStartDateWidget)
    spring_break_application_deadline = schema.Date(
        title='Spring Break Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('spring_interim_application_deadline', SundayStartDateWidget)
    spring_interim_application_deadline = schema.Date(
        title='Spring Interim Application Deadline',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = schema.Datetime(
        title='Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
        required=True,
        defaultFactory=DeadlineHelper.datetime_default_value,
    )

    spring_interim_summer_fall_semester_in_person_orientation = schema.Datetime(
        title='Spring Interim, Summer & Fall Semester In-person Orientation',
        required=True,
        defaultFactory=DeadlineHelper.datetime_default_value,
    )

    winter_interim_spring_semester_participant_orientation_deadline = schema.Datetime(
        title='Winter Interim & Spring Semester Participant Orientation Deadline',
        required=True,
        defaultFactory=DeadlineHelper.datetime_default_value,
    )

    winter_interim_spring_semester_in_person_orientation = schema.Datetime(
        title='Winter Interim & Spring Semester In-person Orientation',
        required=True,
        defaultFactory=DeadlineHelper.datetime_default_value,
    )

    widget('spring_interim_summer_fall_semester_payment_deadline_1', SundayStartDateWidget)
    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title='Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('spring_interim_payment_deadline_2', SundayStartDateWidget)
    spring_interim_payment_deadline_2 = schema.Date(
        title='Spring Interim Payment Deadline 2',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('summer_payment_deadline_2', SundayStartDateWidget)
    summer_payment_deadline_2 = schema.Date(
        title='Summer Payment Deadline 2',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('fall_semester_payment_deadline_2', SundayStartDateWidget)
    fall_semester_payment_deadline_2 = schema.Date(
        title='Fall Semester Payment Deadline 2',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('winter_interim_spring_payment_deadline_1', SundayStartDateWidget)
    winter_interim_spring_payment_deadline_1 = schema.Date(
        title='Winter Interim & Spring Semester Payment Deadline 1',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('winter_interim_spring_payment_deadline_2', SundayStartDateWidget)
    winter_interim_spring_payment_deadline_2 = schema.Date(
        title='Winter Interim & Spring Semester Payment Deadline 2',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    widget('request_for_proposals_due_date', SundayStartDateWidget)
    request_for_proposals_due_date = schema.Date(
        title='Request for Proposals Due Date',
        required=True,
        defaultFactory=DeadlineHelper.date_default_value,
    )

    model.fieldset(
        'step_application_deadlines_fi_fieldset',
        label=_('STEP Application Deadlines (Fall Interim)'),
        fields=[
            'step_1_and_2_application_deadline_fi',
            'step_3_application_deadline_fi',
            'step_4_application_deadline_fi',
        ],
    )
    model.fieldset(
        'step_application_deadlines_ss_fieldset',
        label=_('STEP Application Deadlines (Spring)'),
        fields=[
            'step_1_and_2_application_deadline_ss',
            'step_3_application_deadline_ss',
            'step_4_application_deadline_ss',
        ],
    )
    model.fieldset(
        'step_application_deadlines_sb_fieldset',
        label=_('STEP Application Deadlines (Spring Break)'),
        fields=[
            'step_1_and_2_application_deadline_sb',
            'step_3_application_deadline_sb',
            'step_4_application_deadline_sb',
        ],
    )
    model.fieldset(
        'step_application_deadlines_si_fieldset',
        label=_('STEP Application Deadlines (Spring Interim)'),
        fields=[
            'step_1_and_2_application_deadline_si',
            'step_3_application_deadline_si',
            'step_4_application_deadline_si',
        ],
    )
    model.fieldset(
        'step_application_deadlines_s_fieldset',
        label=_('STEP Application Deadlines (Summer)'),
        fields=[
            'step_1_and_2_application_deadline_s',
            'step_3_application_deadline_s',
            'step_4_application_deadline_s',
        ],
    )
    model.fieldset(
        'step_application_deadlines_f_fieldset',
        label=_('STEP Application Deadlines (Fall)'),
        fields=[
            'step_1_and_2_application_deadline_f',
            'step_3_application_deadline_f',
            'step_4_application_deadline_f',
        ],
    )

    # Fall Interim
    widget('step_1_and_2_application_deadline_fi', SundayStartDateWidget)
    step_1_and_2_application_deadline_fi = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'fall interim')
        ),
        required=False,
    )
    widget('step_3_application_deadline_fi', SundayStartDateWidget)
    step_3_application_deadline_fi = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'fall interim')
        ),
        required=False,
    )
    widget('step_4_application_deadline_fi', SundayStartDateWidget)
    step_4_application_deadline_fi = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'fall interim')
        ),
        required=False,
    )

    # Spring Semester
    widget('step_1_and_2_application_deadline_ss', SundayStartDateWidget)
    step_1_and_2_application_deadline_ss = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'spring semester')
        ),
        required=False,
    )
    widget('step_3_application_deadline_ss', SundayStartDateWidget)
    step_3_application_deadline_ss = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'spring semester')
        ),
        required=False,
    )
    widget('step_4_application_deadline_ss', SundayStartDateWidget)
    step_4_application_deadline_ss = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'spring semester')
        ),
        required=False,
    )

    # Spring Break
    widget('step_1_and_2_application_deadline_sb', SundayStartDateWidget)
    step_1_and_2_application_deadline_sb = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'spring break')
        ),
        required=False,
    )
    widget('step_3_application_deadline_sb', SundayStartDateWidget)
    step_3_application_deadline_sb = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'spring break')
        ),
        required=False,
    )
    widget('step_4_application_deadline_sb', SundayStartDateWidget)
    step_4_application_deadline_sb = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'spring break')
        ),
        required=False,
    )

    # Spring Interim
    widget('step_1_and_2_application_deadline_si', SundayStartDateWidget)
    step_1_and_2_application_deadline_si = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'spring interim')
        ),
        required=False,
    )
    widget('step_3_application_deadline_si', SundayStartDateWidget)
    step_3_application_deadline_si = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'spring interim')
        ),
        required=False,
    )
    widget('step_4_application_deadline_si', SundayStartDateWidget)
    step_4_application_deadline_si = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'spring interim')
        ),
        required=False,
    )

    # Summer
    widget('step_1_and_2_application_deadline_s', SundayStartDateWidget)
    step_1_and_2_application_deadline_s = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'summer semester')
        ),
        required=False,
    )
    widget('step_3_application_deadline_s', SundayStartDateWidget)
    step_3_application_deadline_s = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'summer semester')
        ),
        required=False,
    )
    widget('step_4_application_deadline_s', SundayStartDateWidget)
    step_4_application_deadline_s = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'summer semester')
        ),
        required=False,
    )

    # Fall Semester
    widget('step_1_and_2_application_deadline_f', SundayStartDateWidget)
    step_1_and_2_application_deadline_f = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('steps_1_and_2', 'fall semester')
        ),
        required=False,
    )

    widget('step_3_application_deadline_f', SundayStartDateWidget)
    step_3_application_deadline_f = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_3', 'fall semester')
        ),
        required=False,
    )

    widget('step_4_application_deadline_f', SundayStartDateWidget)
    step_4_application_deadline_f = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_(
            DeadlineHelper.get_application_deadline_description('step_4', 'fall semester')
        ),
        required=False,
    )
