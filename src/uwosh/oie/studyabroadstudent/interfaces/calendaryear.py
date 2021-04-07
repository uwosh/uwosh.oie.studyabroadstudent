from datetime import date, datetime
from plone.supermodel import model
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


def date_default_value():
    return date.today()


def datetime_default_value():
    return datetime.today()


class IOIECalendarYear(Interface):

    title = schema.TextLine(
        title=_('Calendar Year'),
        required=True,
    )

    first_day_of_spring_semester_classes = schema.Date(
        title='First day of Spring Semester Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_spring_semester_classes = schema.Date(
        title='Last day of Spring Semester Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    first_day_of_spring_interim_classes = schema.Date(
        title='First day of Spring Interim Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_spring_interim_classes = schema.Date(
        title='Last day of Spring Interim Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    official_spring_graduation_date = schema.Date(
        title='Official spring graduation date',
        required=True,
        defaultFactory=date_default_value,
    )

    first_day_of_summer_i_classes = schema.Date(
        title='First day of Summer I Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_summer_i_classes = schema.Date(
        title='Last day of Summer I Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    first_day_of_summer_ii_classes = schema.Date(
        title='First day of Summer II Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_summer_ii_classes = schema.Date(
        title='Last day of Summer II Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    official_summer_graduation_date = schema.Date(
        title='Official Summer Graduation Date',
        required=True,
        defaultFactory=date_default_value,
    )

    first_day_of_fall_semester_classes = schema.Date(
        title='First day of Fall Semester Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_fall_semester_classes = schema.Date(
        title='Last day of Fall Semester Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    first_day_of_winter_interim_classes = schema.Date(
        title='First day of Winter Interim Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    last_day_of_winter_interim_classes = schema.Date(
        title='Last day of Winter Interim Classes',
        required=True,
        defaultFactory=date_default_value,
    )

    official_fall_graduation_date = schema.Date(
        title='Official Fall Graduation Date',
        required=True,
        defaultFactory=date_default_value,
    )

    summer_request_for_proposals_deadline_date = schema.Date(
        title='Summer Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )
    fall_semester_request_for_proposals_deadline_date = schema.Date(
        title='Fall Semester Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )
    fall_interim_request_for_proposals_deadline_date = schema.Date(
        title='Fall Interim Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )
    spring_semester_request_for_proposals_deadline_date = schema.Date(
        title='Spring Semester Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )
    spring_break_request_for_proposals_deadline_date = schema.Date(
        title='Spring Break Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )
    spring_interim_request_for_proposals_deadline_date = schema.Date(
        title='Spring Interim Request for Proposals Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    summer_application_deadline = schema.Date(
        title='Summer Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    fall_semester_application_deadline = schema.Date(
        title='Fall Semester Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    fall_interim_application_deadline = schema.Date(
        title='Fall Interim Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    spring_semester_application_deadline = schema.Date(
        title='Spring Semester Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    spring_break_application_deadline = schema.Date(
        title='Spring Break Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    spring_interim_application_deadline = schema.Date(
        title='Spring Interim Application Deadline',
        required=True,
        defaultFactory=date_default_value,
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = \
        schema.Datetime(
            title='Spring Interim, Summer & Fall Semester Participant Orientation Deadline',  # noqa
            required=True,
            defaultFactory=datetime_default_value,
        )

    spring_interim_summer_fall_semester_in_person_orientation = \
        schema.Datetime(
            title='Spring Interim, Summer & Fall Semester In-person Orientation',  # noqa
            required=True,
            defaultFactory=datetime_default_value,
        )

    winter_interim_spring_semester_participant_orientation_deadline = \
        schema.Datetime(
            title='Winter Interim & Spring Semester Participant Orientation Deadline',  # noqa
            required=True,
            defaultFactory=datetime_default_value,
        )

    winter_interim_spring_semester_in_person_orientation = schema.Datetime(
        title='Winter Interim & Spring Semester In-person Orientation',
        required=True,
        defaultFactory=datetime_default_value,
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title='Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=True,
        defaultFactory=date_default_value,
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title='Spring Interim Payment Deadline 2',
        required=True,
        defaultFactory=date_default_value,
    )

    summer_payment_deadline_2 = schema.Date(
        title='Summer Payment Deadline 2',
        required=True,
        defaultFactory=date_default_value,
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title='Fall Semester Payment Deadline 2',
        required=True,
        defaultFactory=date_default_value,
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title='Winter Interim & Spring Semester Payment Deadline 1',
        required=True,
        defaultFactory=date_default_value,
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title='Winter Interim & Spring Semester Payment Deadline 2',
        required=True,
        defaultFactory=date_default_value,
    )

    request_for_proposals_due_date = schema.Date(
        title='Request for Proposals Due Date',
        required=True,
        defaultFactory=date_default_value,
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
    step_1_and_2_application_deadline_fi = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline_fi = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline_fi = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    # Spring Semester
    step_1_and_2_application_deadline_ss = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline_ss = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline_ss = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    # Spring Break
    step_1_and_2_application_deadline_sb = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline_sb = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline_sb = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    # Spring Interim
    step_1_and_2_application_deadline_si = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline_si = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline_si = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    # Summer
    step_1_and_2_application_deadline_s = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline_s = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline_s = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    # Fall Semester
    step_1_and_2_application_deadline_f = schema.Date(
        title=_('STEPs I & II Application Deadline'),
        description=_('The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )

    step_3_application_deadline_f = schema.Date(
        title=_('STEP III Application Deadline'),
        description=_('The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )

    step_4_application_deadline_f = schema.Date(
        title=_('STEP IV Application Deadline'),
        description=_('The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )
