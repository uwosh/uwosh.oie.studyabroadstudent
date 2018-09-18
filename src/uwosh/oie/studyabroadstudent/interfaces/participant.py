# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from plone.supermodel import model
from plone.namedfile import field
from plone.app.textfield import RichText
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, \
    socialmediaservice, contactrelationship, graduation_month_vocabulary, return_transfer_vocabulary, \
    return_mode_transportation_vocabulary, departure_mode_transportation_vocabulary, departure_transfer_vocabulary, \
    RegistryValueVocabulary
from collective import dexteritytextindexer
from plone.directives import form
from Products.CMFPlone.RegistrationTool import checkEmailAddress, EmailAddressInvalid
from zope.schema import ValidationError
import re
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedFile


class InvalidEmailAddress(ValidationError):
    "Invalid email address"


class InvalidStudentID(ValidationError):
    "Invalid UW Oshkosh student ID format"


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
    form = api.portal.get_registry_record('oiestudyabroadstudent.state_of_wisconsin_need_based_travel_grant_form')
    filename, data = b64decode_file(form)
    file = NamedFile(data=data, filename=filename)
    url = "data:%s;base64, %s" % (file.contentType, file.data.encode('base64'))
    html = '<a target="_blank" href="%s">Download this form</a>' % url
    return RichTextValue(html, 'text/html', 'text/html')


def get_url_special_student_form_for_undergraduate_admissions_form():
    form = api.portal.get_registry_record('oiestudyabroadstudent.special_student_form_for_undergraduate_admissions')
    filename, data = b64decode_file(form)
    file = NamedFile(data=data, filename=filename)
    url = "data:%s;base64, %s" % (file.contentType, file.data.encode('base64'))
    html = '<a target="_blank" href="%s">Download this form</a>' % url
    return RichTextValue(html, 'text/html', 'text/html')


def get_url_disciplinary_clearance_form():
    form = api.portal.get_registry_record('oiestudyabroadstudent.disciplinary_clearance_form')
    filename, data = b64decode_file(form)
    file = NamedFile(data=data, filename=filename)
    url = "data:%s;base64, %s" % (file.contentType, file.data.encode('base64'))
    html = '<a target="_blank" href="%s">Download this form</a>' % url
    return RichTextValue(html, 'text/html', 'text/html')


class IOIEStudyAbroadParticipant(Interface):
    dexteritytextindexer.searchable('title')
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
        label=_(u"Progress"),
        fields=['seatNumber', 'waitlistNumber']
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
        label=_(u"Express Interest"),
        fields=['email', 'programName', 'programName2', 'programName3']
    )

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email Address'),
        description=_(
            u'UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.'),
        required=True,
        constraint=validate_email,
    )

    dexteritytextindexer.searchable('programName')
    programName = schema.Choice(
        title=_(u'Program Name (first choice)'),
        description=_(u'The courses listed for this program choice will appear in your Courses tab; you must indicate there which courses you wish to enroll in.'),
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
        label=_(u"Step 1"),
        fields=['studentID']
    )

    dexteritytextindexer.searchable('studentID')
    studentID = schema.TextLine(
        title=_(u'UW Oshkosh Student ID'),
        description=_(u'Do not include the initial "W" in the UW Oshkosh ID.  If you do not have a UW Oshkosh ID (current or past), leave this blank.'),
        required=False,
        constraint=validate_student_id,
    )

    #######################################################
    model.fieldset(
        'contact',
        label=_(u"Contact Information"),
        fields=['stepi_label', 'contact_label', 'mainPhone', 'otherPhone', 'otherContactService', 'otherContactID', 'localAddr',
                'localAddrApt', 'localCity', 'localState', 'localZip', 'homeAddr1', 'homeAddrApt',
                'homeCity', 'homeState', 'homeZip', 'homeCountry', ]
    )
    
    form.mode (stepi_label='display')
        stepi_label = schema.TextLine(
        title=_(u'STEP I'),
     )

    form.mode (contact_label='display')
        contact_label = schema.TextLine(
        title=_(u'Contact Information'),
    )

    mainPhone = schema.TextLine(
        title=_(u'Main phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
        required=True,
    )

    otherPhone = schema.TextLine(
        title=_(u'Other phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
        required=False,
    )

    otherContactService = schema.Choice(
        title=_(u'Other Contact Service'),
        description=_(u'Select the service you use most often, or leave blank if you don't use any of these services.'),
        required=False,
        vocabulary=socialmediaservice,
    )

    otherContactID = schema.TextLine(
        title=_(u'Other contact service username or ID'),
        description=_(u'Enter your username or ID for the service you chose above, or leave blank if you did not select a service above.'),
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
        label=_(u"Emergency Contact"),
        fields=['emergencyContacts_label', 'emerg1fullname', 'emerg1relationship', 'emerg1mail_personal',
                'emerg1mail_work', 'emerg1phone_main', 'emerg1phone_other',
                'emerg2fullname', 'emerg2relationship', 'emerg2mail_personal',
                'emerg2mail_work', 'emerg2phone_main', 'emerg2phone_other',
                'emerg3fullname', 'emerg3relationship', 'emerg3mail_personal',
                'emerg3mail_work', 'emerg3phone_main', 'emerg3phone_other',
                'emerg4fullname', 'emerg4relationship', 'emerg4mail_personal',
                'emerg4mail_work', 'emerg4phone_main', 'emerg4phone_other',
                ]
    )

    form.mode (emergencyContacts_label='display')
        emergencyContacts_label = schema.TextLine(
        title=_(u'Emergency Contact(s)'),
        required=
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
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1mail_work = schema.TextLine(
        title=_(u'1 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1phone_main = schema.TextLine(
        title=_(u'1 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),
        #        required=True,
        required=False,
    )

    emerg1phone_other = schema.TextLine(
        title=_(u'1 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
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
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mail_work = schema.TextLine(
        title=_(u'2 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2phone_main = schema.TextLine(
        title=_(u'2 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),
        #        required=True,
        required=False,
    )

    emerg2phone_other = schema.TextLine(
        title=_(u'2 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
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
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mail_work = schema.TextLine(
        title=_(u'3 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3phone_main = schema.TextLine(
        title=_(u'3 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),
        #        required=True,
        required=False,
    )

    emerg3phone_other = schema.TextLine(
        title=_(u'3 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
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
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4mail_work = schema.TextLine(
        title=_(u'4 Other Email'),
        description=_(u'Strongly recommended.  By typing in an email address here, you permit the UWO OIE to send non-emergency messages intended to update contacts about significant unanticipated events that have occurred or may occur and which have involved or may involve an increase in program risk.'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4phone_main = schema.TextLine(
        title=_(u'4 Main Phone'),
        description=_(u'Strongly recommended.  Include area code (and country code if the phone does not have a U.S. phone number).'),
        #        required=True,
        required=False,
    )

    emerg4phone_other = schema.TextLine(
        title=_(u'4 Other Phone'),
        description=_(u'Include area code (and country code if the phone does not have a U.S. phone number).'),
        #        required=True,
        required=False,
    )

    #######################################################
    model.fieldset(
        'demographics',
        label=_(u"Demographics"),
        fields=['demographics_label', 'ethnicity', 'ethnicityOther', 'stateResidency', 'countrycitizenship', 'immigrationStatus', 'countryBirth']
    )

    form.mode (demographic_label='display')
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
        description=_(u'Enter your ethnicity only if you selected "other" above.'),
        required=False,
    )

    stateResidency = schema.Choice(
        title=_(u'State of Residency'),
        description=_(u''),
        source=RegistryValueVocabulary('oiestudyabroadstudent.us_states_territories'),
        required=True,
    )

    countrycitizenship = schema.Choice(
        title=_(u'Country of Citizenship'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

    immigrationStatus = schema.Choice(
        title=_(u'Immigration Status'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.immigration_status'),
        required=True,
        # TODO appears only if "Country of Citizenship" is NOT United States
    )

    countryBirth = schema.Choice(
        title=_(u'Country of Birth'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
        required=True,
    )

#     dateOfBirth = schema.Date(
#         title=_(u'Birthday'),
#         required=True,
#     )
        
########################################################
    model.fieldset(
        'education',
        label=_(u"Education"),
        fields=['education_label', 'educationLevel', 'universityEnrolledUWO', 'universityEnrolledOther', 
                'major1', 'major2', 'minor1', 'minor2', 'graduationYear', 'graduationMonth']
    )
        
    form.mode (education_label='display')
        education_label = schema.TextLine(
        title=_(u'Education'),
    )

    educationLevel = schema.Choice(
        title=_(u'Current Education Level'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.education_level'),
        required=False,
        # TODO check vocabulary; If MGMT PORTAL "Student Status" is "1", the answer here cannot be "I am not a student'
    )

    universityEnrolledUWO = schema.Choice(
        title=_(u'Are you enrolled at UW Oshkosh?'),
        description=_(u''),
        required=True,
        vocabulary=yes_no_none_vocabulary,
    )

    universityEnrolledOther = schema.TextLine(
        title=_(u'If "School" is "OTHER"'),
        description=_(u'Type the official name of the school you are attending now only if you chose "other" above.'),
        required=False,
    )

    major1 = schema.Choice(
        title=_(u'First Major'),
        description=_(u'This must match the intended major on your STAR report.'),
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    major2 = schema.Choice(
        title=_(u'Second Major'),
        description=_(u'This must match the intended major on your STAR report.  If you don't have a second major, leave this blank.'),
        required=False,
        source=RegistryValueVocabulary('oiestudyabroadstudent.majors'),
    )

    minor1 = schema.TextLine(
        title=_(u'First Minor'),
        description=_(u'This must match the intended minor on your STAR report.  If you don't have a minor, leave this blank.'),
        required=False,
    )

    minor2 = schema.TextLine(
        title=_(u'Second Minor'),
        description=_(u'This must match the intended minor on your STAR report.  If you don't have a minor, leave this blank.'),
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
        description=_(u'Select the month that corresponds to your official graduation date.'),
        vocabulary=graduation_month_vocabulary,
        required=False,
    )

    #######################################################
    model.fieldset(
        'courses',
        label=_(u"Courses"),
        fields=['courses_label', 'courses']
    )
        
    form.mode (courses_label='display')
    courses_label = schema.TextLine(
        title=_(u'Study Away Courses'),
    )

    courses = schema.List(
        title=_(u'Course Selection'),
        description=_(u'Request enrollment in study away courses.  Your selection must match advertised course options.'),
        value_type=schema.Choice(source=RegistryValueVocabulary('oiestudyabroadstudent.course_subject_and_number'))
    )

    #######################################################
    model.fieldset(
        'date',
        label=_(u"Dates"),
        fields=['dates_label', 'interviewDate', 'prePostTravelClassDates', 'orientationDeadline', 'paymentDeadlines',
                'programDepartureDate', 'airportTransferDeparture', 'departureModeOfTransportation',
                'programReturnDate', 'returnModeOfTransportation', 'airportTransferReturn',
                'requestToDeviateFromProgramDates']
    )
        
    form.mode (dates_label='display')
    dates_label = schema.TextLine(
        title=_(u'Dates'),
    )

    interviewDate = schema.Date(
        title=_(u'Interview Date'),
        description=_(
            u'Contact the Program Liaison to schedule an interview.  Make your interview appointment and type your interview date here prior to submiting this application.  The actual interview date may or may not need to occur prior to the STEP II application deadline.  This will be determined by the Program Liaison.'),
        required=False,
        # TODO Displays only if "interview" is checked "yes" in MGMT PORTAL.
    )

    prePostTravelClassDates = schema.Choice(
        title=_(u'Confirm Attendance at Pre- & Post-travel Program-specific Sessions'),
        description=_(
            u'Select 'Yes' to confirm that you will attend all advertised pre- or post-travel sessions.  Select 'No' if you have a conflict on one or more dates.'),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object; Displays only if there are dates in "Pretravel Class & Orientation Dates" or "Post-travel Class Dates" in the MGMT PORTAL.
    )

    orientationDeadline = schema.Choice(
        title=_(u'Orientation Submission Deadline'),
        description=_(
            u'I understand that the Office of International Education deadline for submission of orientation materials is a final deadline.  I understand and agree that all Office of International Education orientation requirements must be completed by this date.  If I forsee conflicts with this date, I will complete requirements in advance of this date.  If not completed by this date, I understand and agree that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply.'),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object
    )

    paymentDeadlines = schema.Choice(
        title=_(u'Payment Deadlines'),
        description=_(
            u'I understand that the payment deadlines are final deadlines and that it is my responsibility to record these dates in my calendar.  I understand that all payments must be made in full by the deadlines, or I must submit the "Notice of Financial Aid Award for Study Abroad/Away" form if making my payments using financial aid, a scholarship that I have already received, veterans benefits or an outside loan.  If not submitted by this date, I understand that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply.'),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object
    )

    programDepartureDate = schema.Date(
        title=_(u'Program Departure Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # TODO insert date from program object when in transfer provided state
    )

    airportTransferDeparture = schema.Choice(
        title=_(u'Confirm Departure from Oshkosh (or alternative city)'),
        description=_(u''),
        vocabulary=departure_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    departureModeOfTransportation = schema.Choice(
        title=_(u'Confirm Flight'),
        description=_(u''),
        vocabulary=departure_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    programReturnDate = schema.Date(
        title=_(u'Program Return Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # TODO insert date from program object when in transfer provided state
    )

    returnModeOfTransportation = schema.Choice(
        title=_(u'Return-Mode of Transportation'),
        description=_(u'Choose one'),
        vocabulary=return_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    airportTransferReturn = schema.Choice(
        title=_(u'Confirm Return to Oshkosh (or alternative city)'),
        description=_(u''),
        vocabulary=return_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    requestToDeviateFromProgramDates = schema.Choice(
        title=_(u'Request to Deviate from Program Dates'),
        description=_(u'Select ''Yes'' once you have printed, read, signed and uploaded this PDF'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO need link to the PDF document
    )

        #######################################################
    model.fieldset(
        'financial_aid',
        label=_(u"Financial Aid"),
        fields=['financialAid_label']
    )

    form.mode (financialAid_label='display')
    financialAid_label = schema.TextLine(
        title=_(u'Financial Aid'),
    )
        
        #######################################################
    model.fieldset(
        'shortanswerquestions',
        label=_(u"Short Answer Questions"),
        fields=['shortAnswer_label', 'applicant_question_text1', 'applicant_question_answer1', 'applicant_question_text2',
                'applicant_question_answer2', 'applicant_question_text3', 'applicant_question_answer3',
                'applicant_question_text4', 'applicant_question_answer4', 'applicant_question_text5',
                'applicant_question_answer5', ]
    )

    form.mode (shortAnswer_label='display')
    shortAnswer_label = schema.TextLine(
        title=_(u'Short Answer Questions'),
        description=_(u'Answer these questions thoroughly and carefully.  Your response may be used in the application selection process (for competitive programs) or to inform your Program Leaders.  If you will need more than 10 minutes to compose your answers, it is highly recommended that you type your answers outside of this system (e.g. in Word) and then copy and paste them into this system.'), 
    )

    form.mode(applicant_question_text1="display")
    applicant_question_text1 = schema.Text(
        title=u'Applicant Question 1',
        description=u'',
        default=u'Question 1 will appear here after you press Save. If a question does not appear after saving, it is because your study away program does not require a response here.',
        required=False,
    )
    applicant_question_answer1 = schema.Text(
        title=u'Answer 1',
        description=u'If a question appears under Applicant Question 1 above, type your response here.',
        required=False,
    )
    form.mode(applicant_question_text2="display")
    applicant_question_text2 = schema.Text(
        title=u'Applicant Question 2',
        description=u'',
        default=u'Question 2 will appear here after you press Save. If a question does not appear after saving, it is because your study away program does not require a response here.,
        required=False,
    )
    applicant_question_answer2 = schema.Text(
        title=u'Answer 2',
        description=u'If a question appears under Applicant Question 2 above, type your response here.',
        required=False,
    )
    form.mode(applicant_question_text3="display")
    applicant_question_text3 = schema.Text(
        title=u'Applicant Question 3',
        description=u'',
        default=u'Question 3 will appear here after you press Save. If a question does not appear after saving, it is because your study away program does not require a response here.',
        required=False,
    )
    applicant_question_answer3 = schema.Text(
        title=u'Answer 3',
        description=u'If a question appears under Applicant Question 3 above, type your response here.',
        required=False,
    )
    form.mode(applicant_question_text4="display")
    applicant_question_text4 = schema.Text(
        title=u'Applicant Question 4',
        description=u'',
        default=u'Question 4 will appear here after you press Save. If a question does not appear after saving, it is because your study away program does not require a response here.',
        required=False,
    )
    applicant_question_answer4 = schema.Text(
        title=u'Answer 4',
        description=u'If a question appears under Applicant Question 4 above, type your response here.',
        required=False,
    )
    form.mode(applicant_question_text5="display")
    applicant_question_text5 = schema.Text(
        title=u'Applicant Question 5',
        description=u'',
        default=u'Question 5 will appear here after you press Save. If a question does not appear after saving, it is because your study away program does not require a response here.',
        required=False,
    )
    applicant_question_answer5 = schema.Text(
        title=u'Answer 5',
        description=u'If a question appears under Applicant Question 5 above, type your response here.',
        required=False,
    )

    #######################################################
    model.fieldset(
        'forms',
        label=_(u"Forms"),
        fields=['state_of_wisconsin_need_based_travel_grant_form_link',
                'state_of_wisconsin_need_based_travel_grant_form_uploaded_file',
                'special_student_form_for_undergraduate_admissions_form_link',
                'special_student_form_for_undergraduate_admissions_uploaded_file',
                'disciplinary_clearance_form_link',
                'disciplinary_clearance_form_uploaded_file', 'cumulativeGPA']
    )
    form.mode(state_of_wisconsin_need_based_travel_grant_form_link="display")
    state_of_wisconsin_need_based_travel_grant_form_link = RichText(
        title=u'State of Wisconsin Need-based Travel Grant Form',
        description=u'Download this PDF, fill it out, and upload it below',
        required=False,
        defaultFactory=get_url_special_student_form,
    )
    state_of_wisconsin_need_based_travel_grant_form_uploaded_file = field.NamedFile(
        title=u'State of Wisconsin Need-based Travel Grant Submission',
        description=u'Upload your completed form.',
        required=False,
    )
    form.mode(special_student_form_for_undergraduate_admissions_form_link="display")
    special_student_form_for_undergraduate_admissions_form_link = RichText(
        title=u'Special/Non-degree Registration-Undergraduate Level',
        description=u'Download this form, fill it out, and upload it below.',
        required=False,
        defaultFactory=get_url_special_student_form_for_undergraduate_admissions_form,
        # TODO appears when "Special/Non-Degree Registration-Graduate Level" is checked "yes" in the MGMT PORTAL
        AND
        "Current Education Level" is NOT "graduate school" 
        AND
        the course request in the PART PORTAL includes at least one course numbered 500-799.

        OR

        appears when "Special/Non-Degree Registration-Graduate Level" is checked "yes" in the MGMT PORTAL
        AND
        "Current Education Level" IS "graduate school" 
        AND
        the course request in the PART PORTAL includes at least one course numbered 100-499.
    )
    special_student_form_for_undergraduate_admissions_uploaded_file = field.NamedFile(
        title=u'Special/Non-degree Registration-Undergraduate Level Submission',
        description=u'Upload your completed form.',
        required=False,
    )
    form.mode(disciplinary_clearance_form_link="display")
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
    cumulativeGPA = schema.Float(
        title=_(u'Cumulative GPA'),
        description=_(u'Type the applicant's CURRENT CUMULATIVE GPA exactly as it appears on the unofficial transcript.'),
        required=False,
    )

    #######################################################
    form.mode (lifestyle_label='display')
    lifestyle_label = schema.TextLine(
        title=_(u'Lifestyle'),
    )
        
food = schema.Choice(
description=_(u'When offered a choice, I prefer food that is (check all that apply):'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
# TODO vegetarian, vegan, gluten free, dairy free OR no preference
)
#     isVegetarian = schema.Choice(
#         title=_(u'Are you vegetarian?'),
#         vocabulary=yes_no_none_vocabulary,
#         #default="No",
# #        required=True,
#         required=False,
#     )
#
#     smokingPreferred = schema.Choice(
#         title=_(u'Smoking Preference'),
#         vocabulary=smoking_vocabulary,
#         default= 'No Preference',
#         required=False,
#     )
#
    form.mode (health_label='display')
    health_label = schema.TextLine(
        title=_(u'Health'),
    )
#     medicalReadStatement = schema.Choice(
#         title=_(u''),
#         description=_(u'I understand that failure to disclose medical or mental health conditions may inhibit or prohibit staff from planning for my participation or assisting me in an emergency and may inhibit or prohibit program leaders, hosts and/or host families from meeting my needs.  It may also cause health professionals abroad/away to take actions that could lead to serious medical consequences, including death.'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
    form.mode (allergies_label='display')
    allergies_label = schema.TextLine(
        title=_(u'Allergies'),
    )
allergiesYesNo = schema.Choice(
description=_(u'I have allergies.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
#     foodAllergies = schema.TextLine(
#         title=_(u''),
#         description=_(u'List all allergies.'),
#         required=False,
#     )
#
allergiesExplain = schema.TextLine(
description=_(u'Explain your medical condition when ingesting or coming into contact with substances that cause an allergic reaction.  How do you avoid having an allergic reaction?  When having a reaction, what treatment do you use?'), 
required=False,
)
    form.mode (healthConditions_label='display')
    healthConditions_label = schema.TextLine(
        title=_(u'Health Conditions & Surgeries'),
    )
healthConditionsYesNo = schema.Choice(
description=_(u'I have one or more current, continuing or recurring physical health and/or mental health conditions, a physical disability (disabilities) and/or medical condition (conditions).'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
#     medicalHealthProblems = schema.Text(
#         title=_(u''),
#         description=_(u'Include all current, continuing or recurring health and/or mental health conditions, including physical disabilities and/or medical conditions and mental health conditions such as anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc.'),
#         required=False,
#     )
#
healthConditionsSurgeriesYesNo = schema.Choice(
description=_(u'I have undergone surgeries that affect my physical health today.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
healthConditionsSurgeriesDetails = chart
description=_(u'Include all surgeries that affect your physical health today.'), 
required=False,
# TODO conditions should be listed in a chart, with columns: Condition Treated, Surgery Date, Healthcare Provider, Recovery Status
)
#     medicalHealthProblems_underCare = schema.Choice(
#         title=_(u''),
            description=_(u'I am currently under the care of a doctor, psychiatrist, substance abuse counselor, mental health professional or other health care professional for conditions listed above.'), 
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
    form.mode (healthPhysical_label='display')
    healthPhysical_label = schema.TextLine(
        title=_(u'Physical Health'),
    )
wheelchair = schema.Choice(
description=_(u'I use a wheelchair, prosthetic or other assistive device.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
assistiveDevice = schema.TextLine(
description=_(u'List the assistive device (devices) that you plan to use while on your program.'), 
required=False,
)
assistiveDeviceOnFlight = schema.Choice(
description=_(u'I will (or I might) bring a medical or mental health-related device onto the airplane (e.g. CPAP machine).'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
assistiveDeviceList = schema.TextLine(
description=_(u'If yes, list the device or devices here.'), 
required=False,
)

#     hasDifficultyWalking = schema.Choice(
#         title=_(u''),
#         description=_(u'It is difficult for me to walk long distances, climb stairs, walk up inclines or down declines, or walk at high altitudes, in heat, in cold or in humidity.'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     maxWalkingDistance = schema.TextLine(
# #    maxWalkingDistance = schema.Int(
#         title=_(u''),
#         description=_(u'If yes, what is the maximum number of minutes you can walk?'),
#         required=False,
#     )
#
stairsMax = schema.Int(
description=_(u'If yes, what is the maximum number of stairs you can climb?'), 
required=False,
)
walkingClimbingDescription = schema.TextLine(
description=_(u'If yes, describe your ability to walk up inclines or down declines, or walk at high altitudes, in heat, in cold or in humidity.'), 
required=False,
)
sight = schema.Choice(
description=_(u'My sight is impaired beyond correction.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
healthPhysicalAdditionalInfoYesNo = schema.Choice(
description=_(u'I would like to share additional information related to my physical or mental health that may be helpful for program organizers, liaisons and/or host families.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
healthPhysicalAdditionalInfo = schema.TextLine(
description=_(u'Share any additional information related to your physical or mental health that may be helpful for program organizers, liaisons and/or host families.'), 
required=False,
)
    form.mode (medications_label='display')
    medications_label = schema.TextLine(
        title=_(u'Medications'),
    )
prescriptionsYesNo = schema.Choice(
description=_(u'I have taken one or more prescription medications in the past three years.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
prescriptionsCarry = schema.Choice(
description=_(u'I will carry over-the-counter medications containing amphetamines when I travel.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
prescriptionsList = chart
description=_(u'Include all prescription medications you have taken in the past three years whether or not you intend to carry these with you when you travel.  Also include all over-the-counter medications containing amphetamines that you intend to carry with you when yo'), 
required=False,
# TODO medications should be listed in a chart, with columns: Medication Name
Medication-related Condition
medication start (month/year)
medication end or anticipated end (month/year)
if end is not in the past: 
--Dose
--Times per Day (1, 2, 3, as needed)
--Sto
)
medicationsStorage = schema.TextLine(
description=_(u'If your medication requires special storage (e.g. refrigeration), describe your storage needs.'), 
required=False,
)
    form.mode (authorizedAccommodation_label='display')
    authorizedAccommodation_label = schema.TextLine(
        title=_(u'Authorized Accommodation'),
    )
authorizedAccommodationYesNo = schema.Choice(
description=_(u'I am currently registered for medical or mental-health related accommodations through the Dean of Students office or Project Success at the University of Wisconsin Oshkosh, or with a similar office at my school.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
)
authorizedAccommodationOffice = schema.Choice(
description=_(u'If so, with which office have you registered?'), 
required=False,
# TODO add vocabulary: Dean of Students Office; Project Success; Other office providing services for students with disabilities
)
authorizedAccommodationList = schema.TextLine(
description=_(u'What accommodations have been authorized for you?'), 
required=False,
)
authorizedAccommodationRequest = schema.TextLine(
description=_(u'What accommodations are you requesting in relation to your program abroad/away?'), 
required=False,
)
    form.mode (healthConfirmation_label='display')
    healthConfirmation_label = schema.TextLine(
        title=_(u'I understand and agree'),
    )
medicationsImport = schema.Choice(
description=_(u'...that whether or not I have disclosed medications here, I am ultimately responsible for ensuring that my medications can be carried into any and all foreign countries I plan to visit and that I my medications can be replaced with a comparable product if'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
# TODO must be 'yes'
)
healthStatusChange = schema.Choice(
description=_(u'...that if my medical or mental health status changes after completing this application, I will inform the OIE by updating my medical or mental health information within this application.'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
# TODO must be 'yes'
)
healthAccess = schema.Choice(
description=_(u'...that this information may be accessed by the following people: program leader/s (for group programs), exchange liaison/s abroad/away (for student exchange and direct enroll programs), program organizer/s outside of UW Oshkosh, my host family (if homest'), 
required=False,
vocabulary=vocabulary=yes_no_none_vocabulary,
# TODO must be 'yes'
)
healthMeetingNotes = field.NamedFile(
title=_(u'Health Meeting Notes'),
required=False,
)
    form.mode (roommate_label='display')
    roommate_label = schema.TextLine(
        title=_(u'Roommate'),
        description=_(u'If you are not traveling with a UW Oshkosh student group, do not list a roommate choice.  If you are traveling on a group program, list your first and second choice roommates here.  Any roommate you request must list you on his/her application in return.'), 
    )
#     roommateName1 = schema.TextLine(
#         title=_(u'Roommate 1 Name'),
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     roommateName2 = schema.TextLine(
#         title=_(u'Roommate 2 Name'),
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#

        
        
        

#     doctorLastname = schema.TextLine(
#         title=_(u'Last Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorFirstname = schema.TextLine(
#         title=_(u'First Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorPhone = schema.TextLine(
#         title=_(u'Doctor''s Phone Number'),
#         description=_(u'Please include country code (if outside US) and area code'),
# #        required=True,
#         required=False,
#     )
#
#     medicalInsuranceCompany = schema.TextLine(
#         title=_(u'Name of Insurance Company'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyHolder = schema.TextLine(
#         title=_(u'Name of Policy Holder'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyGroupNumber = schema.TextLine(
#         title=_(u'Policy / Group Number'),
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'medical2',
#         label=_(u"Medical II"),
#         fields=['medicalReadStatement']
#     )
#
#     model.fieldset(
#         'medical3',
#         label=_(u"Medical III"),
#         fields=['medicalHealthProblems', 'medicalHealthProblems_takenMedication',
#                 'medicalHealthProblems_medications', 'medicalHealthProblems_stable',
#                 'medicalHealthProblems_underCare', 'medicalHealthProblems_whatCondition',
#                 'medicalHealthProblems_willingToPrescribe',
#                 'medicalHealthProblems_additionalInfo', 'medicalMentalProblems',
#                 'medicalMentalProblems_takenMedication', 'medicalMentalProblems_medications',
#                 'medicalMentalProblems_currentDose', 'medicalMentalProblems_stable',
#                 'medicalMentalProblems_underCare', 'medicalMentalProblems_condition',
#                 'medicalMentalProblems_enoughMedication', 'medicalMentalProblems_additionalInfo',
#                 'medicalRegistered', 'medicalRegistered_office',
#                 'medicalRegistered_accommodations', 'medicalAccessOK', ]
#     )
#
#     medicalHealthProblems_takenMedication = schema.Choice(
#         title=_(u'Has Taken Medication'),
#         description=_(u'Are you taking or have you ever taken medication related to your physical health?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_medications = schema.Text(
#         title=_(u'Medication List'),
#         description=_(u'If so, list the medications you have taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_whatCondition = schema.Text(
#         title=_(u'Medical Conditions'),
#         description=_(u'If you are currently under the care of a doctor or other health care professional, for what condition? Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_willingToPrescribe = schema.Choice(
#         title=_(u'Enough Medication'),
#         description=_(u'Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_additionalInfo = schema.Text(
#         title=_(u'Additional Health Info'),
#         description=_(u'Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in blank if appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems = schema.Text(
#         title=_(u'Mental Health Problems'),
#         description=_(u'List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.'),
#         required=False,
#     )
#
#     medicalMentalProblems_takenMedication = schema.Choice(
#         title=_(u'Are you taking/have you ever taken medication related to your mental health?  '),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_medications = schema.Text(
#         title=_(u'Mental Health Medications'),
#         description=_(u'If so, list the medications taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_currentDose = schema.Text(
#         title=_(u'Mental Health Medications Dosage'),
#         description=_(u'What is the current dose? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_underCare = schema.Choice(
#         title=_(u'Mental Health Care'),
#         description=_(u'Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_condition = schema.Text(
#         title=_(u'Mental Health Care Conditions'),
#         description=_(u'If yes, for what condition? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_enoughMedication = schema.Choice(
#         title=_(u'Sufficient Mental Health Medication'),
#         description=_(u'Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_additionalInfo = schema.Text(
#         title=_(u'Mental Health Additional Information'),
#         description=_(u'Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in text area if there isn''t any.'),
#         required=False,
#     )
#
#     medicalRegistered = schema.Choice(
#         title=_(u'Registered with UW Oshkosh for Accommodations'),
#         description=_(u'Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalRegistered_office = schema.TextLine(
#         title=_(u'UW Oshkosh Office Accommodations'),
#         description=_(u'If so, with which office have you registered? Write ''none'' in text area if you have not registered.'),
#         required=False,
#     )
#
#     medicalRegistered_accommodations = schema.Text(
#         title=_(u'Medical Authorized Accommodations'),
#         description=_(u'What accommodations have been authorized for you? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalAccessOK = schema.Choice(
#         title=_(u'Medical Access Granted'),
#         description=_(u'""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'preferences',
#         label=_(u"Preferences"),
#         fields=['smokingPreferred', 'isVegetarian', 'additionalNeeds', ]
#     )
#
#     additionalNeeds = schema.Text(
#         title=_(u'Additional Needs'),
#         description=_(u'Is there anything else your host families or the OIE should know about your accommodation needs?'),
#         required=False,
#     )
#
        
        
        
        

#     emerg1workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 1 Work Phone'),
#         description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
#         # write_permission="UWOshOIE: Modify revisable fields",
#         required=False,
#     )
#
#     emerg1mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 1 Mobile Phone'),
#         description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2name = schema.TextLine(
#         title=_(u'Emergency Contact 2 Name'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2addr1 = schema.TextLine(
#         title=_(u'Emergency Contact 2 Address Line 1'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2addr2 = schema.TextLine(
#         title=_(u'Emergency Contact 2 Address Line 2'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2city = schema.TextLine(
#         title=_(u'Emergency Contact 2 City'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2state = schema.TextLine(
#         title=_(u'Emergency Contact 2 State'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2zip = schema.TextLine(
#         title=_(u'Emergency Contact 2 Zip Code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2country = schema.TextLine(
#         title=_(u'Emergency Contact 2 Country'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2homePhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Home Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Work Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Mobile Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2email = schema.TextLine(
#         title=_(u'Emergency Contact 2 Email'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3name = schema.TextLine(
#         title=_(u'Emergency Contact 3 Name'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3addr1 = schema.TextLine(
#         title=_(u'Emergency Contact 3 Address Line 1'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3addr2 = schema.TextLine(
#         title=_(u'Emergency Contact 3 Address Line 2'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3city = schema.TextLine(
#         title=_(u'Emergency Contact 3 City'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3state = schema.TextLine(
#         title=_(u'Emergency Contact 3 State'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3zip = schema.TextLine(
#         title=_(u'Emergency Contact 3 Zip Code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3country = schema.TextLine(
#         title=_(u'Emergency Contact 3 Country'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3homePhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Home Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Work Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Mobile Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3email = schema.TextLine(
#         title=_(u'Emergency Contact 3 Email'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#
#
#     dexteritytextindexer.searchable('firstName')
#     firstName = schema.TextLine(
#         title=_(u'First Name'),
#         required=True,
#     )
#
#     dexteritytextindexer.searchable('middleName')
#     middleName = schema.TextLine(
#         title=_(u'Middle Name'),
#         required=False,
#     )
#
#     dexteritytextindexer.searchable('lastName')
#     lastName = schema.TextLine(
#         title=_(u'Last Name'),
#         required=True,
#     )
#
#     model.fieldset(
#         'addresses',
#         label=_(u"Addresses"),
#         fields=[ ]
#     )
#
#     homePhone = schema.TextLine(
#         title=_(u'Home Telephone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=True,
#     )
#
#     citizenshipOther = schema.TextLine(
#         title=_(u'Other Citizenship Country'),
#         description=_(u'Enter country of citizenship if you selected Other'),
#         required=False,
#     )
#
#     stateResidencyOther = schema.TextLine(
#         title=_(u'Other State Residency'),
#         description=_(u'Enter state of residency if you selected Other'),
#         required=False,
#     )
#
#     placeOfBirth = schema.TextLine(
#         title=_(u'Place of Birth'),
#         description=_(u'Enter city, state, and country'),
#         required=True,
#     )
#
#     gender = schema.Choice(
#         title=_(u'Gender'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.genders',
#         required=False,
#     )
#
#     marriageStatus = schema.Choice(
#         title=_(u'Marital Status'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.marriage_statuses',
#         required=False,
#     )
#
#     model.fieldset(
#         'passport',
#         label=_(u"Passport"),
#         fields=['passportName', 'passportNumber', 'passportIssueOffice', 'passportExpDate']
#     )
#
#     passportName = schema.TextLine(
#         title=_(u'Passport Full Name'),
#         description=_(u'Enter your full name EXACTLY as it appears on your passport or passport application'),
#         required=False,
#     )
#
#     passportNumber = schema.TextLine(
#         title=_(u'Passport Number'),
#         description=_(u''),
#         required=False,
#     )
#
#     passportIssueOffice = schema.TextLine(
#         title=_(u'Passport Issuing Office'),
#         description=_(u'e.g. New Orleans or U.S. Department of State'),
#         required=False,
#     )
#
#     passportExpDate = schema.Date(
#         title=_(u'Passport Expiry'),
#         required=True,
#     )
#
#     model.fieldset(
#         'additional_questions',
#         label=_(u"Additional Questions"),
#         fields=['questionAcadCareerPlan', 'questionLangCulturalSkills', 'questionPrevTravel',
#                 'questionWorkExp', 'questionEuroBizTravSem', 'questionStuExchComp', ]
#     )
#
#     questionAcadCareerPlan = schema.Text(
#         title=_(u'Academic and Career Plan'),
#         description=_(u'a) Briefly, what are your short- and long-term academic and career goals? <br> b) Why would you like to participate in this program? <br> c) What do you expect to gain from your experience?'),
# #        required=True,
#         required=False,
#     )
#
#     questionLangCulturalSkills = schema.Text(
#         title=_(u'Language and Cultural Skills'),
#         description=_(u'a) Have you studied a foreign language? If so, what is your level of fluency? <br> b) Have you completed any University-level courses on the culture or history of your destination? If so, explain. <br> c) Have you ever been immersed in a language and/or culture abroad? If so, please explain. <br> d) Do you plan to use a foreign language in a professional setting? If yes, please explain.'),
# #        required=True,
#         required=False,
#     )
#
#     questionPrevTravel = schema.Text(
#         title=_(u'Previous Travel Experience'),
#         description=_(u'Have you traveled abroad? If so, list the places to which you have traveled along with the dates and purpose.'),
# #        required=True,
#         required=False,
#     )
#
#     questionWorkExp = schema.Text(
#         title=_(u'Work Experience'),
#         description=_(u'a) Who is your current employer? <br> b) If relevant to your study abroad program, list and describe your responsibilities from current and previous jobs.'),
# #        required=True,
#         required=False,
#     )
#
#     questionEuroBizTravSem = schema.Text(
#         title=_(u'European Business Travel Seminar Only'),
#         description=_(u'Include the name of the company(ies) you are currently working for and your title(s).'),
#         required=False,
#     )
#
#     questionStuExchComp = schema.Text(
#         title=_(u'Student Exchange and Competitive Programs Only'),
#         description=_(u'Add anything else you think we should consider when reviewing your application.'),
#         required=False,
#     )
#
#     model.fieldset(
#         'medical',
#         label=_(u"Medical"),
#         fields=['doctorLastname', 'doctorFirstname', 'doctorPhone', 'medicalInsuranceCompany',
#                 'medicalPolicyHolder', 'medicalPolicyGroupNumber', 'foodAllergies',
#                 'hasDifficultyWalking', 'maxWalkingDistance']
#     )
#
#     doctorLastname = schema.TextLine(
#         title=_(u'Last Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorFirstname = schema.TextLine(
#         title=_(u'First Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorPhone = schema.TextLine(
#         title=_(u'Doctor''s Phone Number'),
#         description=_(u'Please include country code (if outside US) and area code'),
# #        required=True,
#         required=False,
#     )
#
#     medicalInsuranceCompany = schema.TextLine(
#         title=_(u'Name of Insurance Company'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyHolder = schema.TextLine(
#         title=_(u'Name of Policy Holder'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyGroupNumber = schema.TextLine(
#         title=_(u'Policy / Group Number'),
# #        required=True,
#         required=False,
#     )
#
#     foodAllergies = schema.TextLine(
#         title=_(u'Allergies'),
#         description=_(u'List any allergies (food, pet, etc.)'),
#         required=False,
#     )
#
#     hasDifficultyWalking = schema.Choice(
#         title=_(u'Difficulty Walking'),
#         description=_(u'Do you have a condition which would make it difficult to walk long distances?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     maxWalkingDistance = schema.TextLine(
# #    maxWalkingDistance = schema.Int(
#         title=_(u'Max Walking Distance'),
#         description=_(u'If so, what is the maximum number of minutes you can walk?'),
#         required=False,
#     )
#
#     model.fieldset(
#         'medical2',
#         label=_(u"Medical II"),
#         fields=['medicalReadStatement']
#     )
#
#     medicalReadStatement = schema.Choice(
#         title=_(u'I have read the statement below and understand.'),
#         description=_(u'""Pre-existing medical and mental health conditions are often intensified by travel to or living in a foreign environment.  Before committing to a study abroad program, consider how your new environment may affect your personal health both physically and mentally.  For example, your new environment may introduce you to new diseases, such as malaria or yellow fever, or new stresses which may cause additional complications for a person with a preexisting condition.<br> <br> The OIE strongly recommends that you have a physical, talk with a medical provider about any preexisting conditions and recommended and/or required immunizations, talk with a psychiatrist or counselor about any preexisting conditions and take care of any dental work before departure.<br> <br> If you choose not to complete this section before program acceptance, you must forward information related to the following to the OIE within one week of the application deadline for your program.  Failure to disclose medical or mental health conditions will make it extremely difficult for staff at UW Oshkosh and abroad to assist you in an emergency and may cause health professionals abroad to take actions which could lead to serious medical consequences, including death.<br> <br> NOTE ON MEDICATIONS: You are responsible for ensuring that your medications can be carried into the foreign country.  If your medical status changes after completing this application, you must inform the OIE.""'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'medical3',
#         label=_(u"Medical III"),
#         fields=['medicalHealthProblems', 'medicalHealthProblems_takenMedication',
#                 'medicalHealthProblems_medications', 'medicalHealthProblems_stable',
#                 'medicalHealthProblems_underCare', 'medicalHealthProblems_whatCondition',
#                 'medicalHealthProblems_willingToPrescribe',
#                 'medicalHealthProblems_additionalInfo', 'medicalMentalProblems',
#                 'medicalMentalProblems_takenMedication', 'medicalMentalProblems_medications',
#                 'medicalMentalProblems_currentDose', 'medicalMentalProblems_stable',
#                 'medicalMentalProblems_underCare', 'medicalMentalProblems_condition',
#                 'medicalMentalProblems_enoughMedication', 'medicalMentalProblems_additionalInfo',
#                 'medicalRegistered', 'medicalRegistered_office',
#                 'medicalRegistered_accommodations', 'medicalAccessOK', ]
#     )
#
#     medicalHealthProblems = schema.Text(
#         title=_(u'Health Problems'),
#         description=_(u'List and describe any recent (within the past five years) or continuing health problems, including physical disabilities or medical conditions; learning disabilities; drug, plant, food, animal, or insect sting allergies (include information pertaining to reactions); and/or surgeries that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad. Complete this section now or by the Friday following the application deadline.  Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_takenMedication = schema.Choice(
#         title=_(u'Has Taken Medication'),
#         description=_(u'Are you taking or have you ever taken medication related to your physical health?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_medications = schema.Text(
#         title=_(u'Medication List'),
#         description=_(u'If so, list the medications you have taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_underCare = schema.Choice(
#         title=_(u'Are you currently under the care of a doctor or other health care professional?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_whatCondition = schema.Text(
#         title=_(u'Medical Conditions'),
#         description=_(u'If you are currently under the care of a doctor or other health care professional, for what condition? Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_willingToPrescribe = schema.Choice(
#         title=_(u'Enough Medication'),
#         description=_(u'Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_additionalInfo = schema.Text(
#         title=_(u'Additional Health Info'),
#         description=_(u'Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in blank if appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems = schema.Text(
#         title=_(u'Mental Health Problems'),
#         description=_(u'List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.'),
#         required=False,
#     )
#
#     medicalMentalProblems_takenMedication = schema.Choice(
#         title=_(u'Are you taking/have you ever taken medication related to your mental health?  '),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_medications = schema.Text(
#         title=_(u'Mental Health Medications'),
#         description=_(u'If so, list the medications taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_currentDose = schema.Text(
#         title=_(u'Mental Health Medications Dosage'),
#         description=_(u'What is the current dose? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_underCare = schema.Choice(
#         title=_(u'Mental Health Care'),
#         description=_(u'Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_condition = schema.Text(
#         title=_(u'Mental Health Care Conditions'),
#         description=_(u'If yes, for what condition? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_enoughMedication = schema.Choice(
#         title=_(u'Sufficient Mental Health Medication'),
#         description=_(u'Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_additionalInfo = schema.Text(
#         title=_(u'Mental Health Additional Information'),
#         description=_(u'Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in text area if there isn''t any.'),
#         required=False,
#     )
#
#     medicalRegistered = schema.Choice(
#         title=_(u'Registered with UW Oshkosh for Accommodations'),
#         description=_(u'Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalRegistered_office = schema.TextLine(
#         title=_(u'UW Oshkosh Office Accommodations'),
#         description=_(u'If so, with which office have you registered? Write ''none'' in text area if you have not registered.'),
#         required=False,
#     )
#
#     medicalRegistered_accommodations = schema.Text(
#         title=_(u'Medical Authorized Accommodations'),
#         description=_(u'What accommodations have been authorized for you? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalAccessOK = schema.Choice(
#         title=_(u'Medical Access Granted'),
#         description=_(u'""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'preferences',
#         label=_(u"Preferences"),
#         fields=['smokingPreferred', 'isVegetarian', 'additionalNeeds', ]
#     )
#
#     smokingPreferred = schema.Choice(
#         title=_(u'Smoking Preference'),
#         vocabulary=smoking_vocabulary,
#         default= 'No Preference',
#         required=False,
#     )
#
#     isVegetarian = schema.Choice(
#         title=_(u'Are you vegetarian?'),
#         vocabulary=yes_no_none_vocabulary,
#         #default="No",
# #        required=True,
#         required=False,
#     )
#
#     additionalNeeds = schema.Text(
#         title=_(u'Additional Needs'),
#         description=_(u'Is there anything else your host families or the OIE should know about your accommodation needs?'),
#         required=False,
#     )
#
#     dexteritytextindexer.searchable('programYear')
#     programYear = schema.TextLine(
# #    programYear = schema.Int(
#         title=_(u'Program Year'),
#         description=_(u'Enter the year you will actually be attending the program (YYYY)'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     programSemester = schema.Choice(
#         title=_(u'Semester'),
#         vocabulary=semester_vocabulary,
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     studentType = schema.Choice(
#         title=_(u'Student Type'),
#         vocabulary=student_type_vocabulary,
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     emphasis1 = schema.TextLine(
#         title=_(u'Emphasis/Licensure 1'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     emphasis2 = schema.TextLine(
#         title=_(u'Emphasis/Licensure 2'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'transportation',
#         label=_(u"Transportation"),
#         fields=['willTakeBus', 'willFlyWithGroup', 'departureDate', 'returnDate', 'agreeToCosts']
#     )
#
#     willTakeBus = schema.Choice(
#         title=_(u'Bus'),
#         description=_(u'Please note: while a group bus is an option for most programs, not all programs offer this option.'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#         vocabulary=bus_vocabulary,
#     )
#
#     willFlyWithGroup = schema.Choice(
#         title=_(u'Flights'),
# #        required=True,
#         required=False,
#         vocabulary=fly_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     departureDate = schema.Date(
#         title=_(u'Planned Departure Date'),
#         description=_(u'Specify if you are deviating from the group itinerary.'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     returnDate = schema.Date(
#         title=_(u'Planned Return Date'),
#         description=_(u'Specify if you are deviating from the group itinerary.'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     agreeToCosts = schema.TextLine(
#         title=_(u'Agree to Costs'),
#         description=_(u'I understand that if I choose not to fly on dates recommended by the OIE or by my hosts abroad, I remain responsible for the full program cost, regardless of whether I participate in all events or make use of all services. Enter your initials'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'orientation',
#         label=_(u"Orientation"),
#         fields=['orientationDate1', 'orientationHours1', 'orientationDate2', 'orientationHours2',
#                 'numberOfGuests', 'orientationConflict', 'conflictDate']
#     )
#
#     orientationDate1 = schema.Date(
#         title=_(u'I will attend the family orientation on'),
#         description=_(u'Enter one date and time for the four-hour session, or enter two dates and times for the two-hour sessions'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationHours1 = schema.Choice(
#         title=_(u'Orientation Session 1 \"hours\"'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.session_hours',
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationDate2 = schema.Date(
#         title=_(u'Orientation Session part 2 (Date)'),
#         description=_(u'if applicable'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationHours2 = schema.Bool(
#         title=_(u'Will attend orientation Session part 2 from 3pm - 5pm'),
#         description=_(u'if applicable'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     numberOfGuests = schema.TextLine(
# #    numberOfGuests = schema.Int(
#         title=_(u'Number of Guests'),
#         description=_(u'The following number of people will attend with me'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     orientationConflict = schema.Choice(
#         title=_(u'Schedule Conflict'),
#         description=_(u'Do you have a conflict with any of the other pre-travel academic and/or orientation sessions?'),
# #        required=True,
#         required=False,
#         vocabulary=orientation_conflict_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     conflictDate = schema.Date(
#         title=_(u'Date of your conflict'),
#         description=_(u'if you selected Yes above'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#
#     subject1 = schema.Choice(
#         title=_(u'Course 1 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course1 = schema.TextLine(
#         title=_(u'Course Number 1'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits1 = schema.Float(
#         title=_(u'Credits 1'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject2 = schema.Choice(
#         title=_(u'Course 2 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course2 = schema.TextLine(
#         title=_(u'Course Number 2'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits2 = schema.Float(
#         title=_(u'Credits 2'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject3 = schema.Choice(
#         title=_(u'Course 3 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course3 = schema.TextLine(
#         title=_(u'Course Number 3'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits3 = schema.Float(
#         title=_(u'Credits 3'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject4 = schema.Choice(
#         title=_(u'Course 4 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course4 = schema.TextLine(
#         title=_(u'Course Number 4'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits4 = schema.Float(
#         title=_(u'Credits 4'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject5 = schema.Choice(
#         title=_(u'Course 5 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course5 = schema.TextLine(
#         title=_(u'Course Number 5'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits5 = schema.Float(
#         title=_(u'Credits 5'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject6 = schema.Choice(
#         title=_(u'Course 6 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course6 = schema.TextLine(
#         title=_(u'Course Number 6'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits6 = schema.Float(
#         title=_(u'Credits 6'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     readSyllabus = schema.Bool(
#         title=_(u'Has Read Syllabus'),
#         description=_(u'I have read the syllabus for the one-credit course International Studies 333'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     enrolledIS333 = schema.Bool(
#         title=_(u'Enroll me in International Studies 333'),
#         description=_(u'You will only be enrolled if you have read the syllabus'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'financial_aid',
#         label=_(u"Financial Aid"),
#         fields=['applyForAid', 'holdApplication', 'financialAidGranted']
#     )
#
#     applyForAid = schema.Choice(
#         title=_(u'Financial Aid'),
#         description=_(u'I will use financial aid to fund all or part of my program.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     holdApplication = schema.Choice(
#         title=_(u'Should the OIE hold or process your application?'),
#         description=_(u'HOLD your Study Abroad Application (i.e. you will only study abroad IF financial aid is available; at this point the application fee is still refundable but the OIE is not reserving a seat for you), or PROCESS your Study Abroad Applciation (i.e. you will study abroad regardless of your aid package; at this point the application fee is non-refundable and the OIE will reserve your seat.'),
# #        required=True,
#         required=False,
#         vocabulary=hold_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     financialAidGranted = schema.Bool(
#         title=_(u'Financial Aid Granted?'),
#         description=_(u'Set by Financial Aid staff only'),
#         required=False,
#         #write_permission="UWOshOIE: Modify Financial Aid fields",
#     )
#
#     model.fieldset(
#         'accommodation_preferences',
#         label=_(u"Accommodation Preferences"),
#         fields=['roomType', 'roommateName1', 'roommateName2', ]
#     )
#
#     roomType = schema.Choice(
#         title=_(u'Room Type'),
# #        required=True,
#         required=False,
#         vocabulary=room_type_vocabulary,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     model.fieldset(
#         'expectations',
#         label=_(u"Expectations"),
#         fields=['questionExpectations', ]
#     )
#
#     questionExpectations = schema.Text(
#         title=_(u'Your Expectations For'),
#         description=_(u'a) this program as a whole? <br> b) the pre-travel general orientation session? <br> c) the pre-travel academic sessions? <br> d) your hosts (host institution, family, etc.) in the foreign country (if applicable)?'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'verification',
#         label=_(u"Verification"),
#         fields=['awareOfAllMaterials', 'UWOshkoshRelease', 'certification', ]
#     )
#
#     awareOfAllMaterials = schema.Choice(
#         title=_(u'Are you aware of the application requirements for your program?'),
#         description=_(u'Additional application requirements for select programs are listed on individual program web pages.  Not all programs have additional requirements.'),
# #        required=True,
#         required=False,
#         vocabulary=aware_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     UWOshkoshRelease = schema.Choice(
#         title=_(u'Release of Liability'),
#         description=_(u'I hereby agree to hold harmless and indemnify the Board of Regents of the University of Wisconsin System and the University of Wisconsin Oshkosh, their officers, agents and employees, from any and all liability, loss, damages, costs or expenses which are sustained, incurred or required arising out of my actions.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     certification = schema.Choice(
#         title=_(u'Certification'),
#         description=_(u'I certify that the information stated above is true and correct.  If accepted to the program, I agree to follow all payment and withdrawal policies and to regularly check my UW Oshkosh email account for program information beginning today.  If I am a non-UW Oshkosh student, I will use and submit an email address that I check regularly.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#
# #########################
# #OFFICE USE ONLY SECTION
# #########################
#
#     model.fieldset(
#         'office_use_only',
#         label=_(u"OFFICE USE ONLY"),
#         fields=['seatNumber', 'completionDate', 'applicationIsComplete',
#                 'comments', 'applicationFeeOK', 'UWSystemStatementOK', 'UWOshkoshStatementOK',
#                 'withdrawalRefund', 'transcriptsOK', 'programSpecificMaterialsRequired',
#                 'programSpecificMaterialsOK', 'specialStudentFormRequired',
#                 'specialStudentFormOK', 'creditOverloadFormRequired', 'creditOverloadFormOK',
#                 'medicalOK', 'medicalForm', 'passportOK', 'metPassportDeadline',
#                 'programSpecificMaterialsRequiredStepIII', 'programSpecificMaterialsOKStepIII',
#                 'attendedOrientation', 'cisiDates', 'cisiNumberOfMonths', 'programFee',
#                 'tuitionPayment', 'depositOnTime', 'payment2OnTime', 'applicationFeeRefund',
#                 'foreignCourse1', 'foreignCourse2', 'foreignCourse3', 'foreignCourse4',
#                 'foreignCourse5', 'foreignCourse6', 'papersOK', 'noMoreMaterials',
#                 'programMaterials', 'programFee2', ]
#     )
#
#     completionDate = schema.Date(
#         title=_(u'Date Application Was Completed'),
#         description=_(u'This is the date in which the application was completed.'),
#         required=False,
#     )
#
#     applicationIsComplete = schema.Bool(
#         title=_(u'Application is Complete'),
#         required=False,
#     )
#
#     comments = schema.Text(
#         title=_(u'Comments'),
#         required=False,
#     )
#
#     applicationFeeOK = schema.Bool(
#         title=_(u'Application Fee Submitted'),
#         required=False,
#     )
#
#     UWSystemStatementOK = schema.Bool(
#         title=_(u'UW System Statement of Responsibility Submitted'),
#         required=False,
#     )
#
#     UWOshkoshStatementOK = schema.Bool(
#         title=_(u'UW Oshkosh Statement of Responsibility Submitted'),
#         description=_(u'This is the date in which the application was completed.'),
#         required=False,
#     )
#
#     withdrawalRefund = schema.Bool(
#         title=_(u'Withdrawal and Refund Form Submitted'),
#         required=False,
#     )
#
#     transcriptsOK = schema.Bool(
#         title=_(u'Transcripts Submitted'),
#         required=False,
#     )
#
#     programSpecificMaterialsRequired = schema.Choice(
#         title=_(u'Program-Specific Materials Required(Step II)?'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsOK = schema.Bool(
#         title=_(u'Program-Specific Materials Submitted(Step II)'),
#         required=False,
#     )
#
#     specialStudentFormRequired = schema.Choice(
#         title=_(u'Special Student Form Required'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     specialStudentFormOK = schema.Bool(
#         title=_(u'Special Student Form Submitted'),
#         required=False,
#     )
#
#     creditOverloadFormRequired = schema.Choice(
#         title=_(u'Credit Overload Form Required'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     creditOverloadFormOK = schema.Bool(
#         title=_(u'Credit Overload Form Submitted'),
#         required=False,
#     )
#
#     medicalOK = schema.Bool(
#         title=_(u'Medical information is Submitted/Updated'),
#         required=False,
#     )
#
#     medicalForm = schema.Text(
#         title=_(u'Medical Form'),
#         required=False,
#     )
#
#     passportOK = schema.Bool(
#         title=_(u'Passport information or receipt submitted'),
#         required=False,
#     )
#
#     metPassportDeadline = schema.Choice(
#         title=_(u'Passport Deadline Met'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsRequiredStepIII = schema.Choice(
#         title=_(u'Program-Specific Materials Required(Step III)?'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsOKStepIII = schema.Bool(
#         title=_(u'Program-Specific Materials Submitted(Step III)'),
#         required=False,
#     )
#
#     attendedOrientation = schema.Choice(
#         title=_(u'Attended Orientation'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     cisiDates = schema.TextLine(
#         title=_(u'Health Insurance Dates'),
#         description=_(u'Cultural Insurance Services International'),
#         required=False,
#     )
#
#     cisiNumberOfMonths = schema.TextLine(
# #    cisiNumberOfMonths = schema.Int(
#         title=_(u'Health Insurance Number of Months'),
#         description=_(u'Cultural Insurance Services International'),
#         required=False,
#     )
#
#     programFee = schema.Float(
#         title=_(u'Program Fee'),
#         description=_(u''),
#         required=False,
#     )
#
#     tuitionPayment = schema.Float(
#         title=_(u'Tuition Payment (student exchange only)'),
#         description=_(u''),
#         required=False,
#     )
#
#     depositOnTime = schema.Choice(
#         title=_(u'Deposit Paid on Time'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     payment2OnTime = schema.Choice(
#         title=_(u'Final Payment Made on Time (except exchange students)'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     applicationFeeRefund = schema.Choice(
#         title=_(u'Application Fee Refunded'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     foreignCourse1 = schema.TextLine(
#         title=_(u'Foreign institution course 1'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse2 = schema.TextLine(
#         title=_(u'Foreign institution course 2'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse3 = schema.TextLine(
#         title=_(u'Foreign institution course 3'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse4 = schema.TextLine(
#         title=_(u'Foreign institution course 4'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse5 = schema.TextLine(
#         title=_(u'Foreign institution course 5'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse6 = schema.TextLine(
#         title=_(u'Foreign institution course 6'),
#         description=_(u''),
#         required=False,
#     )
#
#     papersOK = schema.Bool(
#         title=_(u'Papers information is OK'),
#         description=_(u''),
#         required=False,
#     )
#
#     noMoreMaterials = schema.Bool(
#         title=_(u'No More Materials'),
#         description=_(u''),
#         required=False,
#     )
#
#     programMaterials = schema.Bool(
#         title=_(u'Program Materials'),
#         description=_(u''),
#         required=False,
#     )
#
#     programFee2 = schema.TextLine(
# #    programFee2 = schema.Int(
#         title=_(u'Program Fee 2'),
#         description=_(u''),
#         required=False,
#     )
