# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.supermodel import model
from plone.namedfile import field

yes_no_none_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=''),
        SimpleTerm(value='Yes'), 
        SimpleTerm(value='No'),
    ]
)

yes_no_na_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='n/a'),
        SimpleTerm(value='Yes'), 
        SimpleTerm(value='No'),
    ]
)

month_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'01', title=_(u'January')),
     SimpleTerm(value=u'02', title=_(u'February')),
     SimpleTerm(value=u'03', title=_(u'March')),
     SimpleTerm(value=u'04', title=_(u'April')),
     SimpleTerm(value=u'05', title=_(u'May')),
     SimpleTerm(value=u'06', title=_(u'June')),
     SimpleTerm(value=u'07', title=_(u'July')),
     SimpleTerm(value=u'08', title=_(u'August')),
     SimpleTerm(value=u'09', title=_(u'September')),
     SimpleTerm(value=u'10', title=_(u'October')),
     SimpleTerm(value=u'11', title=_(u'November')),
     SimpleTerm(value=u'12', title=_(u'December'))]
)

dayofmonth_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'01'),
     SimpleTerm(value=u'02'),
     SimpleTerm(value=u'03'),
     SimpleTerm(value=u'04'),
     SimpleTerm(value=u'05'),
     SimpleTerm(value=u'06'),
     SimpleTerm(value=u'07'),
     SimpleTerm(value=u'08'),
     SimpleTerm(value=u'09'),
     SimpleTerm(value=u'10'),
     SimpleTerm(value=u'11'),
     SimpleTerm(value=u'12'),
     SimpleTerm(value=u'13'),
     SimpleTerm(value=u'14'),
     SimpleTerm(value=u'15'),
     SimpleTerm(value=u'16'),
     SimpleTerm(value=u'17'),
     SimpleTerm(value=u'18'),
     SimpleTerm(value=u'19'),
     SimpleTerm(value=u'20'),
     SimpleTerm(value=u'21'),
     SimpleTerm(value=u'22'),
     SimpleTerm(value=u'23'),
     SimpleTerm(value=u'24'),
     SimpleTerm(value=u'25'),
     SimpleTerm(value=u'26'),
     SimpleTerm(value=u'27'),
     SimpleTerm(value=u'28'),
     SimpleTerm(value=u'29'),
     SimpleTerm(value=u'30'),
     SimpleTerm(value=u'31'), ]
)

class IUwoshOieStudyabroadstudentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IOIEStudyAbroadStudentApplication(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    studentID = schema.TextLine(
        title=_(u'UW Oshkosh Student ID'),
        description=_(u'(if applicable)'),
        required=False,
    )

    firstName = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    middleName = schema.TextLine(
        title=_(u'Middle Name'),
        required=False,
    )

    lastName = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )

    email = schema.TextLine(
        title=_(u'Email Address'),
        description=_(u'UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.'),
        required=True,
    )

    model.fieldset(
        'addresses',
        label=_(u"Addresses"),
        fields=['localAddr1', 'localAddr2', 'localCity', 'localState', 'localZip', 
                'localCountry', 'localPhone', 'mobilePhone', 'homeAddr1', 'homeAddr2', 
                'homeCity', 'homeState', 'homeZip', 'homeCountry', 'homePhone', ]
    )
      
    localAddr1 = schema.TextLine(
        title=_(u'Local Address Line 1'),
        required=True,
    )

    localAddr2 = schema.TextLine(
        title=_(u'Local Address Line 2'),
        required=False,
    )

    localCity = schema.TextLine(
        title=_(u'Local City'),
        required=True,
    )

    localState = schema.TextLine(
        title=_(u'Local State'),
        default=_(u'WI'),
        required=True,
    )

    localZip = schema.TextLine(
        title=_(u'Local Zip Code'),
        default=_(u'54901'),
        required=True,
    )

    localCountry = schema.TextLine(
        title=_(u'Local Country'),
        default=_(u'USA'),
        required=True,
    )

    localPhone = schema.TextLine(
        title=_(u'Local Telephone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=True,
    )

    mobilePhone = schema.TextLine(
        title=_(u'Mobile (cell) phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
    )

    homeAddr1 = schema.TextLine(
        title=_(u'Home Address Line 1'),
        required=True,
    )

    homeAddr2 = schema.TextLine(
        title=_(u'Home Address Line 2'),
        required=False,
    )

    homeCity = schema.TextLine(
        title=_(u'Home City'),
        description=_(u''),
        required=True,
    )

    homeState = schema.TextLine(
        title=_(u'Home State'),
        description=_(u''),
        required=True,
    )

    homeZip = schema.TextLine(
        title=_(u'Home Zip Code'),
        description=_(u''),
        required=True,
    )

    homeCountry = schema.TextLine(
        title=_(u'Home Country'),
        required=True,
    )

    homePhone = schema.TextLine(
        title=_(u'Home Telephone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=True,
    )

    model.fieldset(
        'demographics',
        label=_(u"Demographics"),
        fields=['citizenship', 'citizenshipOther', 'stateResidency', 'stateResidencyOther', 
                'dateOfBirth', 'placeOfBirth', 
                'gender', 'marriageStatus', 'ethnicity', ]
    )
      
    citizenship = schema.Choice(
        title=_(u'Citizenship'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.citizenship',
        required=True,
    )

    citizenshipOther = schema.TextLine(
        title=_(u'Other Citizenship Country'),
        description=_(u'Enter country of citizenship if you selected Other'),
        required=False,
    )

    stateResidency = schema.Choice(
        title=_(u'State Residency'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.states_for_residency',
        required=True,
    )

    stateResidencyOther = schema.TextLine(
        title=_(u'Other State Residency'),
        description=_(u'Enter state of residency if you selected Other'),
        required=False,
    )

#    dateOfBirth = schema.Date(
#        title=_(u'Birthday'),
#        required=True,
#    )

    dateOfBirth_year = schema.TextLine(
        title=_(u'Birthday year'),
        required=True,
    )

    dateOfBirth_month = schema.TextLine(
        title=_(u'Birthday month'),
        required=True,
    )

    dateOfBirth_day = schema.TextLine(
        title=_(u'Birthday day'),
        required=True,
    )

    placeOfBirth = schema.TextLine(
        title=_(u'Place of Birth'),
        description=_(u'Enter city, state, and country'),
        required=True,
    )

    gender = schema.Choice(
        title=_(u'Gender'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.genders',
        required=False,
    )

    marriageStatus = schema.Choice(
        title=_(u'Marital Status'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.marriage_statuses',
        required=False,
    )

    ethnicity = schema.Choice(
        title=_(u'Ethnicity'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.ethnicities',
        required=False,
    )

    model.fieldset(
        'passport',
        label=_(u"Passport"),
        fields=['passportName', 'passportNumber', 'passportIssueOffice', 'passportExpDate']
    )
      
    passportName = schema.TextLine(
        title=_(u'Passport Full Name'),
        description=_(u'Enter your full name EXACTLY as it appears on your passport or passport application'),
        required=False,
    )

    passportNumber = schema.TextLine(
        title=_(u'Passport Number'),
        description=_(u''),
        required=False,
    )

    passportIssueOffice = schema.TextLine(
        title=_(u'Passport Issuing Office'),
        description=_(u'e.g. New Orleans or U.S. Department of State'),
        required=False,
    )

    passportExpDate = schema.Date(
        title=_(u'Passport Expiry'),
        required=False,
    )

    model.fieldset(
        'additional_questions',
        label=_(u"Additional Questions"),
        fields=['questionAcadCareerPlan', 'questionLangCulturalSkills', 'questionPrevTravel', 
                'questionWorkExp', 'questionEuroBizTravSem', 'questionStuExchComp', ]
    )
      
    questionAcadCareerPlan = schema.Text(
        title=_(u'Academic and Career Plan'),
        description=_(u'a) Briefly, what are your short- and long-term academic and career goals? <br> b) Why would you like to participate in this program? <br> c) What do you expect to gain from your experience?'),
#        required=True,
        required=False,
    )

    questionLangCulturalSkills = schema.Text(
        title=_(u'Language and Cultural Skills'),
        description=_(u'a) Have you studied a foreign language? If so, what is your level of fluency? <br> b) Have you completed any University-level courses on the culture or history of your destination? If so, explain. <br> c) Have you ever been immersed in a language and/or culture abroad? If so, please explain. <br> d) Do you plan to use a foreign language in a professional setting? If yes, please explain.'),
#        required=True,
        required=False,
    )

    questionPrevTravel = schema.Text(
        title=_(u'Previous Travel Experience'),
        description=_(u'Have you traveled abroad? If so, list the places to which you have traveled along with the dates and purpose.'),
#        required=True,
        required=False,
    )

    questionWorkExp = schema.Text(
        title=_(u'Work Experience'),
        description=_(u'a) Who is your current employer? <br> b) If relevant to your study abroad program, list and describe your responsibilities from current and previous jobs.'),
#        required=True,
        required=False,
    )

    questionEuroBizTravSem = schema.Text(
        title=_(u'European Business Travel Seminar Only'),
        description=_(u'Include the name of the company(ies) you are currently working for and your title(s).'),
        required=False,
    )

    questionStuExchComp = schema.Text(
        title=_(u'Student Exchange and Competitive Programs Only'),
        description=_(u'Add anything else you think we should consider when reviewing your application.'),
        required=False,
    )

    model.fieldset(
        'medical',
        label=_(u"Medical"),
        fields=['doctorLastname', 'doctorFirstname', 'doctorPhone', 'medicalInsuranceCompany', 
                'medicalPolicyHolder', 'medicalPolicyGroupNumber', 'foodAllergies', 
                'hasDifficultyWalking', 'maxWalkingDistance']
    )
      
    doctorLastname = schema.TextLine(
        title=_(u'Last Name of your Family Doctor'),
#        required=True,
        required=False,
    )

    doctorFirstname = schema.TextLine(
        title=_(u'First Name of your Family Doctor'),
#        required=True,
        required=False,
    )

    doctorPhone = schema.TextLine(
        title=_(u'Doctor''s Phone Number'),
        description=_(u'Please include country code (if outside US) and area code'),
#        required=True,
        required=False,
    )

    medicalInsuranceCompany = schema.TextLine(
        title=_(u'Name of Insurance Company'),
#        required=True,
        required=False,
    )

    medicalPolicyHolder = schema.TextLine(
        title=_(u'Name of Policy Holder'),
#        required=True,
        required=False,
    )

    medicalPolicyGroupNumber = schema.TextLine(
        title=_(u'Policy / Group Number'),
#        required=True,
        required=False,
    )

    foodAllergies = schema.TextLine(
        title=_(u'Allergies'),
        description=_(u'List any allergies (food, pet, etc.)'),
        required=False,
    )

    hasDifficultyWalking = schema.Choice(
        title=_(u'Difficulty Walking'),
        description=_(u'Do you have a condition which would make it difficult to walk long distances?'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    maxWalkingDistance = schema.TextLine(
#    maxWalkingDistance = schema.Int(
        title=_(u'Max Walking Distance'),
        description=_(u'If so, what is the maximum number of minutes you can walk?'),
        required=False,
    )

    model.fieldset(
        'medical2',
        label=_(u"Medical II"),
        fields=['medicalReadStatement']
    )
      
    medicalReadStatement = schema.Choice(
        title=_(u'I have read the statement below and understand.'),
        description=_(u'""Pre-existing medical and mental health conditions are often intensified by travel to or living in a foreign environment.  Before committing to a study abroad program, consider how your new environment may affect your personal health both physically and mentally.  For example, your new environment may introduce you to new diseases, such as malaria or yellow fever, or new stresses which may cause additional complications for a person with a preexisting condition.<br> <br> The OIE strongly recommends that you have a physical, talk with a medical provider about any preexisting conditions and recommended and/or required immunizations, talk with a psychiatrist or counselor about any preexisting conditions and take care of any dental work before departure.<br> <br> If you choose not to complete this section before program acceptance, you must forward information related to the following to the OIE within one week of the application deadline for your program.  Failure to disclose medical or mental health conditions will make it extremely difficult for staff at UW Oshkosh and abroad to assist you in an emergency and may cause health professionals abroad to take actions which could lead to serious medical consequences, including death.<br> <br> NOTE ON MEDICATIONS: You are responsible for ensuring that your medications can be carried into the foreign country.  If your medical status changes after completing this application, you must inform the OIE.""'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    model.fieldset(
        'medical3',
        label=_(u"Medical III"),
        fields=['medicalHealthProblems', 'medicalHealthProblems_takenMedication', 
                'medicalHealthProblems_medications', 'medicalHealthProblems_stable', 
                'medicalHealthProblems_underCare', 'medicalHealthProblems_whatCondition', 
                'medicalHealthProblems_willingToPrescribe', 
                'medicalHealthProblems_additionalInfo', 'medicalMentalProblems', 
                'medicalMentalProblems_takenMedication', 'medicalMentalProblems_medications', 
                'medicalMentalProblems_currentDose', 'medicalMentalProblems_stable', 
                'medicalMentalProblems_underCare', 'medicalMentalProblems_condition', 
                'medicalMentalProblems_enoughMedication', 'medicalMentalProblems_additionalInfo', 
                'medicalRegistered', 'medicalRegistered_office', 
                'medicalRegistered_accommodations', 'medicalAccessOK', ]
    )
      
    medicalHealthProblems = schema.Text(
        title=_(u'Health Problems'),
        description=_(u'List and describe any recent (within the past five years) or continuing health problems, including physical disabilities or medical conditions; learning disabilities; drug, plant, food, animal, or insect sting allergies (include information pertaining to reactions); and/or surgeries that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad. Complete this section now or by the Friday following the application deadline.  Write ''n/a'' in blanks where appropriate.'),
        required=False,
    )

    medicalHealthProblems_takenMedication = schema.Choice(
        title=_(u'Has Taken Medication'),
        description=_(u'Are you taking or have you ever taken medication related to your physical health?'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    medicalHealthProblems_medications = schema.Text(
        title=_(u'Medication List'),
        description=_(u'If so, list the medications you have taken over the past year. Write ''n/a'' in blanks where appropriate.'),
        required=False,
    )

    medicalHealthProblems_stable = schema.Choice(
        title=_(u'Are you stable on this medication?'),
        vocabulary=yes_no_na_vocabulary,
#        required=True,
        required=False,
    )

    medicalHealthProblems_underCare = schema.Choice(
        title=_(u'Are you currently under the care of a doctor or other health care professional?'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    medicalHealthProblems_whatCondition = schema.Text(
        title=_(u''),
        description=_(u'If you are currently under the care of a doctor or other health care professional, for what condition? Write ''n/a'' in blanks where appropriate.'),
        required=False,
    )

    medicalHealthProblems_willingToPrescribe = schema.Choice(
        description=_(u'Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?'),
        vocabulary=yes_no_na_vocabulary,
#        required=True,
        required=False,
    )

    medicalHealthProblems_additionalInfo = schema.Text(
        title=_(u'Additional Health Info'),
        description=_(u'Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in blank if appropriate.'),
        required=False,
    )

    medicalMentalProblems = schema.Text(
        description=_(u'List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.'),
        required=False,
    )

    medicalMentalProblems_takenMedication = schema.Choice(
        title=_(u'Are you taking/have you ever taken medication related to your mental health?  '),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    medicalMentalProblems_medications = schema.Text(
        description=_(u'If so, list the medications taken over the past year. Write ''n/a'' in blanks where appropriate.'),
        required=False,
    )

    medicalMentalProblems_currentDose = schema.Text(
        description=_(u'What is the current dose? Write ''n/a'' in text area when appropriate.'),
        required=False,
    )

    medicalMentalProblems_stable = schema.Choice(
        title=_(u'Are you stable on this medication?'),
        vocabulary=yes_no_na_vocabulary,
#        required=True,
        required=False,
    )

    medicalMentalProblems_underCare = schema.Choice(
        description=_(u'Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    medicalMentalProblems_condition = schema.Text(
        description=_(u'If yes, for what condition? Write ''n/a'' in text area when appropriate.'),
        required=False,
    )

    medicalMentalProblems_enoughMedication = schema.Choice(
        description=_(u'Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?'),
        vocabulary=yes_no_na_vocabulary,
#        required=True,
        required=False,
    )

    medicalMentalProblems_additionalInfo = schema.Text(
        description=_(u'Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in text area if there isn''t any.'),
        required=False,
    )

    medicalRegistered = schema.Choice(
        description=_(u'Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    medicalRegistered_office = schema.TextLine(
        description=_(u'If so, with which office have you registered? Write ''none'' in text area if you have not registered.'),
        required=False,
    )

    medicalRegistered_accommodations = schema.Text(
        title=_(u'Medical Authorized Accomodations'),
        description=_(u'What accommodations have been authorized for you? Write ''n/a'' in text area when appropriate.'),
        required=False,
    )

    medicalAccessOK = schema.Choice(
        title=_(u'Medical Access Granted'),
        description=_(u'""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""'),
        vocabulary=yes_no_none_vocabulary,
#        required=True,
        required=False,
    )

    model.fieldset(
        'preferences',
        label=_(u"Preferences"),
        fields=['smokingPreferred', 'isVegetarian', 'additionalNeeds', ]
    )
      
    smokingPreferred = schema.Choice(
        title=_(u'Smoking Preference'),
        vocabulary=SimpleVocabulary([SimpleTerm(value='Smoking'),SimpleTerm(value='Non-smoking'),SimpleTerm(value='No Preference')]),
        default= 'No Preference',
        required=False,
    )

    isVegetarian = schema.Choice(
        title=_(u'Are you vegetarian?'),
        vocabulary=yes_no_none_vocabulary,
        #default="No",
#        required=True,
        required=False,
    )

    additionalNeeds = schema.Text(
        title=_(u'Additional Needs'),
        description=_(u'Is there anything else your host families or the OIE should know about your accommodation needs?'),
        required=False,
    )

    model.fieldset(
        'emergency_contacts',
        label=_(u"Emergency Contacts"),
        fields=['emerg1name', 'emerg1addr1', 'emerg1addr2', 'emerg1city', 'emerg1state', 
                'emerg1zip', 'emerg1country', 'emerg1homePhone', 'emerg1workPhone', 
                'emerg1mobilePhone', 'emerg1email', 'emerg2name', 'emerg2addr1', 'emerg2addr2', 
                'emerg2city', 'emerg2state', 'emerg2zip', 'emerg2country', 'emerg2homePhone', 
                'emerg2workPhone', 'emerg2mobilePhone', 'emerg2email', 'emerg3name', 
                'emerg3addr1', 'emerg3addr2', 'emerg3city', 'emerg3state', 'emerg3zip', 
                'emerg3country', 'emerg3homePhone', 'emerg3workPhone', 'emerg3mobilePhone', 
                'emerg3email', ]
    )
      
    emerg1name = schema.TextLine(
        title=_(u'Emergency Contact 1 Name'),
#        required=True,
        required=False,
    )

    emerg1addr1 = schema.TextLine(
        title=_(u'Emergency Contact 1 Address Line 1'),
#        required=True,
        required=False,
    )

    emerg1addr2 = schema.TextLine(
        title=_(u'Emergency Contact 1 Address Line 2'),
        required=False,
    )

    emerg1city = schema.TextLine(
        title=_(u'Emergency Contact 1 City'),
#        required=True,
        required=False,
    )

    emerg1state = schema.TextLine(
        title=_(u'Emergency Contact 1 State'),
#        required=True,
        required=False,
    )

    emerg1zip = schema.TextLine(
        title=_(u'Emergency Contact 1 Zip Code'),
#        required=True,
        required=False,
    )

    emerg1country = schema.TextLine(
        title=_(u'Emergency Contact 1 Country'),
#        required=True,
        required=False,
    )

    emerg1homePhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
#        required=True,
        required=False,
    )

    emerg1workPhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Work Phone'),
        description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
        #write_permission="UWOshOIE: Modify revisable fields",
        required=False,
    )

    emerg1mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Mobile Phone'),
        description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1email = schema.TextLine(
        title=_(u'Emergency Contact 1 Email'),
        description=_(u'Strongly recommended'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2name = schema.TextLine(
        title=_(u'Emergency Contact 2 Name'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2addr1 = schema.TextLine(
        title=_(u'Emergency Contact 2 Address Line 1'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2addr2 = schema.TextLine(
        title=_(u'Emergency Contact 2 Address Line 2'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2city = schema.TextLine(
        title=_(u'Emergency Contact 2 City'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2state = schema.TextLine(
        title=_(u'Emergency Contact 2 State'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2zip = schema.TextLine(
        title=_(u'Emergency Contact 2 Zip Code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2country = schema.TextLine(
        title=_(u'Emergency Contact 2 Country'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2homePhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2workPhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Work Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2email = schema.TextLine(
        title=_(u'Emergency Contact 2 Email'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3name = schema.TextLine(
        title=_(u'Emergency Contact 3 Name'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3addr1 = schema.TextLine(
        title=_(u'Emergency Contact 3 Address Line 1'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3addr2 = schema.TextLine(
        title=_(u'Emergency Contact 3 Address Line 2'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3city = schema.TextLine(
        title=_(u'Emergency Contact 3 City'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3state = schema.TextLine(
        title=_(u'Emergency Contact 3 State'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3zip = schema.TextLine(
        title=_(u'Emergency Contact 3 Zip Code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3country = schema.TextLine(
        title=_(u'Emergency Contact 3 Country'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3homePhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3workPhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Work Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3email = schema.TextLine(
        title=_(u'Emergency Contact 3 Email'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    programName = schema.Choice(
        title=_(u'Program Name'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.programs',
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields", 
    )

    programYear = schema.TextLine(
#    programYear = schema.Int(
        title=_(u'Program Year'),
        description=_(u'Enter the year you will actually be attending the program (YYYY)'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    programSemester = schema.Choice(
        title=_(u'Semester'),
        vocabulary=SimpleVocabulary([SimpleTerm(value='Fall'),SimpleTerm(value='Fall Interim'),SimpleTerm(value='Spring'),SimpleTerm(value='Spring Interim'),SimpleTerm(value='Summer')]),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'education',
        label=_(u"Education"),
        fields=['studentType', 'universityEnrolled', 'graduationMonth', 'graduationYear', 
                'cumulativeGPA', 'major1', 'major2', 'minor1', 'minor2', 'emphasis1', 'emphasis2', ]
    )
      
    studentType = schema.Choice(
        title=_(u'Student Type'),
        vocabulary=SimpleVocabulary([SimpleTerm(value='UW Oshkosh Freshman'),SimpleTerm(value='UW Oshkosh Sophomore'),SimpleTerm(value='UW Oshkosh Junior'),SimpleTerm(value='UW Oshkosh Senior'),SimpleTerm(value='UW Oshkosh Graduate Student'),SimpleTerm(value='Student at another University (please complete and submit the "Special Student" form)'),SimpleTerm(value='I am not a Student (please complete and submit the "Special Student" form)')]),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    universityEnrolled = schema.TextLine(
        title=_(u'Name of other university'),
        description=_(u'No abbreviations please'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    graduationMonth = schema.Choice(
        title=_(u'Expected Graduation Month'),
        vocabulary=month_vocabulary,
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    graduationYear = schema.TextLine(
#    graduationYear = schema.Int(
        title=_(u'Expected Graduation Year'),
        description=_(u'YYYY (use ''0000'' if not a student)'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    cumulativeGPA = schema.Float(
        title=_(u'Cumulative GPA'),
        description=_(u'out of 4.0 (use 0.0 if not a student)'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    major1 = schema.Choice(
        title=_(u'First Major'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.majors',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    major2 = schema.Choice(
        title=_(u'Second Major'),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.majors',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    minor1 = schema.TextLine(
        title=_(u'Minor 1'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    minor2 = schema.TextLine(
        title=_(u'Minor 2'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    emphasis1 = schema.TextLine(
        title=_(u'Emphasis/Licensure 1'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    emphasis2 = schema.TextLine(
        title=_(u'Emphasis/Licensure 2'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'transportation',
        label=_(u"Transportation"),
        fields=['willTakeBus', 'willFlyWithGroup', 'departureDate', 'returnDate', 'agreeToCosts']
    )

    willTakeBus = schema.Choice(
        title=_(u'Bus'),
        description=_(u'Please note: while a group bus is an option for most programs, not all programs offer this option.'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
        vocabulary=SimpleVocabulary([SimpleTerm(value='I will take the group bus from Oshkosh to the airport'),SimpleTerm(value=
                                                                                                                          'I will arrange for my own transportation from Oshkosh to the airport.')]),
    )

    willFlyWithGroup = schema.Choice(
        title=_(u'Flights'),
#        required=True,
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='I will fly with the group'),SimpleTerm(value='I will deviate from the group itinerary')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    departureDate = schema.Date(
        title=_(u'Planned Departure Date'),
        description=_(u'Specify if you are deviating from the group itinerary.'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    returnDate = schema.Date(
        title=_(u'Planned Return Date'),
        description=_(u'Specify if you are deviating from the group itinerary.'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    agreeToCosts = schema.TextLine(
        description=_(u'I understand that if I choose not to fly on dates recommended by the OIE or by my hosts abroad, I remain responsible for the full program cost, regardless of whether I participate in all events or make use of all services. Enter your initials'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'orientation',
        label=_(u"Orientation"),
        fields=['orientationDate1', 'orientationHours1', 'orientationDate2', 'orientationHours2', 
                'numberOfGuests', 'orientationConflict', 'conflictDate']
    )

    orientationDate1 = schema.Date(
        title=_(u'I will attend the family orientation on'),
        description=_(u'Enter one date and time for the four-hour session, or enter two dates and times for the two-hour sessions'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationHours1 = schema.Choice(
        title=_(u'Orientation Session 1 \"hours\"'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.session_hours',
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationDate2 = schema.Date(
        title=_(u'Orientation Session part 2 (Date)'),
        description=_(u'if applicable'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationHours2 = schema.Bool(
        title=_(u'Will attend orientation Session part 2 from 3pm - 5pm'),
        description=_(u'if applicable'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    numberOfGuests = schema.TextLine(
#    numberOfGuests = schema.Int(
        title=_(u'Number of Guests'),
        description=_(u'The following number of people will attend with me'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    orientationConflict = schema.Choice(
        title=_(u''),
        description=_(u'Do you have a conflict with any of the other pre-travel academic and/or orientation sessions?'),
#        required=True,
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='No'),SimpleTerm(value='Yes, I have a conflict on (enter the date next):'),SimpleTerm(value='No dates are listed')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    conflictDate = schema.Date(
        title=_(u'Date of your conflict'),
        description=_(u'if you selected Yes above'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'courses',
        label=_(u"Courses"),
        fields=['subject1', 'course1', 'credits1', 'subject2', 'course2', 'credits2', 'subject3', 
                'course3', 'credits3', 'subject4', 'course4', 'credits4', 'subject5', 'course5', 
                'credits5', 'subject6', 'course6', 'credits6', 'readSyllabus', 'enrolledIS333', ]
    )

    subject1 = schema.Choice(
        title=_(u'Course 1 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course1 = schema.TextLine(
        title=_(u'Course Number 1'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits1 = schema.Float(
        title=_(u'Credits 1'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject2 = schema.Choice(
        title=_(u'Course 2 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course2 = schema.TextLine(
        title=_(u'Course Number 2'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits2 = schema.Float(
        title=_(u'Credits 2'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject3 = schema.Choice(
        title=_(u'Course 3 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course3 = schema.TextLine(
        title=_(u'Course Number 3'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits3 = schema.Float(
        title=_(u'Credits 3'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject4 = schema.Choice(
        title=_(u'Course 4 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course4 = schema.TextLine(
        title=_(u'Course Number 4'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits4 = schema.Float(
        title=_(u'Credits 4'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject5 = schema.Choice(
        title=_(u'Course 5 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course5 = schema.TextLine(
        title=_(u'Course Number 5'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits5 = schema.Float(
        title=_(u'Credits 5'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject6 = schema.Choice(
        title=_(u'Course 6 subject'),
#        required=True,
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course6 = schema.TextLine(
        title=_(u'Course Number 6'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits6 = schema.Float(
        title=_(u'Credits 6'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    readSyllabus = schema.Bool(
        title=_(u'Has Read Syllabus'),
        description=_(u'I have read the syllabus for the one-credit course International Studies 333'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    enrolledIS333 = schema.Bool(
        title=_(u'Enroll me in International Studies 333'),
        description=_(u'You will only be enrolled if you have read the syllabus'),
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'financial_aid',
        label=_(u"Financial Aid"),
        fields=['applyForAid', 'holdApplication', 'financialAidGranted']
    )

    applyForAid = schema.Choice(
        title=_(u'Are you applying for financial aid?'),
        description=_(u'If you are not applying for financial aid, skip to the next section.'),
#        required=True,
        required=False,
        vocabulary=yes_no_none_vocabulary,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    holdApplication = schema.Choice(
        title=_(u'Should the OIE hold or process your application?'),
        description=_(u'HOLD your Study Abroad Application (i.e. you will only study abroad IF financial aid is available; at this point the application fee is still refundable but the OIE is not reserving a seat for you), or PROCESS your Study Abroad Applciation (i.e. you will study abroad regardless of your aid package; at this point the application fee is non-refundable and the OIE will reserve your seat.'),
#        required=True,
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='HOLD'),SimpleTerm(value='PROCESS')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    financialAidGranted = schema.Bool(
        title=_(u'Financial Aid Granted?'),
        description=_(u'Set by Financial Aid staff only'),
        required=False,
        #write_permission="UWOshOIE: Modify Financial Aid fields",
    )

    model.fieldset(
        'accommodation_preferences',
        label=_(u"Accommodation Preferences"),
        fields=['roomType', 'roommateName1', 'roommateName2', ]
    )

    roomType = schema.Choice(
        title=_(u'Room Type'),
#        required=True,
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Single Room'),SimpleTerm(value='Double Room'),SimpleTerm(value='Triple Room')]),
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    roommateName1 = schema.TextLine(
        title=_(u'Roommate 1 Name'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    roommateName2 = schema.TextLine(
        title=_(u'Roommate 2 Name'),
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    model.fieldset(
        'expectations',
        label=_(u"Expectations"),
        fields=['questionExpectations', ]
    )

    questionExpectations = schema.Text(
        title=_(u'Your Expectations For'),
        description=_(u'a) this program as a whole? <br> b) the pre-travel general orientation session? <br> c) the pre-travel academic sessions? <br> d) your hosts (host institution, family, etc.) in the foreign country (if applicable)?'),
#        required=True,
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    model.fieldset(
        'verification',
        label=_(u"Verification"),
        fields=['awareOfAllMaterials', 'UWOshkoshRelease', 'certification', ]
    )

    awareOfAllMaterials = schema.Choice(
        title=_(u'Are you aware of the application requirements for your program?'),
        description=_(u'Additional application requirements for select programs are listed on individual program web pages.  Not all programs have additional requirements.'),
#        required=True,
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes, I am aware of the application requirements for my program'),SimpleTerm(value='There are no additional application requirements for my program')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    UWOshkoshRelease = schema.Choice(
        title=_(u'Release of Liability'),
        description=_(u'I hereby agree to hold harmless and indemnify the Board of Regents of the University of Wisconsin System and the University of Wisconsin Oshkosh, their officers, agents and employees, from any and all liability, loss, damages, costs or expenses which are sustained, incurred or required arising out of my actions.'),
#        required=True,
        required=False,
        vocabulary=yes_no_none_vocabulary,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    certification = schema.Choice(
        title=_(u'Certification'),
        description=_(u'I certify that the information stated above is true and correct.  If accepted to the program, I agree to follow all payment and withdrawal policies and to regularly check my UW Oshkosh email account for program information beginning today.  If I am a non-UW Oshkosh student, I will use and submit an email address that I check regularly.'),
#        required=True,
        required=False,
        vocabulary=yes_no_none_vocabulary,
        #write_permission="UWOshOIE: Modify normal fields",
    )


#########################
#OFFICE USE ONLY SECTION
#########################

    model.fieldset(
        'office_use_only',
        label=_(u"OFFICE USE ONLY"),
        fields=['seatNumber', 'completionDate', 'applicationIsComplete', 
                'comments', 'applicationFeeOK', 'UWSystemStatementOK', 'UWOshkoshStatementOK', 
                'withdrawalRefund', 'transcriptsOK', 'programSpecificMaterialsRequired', 
                'programSpecificMaterialsOK', 'specialStudentFormRequired', 
                'specialStudentFormOK', 'creditOverloadFormRequired', 'creditOverloadFormOK', 
                'medicalOK', 'medicalForm', 'passportOK', 'metPassportDeadline', 
                'programSpecificMaterialsRequiredStepIII', 'programSpecificMaterialsOKStepIII', 
                'attendedOrientation', 'cisiDates', 'cisiNumberOfMonths', 'programFee', 
                'tuitionPayment', 'depositOnTime', 'payment2OnTime', 'applicationFeeRefund', 
                'foreignCourse1', 'foreignCourse2', 'foreignCourse3', 'foreignCourse4', 
                'foreignCourse5', 'foreignCourse6', 'papersOK', 'noMoreMaterials', 
                'programMaterials', 'programFee2', ]
    )

    seatNumber = schema.TextLine(
        title=_(u'Seat Number'),
        required=False,
    )

    completionDate = schema.Date(
        title=_(u'Date Application Was Completed'),
        description=_(u'This is the date in which the application was completed.'),
        required=False,
    )

    applicationIsComplete = schema.Bool(
        title=_(u'Application is Complete'),
        required=False,
    )

    comments = schema.Text(
        title=_(u'Comments'),
        required=False,
    )

    applicationFeeOK = schema.Bool(
        title=_(u'Application Fee Submitted'),
        required=False,
    )

    UWSystemStatementOK = schema.Bool(
        title=_(u'UW System Statement of Responsibility Submitted'),
        required=False,
    )

    UWOshkoshStatementOK = schema.Bool(
        title=_(u'UW Oshkosh Statement of Responsibility Submitted'),
        description=_(u'This is the date in which the application was completed.'),
        required=False,
    )

    withdrawalRefund = schema.Bool(
        title=_(u'Withdrawal and Refund Form Submitted'),
        required=False,
    )

    transcriptsOK = schema.Bool(
        title=_(u'Transcripts Submitted'),
        required=False,
    )

    programSpecificMaterialsRequired = schema.Choice(
        title=_(u'Program-Specific Materials Required(Step II)?'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    programSpecificMaterialsOK = schema.Bool(
        title=_(u'Program-Specific Materials Submitted(Step II)'),
        required=False,
    )

    specialStudentFormRequired = schema.Choice(
        title=_(u'Special Student Form Required'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    specialStudentFormOK = schema.Bool(
        title=_(u'Special Student Form Submitted'),
        required=False,
    )

    creditOverloadFormRequired = schema.Choice(
        title=_(u'Credit Overload Form Required'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    creditOverloadFormOK = schema.Bool(
        title=_(u'Credit Overload Form Submitted'),
        required=False,
    )

    medicalOK = schema.Bool(
        title=_(u'Medical information is Submitted/Updated'),
        required=False,
    )

    medicalForm = schema.Text(
        title=_(u'Medical Form'),
        required=False,
    )

    passportOK = schema.Bool(
        title=_(u'Passport information or receipt submitted'),
        required=False,
    )

    metPassportDeadline = schema.Choice(
        title=_(u'Passport Deadline Met'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    programSpecificMaterialsRequiredStepIII = schema.Choice(
        title=_(u'Program-Specific Materials Required(Step III)?'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    programSpecificMaterialsOKStepIII = schema.Bool(
        title=_(u'Program-Specific Materials Submitted(Step III)'),
        required=False,
    )

    attendedOrientation = schema.Choice(
        title=_(u'Attended Orientation'),
        required=False,
        vocabulary=yes_no_none_vocabulary
    )

    cisiDates = schema.TextLine(
        title=_(u'Health Insurance Dates'),
        description=_(u'Cultural Insurance Services International'),
        required=False,
    )

    cisiNumberOfMonths = schema.TextLine(
#    cisiNumberOfMonths = schema.Int(
        title=_(u'Health Insurance Number of Months'),
        description=_(u'Cultural Insurance Services International'),
        required=False,
    )

    programFee = schema.Float(
        title=_(u'Program Fee'),
        description=_(u''),
        required=False,
    )

    tuitionPayment = schema.Float(
        title=_(u'Tuition Payment (student exchange only)'),
        description=_(u''),
        required=False,
    )

    depositOnTime = schema.Choice(
        title=_(u'Deposit Paid on Time'),
        description=_(u''),
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )

    payment2OnTime = schema.Choice(
        title=_(u'Final Payment Made on Time (except exchange students)'),
        description=_(u''),
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )

    applicationFeeRefund = schema.Choice(
        title=_(u'Application Fee Refunded'),
        description=_(u''),
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )

    foreignCourse1 = schema.TextLine(
        title=_(u'Foreign institution course 1'),
        description=_(u''),
        required=False,
    )

    foreignCourse2 = schema.TextLine(
        title=_(u'Foreign institution course 2'),
        description=_(u''),
        required=False,
    )

    foreignCourse3 = schema.TextLine(
        title=_(u'Foreign institution course 3'),
        description=_(u''),
        required=False,
    )

    foreignCourse4 = schema.TextLine(
        title=_(u'Foreign institution course 4'),
        description=_(u''),
        required=False,
    )

    foreignCourse5 = schema.TextLine(
        title=_(u'Foreign institution course 5'),
        description=_(u''),
        required=False,
    )

    foreignCourse6 = schema.TextLine(
        title=_(u'Foreign institution course 6'),
        description=_(u''),
        required=False,
    )

    papersOK = schema.Bool(
        title=_(u'Papers information is OK'),
        description=_(u''),
        required=False,
    )

    noMoreMaterials = schema.Bool(
        title=_(u'No More Materials'),
        description=_(u''),
        required=False,
    )

    programMaterials = schema.Bool(
        title=_(u'Program Materials'),
        description=_(u''),
        required=False,
    )

    programFee2 = schema.TextLine(
#    programFee2 = schema.Int(
        title=_(u'Program Fee 2'),
        description=_(u''),
        required=False,
    )


class IOIEStudyAbroadProgram(Interface):

    title = schema.TextLine(
        title=_(u'Program Title'),
        description=_(u'The full Program Title will be displayed in all OIE print and on-line marketing and in all official OIE program-related materials.  To avoid confusion and increase "brand" awareness for your program, consistently use this program name in full, exactly as it appears here, in your print and electronic media.  Do not include country or city names in this field.'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        description=_(u'This is the description that will be used to promote your program.  Your description should capture the purpose of your program, include an overview of what students will be engaged in while abroad/away, and capture students’ interest! '),
        required=False,
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
        description=_(u'Comments entered here are visible by all OIE users.'),
        required=False,
    )

    model.fieldset(
        'program_code_fieldset',
        label=_(u"Program Code"),
        fields=['calendar_year', 'term', 'college_or_unit', 'countries', 'program_code',]
    )

    calendar_year = schema.TextLine(
        title=_(u'Calendar Year'),
        description=_(u'Use the year during which the program runs; this is not the year that is associated with the term of study.  For example, a January interim program running from Jan 2-28, 2017 will be associated with "2017".   A program running Dec 28, 2016-Jan 28, 2017 will also be associated with "2017".'),
        required=True,
    )

    term = schema.TextLine(
        title=_(u'Term'),
        description=_(u''),
        required=True,
    )

    college_or_unit = schema.TextLine(
        title=_(u'College or Unit'),
        description=_(u''),
        required=True,
    )

    countries = schema.Choice(
        title=_(u'Country or Countries'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries',
    )

    program_code = schema.TextLine(
        title=_(u'Program Code'),
        description=_(u'(auto-generated)'),
        required=True,
    )

    model.fieldset(
        'academic_program_fieldset',
        label=_(u"Academic Program"),
        fields=[]
    )

    sponsoring_unit_or_department = schema.TextLine(
        title=_(u'Sponsoring Unit or Department'),
        description=_(u'Select all that apply.'),
        required=True,
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

    learning_objectives = schema.Text(
        title=_(u'Learning Objectives'),
        description=_(u'State the learning objectives for this program.  Include only one learning objective per text field. These learning objectives will be included in end-of-program assessment and may be used to support Higher Learning Commission and other accreditation processes.'),
        required=False,
    )

    equipment_and_space = schema.Choice(
        title=_(u'Equipment & Space'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.equipment_and_space',
    )

    equipment_and_space_needs = schema.Text(
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




#"Syllabus & Other Supporting Documents
#Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel."
#"Number of Credits to be Earned by Each Applicant
#Minimum
#Maximum"
#"Language of Study
#Select all that apply.  Contact the Office of International Education to add a language (abroad@uwosh.edu)."
#"Cooperating Partners
#Only entities listed on the UW System Preferred Provider List or academic institutions with a current affiliation agreement with UWO may be selected here.  All other cooperating partners must be selected by following UW System procurement policies."
