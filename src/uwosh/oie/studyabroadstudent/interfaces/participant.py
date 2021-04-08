
# IOIEStudyAbroadParticipant: the new content type for participant applications

from collective import dexteritytextindexer
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.autoform.directives import omitted, widget
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile import field
from plone.namedfile.file import NamedFile
from plone.supermodel import model
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid, checkEmailAddress
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import departure_mode_transportation_vocabulary  # noqa : E501
from uwosh.oie.studyabroadstudent.vocabularies import departure_transfer_vocabulary  # noqa : E501
from uwosh.oie.studyabroadstudent.vocabularies import graduation_month_vocabulary  # noqa : E501
from uwosh.oie.studyabroadstudent.vocabularies import return_mode_transportation_vocabulary  # noqa : E501
from uwosh.oie.studyabroadstudent.vocabularies import return_transfer_vocabulary  # noqa : E501
from uwosh.oie.studyabroadstudent.vocabularies import (
    RegistryValueVocabulary,
    contactrelationship,
    socialmediaservice,
    yes_no_vocabulary,
)
from zope import schema
from zope.interface import Interface
from zope.schema import ValidationError

import re


class InvalidEmailAddress(ValidationError):
    """Invalid email address"""


class InvalidStudentID(ValidationError):
    """Invalid UW Oshkosh student ID format"""


def validate_email(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


STUDENT_ID_RE = re.compile(r'^\d\d\d\d\d\d\d$')


def validate_student_id(value):
    if len(value) != 7 or not STUDENT_ID_RE.match(value):
        raise InvalidStudentID(value)
    return True


def get_url_special_student_form():
    form = api.portal.get_registry_record(
        'oiestudyabroadstudent.state_of_wisconsin_need_based_travel_grant_form',  # noqa : E501
    )
    if form is not None:
        filename, data = b64decode_file(form)
        file = NamedFile(data=data, filename=filename)
        url = 'data:{0};base64, {1}'.format(
            file.contentType,
            file.data.encode('base64'),
        )
        html = '<a target="_blank" href="{0}">Download this form</a>'.format(
            url,
        )
        return RichTextValue(html, 'text/html', 'text/html')
    else:
        return RichTextValue(
            '<em>The Wisconsin need based travel grant form has not yet been specified by an administrator</em>',  # noqa : E501
            'text/html',
            'text/html',
        )


def get_url_special_student_form_for_undergraduate_admissions_form():
    form = api.portal.get_registry_record(
        'oiestudyabroadstudent.special_student_form_for_undergraduate_admissions',  # noqa : E501
    )
    if form is not None:
        filename, data = b64decode_file(form)
        file = NamedFile(data=data, filename=filename)
        url = 'data:{0};base64, {1}'.format(
            file.contentType,
            file.data.encode('base64'),
        )
        html = '<a target="_blank" href="{0}">Download this form</a>'.format(
            url,
        )
        return RichTextValue(html, 'text/html', 'text/html')
    else:
        return RichTextValue(
            '<em>The special student form for undergraduate admissions has not yet been specified by an administrator</em>',  # noqa : E501
            'text/html',
            'text/html',
        )


def get_url_disciplinary_clearance_form():
    form = api.portal.get_registry_record(
        'oiestudyabroadstudent.disciplinary_clearance_form',
    )
    if form is not None:
        filename, data = b64decode_file(form)
        file = NamedFile(data=data, filename=filename)
        url = 'data:{0};base64, {1}'.format(
            file.contentType,
            file.data.encode('base64'),
        )
        html = '<a target="_blank" href="{0}">Download this form</a>'.format(
            url,
        )
        return RichTextValue(html, 'text/html', 'text/html')
    else:
        return RichTextValue(
            '<em>The disciplinary clearance form has not yet been specified by an administrator</em>',  # noqa : E501
            'text/html',
            'text/html',
        )


class IOIEStudyAbroadParticipant(Interface):
    dexteritytextindexer.searchable('title')
    omitted('title')
    title = schema.TextLine(
        title=_('Title'),
        required=False,
        readonly=True,
        default=_('will be auto-generated'),
    )

    #######################################################
    model.fieldset(
        'participant_name',
        label=_('Name'),
        fields=[
            'firstName',
            'middleName',
            'lastName',
        ],
    )

    dexteritytextindexer.searchable('firstName')
    firstName = schema.TextLine(
        title=_('First Name'),
        required=True,
    )

    dexteritytextindexer.searchable('middleName')
    middleName = schema.TextLine(
        title=_('Middle Name'),
        required=False,
    )

    dexteritytextindexer.searchable('lastName')
    lastName = schema.TextLine(
        title=_('Last Name'),
        required=True,
    )

    #######################################################
    model.fieldset(
        'progress',
        label=_('Progress'),
        fields=[
            'seatNumber',
            'waitlistNumber',
        ],
    )

    seatNumber = schema.TextLine(
        title=_('Seat Number'),
        description=_('auto generate using STEP II date/time stamp and min/max participant fields from "program development" workflow'), # noqa : E501
        #  TODO (BD) - verify this functionality  # noqa : T000
        # required=False,
    )

    waitlistNumber = schema.TextLine(
        title=_('Waitlist Number'),
        description=_('auto generate using STEP II date/time stamp and min/max participant fields from "program development" workflow'), # noqa : E501
        #  TODO (BD) - verify this functionality  # noqa : T000
        # required=False,
    )

    #######################################################
    model.fieldset(
        'interest',
        label=_('Express Interest'),
        fields=[
            'email',
            'programName',
            'programName2',
            'programName3',
        ],
    )

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_('Email Address'),
        description=_(
            'UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.'),  # noqa : E501
        constraint=validate_email,
        # TODO - write test_validate_email  # noqa : T000
        required=True,
    )

    dexteritytextindexer.searchable('programName')
    programName = schema.Choice(
        title=_('Program Name (first choice)'),
        description=_('The courses listed for this program choice will appear in your Courses tab; you must indicate there which courses you wish to enroll in.'),  # noqa : E501
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=True,
    )

    dexteritytextindexer.searchable('programName2')
    programName2 = schema.Choice(
        title=_('Program Name (second choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    dexteritytextindexer.searchable('programName3')
    programName3 = schema.Choice(
        title=_('Program Name (third choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    #######################################################
    model.fieldset(
        'step1',
        label=_('Step 1'),
        fields=['studentID'],
    )

    dexteritytextindexer.searchable('studentID')
    studentID = schema.TextLine(
        title=_('UW Oshkosh Student ID'),
        description=_('Do not include the initial "W" in the UW Oshkosh ID.  If you do not have a UW Oshkosh ID (current or past), leave this blank.'),  # noqa : E501
        required=False,
        constraint=validate_student_id,
        # TODO - write test_validate_student_id  # noqa : T000
    )

    #######################################################
    model.fieldset(
        'contact',
        label=_('Step1: Contact Information'),
        fields=[
            'mainPhone',
            'otherPhone',
            'otherContactService',
            'otherContactID',
            'localAddr',
            'localAddrApt',
            'localCity',
            'localState',
            'localZip',
            'homeAddr1',
            'homeAddrApt',
            'homeCity',
            'homeState',
            'homeZip',
            'homeCountry',
        ],
    )

    mainPhone = schema.TextLine(
        title=_('Main phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=True,
    )

    otherPhone = schema.TextLine(
        title=_('Other phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    widget(
        'otherContactService',
        onchange='javascript:otherContactServiceChanged(event)',
    )
    otherContactService = schema.Choice(
        title=_('Other Contact Service'),
        description=_(
            'Select the service you use most often, '
            "or select 'No value' if you don't use any of these services.",
        ),
        required=False,
        vocabulary=socialmediaservice,
    )

    otherContactID = schema.TextLine(
        title=_('Other contact service username or ID'),
        description=_('Enter your username or ID for the service you chose above.'),  # noqa : E501
        required=False,
    )

    localAddr = schema.TextLine(
        title=_('Local Address: Street'),
        required=True,
    )

    localAddrApt = schema.TextLine(
        title=_('Local Address: Apartment Number'),
        required=False,
    )

    localCity = schema.TextLine(
        title=_('Local Address: City'),
        required=True,
    )

    localState = schema.TextLine(
        title=_('Local Address: State'),
        default=_('WI'),
        required=True,
    )

    localZip = schema.TextLine(
        title=_('Local Address: Zip Code'),
        default=_('54901'),
        required=True,
    )

    homeAddr1 = schema.TextLine(
        title=_('Home Address: Street'),
        required=True,
    )

    homeAddrApt = schema.TextLine(
        title=_('Home Address: Apartment Number'),
        required=False,
    )

    homeCity = schema.TextLine(
        title=_('Home Address: City'),
        description=_(''),
        required=True,
    )

    homeState = schema.TextLine(
        title=_('Home Address: State/Province/Department'),
        description=_(''),
        required=True,
    )

    homeZip = schema.TextLine(
        title=_('Home Address: Zip or Postal Code'),
        description=_(''),
        required=True,
    )

    homeCountry = schema.Choice(
        title=_('Home Address: Country'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    #######################################################
    model.fieldset(
        'emergency_contact',
        label=_('Emergency Contact'),
        fields=[
            'emerg1fullname',
            'emerg1relationship',
            'emerg1mail_personal',
            'emerg1mail_work',
            'emerg1phone_main',
            'emerg1phone_other',
            'emerg2fullname',
            'emerg2relationship',
            'emerg2mail_personal',
            'emerg2mail_work',
            'emerg2phone_main',
            'emerg2phone_other',
            'emerg3fullname',
            'emerg3relationship',
            'emerg3mail_personal',
            'emerg3mail_work',
            'emerg3phone_main',
            'emerg3phone_other',
            'emerg4fullname',
            'emerg4relationship',
            'emerg4mail_personal',
            'emerg4mail_work',
            'emerg4phone_main',
            'emerg4phone_other',
        ],
    )

    widget(
        'emerg1fullname',
        onchange='javascript:emergencyFullNameChanged(event)',
    )
    emerg1fullname = schema.TextLine(
        title=_('1 Full Name'),
        required=False,
    )

    emerg1relationship = schema.Choice(
        title=_('1 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg1mail_personal = schema.TextLine(
        title=_('1 Main Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1mail_work = schema.TextLine(
        title=_('1 Other Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1phone_main = schema.TextLine(
        title=_('1 Main Phone'),
        description=_('Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    emerg1phone_other = schema.TextLine(
        title=_('1 Other Phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    ###############

    widget('emerg2fullname', onchange='javascript:fullNameChanged(event)')
    emerg2fullname = schema.TextLine(
        title=_('2 Full Name'),
        required=False,
    )

    emerg2relationship = schema.Choice(
        title=_('2 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg2mail_personal = schema.TextLine(
        title=_('2 Main Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mail_work = schema.TextLine(
        title=_('2 Other Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2phone_main = schema.TextLine(
        title=_('2 Main Phone'),
        description=_('Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    emerg2phone_other = schema.TextLine(
        title=_('2 Other Phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    #############

    widget('emerg3fullname', onchange='javascript:fullNameChanged(event)')
    emerg3fullname = schema.TextLine(
        title=_('3 Full Name'),
        required=False,
    )

    emerg3relationship = schema.Choice(
        title=_('3 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg3mail_personal = schema.TextLine(
        title=_('3 Main Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mail_work = schema.TextLine(
        title=_('3 Other Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3phone_main = schema.TextLine(
        title=_('3 Main Phone'),
        description=_('Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    emerg3phone_other = schema.TextLine(
        title=_('3 Other Phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    #############

    widget('emerg4fullname', onchange='javascript:fullNameChanged(event)')
    emerg4fullname = schema.TextLine(
        title=_('4 Full Name'),
        required=False,
    )

    emerg4relationship = schema.Choice(
        title=_('4 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg4mail_personal = schema.TextLine(
        title=_('4 Main Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4mail_work = schema.TextLine(
        title=_('4 Other Email'),
        description=_('Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa : E501
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4phone_main = schema.TextLine(
        title=_('4 Main Phone'),
        description=_('Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    emerg4phone_other = schema.TextLine(
        title=_('4 Other Phone'),
        description=_('Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa : E501
        required=False,
    )

    #######################################################
    model.fieldset(
        'demographics',
        label=_('Demographics'),
        fields=[
            'ethnicity',
            'ethnicityOther',
            'stateResidency',
            'countrycitizenship',
            'immigrationStatus',
            'countryBirth',
            'dateOfBirth',
        ],
    )

    ethnicity = schema.Choice(
        title=_('Ethnicity'),
        description=_(''),
        source=RegistryValueVocabulary('oiestudyabroadstudent.ethnicities'),
        required=False,
    )

    ethnicityOther = schema.TextLine(
        title=_('Ethnicity: Other'),
        description=_('Enter your ethnicity only if you selected "other" above.'),  # noqa : E501
        required=False,
    )

    stateResidency = schema.Choice(
        title=_('State of Residency'),
        description=_(''),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.us_states_territories',
        ),
        required=True,
    )

    countrycitizenship = schema.Choice(
        title=_('Country of Citizenship'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    immigrationStatus = schema.Choice(
        title=_('Immigration Status'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.immigration_status',
        ),
        required=True,
    )

    countryBirth = schema.Choice(
        title=_('Country of Birth'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    dateOfBirth = schema.Date(
        title=_('Date of Birth'),
        required=True,
    )

########################################################
    model.fieldset(
        'education',
        label=_('Education'),
        fields=[
            'educationLevel',
            'universityEnrolledUWO',
            'universityEnrolledOther',
            'major1',
            'major2',
            'minor1',
            'minor2',
            'graduationYear',
            'graduationMonth',
        ],
    )

    educationLevel = schema.Choice(
        title=_('Current Education Level'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.education_level',
        ),
        required=False,
    )

    universityEnrolledUWO = schema.Choice(
        title=_('Are you enrolled at UW Oshkosh?'),
        description=_(''),
        vocabulary=yes_no_vocabulary,
        required=True,
    )

    universityEnrolledOther = schema.TextLine(
        title=_('If "School" is "OTHER"'),
        description=_('Type the official name of the school you are attending now only if you chose "No" above.'),  # noqa : E501
        required=False,
    )

    major1 = schema.Choice(
        title=_('First Major'),
        description=_('This must match the intended major on your STAR report.'),  # noqa : E501
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    major2 = schema.Choice(
        title=_('Second Major'),
        description=_('This must match the intended major on your STAR report.  If you don\'t have a second major, leave this blank.'),  # noqa : E501
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    minor1 = schema.TextLine(
        title=_('First Minor'),
        description=_('This must match the intended minor on your STAR report.  If you don\'t have a minor, leave this blank.'),  # noqa : E501
        required=False,
    )

    minor2 = schema.TextLine(
        title=_('Second Minor'),
        description=_('This must match the intended minor on your STAR report.  If you don\'t have a minor, leave this blank.'),  # noqa : E501
        required=False,
    )

    graduationYear = schema.Int(
        title=_('Graduation: Anticipated Year'),
        description=_('Enter the full 4-digit year.'),
        min=2018,
        max=2100,
        required=False,
    )

    graduationMonth = schema.Choice(
        title=_('Graduation: Anticipated Month'),
        description=_('Select the month that corresponds to your official graduation date.'),  # noqa : E501
        vocabulary=graduation_month_vocabulary,
        required=False,
    )

    #######################################################
    model.fieldset(
        'courses',
        label=_('Study Away Courses'),
        fields=['courses'],
    )

    courses = schema.List(
        title=_('Course Selection'),
        description=_('Request enrollment in study away courses.  Your selection must match advertised course options.'),  # noqa : E501
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.course_subject_and_number',
            ),
        ),
    )

    #######################################################
    model.fieldset(
        'date',
        label=_('Dates'),
        fields=[
            'interviewDate',
            'prePostTravelClassDates',
            'orientationDeadline',
            'paymentDeadlines',
            'departureDate',
            'airportTransferDeparture',
            'departureModeOfTransportation',
            'returnDepartureDate',
            'returnModeOfTransportation',
            'airportTransferReturn',
            'requestToDeviateFromProgramDates',
        ],
    )

    interviewDate = schema.Date(
        title=_('Interview Date'),
        description=_(
            'Contact the Program Liaison to schedule an interview. Make your interview appointment '
            'and type your interview date here prior to submiting this application.  The actual '
            'interview date may or may not need to occur prior to the STEP II application deadline. '
            'This will be determined by the Program Liaison.'
        ),
        required=False,
    )

    prePostTravelClassDates = schema.Choice(
        title=_('Confirm Attendance at Pre- & Post-travel Program-specific Sessions'),
        description=_(
            'Select ''Yes'' to confirm that you will attend all advertised pre- or post-travel '
            'sessions.  Select ''No'' if you have a conflict on one or more dates.'
        ),
        vocabulary=yes_no_vocabulary,
        required=True,
        # TODO insert date from program object; Displays only if there are dates in "Pretravel Class & Orientation Dates" or "Post-travel Class Dates" in the MGMT PORTAL.  # noqa : E501
    )

    orientationDeadline = schema.Choice(
        title=_('Orientation Submission Deadline'),
        description=_(
            'I understand that the Office of International Education deadline for submission '
            'of orientation materials is a final deadline.  I understand and agree that all '
            'Office of International Education orientation requirements must be completed by '
            'this date.  If I forsee conflicts with this date, I will complete requirements in '
            'advance of this date.  If not completed by this date, I understand and agree that '
            'the Office of International Education will begin the process of removing me from my '
            'program and that the Withdrawal & Refund Policy will apply.'
        ),
        vocabulary=yes_no_vocabulary,
        required=True,
    )

    paymentDeadlines = schema.Choice(
        title=_('Payment Deadlines'),
        description=_(
            'I understand that the payment deadlines are final deadlines and that it is my '
            'responsibility to record these dates in my calendar.  I understand that all '
            'payments must be made in full by the deadlines, or I must submit the '
            '"Notice of Financial Aid Award for Study Abroad/Away" form if making my payments '
            'using financial aid, a scholarship that I have already received, veterans benefits '
            'or an outside loan.  If not submitted by this date, I understand that the Office of '
            'International Education will begin the process of removing me from my program and that '
            'the Withdrawal & Refund Policy will apply.'
        ),
        vocabulary=yes_no_vocabulary,
        required=True,
    )

    departureDate = schema.Date(
        title=_('Program Departure Date'),
        description=_('will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # noqa: T000  # TODO insert date from program object when in transfer provided state
    )

    airportTransferDeparture = schema.Choice(
        title=_('Confirm Departure from Oshkosh (or alternative city)'),
        description=_(''),
        vocabulary=departure_transfer_vocabulary,
        required=False,
        # noqa: T000  # TODO this should appear only when "transfer provided" is selected
        #  on the "program workflow"
    )

    departureModeOfTransportation = schema.Choice(
        title=_('Confirm Flight'),
        description=_(''),
        vocabulary=departure_mode_transportation_vocabulary,
        required=False,
        # noqa: T000  # TODO this should appear only when "transfer provided" is selected
        #  on the "program workflow"
    )

    returnDepartureDate = schema.Date(
        title=_('Program Return Date'),
        description=_('will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # noqa: T000  # TODO insert date from program object when in transfer provided state
    )

    returnModeOfTransportation = schema.Choice(
        title=_('Return-Mode of Transportation'),
        description=_('Choose one'),
        vocabulary=return_mode_transportation_vocabulary,
        required=False,
        # noqa: T000  # TODO this should appear only when "transfer provided" is selected
        #  on the "program workflow"
    )

    airportTransferReturn = schema.Choice(
        title=_('Confirm Return to Oshkosh (or alternative city)'),
        description=_(''),
        vocabulary=return_transfer_vocabulary,
        required=False,
        # noqa: T000  # TODO this should appear only when "transfer provided" is selected
        #  on the "program workflow"
    )

    requestToDeviateFromProgramDates = schema.Choice(
        title=_('Request to Deviate from Program Dates'),
        description=_('Select ''Yes'' once you have printed, read, signed and uploaded this PDF'),
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO need link to the PDF document  # noqa : E501
        # currently 'https://www.uwosh.edu/oie/away/documents/deviationletter.pdf/view'
    )

    #######################################################
    model.fieldset(
        'financial_aid',
        label=_('Financial Aid'),
        fields=[],
    )

    #######################################################
    model.fieldset(
        'shortanswerquestions',
        label=_('Short Answer Questions'),
        fields=[
            'applicant_question_text1',
            'applicant_question_answer1',
            'applicant_question_text2',
            'applicant_question_answer2',
            'applicant_question_text3',
            'applicant_question_answer3',
            'applicant_question_text4',
            'applicant_question_answer4',
            'applicant_question_text5',
            'applicant_question_answer5',
        ],
    )

    applicant_question_text1 = schema.Text(
        title='Applicant Question 1',
        description='',
        default='If this help text appears, you may skip this question. This program does not require a response.',  # noqa : E501
        required=False,
    )

    applicant_question_answer1 = schema.Text(
        title='Answer 1',
        description='If a question appears under Applicant Question 1 above, type your response here.',
        required=False,
    )

    applicant_question_text2 = schema.Text(
        title='Applicant Question 2',
        description='',
        default='If this help text appears, you may skip this question. This program does not require a response.',  # noqa : E501
        required=False,
    )

    applicant_question_answer2 = schema.Text(
        title='Answer 2',
        description='If a question appears under Applicant Question 2 above, type your response here.',
        required=False,
    )

    applicant_question_text3 = schema.Text(
        title='Applicant Question 3',
        description='',
        default='If this help text appears, you may skip this question. This program does not require a response.',  # noqa : E501
        required=False,
    )
    applicant_question_answer3 = schema.Text(
        title='Answer 3',
        description='If a question appears under Applicant Question 3 above, type your response here.',  # noqa : E501
        required=False,
    )

    applicant_question_text4 = schema.Text(
        title='Applicant Question 4',
        description='',
        default='If this help text appears, you may skip this question. This program does not require a response.',  # noqa : E501
        required=False,
    )

    applicant_question_answer4 = schema.Text(
        title='Answer 4',
        description='If a question appears under Applicant Question 4 above, type your response here.',  # noqa : E501
        required=False,
    )
    applicant_question_text5 = schema.Text(
        title='Applicant Question 5',
        description='',
        default='If this help text appears, you may skip this question. This program does not require a response.',  # noqa : E501
        required=False,
    )

    applicant_question_answer5 = schema.Text(
        title='Answer 5',
        description='If a question appears under Applicant Question 5 above, type your response here.',  # noqa : E501
        required=False,
    )
    #######################################################

    model.fieldset(
        'background',
        label=_('Background'),
        description=_('If you are required to apply for advance permission (a visa) to enter one or more of your host countries, your visa application may require you to disclose citations, convictions and/or arrests in a criminal record.'),  # noqa : E501
        fields=[],
    )
    #######################################################

    model.fieldset(
        'release',
        label=_('Release'),
        fields=[
            'UWOshkoshRelease',
            'certification',
        ],
    )
    #######################################################

    model.fieldset(
        'forms',
        label=_('STEP II Forms'),
        description=_('To complete STEP II, print relevant documents, clearly print your responses, sign forms by hand where indicated, and follow instructions below.  Signatures cannot be typed.'),  # noqa : E501
        fields=[
            'applicationFeeOK',
            'disciplinary_clearance_form_link',
            'disciplinary_clearance_form_uploaded_file',
            'specialStudentFormOK',
            'state_of_wisconsin_need_based_travel_grant_form_link',
            'state_of_wisconsin_need_based_travel_grant_form_uploaded_file',
            'special_student_form_for_undergraduate_admissions_form_link',
            'special_student_form_for_undergraduate_admissions_uploaded_file',
            'transcriptsOK',
            'UWOshkoshStatementOK',
            'UWSystemStatementOK',
            'withdrawalRefund',
            'cumulativeGPA',
        ],
    )

    disciplinary_clearance_form_link = RichText(
        title='Disciplinary Clearance Form',
        description='Download this PDF, fill it out, and upload it below',
        required=False,
        defaultFactory=get_url_disciplinary_clearance_form,
    )

    disciplinary_clearance_form_uploaded_file = field.NamedFile(
        title='Disciplinary Clearance Form',
        description='Upload your filled-out copy of the form',
        required=False,
    )

    state_of_wisconsin_need_based_travel_grant_form_link = RichText(
        title='State of Wisconsin Need-based Travel Grant Form',
        description='Download this PDF, fill it out, and upload it below',
        required=False,
        defaultFactory=get_url_special_student_form,
    )

    state_of_wisconsin_need_based_travel_grant_form_uploaded_file = \
        field.NamedFile(
            title='State of Wisconsin Need-based Travel Grant Submission',
            description='Upload your completed form.',
            required=False,
        )

    special_student_form_for_undergraduate_admissions_form_link = RichText(
        title='Special/Non-degree Registration-Undergraduate Level',
        description='Download this form, fill it out, and upload it below.',
        required=False,
        defaultFactory=get_url_special_student_form_for_undergraduate_admissions_form,  # noqa : E501
        # TODO appears when "Special/Non-Degree Registration-Graduate Level"  # noqa : E501
        #  is checked "yes" in the MGMT PORTAL
        #   AND
        #   "Current Education Level" is NOT "graduate school"
        #   AND
        #   the course request in the PART PORTAL includes at least one course
        #   numbered 500-799.
        #   OR
        #   appears when "Special/Non-Degree Registration-Graduate Level" is
        #   checked "yes" in the MGMT PORTAL
        #   AND
        #   "Current Education Level" IS "graduate school"
        #   AND
        #   the course request in the PART PORTAL includes at least one course
        #   numbered 100-499.
    )

    special_student_form_for_undergraduate_admissions_uploaded_file = \
        field.NamedFile(
            title='Special/Non-degree Registration-Undergraduate Level Submission',  # noqa : E501
            description='Upload your completed form.',
            required=False,
        )

    cumulativeGPA = schema.Float(
        title=_('Cumulative GPA'),
        description=_('Type the applicant''s CURRENT CUMULATIVE GPA exactly as it appears on the unofficial transcript.'),  # noqa : E501
        required=False,
    )

    #######################################################
    model.fieldset(
        'stepiii_documentation',
        label=_('Documentation'),
        description=_('Step 3 Documentation'),
        fields=[
            'transferCreditForm_link',
            'transferCreditSubmission',
            'transferCreditVerified',
        ],
    )

    #######################################################
    model.fieldset(
        'stepiii_identification',
        label=_('Step 3 Identification'),
        description=_('Complete the following using information from your unexpired passport (required for international travel) or with your unexpired driver\'s license (for domestic travel only).'),  # noqa : E501
        fields=[
            'travelDocLast',
            'travelDocFirst',
            'travelDocMiddle',
            'travelDocSex',
            'travelDocNumber',
            'travelDocExpiration',
            'passportReceipt',
            'passportOK',
            'driversLicenseReceipt',
            'driversLicenseReceiptVerified',
            'photoPaperOfficial',
            'photoPaperOfficialVerified',
            'photoDigitalOfficial',
            'photoDigitalOfficialVerified',
            'photoPaper',
            'photoPaperVerified',
            'photoDigital',
            'photoDigitalVerified',
        ],
    )

    #######################################################
    model.fieldset(
        'stepiii_fecop',
        label=_('STEP 3 FECOP'),
        description=_('Financial'),
        fields=[
            'fecop_label',
            'fecop_link',
            'fecopSubmission',
            'fecopVerified',
        ],
    )

    #######################################################
    model.fieldset(
        'stepiii_lifestyle',
        label=_('STEP 3 Lifestyle'),
        fields=[
            'isVegetarian',
            'smokingPreferred',
        ],
    )

    #######################################################
    model.fieldset(
        'stepiii_health',
        label=_('STEP 3 Health'),
        fields=[
            'medicalReadStatement',
            'medicalHealthProblems_whatCondition',
            'medicalHealthProblems_stable',
            'medicalHealthProblems',
            'healthConditionsSurgeriesYesNo',
            'healthConditionsSurgeriesDetails',
            'medicalHealthProblems_underCare',
            'wheelchair',
            'assistiveDevice',
            'assistiveDeviceOnFlight',
            'assistiveDeviceList',
            'hasDifficultyWalking',
            'maxWalkingDistance',
            'stairsMax',
            'walkingClimbingDescription',
            'sight',
            'healthPhysicalAdditionalInfoYesNo',
            'additionalNeeds',
            'medicalRegistered',
            'medicalRegistered_office',
            'medicalRegistered_accommodations',
            'medicalHealthProblems_additionalInfo',
            'medicalMentalProblems_enoughMedication',
            'medicalMentalProblems_stable',
            'medicalAccessOK',
            'healthMeetingNotes',
        ],
    )

    # healthConfirmation_label = schema.TextLine(
    #     title=_('I understand and agree'),
    # )

    #######################################################
    model.fieldset(
        'stepiii_allergies_and_medication',
        label=_('STEP 3 Allergies & Medications'),
        fields=[
            'allergiesYesNo',
            'foodAllergies',
            'medications_label',
            'medicalHealthProblems_takenMedication',
            'medicalHealthProblems_willingToPrescribe',
            'medicalHealthProblems_medications',
            'medicationsStorage',
        ],
    )

    #######################################################
    model.fieldset(
        'stepiii_roommate',
        label=_('STEP III Roommate'),
        description=_('If you are not traveling with a UW Oshkosh student group, do not list a roommate choice.  If you are traveling on a group program, list your first and second choice roommates here.  Any roommate you request must list you on his/her application in return.'),  # noqa : E501
        fields=[
            'roommateName1',
            'roommateName2',
        ],
    )

    #######################################################
    # model.fieldset(
    #     'stepivforms',
    #     label=_('STEP IV Forms'),
    #     fields=[
    #         'stepiv_label',
    #         'enrollment_label',
    #         'cbc_label',
    #         'financial_label',
    #         'depositOnTime',
    #         'payment2OnTime',
    #         'orientation_label',
    #         'attendedOrientation',
    #         'travelDocuments_label',
    #         'flight_label',
    #         'flightDeparture_label',
    #         'flightReturn_label',
    #     ],
    # )

    # stepiv_label = schema.TextLine(
    #     title=_('STEP IV'),
    # )

    # enrollment_label = schema.TextLine(
    #     title=_('Course Enrollment'),
    # )

    # financial_label = schema.TextLine(
    #     title=_('Financial'),
    # )

    # orientation_label = schema.TextLine(
    #     title=_('Orientation'),
    # )

    # travelDocuments_label = schema.TextLine(
    #     title=_('Travel Documents'),
    # )

    # flight_label = schema.TextLine(
    #     title=_('Flight'),
    # )

    # flightDeparture_label = schema.TextLine(
    #     title=_('Departure Flight'),
    #     # TODO appears if "Application for Permission to follow an Alternative  # noqa : E501
    #     #   Schedule on the Outbound Flight Only or on my Roundtrip Flights"
    #     #   is "yes" in the MGMT PORTAL AND one of the following selections has  # noqa : E501
    #     #   been made above:  --I will apply for permission to fly to my
    #     #   program site on an alternative flight but will return from my
    #     #   program site with the group.  --I will apply for permission to fly  # noqa : E501
    #     #   to and from my program site on an alternative flight.  OR
    #     #   appears if "Application for Permission to follow an Alternative
    #     #   Schedule on the Outbound Flight Only or on my Roundtrip Flights"
    #     #   is "yes" in the MGMT PORTAL AND "Program Dates" selection is one
    #     #   of the following:  --I will apply for permission to arrive at my
    #     #   program site on an alternative date but will depart from my
    #     #   program site on the official program date.  --I will apply for
    #     #   permission to arrive at and depart from my program site on
    #     #   alternative dates. OR  appears if "Program Type" in MGMT PORTAL
    #     #   does NOT begin with "group..."
    # )

    # flightReturn_label = schema.TextLine(
    #     title=_('Return Flight'),
    #     # TODO appears if "Application for Permission to follow an Alternative  # noqa : E501
    #     #   Schedule on the Return Flight Only" is "yes" or if "Application for  # noqa : E501
    #     #   Permission to follow an Alternative Schedule on the Outbound Flight  # noqa : E501
    #     #   Only or on my Roundtrip Flights" is "yes"in the MGMT PO
    # )

    #######################################################
    # model.fieldset(
    #     'programChanges',
    #     label=_('Program Changes'),
    #     fields=['programChanges_label', 'agreements_label',
    #             'nonSponsoredTravel_label'],
    # )

    # programChanges_label = schema.TextLine(
    #     title=_('Program Changes'),
    #     description=_('Please review information provided to you by the OIE carefully and contact the OIE with questions, if needed, prior to making your decision.'),  # noqa : E501
    # )

    # agreements_label = schema.TextLine(
    #     title=_('Agreements'),
    #     description=_('Please review information provided to you by the OIE carefully and contact the OIE with questions, if needed, prior to making your decision.'),  # noqa : E501
    # )

    # nonSponsoredTravel_label = schema.TextLine(
    #     title=_('Non-sponsored Out-of-Country (or out-of-state) Travel'),
    # )
