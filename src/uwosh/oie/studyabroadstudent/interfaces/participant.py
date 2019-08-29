# -*- coding: utf-8 -*-

# IOIEStudyAbroadParticipant: the new content type for participant applications

from collective import dexteritytextindexer
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.directives import form
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile import field
from plone.namedfile.file import NamedFile
from plone.supermodel import model
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import contactrelationship
from uwosh.oie.studyabroadstudent.vocabularies import departure_mode_transportation_vocabulary  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import departure_transfer_vocabulary  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import graduation_month_vocabulary  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from uwosh.oie.studyabroadstudent.vocabularies import return_mode_transportation_vocabulary  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import return_transfer_vocabulary  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import socialmediaservice
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_vocabulary
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
        'oiestudyabroadstudent.state_of_wisconsin_need_based_travel_grant_form',  # noqa
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
            '<em>The Wisconsin need based travel grant form has not yet been specified by an administrator</em>',  # noqa
            'text/html',
            'text/html',
        )


def get_url_special_student_form_for_undergraduate_admissions_form():
    form = api.portal.get_registry_record(
        'oiestudyabroadstudent.special_student_form_for_undergraduate_admissions',  # noqa
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
            '<em>The special student form for undergraduate admissions has not yet been specified by an administrator</em>',  # noqa
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
            '<em>The disciplinary clearance form has not yet been specified by an administrator</em>',  # noqa
            'text/html',
            'text/html',
        )


class IOIEStudyAbroadParticipant(Interface):
    dexteritytextindexer.searchable('title')
    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        readonly=True,
        default=_(u'will be auto-generated'),
    )

    dexteritytextindexer.searchable('firstName')
    firstName = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    dexteritytextindexer.searchable('middleName')
    middleName = schema.TextLine(
        title=_(u'Middle Name'),
        required=False,
    )

    dexteritytextindexer.searchable('lastName')
    lastName = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )

    #######################################################
    model.fieldset(
        'progress',
        label=_(u'Progress'),
        fields=['seatNumber', 'waitlistNumber'],
    )

    seatNumber = schema.TextLine(
        title=_(u'Seat Number'),
        required=False,
    )

    waitlistNumber = schema.TextLine(
        title=_(u'Waitlist Number'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'interest',
        label=_(u'Express Interest'),
        fields=['email', 'programName', 'programName2', 'programName3'],
    )

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email Address'),
        description=_(
            u'UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.'),  # noqa
        required=True,
        constraint=validate_email,
    )

    dexteritytextindexer.searchable('programName')
    programName = schema.Choice(
        title=_(u'Program Name (first choice)'),
        description=_(u'The courses listed for this program choice will appear in your Courses tab; you must indicate there which courses you wish to enroll in.'),  # noqa
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=True,
    )

    dexteritytextindexer.searchable('programName2')
    programName2 = schema.Choice(
        title=_(u'Program Name (second choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    dexteritytextindexer.searchable('programName3')
    programName3 = schema.Choice(
        title=_(u'Program Name (third choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    #######################################################
    model.fieldset(
        'step1',
        label=_(u'Step 1'),
        fields=['studentID'],
    )

    dexteritytextindexer.searchable('studentID')
    studentID = schema.TextLine(
        title=_(u'UW Oshkosh Student ID'),
        description=_(u'Do not include the initial "W" in the UW Oshkosh ID.  If you do not have a UW Oshkosh ID (current or past), leave this blank.'),  # noqa
        required=False,
        constraint=validate_student_id,
    )

    #######################################################
    model.fieldset(
        'contact',
        label=_(u'Contact Information'),
        fields=['stepi_label', 'contact_label', 'mainPhone', 'otherPhone',
                'otherContactService', 'otherContactID', 'localAddr',
                'localAddrApt', 'localCity', 'localState', 'localZip',
                'homeAddr1', 'homeAddrApt', 'homeCity', 'homeState',
                'homeZip', 'homeCountry'],
    )

    form.mode(stepi_label='display')
    stepi_label = schema.TextLine(
        title=_(u'STEP I'),
     )

    form.mode(contact_label='display')
    contact_label = schema.TextLine(
        title=_(u'Contact Information'),
    )

    mainPhone = schema.TextLine(
        title=_(u'Main phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        required=True,
    )

    otherPhone = schema.TextLine(
        title=_(u'Other phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        required=False,
    )

    otherContactService = schema.Choice(
        title=_(u'Other Contact Service'),
        description=_(u'Select the service you use most often, or leave blank if you don\'t use any of these services.'),  # noqa
        required=False,
        vocabulary=socialmediaservice,
    )

    otherContactID = schema.TextLine(
        title=_(u'Other contact service username or ID'),
        description=_(u'Enter your username or ID for the service you chose above, or leave blank if you did not select a service above.'),  # noqa
        required=False,
    )

    localAddr = schema.TextLine(
        title=_(u'Local Address: Street'),
        required=True,
    )

    localAddrApt = schema.TextLine(
        title=_(u'Local Address: Apartment Number'),
        required=False,
    )

    localCity = schema.TextLine(
        title=_(u'Local Address: City'),
        required=True,
    )

    localState = schema.TextLine(
        title=_(u'Local Address: State'),
        default=_(u'WI'),
        required=True,
    )

    localZip = schema.TextLine(
        title=_(u'Local Address: Zip Code'),
        default=_(u'54901'),
        required=True,
    )

    homeAddr1 = schema.TextLine(
        title=_(u'Home Address: Street'),
        required=True,
    )

    homeAddrApt = schema.TextLine(
        title=_(u'Home Address: Apartment Number'),
        required=False,
    )

    homeCity = schema.TextLine(
        title=_(u'Home Address: City'),
        description=_(u''),
        required=True,
    )

    homeState = schema.TextLine(
        title=_(u'Home Address: State/Province/Department'),
        description=_(u''),
        required=True,
    )

    homeZip = schema.TextLine(
        title=_(u'Home Address: Zip or Postal Code'),
        description=_(u''),
        required=True,
    )

    homeCountry = schema.Choice(
        title=_(u'Home Address: Country'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
    )

    #######################################################
    model.fieldset(
        'emergency_contact',
        label=_(u'Emergency Contact'),
        fields=['emergencyContacts_label', 'emerg1fullname',
                'emerg1relationship', 'emerg1mail_personal',
                'emerg1mail_work', 'emerg1phone_main', 'emerg1phone_other',
                'emerg2fullname', 'emerg2relationship', 'emerg2mail_personal',
                'emerg2mail_work', 'emerg2phone_main', 'emerg2phone_other',
                'emerg3fullname', 'emerg3relationship', 'emerg3mail_personal',
                'emerg3mail_work', 'emerg3phone_main', 'emerg3phone_other',
                'emerg4fullname', 'emerg4relationship', 'emerg4mail_personal',
                'emerg4mail_work', 'emerg4phone_main', 'emerg4phone_other'],
    )

    form.mode(emergencyContacts_label='display')
    emergencyContacts_label = schema.TextLine(
        title=_(u'Emergency Contact(s)'),
        required=False,
    )

    emerg1fullname = schema.TextLine(
        title=_(u'1 Full Name'),
        #        required=True,
        required=False,
    )

    emerg1relationship = schema.Choice(
        title=_(u'1 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg1mail_personal = schema.TextLine(
        title=_(u'1 Main Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1mail_work = schema.TextLine(
        title=_(u'1 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1phone_main = schema.TextLine(
        title=_(u'1 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    emerg1phone_other = schema.TextLine(
        title=_(u'1 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    ###############

    emerg2fullname = schema.TextLine(
        title=_(u'2 Full Name'),
        #        required=True,
        required=False,
    )

    emerg2relationship = schema.Choice(
        title=_(u'2 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg2mail_personal = schema.TextLine(
        title=_(u'2 Main Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mail_work = schema.TextLine(
        title=_(u'2 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2phone_main = schema.TextLine(
        title=_(u'2 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    emerg2phone_other = schema.TextLine(
        title=_(u'2 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    #############

    emerg3fullname = schema.TextLine(
        title=_(u'3 Full Name'),
        #        required=True,
        required=False,
    )

    emerg3relationship = schema.Choice(
        title=_(u'3 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg3mail_personal = schema.TextLine(
        title=_(u'3 Main Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mail_work = schema.TextLine(
        title=_(u'3 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3phone_main = schema.TextLine(
        title=_(u'3 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    emerg3phone_other = schema.TextLine(
        title=_(u'3 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    #############

    emerg4fullname = schema.TextLine(
        title=_(u'4 Full Name'),
        #        required=True,
        required=False,
    )

    emerg4relationship = schema.Choice(
        title=_(u'4 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg4mail_personal = schema.TextLine(
        title=_(u'4 Main Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4mail_work = schema.TextLine(
        title=_(u'4 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),  # noqa
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4phone_main = schema.TextLine(
        title=_(u'4 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    emerg4phone_other = schema.TextLine(
        title=_(u'4 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),  # noqa
        #        required=True,
        required=False,
    )

    #######################################################
    model.fieldset(
        'demographics',
        label=_(u'Demographics'),
        fields=['demographics_label', 'ethnicity', 'ethnicityOther',
                'stateResidency', 'countrycitizenship',
                'immigrationStatus', 'countryBirth', 'dateOfBirth'],
    )

    form.mode(demographic_label='display')
    demographics_label = schema.TextLine(
        title=_(u'Demographics'),
    )

    ethnicity = schema.Choice(
        title=_(u'Ethnicity'),
        description=_(u''),
        source=RegistryValueVocabulary('oiestudyabroadstudent.ethnicities'),
        required=False,
    )

    ethnicityOther = schema.TextLine(
        title=_(u'Ethnicity: Other'),
        description=_(u'Enter your ethnicity only if you selected "other" above.'),  # noqa
        required=False,
    )

    stateResidency = schema.Choice(
        title=_(u'State of Residency'),
        description=_(u''),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.us_states_territories',
        ),
        required=True,
    )

    countrycitizenship = schema.Choice(
        title=_(u'Country of Citizenship'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    immigrationStatus = schema.Choice(
        title=_(u'Immigration Status'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.immigration_status',
        ),
        required=True,
    )

    countryBirth = schema.Choice(
        title=_(u'Country of Birth'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    dateOfBirth = schema.Date(
        title=_(u'Date of Birth'),
        required=True,
    )

########################################################
    model.fieldset(
        'education',
        label=_(u'Education'),
        fields=['education_label', 'educationLevel', 'universityEnrolledUWO',
                'universityEnrolledOther', 'major1', 'major2', 'minor1',
                'minor2', 'graduationYear', 'graduationMonth'],
    )

    form.mode(education_label='display')
    education_label = schema.TextLine(
        title=_(u'Education'),
    )

    educationLevel = schema.Choice(
        title=_(u'Current Education Level'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.education_level',
        ),
        required=False,
    )

    universityEnrolledUWO = schema.Choice(
        title=_(u'Are you enrolled at UW Oshkosh?'),
        description=_(u''),
        required=True,
        vocabulary=yes_no_vocabulary,
    )

    universityEnrolledOther = schema.TextLine(
        title=_(u'If "School" is "OTHER"'),
        description=_(u'Type the official name of the school you are attending now only if you chose "other" above.'),  # noqa
        required=False,
    )

    major1 = schema.Choice(
        title=_(u'First Major'),
        description=_(u'This must match the intended major on your STAR report.'),  # noqa
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    major2 = schema.Choice(
        title=_(u'Second Major'),
        description=_(u'This must match the intended major on your STAR report.  If you don\'t have a second major, leave this blank.'),  # noqa
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    minor1 = schema.TextLine(
        title=_(u'First Minor'),
        description=_(u'This must match the intended minor on your STAR report.  If you don\'t have a minor, leave this blank.'),  # noqa
        required=False,
    )

    minor2 = schema.TextLine(
        title=_(u'Second Minor'),
        description=_(u'This must match the intended minor on your STAR report.  If you don\'t have a minor, leave this blank.'),  # noqa
        required=False,
    )

    graduationYear = schema.Int(
        title=_(u'Graduation: Anticipated Year'),
        description=_(u'Enter the full 4-digit year.'),
        min=2018,
        max=2100,
        required=False,
    )

    graduationMonth = schema.Choice(
        title=_(u'Graduation: Anticipated Month'),
        description=_(u'Select the month that corresponds to your official graduation date.'),  # noqa
        vocabulary=graduation_month_vocabulary,
        required=False,
    )

    #######################################################
    model.fieldset(
        'courses',
        label=_(u'Courses'),
        fields=['courses_label', 'courses'],
    )

    form.mode(courses_label='display')
    courses_label = schema.TextLine(
        title=_(u'Study Away Courses'),
    )

    courses = schema.List(
        title=_(u'Course Selection'),
        description=_(u'Request enrollment in study away courses.  Your selection must match advertised course options.'),  # noqa
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.course_subject_and_number',
            ),
        ),
    )

    #######################################################
    model.fieldset(
        'date',
        label=_(u'Dates'),
        fields=['dates_label', 'interviewDate', 'prePostTravelClassDates',
                'orientationDeadline', 'paymentDeadlines',
                'programDepartureDate', 'airportTransferDeparture',
                'departureModeOfTransportation', 'programReturnDate',
                'returnModeOfTransportation', 'airportTransferReturn',
                'requestToDeviateFromProgramDates'],
    )

    form.mode(dates_label='display')
    dates_label = schema.TextLine(
        title=_(u'Dates'),
    )

    interviewDate = schema.Date(
        title=_(u'Interview Date'),
        description=_(
            u'Contact the Program Liaison to schedule an interview.  Make your interview appointment and type your interview date here prior to submiting this application.  The actual interview date may or may not need to occur prior to the STEP II application deadline.  This will be determined by the Program Liaison.'),  # noqa
        required=False,
    )

    prePostTravelClassDates = schema.Choice(
        title=_(u'Confirm Attendance at Pre- & Post-travel Program-specific Sessions'),  # noqa
        description=_(
            u'Select ''Yes'' to confirm that you will attend all advertised pre- or post-travel sessions.  Select ''No'' if you have a conflict on one or more dates.'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=True,
        # TODO insert date from program object; Displays only if there are dates in "Pretravel Class & Orientation Dates" or "Post-travel Class Dates" in the MGMT PORTAL.  # noqa
    )

    orientationDeadline = schema.Choice(
        title=_(u'Orientation Submission Deadline'),
        description=_(
            u'I understand that the Office of International Education deadline for submission of orientation materials is a final deadline.  I understand and agree that all Office of International Education orientation requirements must be completed by this date.  If I forsee conflicts with this date, I will complete requirements in advance of this date.  If not completed by this date, I understand and agree that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply.'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=True,
    )

    paymentDeadlines = schema.Choice(
        title=_(u'Payment Deadlines'),
        description=_(
            u'I understand that the payment deadlines are final deadlines and that it is my responsibility to record these dates in my calendar.  I understand that all payments must be made in full by the deadlines, or I must submit the "Notice of Financial Aid Award for Study Abroad/Away" form if making my payments using financial aid, a scholarship that I have already received, veterans benefits or an outside loan.  If not submitted by this date, I understand that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply.'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=True,
    )

    programDepartureDate = schema.Date(
        title=_(u'Program Departure Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),  # noqa
        required=False,
        # TODO insert date from program object when in transfer provided state  # noqa
    )

    airportTransferDeparture = schema.Choice(
        title=_(u'Confirm Departure from Oshkosh (or alternative city)'),
        description=_(u''),
        vocabulary=departure_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected  # noqa
        #  on the "program workflow"
    )

    departureModeOfTransportation = schema.Choice(
        title=_(u'Confirm Flight'),
        description=_(u''),
        vocabulary=departure_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected  # noqa
        #  on the "program workflow"
    )

    programReturnDate = schema.Date(
        title=_(u'Program Return Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),  # noqa
        required=False,
        # TODO insert date from program object when in transfer provided state  # noqa
    )

    returnModeOfTransportation = schema.Choice(
        title=_(u'Return-Mode of Transportation'),
        description=_(u'Choose one'),
        vocabulary=return_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected  # noqa
        #  on the "program workflow"
    )

    airportTransferReturn = schema.Choice(
        title=_(u'Confirm Return to Oshkosh (or alternative city)'),
        description=_(u''),
        vocabulary=return_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected  # noqa
        #  on the "program workflow"
    )

    requestToDeviateFromProgramDates = schema.Choice(
        title=_(u'Request to Deviate from Program Dates'),
        description=_(u'Select ''Yes'' once you have printed, read, signed and uploaded this PDF'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO need link to the PDF document  # noqa
        # currently 'https://www.uwosh.edu/oie/away/documents/deviationletter.pdf/view'  # noqa
    )

    #######################################################
    model.fieldset(
        'financial_aid',
        label=_(u'Financial Aid'),
        fields=['financialAid_label'],
    )

    form.mode(financialAid_label='display')
    financialAid_label = schema.TextLine(
        title=_(u'Financial Aid'),
    )

    #######################################################
    model.fieldset(
        'shortanswerquestions',
        label=_(u'Short Answer Questions'),
        fields=['shortAnswer_label', 'applicant_question_text1',
                'applicant_question_answer1', 'applicant_question_text2',
                'applicant_question_answer2', 'applicant_question_text3',
                'applicant_question_answer3', 'applicant_question_text4',
                'applicant_question_answer4', 'applicant_question_text5',
                'applicant_question_answer5'],
    )

    form.mode(shortAnswer_label='display')
    shortAnswer_label = schema.TextLine(
        title=_(u'Short Answer Questions'),
        description=_(u'Answer these questions thoroughly and carefully.  Your response may be used in the application selection process (for competitive programs) or to inform your Program Leaders.  If you will need more than 10 minutes to compose your answers, it is highly recommended that you type your answers outside of this system (e.g. in Word) and then copy and paste them into this system.'),  # noqa
    )

    form.mode(applicant_question_text1='display')
    applicant_question_text1 = schema.Text(
        title=u'Applicant Question 1',
        description=u'',
        default=u'If this help text appears, you may skip this question. This program does not require a response.',  # noqa
        required=False,
    )

    applicant_question_answer1 = schema.Text(
        title=u'Answer 1',
        description=u'If a question appears under Applicant Question 1 above, type your response here.',  # noqa
        required=False,
    )

    form.mode(applicant_question_text2='display')
    applicant_question_text2 = schema.Text(
        title=u'Applicant Question 2',
        description=u'',
        default=u'If this help text appears, you may skip this question. This program does not require a response.',  # noqa
        required=False,
    )

    applicant_question_answer2 = schema.Text(
        title=u'Answer 2',
        description=u'If a question appears under Applicant Question 2 above, type your response here.',  # noqa
        required=False,
    )

    form.mode(applicant_question_text3='display')
    applicant_question_text3 = schema.Text(
        title=u'Applicant Question 3',
        description=u'',
        default=u'If this help text appears, you may skip this question. This program does not require a response.',  # noqa
        required=False,
    )
    applicant_question_answer3 = schema.Text(
        title=u'Answer 3',
        description=u'If a question appears under Applicant Question 3 above, type your response here.',  # noqa
        required=False,
    )

    form.mode(applicant_question_text4='display')
    applicant_question_text4 = schema.Text(
        title=u'Applicant Question 4',
        description=u'',
        default=u'If this help text appears, you may skip this question. This program does not require a response.',  # noqa
        required=False,
    )

    applicant_question_answer4 = schema.Text(
        title=u'Answer 4',
        description=u'If a question appears under Applicant Question 4 above, type your response here.',  # noqa
        required=False,
    )
    form.mode(applicant_question_text5='display')
    applicant_question_text5 = schema.Text(
        title=u'Applicant Question 5',
        description=u'',
        default=u'If this help text appears, you may skip this question. This program does not require a response.',  # noqa
        required=False,
    )

    applicant_question_answer5 = schema.Text(
        title=u'Answer 5',
        description=u'If a question appears under Applicant Question 5 above, type your response here.',  # noqa
        required=False,
    )
    #######################################################
    model.fieldset(
        'background',
        label=_(u'Background'),
        fields=['background_label'],
    )

    form.mode(background_label='display')
    background_label = schema.TextLine(
        title=_(u'Criminal Background Check'),
        description=_(u'If you are required to apply for advance permission (a visa) to enter one or more of your host countries, your visa application may require you to disclose citations, convictions and/or arrests in a criminal record.'),  # noqa
    )

    #######################################################
    model.fieldset(
        'release',
        label=_(u'Release'),
        fields=['release_label', 'UWOshkoshRelease', 'certification'],
    )

    form.mode(release_label='display')
    release_label = schema.TextLine(
        title=_(u'Release'),
    )

    #######################################################
    model.fieldset(
        'forms',
        label=_(u'STEP II Forms'),
        fields=[
            'stepii_label', 'applicationFeeOK',
            'disciplinary_clearance_form_link',
            'disciplinary_clearance_form_uploaded_file',
            'specialStudentFormOK',
            'state_of_wisconsin_need_based_travel_grant_form_link',
            'state_of_wisconsin_need_based_travel_grant_form_uploaded_file',
            'special_student_form_for_undergraduate_admissions_form_link',
            'special_student_form_for_undergraduate_admissions_uploaded_file',
            'transcriptsOK', 'UWOshkoshStatementOK', 'UWSystemStatementOK',
            'withdrawalRefund', 'cumulativeGPA',
        ],
    )

    form.mode(stepii_label='display')
    stepii_label = schema.TextLine(
        title=_(u'STEP II'),
        description=_(u'To complete STEP II, print relevant documents, clearly print your responses, sign forms by hand where indicated, and follow instructions below.  Signatures cannot be typed.'),  # noqa
    )

    form.mode(disciplinary_clearance_form_link='display')
    disciplinary_clearance_form_link = RichText(
        title=u'Disciplinary Clearance Form',
        description=u'Download this PDF, fill it out, and upload it below',
        required=False,
        defaultFactory=get_url_disciplinary_clearance_form,
    )

    disciplinary_clearance_form_uploaded_file = field.NamedFile(
        title=u'Disciplinary Clearance Form',
        description=u'Upload your filled-out copy of the form',
        required=False,
    )

    form.mode(
        state_of_wisconsin_need_based_travel_grant_form_link='display',
    )
    state_of_wisconsin_need_based_travel_grant_form_link = RichText(
        title=u'State of Wisconsin Need-based Travel Grant Form',
        description=u'Download this PDF, fill it out, and upload it below',
        required=False,
        defaultFactory=get_url_special_student_form,
    )

    state_of_wisconsin_need_based_travel_grant_form_uploaded_file = \
        field.NamedFile(
            title=u'State of Wisconsin Need-based Travel Grant Submission',
            description=u'Upload your completed form.',
            required=False,
        )

    form.mode(
        special_student_form_for_undergraduate_admissions_form_link='display',
    )
    special_student_form_for_undergraduate_admissions_form_link = RichText(
        title=u'Special/Non-degree Registration-Undergraduate Level',
        description=u'Download this form, fill it out, and upload it below.',
        required=False,
        defaultFactory=get_url_special_student_form_for_undergraduate_admissions_form,  # noqa
        # TODO appears when "Special/Non-Degree Registration-Graduate Level"  # noqa
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
            title=u'Special/Non-degree Registration-Undergraduate Level Submission',  # noqa
            description=u'Upload your completed form.',
            required=False,
        )

    cumulativeGPA = schema.Float(
        title=_(u'Cumulative GPA'),
        description=_(u'Type the applicant''s CURRENT CUMULATIVE GPA exactly as it appears on the unofficial transcript.'),  # noqa
        required=False,
    )

    #######################################################
    model.fieldset(
        'stepiiiforms',
        label=_(u'STEP III Forms'),
        fields=['stepiii_label', 'documentation_label',
                'transferCreditForm_link', 'transferCreditSubmission',
                'transferCreditVerified', 'identification_label',
                'travelDocLast', 'travelDocFirst', 'travelDocMiddle',
                'travelDocSex', 'travelDocNumber', 'travelDocExpiration',
                'passportReceipt', 'passportOK',
                'driversLicenseReceipt', 'driversLicenseReceiptVerified',
                'photoPaperOfficial',
                'photoPaperOfficialVerified', 'photoDigitalOfficial',
                'photoDigitalOfficialVerified', 'photoPaper',
                'photoPaperVerified', 'photoDigital', 'photoDigitalVerified',
                'fecop_label', 'fecop_link',
                'fecopSubmission', 'fecopVerified', 'lifestyle_label',
                'isVegetarian', 'smokingPreferred', 'health_label',
                'medicalReadStatement', 'allergies_label', 'allergiesYesNo',
                'foodAllergies',
                'medicalHealthProblems_whatCondition',
                'healthConditions_label', 'medicalHealthProblems_stable',
                'medicalHealthProblems', 'healthConditionsSurgeriesYesNo',
                'healthConditionsSurgeriesDetails',
                'medicalHealthProblems_underCare', 'healthPhysical_label',
                'wheelchair', 'assistiveDevice',
                'assistiveDeviceOnFlight', 'assistiveDeviceList',
                'hasDifficultyWalking', 'maxWalkingDistance', 'stairsMax',
                'walkingClimbingDescription', 'sight',
                'healthPhysicalAdditionalInfoYesNo', 'additionalNeeds',
                'medications_label', 'medicalHealthProblems_takenMedication',
                'medicalHealthProblems_willingToPrescribe',
                'medicalHealthProblems_medications', 'medicationsStorage',
                'authorizedAccommodation_label',
                'medicalRegistered', 'medicalRegistered_office',
                'medicalRegistered_accommodations',
                'medicalHealthProblems_additionalInfo',
                'healthConfirmation_label',
                'medicalMentalProblems_enoughMedication',
                'medicalMentalProblems_stable', 'medicalAccessOK',
                'healthMeetingNotes', 'roommate_label', 'roommateName1',
                'roommateName2'],
    )

    form.mode(stepiii_label='display')
    stepiii_label = schema.TextLine(
        title=_(u'STEP III'),
    )

    form.mode(documentation_label='display')
    documentation_label = schema.TextLine(
        title=_(u'Documentation'),
    )

    form.mode(identification_label='display')
    identification_label = schema.TextLine(
        title=_(u'Identification'),
        description=_(u'Complete the following using information from your unexpired passport (required for international travel) or with your unexpired driver\'s license (for domestic travel only).'),  # noqa
    )

    form.mode(fecop_label='display')
    fecop_label = schema.TextLine(
        title=_(u'Financial'),
    )

    form.mode(lifestyle_label='display')
    lifestyle_label = schema.TextLine(
        title=_(u'Lifestyle'),
    )

    form.mode(health_label='display')
    health_label = schema.TextLine(
        title=_(u'Health'),
    )

    form.mode(allergies_label='display')
    allergies_label = schema.TextLine(
        title=_(u'Allergies'),
    )

    form.mode(healthConditions_label='display')
    healthConditions_label = schema.TextLine(
        title=_(u'Health Conditions & Surgeries'),
    )

    form.mode(healthPhysical_label='display')
    healthPhysical_label = schema.TextLine(
        title=_(u'Physical & Mental Health'),
    )

    form.mode(medications_label='display')
    medications_label = schema.TextLine(
        title=_(u'Medications'),
    )

    form.mode(authorizedAccommodation_label='display')
    authorizedAccommodation_label = schema.TextLine(
        title=_(u'Authorized Accommodation'),
    )

    form.mode(healthConfirmation_label='display')
    healthConfirmation_label = schema.TextLine(
        title=_(u'I understand and agree'),
    )

    form.mode(roommate_label='display')
    roommate_label = schema.TextLine(
        title=_(u'Roommate'),
        description=_(u'If you are not traveling with a UW Oshkosh student group, do not list a roommate choice.  If you are traveling on a group program, list your first and second choice roommates here.  Any roommate you request must list you on his/her application in return.'),  # noqa
    )

    #######################################################
    model.fieldset(
        'stepivforms',
        label=_(u'STEP IV Forms'),
        fields=['stepiv_label', 'enrollment_label', 'cbc_label',
                'financial_label', 'depositOnTime', 'payment2OnTime',
                'orientation_label', 'attendedOrientation',
                'travelDocuments_label', 'flight_label',
                'flightDeparture_label', 'flightReturn_label'],
    )

    form.mode(stepiv_label='display')
    stepiv_label = schema.TextLine(
        title=_(u'STEP IV'),
    )

    form.mode(enrollment_label='display')
    enrollment_label = schema.TextLine(
        title=_(u'Course Enrollment'),
    )

    form.mode(financial_label='display')
    financial_label = schema.TextLine(
        title=_(u'Financial'),
    )

    form.mode(orientation_label='display')
    orientation_label = schema.TextLine(
        title=_(u'Orientation'),
    )

    form.mode(travelDocuments_label='display')
    travelDocuments_label = schema.TextLine(
        title=_(u'Travel Documents'),
    )

    form.mode(flight_label='display')
    flight_label = schema.TextLine(
        title=_(u'Flight'),
    )

    form.mode(flightDeparture_label='display')
    flightDeparture_label = schema.TextLine(
        title=_(u'Departure Flight'),
        # TODO appears if "Application for Permission to follow an Alternative  # noqa
        #   Schedule on the Outbound Flight Only or on my Roundtrip Flights"
        #   is "yes" in the MGMT PORTAL AND one of the following selections has
        #   been made above:  --I will apply for permission to fly to my
        #   program site on an alternative flight but will return from my
        #   program site with the group.  --I will apply for permission to fly
        #   to and from my program site on an alternative flight.  OR
        #   appears if "Application for Permission to follow an Alternative
        #   Schedule on the Outbound Flight Only or on my Roundtrip Flights"
        #   is "yes" in the MGMT PORTAL AND "Program Dates" selection is one
        #   of the following:  --I will apply for permission to arrive at my
        #   program site on an alternative date but will depart from my
        #   program site on the official program date.  --I will apply for
        #   permission to arrive at and depart from my program site on
        #   alternative dates. OR  appears if "Program Type" in MGMT PORTAL
        #   does NOT begin with "group..."
    )

    form.mode(flightReturn_label='display')
    flightReturn_label = schema.TextLine(
        title=_(u'Return Flight'),
        # TODO appears if "Application for Permission to follow an Alternative  # noqa
        #   Schedule on the Return Flight Only" is "yes" or if "Application for
        #   Permission to follow an Alternative Schedule on the Outbound Flight
        #   Only or on my Roundtrip Flights" is "yes"in the MGMT PO
    )

    #######################################################
    model.fieldset(
        'programChanges',
        label=_(u'Program Changes'),
        fields=['programChanges_label', 'agreements_label',
                'nonSponsoredTravel_label'],
    )

    form.mode(programChanges_label='display')
    programChanges_label = schema.TextLine(
        title=_(u'Program Changes'),
        description=_(u'Please review information provided to you by the OIE carefully and contact the OIE with questions, if needed, prior to making your decision.'),  # noqa
    )

    form.mode(agreements_label='display')
    agreements_label = schema.TextLine(
        title=_(u'Agreements'),
        description=_(u'Please review information provided to you by the OIE carefully and contact the OIE with questions, if needed, prior to making your decision.'),  # noqa
    )

    form.mode(nonSponsoredTravel_label='display')
    nonSponsoredTravel_label = schema.TextLine(
        title=_(u'Non-sponsored Out-of-Country (or out-of-state) Travel'),
    )
