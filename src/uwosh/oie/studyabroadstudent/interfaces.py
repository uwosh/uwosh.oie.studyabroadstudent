# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

subjects_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='History'),
        SimpleTerm(value='Math'),
    ]
)

sessionhours_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='09:00-11:00'),
        SimpleTerm(value='15:00-17:00'),
    ]
)

major_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='History'),
        SimpleTerm(value='Arts'),
    ]
)

minor_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='Minor 1'),
        SimpleTerm(value='Minor 2'),
    ]
)

program_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='Basking in the Sun'),
        SimpleTerm(value='European Odyssey'),
    ]
)

ethnicity_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'no answer', title=u'no answer'),
        SimpleTerm(value=u'Caucasian', title=u'Caucasian'),
        SimpleTerm(value=u'African-American', title=u'African-American'),
        SimpleTerm(value=u'Hispanic', title=u'Hispanic'),
        SimpleTerm(value=u'Native American', title=u'Native American'),
        SimpleTerm(value=u'Asian/Pacific Islander', title=u'Asian/Pacific Islander'),
        SimpleTerm(value=u'Other', title=u'Other'),
    ]
)

marriage_status_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Married', title=u'Married'),
        SimpleTerm(value=u'Single', title=u'Single'),
    ]
)

gender_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'Male', title=_(u'Male')),
     SimpleTerm(value=u'Female', title=_(u'Female')),
     SimpleTerm(value=u'Other', title=_(u'Other'))]
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

state_residency_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'Wisconsin', title=_(u'Wisconsin')),
     SimpleTerm(value=u'Minnesota', title=_(u'Minnesota')),
     SimpleTerm(value=u'Other', title=_(u'Other'))]
)

citizenship_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'U.S. Citizen', title=_(u'U.S. Citizen')),
     SimpleTerm(value=u'Permanent U.S. Resident', title=_(u'Permanent U.S. Resident')),
     SimpleTerm(value=u'Other Citizenship', title=_(u'Other Citizenship'))]
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
        title=_(u'UWOshOIE_label_middleName'),
        description=_(u'Middle Name'),
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

    localAddr1 = schema.TextLine(
        title=_(u'Local Address Line 1'),
        #schemata="Addresses",
        required=True,
    )

    localAddr2 = schema.TextLine(
        title=_(u'Local Address Line 2'),
        #schemata="Addresses",
        required=False,
    )

    localCity = schema.TextLine(
        title=_(u'Local City'),
        #schemata="Addresses",
        required=True,
    )

    localState = schema.TextLine(
        title=_(u'Local State'),
        default=_(u'WI'),
        #schemata="Addresses",
        required=True,
    )

    localZip = schema.TextLine(
        title=_(u'Local Zip Code'),
        default=_(u'54901'),
        #schemata="Addresses",
        required=True,
    )

    localCountry = schema.TextLine(
        title=_(u'Local Country'),
        description=_(u'tringWidge'),
        default=_(u'USA'),
        #schemata="Addresses",
        required=True,
    )

    localPhone = schema.TextLine(
        title=_(u'Local Telephone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Addresses",
        required=True,
    )

    mobilePhone = schema.TextLine(
        title=_(u'Mobile (cell) phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Addresses",
        required=False,
    )

    homeAddr1 = schema.TextLine(
        title=_(u'Home Address Line 1'),
        #schemata="Addresses",
        required=True,
    )

    homeAddr2 = schema.TextLine(
        title=_(u'Home Address Line 2'),
        #schemata="Addresses",
        required=False,
    )

    homeCity = schema.TextLine(
        title=_(u'Home City'),
        description=_(u''),
        #schemata="Addresses",
        required=True,
    )

    homeState = schema.TextLine(
        title=_(u'Home State'),
        description=_(u''),
        #schemata="Addresses",
        required=True,
    )

    homeZip = schema.TextLine(
        title=_(u'Home Zip Code'),
        description=_(u''),
        #schemata="Addresses",
        required=True,
    )

    homeCountry = schema.TextLine(
        title=_(u'Home Country'),
        description=_(u'tringWidge'),
        #schemata="Addresses",
        required=True,
    )

    homePhone = schema.TextLine(
        title=_(u'Home Telephone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Addresses",
        required=True,
    )

    citizenship = schema.Choice(
        title=_(u'Citizenship'),
        description=_(u'field description'),
        vocabulary=citizenship_vocabulary,
        #schemata="Demographics",
        required=True,
    )

    citizenshipOther = schema.TextLine(
        title=_(u'Other Citizenship Country'),
        description=_(u'Enter country of citizenship if you selected Other'),
        #schemata="Demographics",
        required=False,
    )

    stateResidency = schema.Choice(
        title=_(u'State Residency'),
        description=_(u''),
        #schemata="Demographics",
        vocabulary=state_residency_vocabulary,
        required=True,
    )

    stateResidencyOther = schema.TextLine(
        title=_(u'Other State Residency'),
        description=_(u'Enter state of residency if you selected Other'),
        #schemata="Demographics",
        required=False,
    )

    dateOfBirth_year = schema.Int(
        title=_(u'Birthday (Year)'),
        description=_(u'Birthday (Year, YYYY)'),
        #schemata="Demographics",
        required=True,
    )

    dateOfBirth_month = schema.Choice(
        title=_(u'Birthday (Month)'),
        description=_(u'Birthday (Month)'),
        #schemata="Demographics",
        vocabulary=month_vocabulary,
        required=True,
    )

    dateOfBirth_day = schema.Choice(
        title=_(u'Birthday (Day)'),
        description=_(u'Birthday (Day)'),
        #schemata="Demographics",
        vocabulary=dayofmonth_vocabulary,
        required=True,
    )

    placeOfBirth = schema.TextLine(
        title=_(u'Place of Birth'),
        description=_(u'Enter city, state, and country'),
        #schemata="Demographics",
        required=True,
    )

    gender = schema.Choice(
        title=_(u'Gender'),
        description=_(u''),
        #schemata="Demographics",
        vocabulary=gender_vocabulary,
        required=False,
    )

    marriageStatus = schema.Choice(
        title=_(u'Marital Status'),
        description=_(u''),
        #schemata="Demographics",
        vocabulary=marriage_status_vocabulary,
        required=False,
    )

    ethnicity = schema.Choice(
        title=_(u'Ethnicity'),
        description=_(u''),
        #schemata="Demographics",
        vocabulary=ethnicity_vocabulary,
        required=False,
    )

    passportName = schema.TextLine(
        title=_(u'Passport Full Name'),
        description=_(u'Enter your full name EXACTLY as it appears on your passport or passport application'),
        #schemata="Passport",
        required=False,
    )

    passportNumber = schema.TextLine(
        title=_(u'Passport Number'),
        description=_(u''),
        #schemata="Passport",
        required=False,
    )

    passportIssueOffice = schema.TextLine(
        title=_(u'Passport Issuing Office'),
        description=_(u'E.g. New Orleans or U.S. Department of State'),
        #schemata="Passport",
        required=False,
    )

    passportExpDate_year = schema.TextLine(
        title=_(u'Passport Expiry Year'),
        description=_(u'UWOshOIE_label_passportExpDate_year'),
        #schemata="Demographics",
        required=False,
    )

    passportExpDate_month = schema.Choice(
        title=_(u'Passport Expiry Month'),
        description=_(u'UWOshOIE_label_passportExpDate_month'),
        #schemata="Demographics",
        vocabulary=month_vocabulary,
        required=False,
    )

    passportExpDate_day = schema.Choice(
        title=_(u'Passport Expiry Day'),
        #schemata="Demographics",
        vocabulary=dayofmonth_vocabulary,
        required=False,
    )

    questionAcadCareerPlan = schema.Text(
        title=_(u'Academic and Career Plan'),
        description=_(u'a) Briefly, what are your short- and long-term academic and career goals? <br> b) Why would you like to participate in this program? <br> c) What do you expect to gain from your experience?'),
        #schemata="Additional Questions",
        required=True,
    )

    questionLangCulturalSkills = schema.Text(
        title=_(u'Language and Cultural Skills'),
        description=_(u'a) Have you studied a foreign language? If so, what is your level of fluency? <br> b) Have you completed any University-level courses on the culture or history of your destination? If so, explain. <br> c) Have you ever been immersed in a language and/or culture abroad? If so, please explain. <br> d) Do you plan to use a foreign language in a professional setting? If yes, please explain.'),
        #schemata="Additional Questions",
        required=True,
    )

    questionPrevTravel = schema.Text(
        title=_(u'Previous Travel Experience'),
        description=_(u'Have you traveled abroad? If so, list the places to which you have traveled along with the dates and purpose.'),
        #schemata="Additional Questions",
        required=True,
    )

    questionWorkExp = schema.Text(
        title=_(u'Work Experience'),
        description=_(u'a) Who is your current employer? <br> b) If relevant to your study abroad program, list and describe your responsibilities from current and previous jobs.'),
        #schemata="Additional Questions",
        required=True,
    )

    questionEuroBizTravSem = schema.Text(
        title=_(u'European Business Travel Seminar Only'),
        description=_(u'Include the name of the company(ies) you are currently working for and your title(s).'),
        #schemata="Additional Questions",
        required=False,
    )

    questionStuExchComp = schema.Text(
        title=_(u'Student Exchange and Competitive Programs Only'),
        description=_(u'Add anything else you think we should consider when reviewing your application.'),
        #schemata="Additional Questions",
        required=False,
    )

    doctorLastname = schema.TextLine(
        title=_(u'Last Name of your Family Doctor'),
        #schemata="Medical",
        required=True,
    )

    doctorFirstname = schema.TextLine(
        title=_(u'First Name of your Family Doctor'),
        #schemata="Medical",
        required=True,
    )

    doctorPhone = schema.TextLine(
        title=_(u'Doctor''s Phone Number'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Medical",
        required=True,
    )

    medicalInsuranceCompany = schema.TextLine(
        title=_(u'Name of Insurance Company'),
        #schemata="Medical",
        required=True,
    )

    medicalPolicyHolder = schema.TextLine(
        title=_(u'Name of Policy Holder'),
        description=_(u'UWOshOIE_label_medicalPolicyHolder'),
        #schemata="Medical",
        required=True,
    )

    medicalPolicyGroupNumber = schema.TextLine(
        title=_(u'Policy / Group Number'),
        #schemata="Medical",
        required=True,
    )

    foodAllergies = schema.TextLine(
        title=_(u'Allergies'),
        description=_(u'List any allergies (food, pet, etc.)'),
        #schemata="Medical",
        required=False,
    )

    hasDifficultyWalking = schema.Choice(
        title=_(u'Difficulty Walking'),
        description=_(u'Do you have a condition which would make it difficult to walk long distances?'),
        #schemata="Medical",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'), SimpleTerm(value='No')]),
        required=True,
    )

    maxWalkingDistance = schema.Int(
        description=_(u'Max Walking Distance'),
        title=_(u'If so, what is the maximum number of minutes you can walk?'),
        #schemata="Medical",
        required=False,
    )

    medicalReadStatement = schema.Choice(
        title=_(u'I have read the statement below and understand.'),
        description=_(u'""Pre-existing medical and mental health conditions are often intensified by travel to or living in a foreign environment.  Before committing to a study abroad program, consider how your new environment may affect your personal health both physically and mentally.  For example, your new environment may introduce you to new diseases, such as malaria or yellow fever, or new stresses which may cause additional complications for a person with a preexisting condition.<br> <br> The OIE strongly recommends that you have a physical, talk with a medical provider about any preexisting conditions and recommended and/or required immunizations, talk with a psychiatrist or counselor about any preexisting conditions and take care of any dental work before departure.<br> <br> If you choose not to complete this section before program acceptance, you must forward information related to the following to the OIE within one week of the application deadline for your program.  Failure to disclose medical or mental health conditions will make it extremely difficult for staff at UW Oshkosh and abroad to assist you in an emergency and may cause health professionals abroad to take actions which could lead to serious medical consequences, including death.<br> <br> NOTE ON MEDICATIONS: You are responsible for ensuring that your medications can be carried into the foreign country.  If your medical status changes after completing this application, you must inform the OIE.""'),
        #schemata="Medical II",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'), SimpleTerm(value='No')]),
        required=True,
    )

    medicalHealthProblems = schema.Text(
        title=_(u'Health Problems'),
        description=_(u'List and describe any recent (within the past five years) or continuing health problems, including physical disabilities or medical conditions; learning disabilities; drug, plant, food, animal, or insect sting allergies (include information pertaining to reactions); and/or surgeries that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad. Complete this section now or by the Friday following the application deadline.  Write ''n/a'' in blanks where appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalHealthProblems_takenMedication = schema.Choice(
        title=_(u'Has Taken Medication'),
        description=_(u'Are you taking or have you ever taken medication related to your physical health?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'), SimpleTerm(value='No')]),
        required=False,
    )

    medicalHealthProblems_medications = schema.Text(
        title=_(u'Medication List'),
        description=_(u'If so, list the medications you have taken over the past year. Write ''n/a'' in blanks where appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalHealthProblems_stable = schema.Choice(
        title=_(u'Are you stable on this medication?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No'),SimpleTerm(value= 'n/a')]),
        required=False,
    )

    medicalHealthProblems_underCare = schema.Choice(
        title=_(u'Are you currently under the care of a doctor or other health care professional?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        required=False,
    )

    medicalHealthProblems_whatCondition = schema.Text(
        title=_(u''),
        description=_(u'If you are currently under the care of a doctor or other health care professional, for what condition? Write ''n/a'' in blanks where appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalHealthProblems_willingToPrescribe = schema.Choice(
        description=_(u'Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No'),SimpleTerm(value= 'n/a')]),
        required=False,
    )

    medicalHealthProblems_additionalInfo = schema.Text(
        title=_(u'Additional Health Info'),
        description=_(u'Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in blank if appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalMentalProblems = schema.Text(
        description=_(u'List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.'),
        #schemata="Medical III",
        required=False,
    )

    medicalMentalProblems_takenMedication = schema.Choice(
        description=_(u'UWOshOIE_label_medicalMentalProblems_takenMedication'),
        title=_(u'Are you taking/have you ever taken medication related to your mental health?  '),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        required=False,
    )

    medicalMentalProblems_medications = schema.Text(
        description=_(u'If so, list the medications taken over the past year. Write ''n/a'' in blanks where appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalMentalProblems_currentDose = schema.Text(
        description=_(u'What is the current dose? Write ''n/a'' in text area when appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalMentalProblems_stable = schema.Choice(
        description=_(u'UWOshOIE_label_medicalMentalProblems_stable'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No'),SimpleTerm(value= 'n/a')]),
        required=False,
    )

    medicalMentalProblems_underCare = schema.Choice(
        description=_(u'Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        required=False,
    )

    medicalMentalProblems_condition = schema.Text(
        description=_(u'If yes, for what condition? Write ''n/a'' in text area when appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalMentalProblems_enoughMedication = schema.Choice(
        description=_(u'Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No'),SimpleTerm(value= 'n/a')]),
        required=False,
    )

    medicalMentalProblems_additionalInfo = schema.Text(
        description=_(u'Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in text area if there isn''t any.'),
        #schemata="Medical III",
        required=False,
    )

    medicalRegistered = schema.Choice(
        description=_(u'Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        required=False,
    )

    medicalRegistered_office = schema.TextLine(
        description=_(u'If so, with which office have you registered? Write ''none'' in text area if you have not registered.'),
        #schemata="Medical III",
        required=False,
    )

    medicalRegistered_accommodations = schema.Text(
        title=_(u'Medical Authorized Accomodations'),
        description=_(u'What accommodations have been authorized for you? Write ''n/a'' in text area when appropriate.'),
        #schemata="Medical III",
        required=False,
    )

    medicalAccessOK = schema.Choice(
        title=_(u'Medical Access Granted'),
        description=_(u'""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""'),
        #schemata="Medical III",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        required=True,
    )

    smokingPreferred = schema.Choice(
        title=_(u'Smoking Preference'),
        #schemata="Preferences",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Smoking'),SimpleTerm(value='Non-smoking'),SimpleTerm(value='No Preference')]),
        default= 'No Preference',
        required=False,
    )

    isVegetarian = schema.Choice(
        title=_(u'Are you vegetarian?'),
        #schemata="Preferences",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        default="No",
    )

    additionalNeeds = schema.Text(
        title=_(u'Additional Needs'),
        description=_(u'Is there anything else your host families or the OIE should know about your accommodation needs?'),
        #schemata="Preferences",
        required=False,
    )

    emerg1name = schema.TextLine(
        title=_(u'Emergency Contact 1 Name'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1addr1 = schema.TextLine(
        title=_(u'Emergency Contact 1 Address Line 1'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1addr2 = schema.TextLine(
        title=_(u'Emergency Contact 1 Address Line 2'),
        #schemata="Emergency Contacts",
        required=False,
    )

    emerg1city = schema.TextLine(
        title=_(u'Emergency Contact 1 City'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1state = schema.TextLine(
        title=_(u'Emergency Contact 1 State'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1zip = schema.TextLine(
        title=_(u'Emergency Contact 1 Zip Code'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1country = schema.TextLine(
        title=_(u'Emergency Contact 1 Country'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1homePhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=True,
    )

    emerg1workPhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Work Phone'),
        description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
        #write_permission="UWOshOIE: Modify revisable fields",
        #schemata="Emergency Contacts",
        required=False,
    )

    emerg1mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 1 Mobile Phone'),
        description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1email = schema.TextLine(
        title=_(u'Emergency Contact 1 Email'),
        description=_(u'Strongly recommended'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2name = schema.TextLine(
        title=_(u'Emergency Contact 2 Name'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2addr1 = schema.TextLine(
        title=_(u'Emergency Contact 2 Address Line 1'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2addr2 = schema.TextLine(
        title=_(u'Emergency Contact 2 Address Line 2'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2city = schema.TextLine(
        title=_(u'Emergency Contact 2 City'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2state = schema.TextLine(
        title=_(u'Emergency Contact 2 State'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2zip = schema.TextLine(
        title=_(u'Emergency Contact 2 Zip Code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2country = schema.TextLine(
        title=_(u'Emergency Contact 2 Country'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2homePhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2workPhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Work Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 2 Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2email = schema.TextLine(
        title=_(u'Emergency Contact 2 Email'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3name = schema.TextLine(
        title=_(u'Emergency Contact 3 Name'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3addr1 = schema.TextLine(
        title=_(u'Emergency Contact 3 Address Line 1'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3addr2 = schema.TextLine(
        title=_(u'Emergency Contact 3 Address Line 2'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3city = schema.TextLine(
        title=_(u'Emergency Contact 3 City'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3state = schema.TextLine(
        title=_(u'Emergency Contact 3 State'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3zip = schema.TextLine(
        title=_(u'Emergency Contact 3 Zip Code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3country = schema.TextLine(
        title=_(u'Emergency Contact 3 Country'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3homePhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Home Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3workPhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Work Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mobilePhone = schema.TextLine(
        title=_(u'Emergency Contact 3 Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3email = schema.TextLine(
        title=_(u'Emergency Contact 3 Email'),
        #schemata="Emergency Contacts",
        required=False,
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    programName = schema.Choice(
        title=_(u'Program Name'),
        vocabulary=program_vocabulary,
        required=True,
        #write_permission="UWOshOIE: Modify normal fields", 
    )

    programYear = schema.Int(
        title=_(u'Program Year'),
        description=_(u'Enter the year you will actually be attending the program (YYYY)'),
        #schemata="default",
        required=True,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    programSemester = schema.Choice(
        title=_(u'Semester'),
        #schemata="default",
        vocabulary=SimpleVocabulary([SimpleTerm(value='Fall'),SimpleTerm(value='Fall Interim'),SimpleTerm(value='Spring'),SimpleTerm(value='Spring Interim'),SimpleTerm(value='Summer')]),
        required=True,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    studentType = schema.Choice(
        title=_(u'Student Type'),
        #schemata="Education",
        vocabulary=SimpleVocabulary([SimpleTerm(value='UW Oshkosh Freshman'),SimpleTerm(value='UW Oshkosh Sophomore'),SimpleTerm(value='UW Oshkosh Junior'),SimpleTerm(value='UW Oshkosh Senior'),SimpleTerm(value='UW Oshkosh Graduate Student'),SimpleTerm(value='Student at another University (please complete and submit the "Special Student" form)'),SimpleTerm(value='I am not a Student (please complete and submit the "Special Student" form)')]),
        required=True,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    universityEnrolled = schema.TextLine(
        title=_(u'Name of other university'),
        description=_(u'No abbreviations please'),
        #schemata="Education",
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    graduationMonth = schema.Choice(
        title=_(u'Expected Graduation Month'),
        #schemata="Education",
        vocabulary=month_vocabulary,
        required=True,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    graduationYear = schema.Int(
        title=_(u'Expected Graduation Year'),
        description=_(u'YYYY (use ''0000'' if not a student)'),
        required=True,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    cumulativeGPA = schema.Float(
        title=_(u'Cumulative GPA'),
        description=_(u'out of 4.0 (use 0.0 if not a student)'),
        required=True,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    major1 = schema.Choice(
        title=_(u'First Major'),
        required=True,
        vocabulary=major_vocabulary,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    major2 = schema.Choice(
        title=_(u'Second Major'),
        required=True,
        vocabulary=major_vocabulary,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    minor1 = schema.Choice(
        title=_(u'Minor 1'),
        required=False,
        #schemata="Education",
        vocabulary=minor_vocabulary,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    minor2 = schema.Choice(
        title=_(u'Minor 2'),
        required=False,
        #schemata="Education",
        vocabulary=minor_vocabulary,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    emphasis1 = schema.TextLine(
        title=_(u'Emphasis/Licensure 1'),
        required=False,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    emphasis2 = schema.TextLine(
        title=_(u'Emphasis/Licensure 2'),
        required=False,
        #schemata="Education",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    willTakeBus = schema.Choice(
        title=_(u'Bus'),
        description=_(u'Please note: while a group bus is an option for most programs, not all programs offer this option.'),
        required=True,
        #write_permission="UWOshOIE: Modify revisable fields",
        #schemata="Transportation",
        vocabulary=SimpleVocabulary([SimpleTerm(value='I will take the group bus from Oshkosh to the airport'),SimpleTerm(value=
                                                                                                                          'I will arrange for my own transportation from Oshkosh to the airport.')]),
    )

    willFlyWithGroup = schema.Choice(
        title=_(u'Flights'),
        required=True,
        #schemata="Transportation",
        vocabulary=SimpleVocabulary([SimpleTerm(value='I will fly with the group'),SimpleTerm(value='I will deviate from the group itinerary')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    departureDate = schema.Date(
        title=_(u'Planned Departure Date'),
        description=_(u'Specify if you are deviating from the group itinerary.'),
        required=False,
        #schemata="Transportation",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    returnDate = schema.Date(
        title=_(u'Planned Return Date'),
        description=_(u'Specify if you are deviating from the group itinerary.'),
        #schemata="Transportation",
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    agreeToCosts = schema.TextLine(
        description=_(u'I understand that if I choose not to fly on dates recommended by the OIE or by my hosts abroad, I remain responsible for the full program cost, regardless of whether I participate in all events or make use of all services. Enter your initials'),
        #schemata="Transportation",
        required=True,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationDate1 = schema.Date(
        title=_(u'I will attend the family orientation on'),
        description=_(u'Enter one date and time for the four-hour session, or enter two dates and times for the two-hour sessions'),
        required=True,
        #schemata="Orientation",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationHours1 = schema.Choice(
        title=_(u'Orientation Session 1 \"hours\"'),
        description=_(u''),
        vocabulary=sessionhours_vocabulary,
        required=True,
        #schemata="Orientation",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationDate2 = schema.Date(
        title=_(u'Orientation Session part 2 (Date)'),
        description=_(u'if applicable'),
        required=False,
        #schemata="Orientation",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    orientationHours2 = schema.Bool(
        title=_(u'Will attend orientation Session part 2 from 3pm - 5pm'),
        description=_(u'if applicable'),
        required=False,
        #schemata="Orientation",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    numberOfGuests = schema.Int(
        title=_(u'Number of Guests'),
        description=_(u'The following number of people will attend with me'),
        required=True,
        #schemata="Orientation",
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    orientationConflict = schema.Choice(
        title=_(u''),
        description=_(u'Do you have a conflict with any of the other pre-travel academic and/or orientation sessions?'),
        required=True,
        #schemata="Orientation",
        vocabulary=SimpleVocabulary([SimpleTerm(value='No'),SimpleTerm(value='Yes, I have a conflict on (enter the date next):'),SimpleTerm(value='No dates are listed')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    conflictDate = schema.Date(
        title=_(u'Date of your conflict'),
        description=_(u'if you selected Yes above'),
        #schemata="Orientation",
        required=False,
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject1 = schema.Choice(
        title=_(u'Course 1 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course1 = schema.TextLine(
        title=_(u'Course Number 1'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits1 = schema.Float(
        title=_(u'Credits 1'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject2 = schema.Choice(
        title=_(u'Course 2 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course2 = schema.TextLine(
        title=_(u'Course Number 2'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits2 = schema.Float(
        title=_(u'Credits 2'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject3 = schema.Choice(
        title=_(u'Course 3 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course3 = schema.TextLine(
        title=_(u'Course Number 3'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits3 = schema.Float(
        title=_(u'Credits 3'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject4 = schema.Choice(
        title=_(u'Course 4 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course4 = schema.TextLine(
        title=_(u'Course Number 4'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits4 = schema.Float(
        title=_(u'Credits 4'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject5 = schema.Choice(
        title=_(u'Course 5 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course5 = schema.TextLine(
        title=_(u'Course Number 5'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits5 = schema.Float(
        title=_(u'Credits 5'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    subject6 = schema.Choice(
        title=_(u'Course 6 subject'),
        required=True,
        vocabulary=subjects_vocabulary,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    course6 = schema.TextLine(
        title=_(u'Course Number 6'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    credits6 = schema.Float(
        title=_(u'Credits 6'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    readSyllabus = schema.Bool(
        title=_(u'Has Read Syllabus'),
        description=_(u'I have read the syllabus for the one-credit course International Studies 333'),
        required=True,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    enrolledIS333 = schema.Bool(
        title=_(u'Enroll me in International Studies 333'),
        description=_(u'You will only be enrolled if you have read the syllabus'),
        required=False,
        #schemata="Courses",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    applyForAid = schema.Choice(
        title=_(u'Are you applying for financial aid?'),
        description=_(u'If you are not applying for financial aid, skip to the next section.'),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        #schemata="Financial Aid",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    holdApplication = schema.Choice(
        title=_(u'Should the OIE hold or process your application?'),
        description=_(u'HOLD your Study Abroad Application (i.e. you will only study abroad IF financial aid is available; at this point the application fee is still refundable but the OIE is not reserving a seat for you), or PROCESS your Study Abroad Applciation (i.e. you will study abroad regardless of your aid package; at this point the application fee is non-refundable and the OIE will reserve your seat.'),
        required=True,
        #schemata="Financial Aid",
        vocabulary=SimpleVocabulary([SimpleTerm(value='HOLD'),SimpleTerm(value='PROCESS')]),
        #write_permission="UWOshOIE: Modify normal fields",
    )

    financialAidGranted = schema.Bool(
        title=_(u'Financial Aid Granted?'),
        description=_(u'Set by Financial Aid staff only'),
        required=False,
        #schemata="Financial Aid",
        #write_permission="UWOshOIE: Modify Financial Aid fields",
    )

    roomType = schema.Choice(
        title=_(u'Room Type'),
        description=_(u'UWOshOIE_label_roomType'),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Single Room'),SimpleTerm(value='Double Room'),SimpleTerm(value='Triple Room')]),
        #schemata="Accommodation Preferences",
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    roommateName1 = schema.TextLine(
        title=_(u'Roommate 1 Name'),
        required=False,
        #schemata="Accommodation Preferences",
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    roommateName2 = schema.TextLine(
        title=_(u'Roommate 2 Name'),
        required=False,
        #schemata="Accommodation Preferences",
        #write_permission="UWOshOIE: Modify revisable fields",
    )

    questionExpectations = schema.Text(
        title=_(u'Your Expectations For'),
        description=_(u'a) this program as a whole? <br> b) the pre-travel general orientation session? <br> c) the pre-travel academic sessions? <br> d) your hosts (host institution, family, etc.) in the foreign country (if applicable)?'),
        required=True,
        #schemata="Expectations",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    awareOfAllMaterials = schema.Choice(
        title=_(u'Are you aware of the application requirements for your program?'),
        description=_(u'Additional application requirements for select programs are listed on individual program web pages.  Not all programs have additional requirements.'),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes, I am aware of the application requirements for my program'),SimpleTerm(value='There are no additional application requirements for my program')]),
        #schemata="Verification",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    UWOshkoshRelease = schema.Choice(
        title=_(u'Release of Liability'),
        description=_(u'I hereby agree to hold harmless and indemnify the Board of Regents of the University of Wisconsin System and the University of Wisconsin Oshkosh, their officers, agents and employees, from any and all liability, loss, damages, costs or expenses which are sustained, incurred or required arising out of my actions.'),
        required=False,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        #schemata="Verification",
        #write_permission="UWOshOIE: Modify normal fields",
    )

    certification = schema.Choice(
        title=_(u'Certification'),
        description=_(u'I certify that the information stated above is true and correct.  If accepted to the program, I agree to follow all payment and withdrawal policies and to regularly check my UW Oshkosh email account for program information beginning today.  If I am a non-UW Oshkosh student, I will use and submit an email address that I check regularly.'),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value='Yes'),SimpleTerm(value='No')]),
        #schemata="Verification",
        #write_permission="UWOshOIE: Modify normal fields",
    )


# #########################
# #OFFICE USE ONLY SECTION
# #########################

#     StringField('seatNumber',
#         widget=StringWidget(
#             label='Seat Number',
#             label_msgid='UWOshOIE_label_seatNumber',
#             description_msgid='UWOshOIE_help_seatNumber',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),
    
#     DateTimeField('completionDate',
#         widget=CalendarWidget(
#             label="Date Application Was Completed",
#             description="This is the date in which the application was completed.",
#             show_hm="0",
#             label_msgid='UWOshOIE_label_completionDate',
#             description_msgid='UWOshOIE_help_completionDate',
#             i18n_domain='UWOshOIE',
#         ),
#         required_by_state=['needsDirectorReview'],
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     BooleanField('applicationIsComplete',
#         widget=BooleanWidget(
#             label="Application is Complete",
#             label_msgid='UWOshOIE_label_applicationIsComplete',
#             description_msgid='UWOshOIE_help_applicationIsComplete',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#     ),
    
#     TextField('comments',
#         allowable_content_types=('text/plain',),
#         widget=TextAreaWidget(
#             label='Comments',
#             label_msgid='UWOshOIE_label_comments',
#             description_msgid='UWOshOIE_help_comments',
#             i18n_domain='UWOshOIE',
#         ),
#         default_output_type='text/plain',
#         schemata="OFFICE USE ONLY",
#         read_permission="UWOshOIE: Modify Office Use Only fields",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     BooleanField('applicationFeeOK',
#         widget=BooleanWidget(
#             label="Application Fee Submitted",
#             label_msgid='UWOshOIE_label_applicationFeeOK',
#             description_msgid='UWOshOIE_help_applicationFeeOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['needsDirectorReview'],
#         must_not_be=False
#     ),

#     BooleanField('UWSystemStatementOK',
#         widget=BooleanWidget(
#             label="UW System Statement of Responsibility Submitted",
#             label_msgid='UWOshOIE_label_UWSystemStatementOK',
#             description_msgid='UWOshOIE_help_UWSystemStatementOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['needsDirectorReview'],
#         must_not_be=False
#     ),

#     BooleanField('UWOshkoshStatementOK',
#         widget=BooleanWidget(
#             label="UW Oshkosh Statement of Responsibility Submitted",
#             label_msgid='UWOshOIE_label_UWOshkoshStatementOK',
#             description_msgid='UWOshOIE_help_UWOshkoshStatementOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['needsDirectorReview'],
#         must_not_be=False
#     ),
    
#     BooleanField('withdrawalRefund',
#         widget=BooleanWidget(
#             label="Withdrawal and Refund Form Submitted",
#             label_msgid='UWOshOIE_label_withdrawalRefund',
#             description_msgid='UWOshOIE_help_withdrawalRefund',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['needsDirectorReview'],
#         must_not_be=False
#     ),
    
#     BooleanField('transcriptsOK',
#         widget=BooleanWidget(
#             label="Transcripts Submitted",
#             label_msgid='UWOshOIE_label_transcriptsOK',
#             description_msgid='UWOshOIE_help_transcriptsOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['needsDirectorReview'],
#         must_not_be=False
#     ),
        
#     StringField('programSpecificMaterialsRequired',
#         widget=SelectionWidget(
#             label="Program-Specific Materials Required(Step II)?",
#             label_msgid='UWOshOIE_label_programSpecificMaterialsRequired',
#             description_msgid='UWOshOIE_help_programSpecificMaterialsRequired',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=["Yes", "No", ''],
#         required_by_state=['needsDirectorReview'],
#         must_not_be=None,
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     BooleanField('programSpecificMaterialsOK',
#         widget=BooleanWidget(
#             label="Program-Specific Materials Submitted(Step II)",
#             label_msgid='UWOshOIE_label_programSpecificMaterialsOK',
#             description_msgid='UWOshOIE_help_programSpecificMaterialsOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     StringField('specialStudentFormRequired',
#         widget=SelectionWidget(
#             label="Special Student Form Required",
#             label_msgid='UWOshOIE_label_specialStudentFormRequired',
#             description_msgid='UWOshOIE_help_specialStudentFormRequired',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=["Yes", "No", ''],
#         required_by_state=['needsDirectorReview'],
#         must_not_be=None,
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     BooleanField('specialStudentFormOK',
#         widget=BooleanWidget(
#             label="Special Student Form Submitted",
#             label_msgid='UWOshOIE_label_specialStudentFormOK',
#             description_msgid='UWOshOIE_help_specialStudentFormOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     StringField('creditOverloadFormRequired',
#         widget=SelectionWidget(
#             label="Credit Overload Form Required",
#             label_msgid='UWOshOIE_label_creditOverloadFormRequired',
#             description_msgid='UWOshOIE_help_creditOverloadFormRequired',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=['Yes', 'No', ''],
#         required_by_state=['needsDirectorReview'],
#         must_not_be=None,
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     BooleanField('creditOverloadFormOK',
#         widget=BooleanWidget(
#             label="Credit Overload Form Submitted",
#             label_msgid='UWOshOIE_label_creditOverloadFormOK',
#             description_msgid='UWOshOIE_help_creditOverloadFormOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     BooleanField('medicalOK',
#         widget=BooleanWidget(
#             label="Medical information is Submitted/Updated",
#             label_msgid='UWOshOIE_label_medicalOK',
#             description_msgid='UWOshOIE_help_medicalOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['seatAssigned'],
#         must_be=True
#     ),
    
#     TextField('medicalForm',
#         allowable_content_types=('text/plain',),
#         widget=TextAreaWidget(
#             label='Medical Form',
#             label_msgid='UWOshOIE_label_medicalForm',
#             description_msgid='UWOshOIE_help_medicalForm',
#             i18n_domain='UWOshOIE',
#             ),
#         default_output_type='text/plain',
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),
    
#     BooleanField('passportOK',
#         widget=BooleanWidget(
#             label="Passport information or receipt Submitted",
#             label_msgid='UWOshOIE_label_passportOK',
#             description_msgid='UWOshOIE_help_passportOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         required_by_state=['seatAssigned'],
#         must_be=True
#     ),

#     StringField('metPassportDeadline',
#         widget=SelectionWidget(
#             label="Passport Deadline Met",
#             label_msgid='UWOshOIE_label_metPassportDeadline',
#             description_msgid='UWOshOIE_help_metPassportDeadline',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=["Yes", "No", ""],
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     StringField('programSpecificMaterialsRequiredStepIII',
#         widget=SelectionWidget(
#             label="Program-Specific Materials Required(Step III)?",
#             label_msgid='UWOshOIE_label_programSpecificMaterialsRequired',
#             description_msgid='UWOshOIE_help_programSpecificMaterialsRequired',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=["Yes", "No", ""],
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     BooleanField('programSpecificMaterialsOKStepIII',
#         widget=BooleanWidget(
#             label="Program-Specific Materials Submitted(Step III)",
#             label_msgid='UWOshOIE_label_programSpecificMaterialsOK',
#             description_msgid='UWOshOIE_help_programSpecificMaterialsOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     StringField('attendedOrientation',
#         widget=SelectionWidget(
#             label="Attended Orientation",
#             label_msgid='UWOshOIE_label_attendedOrientation',
#             description_msgid='UWOshOIE_help_attendedOrientation',
#             i18n_domain='UWOshOIE',
#             macro="selectioninline"
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=["Yes", "No", ""],
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     StringField('cisiDates',
#         widget=StringWidget(
#             label="Health Insurance Dates",
#             description="Cultural Insurance Services International",
#             label_msgid='UWOshOIE_label_cisiDates',
#             description_msgid='UWOshOIE_help_cisiDates',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     IntegerField('cisiNumberOfMonths',
#         widget=IntegerWidget(
#             label="Health Insurance Number of Months",
#             description="Cultural Insurance Services International",
#             label_msgid='UWOshOIE_label_cisiNumberOfMonths',
#             description_msgid='UWOshOIE_help_cisiNumberOfMonths',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     FloatField('programFee',
#         widget=DecimalWidget(
#             label="Program Fee",
#             label_msgid='UWOshOIE_label_programFee',
#             description_msgid='UWOshOIE_help_programFee',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     FloatField('tuitionPayment',
#         widget=DecimalWidget(
#             label="Tuition Payment(student exchange only)",
#             label_msgid='UWOshOIE_label_tuitionPayment',
#             description_msgid='UWOshOIE_help_tuitionPayment',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     StringField('depositOnTime',
#         widget=SelectionWidget(
#             label="Deposit Paid on Time",
#             label_msgid='UWOshOIE_label_depositOnTime',
#             description_msgid='UWOshOIE_help_depositOnTime',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=['Yes','No'],
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         must_be="Yes"
#     ),

#     StringField('payment2OnTime',
#         widget=SelectionWidget(
#             label="Final Payment Made on Time(except exchange students)",
#             label_msgid='UWOshOIE_label_payment2OnTime',
#             description_msgid='UWOshOIE_help_payment2OnTime',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=['Yes','No'],
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     StringField('applicationFeeRefund',
#         widget=SelectionWidget(
#             label="Application Fee Refunded",
#             label_msgid='UWOshOIE_label_applicationFeeRefund',
#             description_msgid='UWOshOIE_help_applicationFeeRefund',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         vocabulary=['Yes','No'],
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
    
#     StringField('foreignCourse1',
#         widget=StringWidget(
#             label="Foreign institution course 1",
#             label_msgid='UWOshOIE_label_foreignCourse1',
#             description_msgid='UWOshOIE_help_foreignCourse1',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     StringField('foreignCourse2',
#         widget=StringWidget(
#             label="Foreign institution course 2",
#             label_msgid='UWOshOIE_label_foreignCourse2',
#             description_msgid='UWOshOIE_help_foreignCourse2',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     StringField('foreignCourse3',
#         widget=StringWidget(
#             label="Foreign institution course 3",
#             label_msgid='UWOshOIE_label_foreignCourse3',
#             description_msgid='UWOshOIE_help_foreignCourse3',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     StringField('foreignCourse4',
#         widget=StringWidget(
#             label="Foreign institution course 4",
#             label_msgid='UWOshOIE_label_foreignCourse4',
#             description_msgid='UWOshOIE_help_foreignCourse4',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     StringField('foreignCourse5',
#         widget=StringWidget(
#             label="Foreign institution course 5",
#             label_msgid='UWOshOIE_label_foreignCourse5',
#             description_msgid='UWOshOIE_help_foreignCourse5',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),

#     StringField('foreignCourse6',
#         widget=StringWidget(
#             label="Foreign institution course 6",
#             label_msgid='UWOshOIE_label_foreignCourse6',
#             description_msgid='UWOshOIE_help_foreignCourse6',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields",
#         searchable=True
#     ),
    
#     BooleanField('papersOK',
#         widget=BooleanWidget(
#             label="Papers information is OK",
#             label_msgid='UWOshOIE_label_papersOK',
#             description_msgid='UWOshOIE_help_papersOK',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     BooleanField('noMoreMaterials',
#         widget=BooleanWidget(
#             label='No More Materials',
#             label_msgid='UWOshOIE_label_noMoreMaterials',
#             description_msgid='UWOshOIE_help_noMoreMaterials',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     BooleanField('programMaterials',
#         widget=BooleanWidget(
#             label='Program Materials',
#             label_msgid='UWOshOIE_label_programMaterials',
#             description_msgid='UWOshOIE_help_programMaterials',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),

#     IntegerField('programFee2',
#         widget=IntegerWidget(
#             label='Program Fee 2',
#             label_msgid='UWOshOIE_label_programFee2',
#             description_msgid='UWOshOIE_help_programFee2',
#             i18n_domain='UWOshOIE',
#         ),
#         schemata="OFFICE USE ONLY",
#         read_permission="View",
#         write_permission="UWOshOIE: Modify Office Use Only fields"
#     ),
