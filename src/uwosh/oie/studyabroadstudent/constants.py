from datetime import date

CURRENT_YEAR = date.today().year
NEXT_YEAR = CURRENT_YEAR + 1

DURATIONS = [
    7,
    14,
    21,
    35,
    65,
    95,
    125,
    155,
    185,
    215,
    245,
    275,
    305,
    335,
    365,
]
PASSWORD_LENGTH = 50
SPECIAL_DAYS = [
    'first_day_of_spring_semester_classes',
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
    'spring_interim_summer_fall_semester_participant_orientation_deadline',
    'spring_interim_summer_fall_semester_in_person_orientation',
    'winter_interim_spring_semester_participant_orientation_deadline',
    'winter_interim_spring_semester_in_person_orientation',
    'spring_interim_summer_fall_semester_payment_deadline_1',
    'spring_interim_payment_deadline_2',
    'summer_payment_deadline_2', 'fall_semester_payment_deadline_2',
    'winter_interim_spring_payment_deadline_1',
    'winter_interim_spring_payment_deadline_2',
    'request_for_proposals_due_date',
]
EMERGENCY_EMAIL_FIELD_DESCRIPTION = (
    'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send '
    'non-emergency messages intended to update contacts about significant unanticipated events that '
    'have occurred or may occur and which have involved or may involve an increase in program risk.'
)
EMERGENCY_PHONE_SECONDARY_DESCRIPTION = (
    'Include area code (and country code if the phone does not have a U.S. phone number).'
)
EMERGENCY_PHONE_PRIMARY_DESCRIPTION = f'Strongly recommended. {EMERGENCY_PHONE_SECONDARY_DESCRIPTION}'

DEFAULT_ELIGIBILITY_REQUIREMENT_1 = (
    'Undergraduate students must have a minimum G.P.A. of 2.0, be in good standing, and meet course '
    'prerequisites. As part of the application process, your disciplinary file will be reviewed. '
    'If you have a campus disciplinary file, this will be taken into consideration when determining '
    'your eligibility. Undergraduates who do not meet minimum GPA and course requirements should contact '
    'the program leader prior to applying to determine course eligibility.'
)
DEFAULT_ELIGIBILITY_REQUIREMENT_2 = (
    'Undergraduate students must have a minimum G.P.A. of 2.0, be in good standing, and meet course '
    'prerequisites. Undergraduate students who are required to complete a Quest III course to fulfill '
    'graduation requirements may apply. Students must have a minimum G.P.A. of 2.0, be in good standing, '
    'meet course prerequisites, and meet Quest III prerequisites. As part of the application process, '
    'your disciplinary file will be reviewed. If you have a campus disciplinary file, this will be taken '
    'into consideration when determining your eligibility. Undergraduates who are not required to complete '
    'a Quest III course to graduate are not eligible; however, they may apply for consideration on a '
    'space-available basis along with USP & instructor consent. Seats will be assigned to these applicants '
    'only after all applicants who are required to complete Quest III to graduate and who have met the '
    'STEP III deadline have been awarded a seat.'
)
DEFAULT_ELIGIBILITY_REQUIREMENT_3 = (
    'Students must have a minimum G.P.A. of 3.25, be accepted into the Professional Counseling Graduate '
    'program, be in good standing, and meet course prerequisites. As part of the application process, '
    'your disciplinary file will be reviewed. If you have a campus disciplinary file, this will be taken '
    'into consideration when determining your eligibility. Undergraduates who do not meet minimum GPA '
    'and course requirements should contact the program leader prior to applying to determine course '
    'eligibility.'
)
DEFAULT_ELIGIBILITY_REQUIREMENTS = (
    DEFAULT_ELIGIBILITY_REQUIREMENT_1,
    DEFAULT_ELIGIBILITY_REQUIREMENT_2,
    DEFAULT_ELIGIBILITY_REQUIREMENT_3,
)
DEADLINES = {
    'steps_1_and_2': {
        'spring interim': 'the 1st Friday of Spring Semester',
        'summer semester': 'the last Friday in February',
        'fall semester': 'the last Friday in February',
        'fall interim': 'the 2nd Friday in September',
        'spring semester': 'the last Friday in September',
        'base_description': (
            'The STEPs I & II application deadline must be the OIE default student application date, '
            'or a date that is two weeks prior to the contracted date to release airline tickets, '
            'whichever is earlier. Alternatively, the Program Liaison may identify an even earlier '
            'deadline, provided OIE can provide sufficient staffing in the week leading up to the '
            'proposed deadline.'
        ),
    },
    'step_3': {
        'spring interim': 'the 2nd Friday of Spring Semester',
        'summer semester': 'the 1st Friday in March',
        'fall semester': 'the 1st Friday in March',
        'fall interim': 'the 3rd Friday in September',
        'spring semester': 'the 1st Friday in October',
        'base_description': (
            'The STEP III application deadline must be the OIE default student application date, '
            'or a date that is one week prior to the contracted date to release airline tickets, '
            'whichever is earlier. Alternatively, the Program Liaison may identify an even earlier '
            'deadline, provided OIE can provide sufficient staffing in the week leading up to the '
            'proposed deadline.'
        ),
    },
    'step_4': {
        'base_description': (
            'The STEP IV application deadline must take into consideration external deadlines and '
            'processing time in the OIE from the point of receiving completed application documents, '
            'and the anticipated dates on which documents can be sent to external partners and '
            'received by them.'
        ),
    },
}
DEFAULT_TUITION_AND_FEES = (
    '$0 Tuition; $0 Seg Fees',
    '$0 Tuition; $0 Seg Fees; relevant tuition equivalent to be charged',
    'No Change to Course Tuition & Fees',
    'Tuition Charged for 01 cr + related fees; charge outside of the tuition plateau',
    'Tuition Charged for 01 cr; Seg Fees Also Charged',
    'Tuition Charged for 02 cr; Seg Fees Also Charged',
    'Tuition Charged for 03 cr; $0 Seg Fees',
    'Tuition Charged for 03 cr + related fees; charge outside of the tuition plateau',
    'Tuition Charged for 03 cr; Seg Fees Also Charged',
    'Tuition Charged for 04 cr; Seg Fees Also Charged',
    'Tuition Charged for 05 cr; Seg Fees Also Charged',
    'Tuition Charged for 06 cr outside of the tuition plateau; $0 Seg Fees',
    'Tuition Charged for 06 cr; $0 Seg Fees',
    'Tuition Charged for 06 cr; Seg Fees Also Charged',
    'Tuition Charged for 07 cr; Seg Fees Also Charged',
    'Tuition Charged for 08 cr; Seg Fees Also Charged',
    'Tuition Charged for 09 cr; Seg Fees Also Charged',
    'Tuition Charged for 1.5 cr; Seg Fees Also Charged',
    'Tuition Charged for 10 cr; Seg Fees Also Charged',
    'Tuition Charged for 11 cr; Seg Fees Also Charged',
    'Tuition Charged for 12 cr; $0 Seg Fees',
    'Tuition Charged for 12 cr; Seg Fees Also Charged',
)


CALENDAR_YEAR_DESCRIPTION = (
    'Select the calendar year during which the program will run. '
    'This is not the year associated with the term of study. '
    f'For example, a January interim program running from Jan 2-28, {NEXT_YEAR} '
    f'will be associated with "{NEXT_YEAR}". A program running Dec 28, {CURRENT_YEAR}-Jan 28, {NEXT_YEAR} '
    f'will also be associated with "{NEXT_YEAR}".'
)

STATES_FOR_DISPLAYING_PROGRAMS = (
    'pending-discussions-with-program-manager',
    'request-for-proposals-under-development',
    'request-for-proposals-under-liaison-review',
    'pending-provider-responses',
    'provider-proposals-under-oie-review',
    'provider-proposals-under-liaison-review',
    'pending-program-fee-determination-by-oie',
    'program-fee-under-liaison-review',
    'program-fee-pending-publication',
    'applicants-considering-change',
    'application-intake-in-progress',
)
