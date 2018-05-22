# -*- coding: utf-8 -*-
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIECalendarYear(Interface):

    title = schema.TextLine(
        title=_('Calendar Year'),
        required=True,
    )

    first_day_of_spring_semester_classes = schema.Date(
        title=u'First day of Spring Semester Classes',
        required=True,
    )

    last_day_of_spring_semester_classes = schema.Date(
        title=u'Last day of Spring Semester Classes',
        required=True,
    )

    first_day_of_spring_interim_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=True,
    )

    last_day_of_spring_interim_classes = schema.Date(
        title=u'Last day of Spring Interim Classes',
        required=True,
    )

    official_spring_graduation_date = schema.Date(
        title=u'official spring graduation date',
        required=True,
    )

    first_day_of_summer_i_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=True,
    )

    last_day_of_summer_i_classes = schema.Date(
        title=u'Last day of Summer I Classes',
        required=True,
    )

    first_day_of_summer_ii_classes = schema.Date(
        title=u'First day of Summer II Classes',
        required=True,
    )

    last_day_of_summer_ii_classes = schema.Date(
        title=u'Last day of Summer II Classes',
        required=True,
    )

    official_summer_graduation_date = schema.Date(
        title=u'Official Summer Graduation Date',
        required=True,
    )

    first_day_of_fall_semester_classes = schema.Date(
        title=u'First day of Fall Semester Classes',
        required=True,
    )

    last_day_of_fall_semester_classes = schema.Date(
        title=u'Last day of Fall Semester Classes',
        required=True,
    )

    first_day_of_winter_interim_classes = schema.Date(
        title=u'First day of Winter Interim Classes',
        required=True,
    )

    last_day_of_winter_interim_classes = schema.Date(
        title=u'Last day of Winter Interim Classes',
        required=True,
    )

    official_fall_graduation_date = schema.Date(
        title=u'Official Fall Graduation Date',
        required=True,
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = schema.Datetime(
        title=u'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
        required=True,
    )

    spring_interim_summer_fall_semester_in_person_orientation = schema.Datetime(
        title=u'Spring Interim, Summer & Fall Semester In-person Orientation',
        required=True,
    )

    winter_interim_spring_semester_participant_orientation_deadline = schema.Datetime(
        title=u'Winter Interim & Spring Semester Participant Orientation Deadline',
        required=True,
    )

    winter_interim_spring_semester_in_person_orientation = schema.Datetime(
        title=u'Winter Interim & Spring Semester In-person Orientation',
        required=True,
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=True,
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title=u'Spring Interim Payment Deadline 2',
        required=True,
    )

    sunmmer_payment_deadline_2 = schema.Date(
        title=u'Sunmmer Payment Deadline 2',
        required=True,
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title=u'Fall Semester Payment Deadline 2',
        required=True,
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 1',
        required=True,
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 2',
        required=True,
    )
