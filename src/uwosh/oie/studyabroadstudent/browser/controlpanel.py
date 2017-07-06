# -*- coding: utf-8 -*-
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IOIEStudyAbroadStudentControlPanel(Interface):

    majors = schema.Tuple(
        title=u'Majors',
        default=(
            u'-- choose one --',
            u'Accounting',
            u'African American Studies',
            u'Anthropology',
            u'Art',
            u'Biology',
            u'Broadfield Natural Science',
            u'Broadfield Social Science',
            u'business-undeclared-prebus',
            u'Canada and U.S. Studies',
            u'Chemistry',
            u'Communication',
            u'Computer Science',
            u'Criminal Justice',
            u'Dual Early Childhood PK-3 and Special Education Birth through Age 8',
            u'Dual Elementary 1-6 and Special',
            u'emba',
            u'Earth Science',
            u'Economics',
            u'Education',
            u'Elementary Education',
            u'engineering-technology',
            u'English',
            u'English as a Second Language',
            u'Environmental Studies',
            u'Finance',
            u'Fine Arts',
            u'French',
            u'Geography',
            u'Geology',
            u'German',
            u'History',
            u'Human Resources',
            u'Human Services',
            u'Individually Planned',
            u'Interdisciplinary Studies',
            u'International Studies',
            u'japanese',
            u'Journalism',
            u'kinesiology',
            u'Liberal Arts',
            u'Liberal Studies',
            u'MBA',
            u'Management Information Systems (MIS)',
            u'Marketing',
            u'Mathematics',
            u'Medical Technology',
            u'Microbiology',
            u'Military Science',
            u'Music',
            u'Music Education',
            u'Music Therapy',
            u'Nursing',
            u'Operations Management',
            u'Philosophy',
            u'Physical Education',
            u'Physics',
            u'Political Science',
            u'Pre-Professional Studies',
            u'professional-counseling',
            u'Psychology',
            u'Public Affairs',
            u'Radio TV Film (RTF)',
            u'Religious Studies',
            u'Secondary Education',
            u'Social Work',
            u'Sociology',
            u'Spanish',
            u'Special Education Cross-Categorical',
            u'THEATRE ARTS',
            u'Urban and Regional Studies',
            u'Womens Studies',
            u'pre-engineering',
        ),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    programs = schema.Tuple(
        title=u'Programs',
        default=(
            u'20th Century British Philosophy in Cambridge, UK',
            u'20th Century Eastern Europe and the Holocaust',
            u'3D Design, Art and Technology in Korea',
            u'Activism, Resistance, and Visual Rhetoric in Germany',
            u'American University of Rome, Italy (UW-Platteville)',
            u'American Writers in Paris',
            u'Animal Behavior Observation in Tanzania',
            u'Applied Parasitology in Nicaragua and Costa Rica',
            u'Applied Pharmacology',
            u'Approaches to Resource Management of Tropical Ecosystems in Belize',
            u'Asia-Pacific TEFL Workshop',
            u'AustraLearn - academic year',
            u'AustraLearn - semester',
            u'AustraLearn - short-term',
            u'Black Howler Monkey Research in Belize',
            u'British Politics and Political Thought',
            u'Business & Economics in China',
            u'Business & Economics in Peru',
            u'Business in Fulda, Germany',
            u'Business in India: Opportunities & Challenges (business participant)',
            u'Business in India: Opportunities & Challenges (student participants)',
            u'Camp Kyushu',
            u'Challenge Australia: Leadership Development',
            u'Challenge New Zealand: Leadership Development',
            u'Communication, Social Justice, Women and Gender Studies in Tanzania',
            u'Comparative Criminal Justice Systems in Great Britain & France',
            u'Coral Reefs and Geology of Bermuda',
            u'Counseling, Culture and Spirituality in India',
            u'Cross-Cultural Psychology Research in Brazil',
            u'Culture & Community Change in Costa Rica',
            u'Culture and Communication in Italy and Greece',
            u'Culture and Style in England and Italy',
            u'Czech Culture & Society in a Global Context',
            u'EMBA Abroad',
            u'Economics of the Carribean through Service Learning in Jamaica',
            u'Educators Abroad Student Teaching',
            u'Estonia, Russia and Eastern Europe in the 20th Century',
            u'Estudio de Lectoescritura en Costa Rica',
            u'Ethics & Community in Martha''s Vineyard, MA (USA)',
            u'European Business Travel Seminar',
            u'European Odyssey',
            u'Experience Scotland',
            u'Field Geology in China',
            u'Harbin Institute of Technology-Summer Program',
            u'Hessen - Frankfurt University of Applied Sciences - academic year',
            u'Hessen - Frankfurt University of Applied Sciences - semester',
            u'Hessen - Hochschule Darmstadt - academic year',
            u'Hessen - Hochschule Darmstadt - semester',
            u'Hessen - Hochschule Fulda - academic year',
            u'Hessen - Hochschule Fulda - semester',
            u'Hessen - Hochschule RheinMain - academic year',
            u'Hessen - Hochschule RheinMain - semester',
            u'Hessen - Hochschule für Gestaltung Offenbach am Main - academic year',
            u'Hessen - Hochschule für Gestaltung Offenbach am Main - semester',
            u'Hessen - Hochschule für Musik und Darstellende Kunst Frankfurt - academic year',
            u'Hessen - Hochschule für Musik und Darstellende Kunst Frankfurt - semester',
            u'Hessen - Johann Wolfgang Goethe-Universität Frankfurt - academic year',
            u'Hessen - Johann Wolfgang Goethe-Universität Frankfurt - semester',
            u'Hessen - Justus-Liebig-Universität Gießen - academic year',
            u'Hessen - Justus-Liebig-Universität Gießen - semester',
            u'Hessen - Philipps-Universität Marburg - IUSP',
            u'Hessen - Philipps-Universität Marburg - academic year',
            u'Hessen - Philipps-Universität Marburg - semester',
            u'Hessen - Technische Hochschule Mittelhessen - academic year',
            u'Hessen - Technische Hochschule Mittelhessen - semester',
            u'Hessen - Technische Universität Darmstadt - academic year',
            u'Hessen - Technische Universität Darmstadt - semester',
            u'Hessen - Universität Kassel - academic year',
            u'Hessen - Universität Kassel - semester',
            u'Hessen, Germany Student Exchange - academic year',
            u'Hessen, Germany Student Exchange - semester',
            u'History of British Philosophy in Cambridge, England',
            u'History of Styles',
            u'Hochschule Osnabrueck - academic year',
            u'Hochschule Osnabrueck - semester',
            u'Intensive Spanish in Salamanca, Spain - CAPP',
            u'Intensive Spanish in Salamanca, Spain - academic year',
            u'Intensive Spanish in Salamanca, Spain - semester',
            u'Intensive Spanish in Salamanca, Spain - short-term',
            u'International Operations Management in Ireland',
            u'International Summer University in Darmstadt, Germany',
            u'International Summer University in Frankfurt, Germany',
            u'International Summer University in Fulda, Germany',
            u'International Summer University in Giessen, Germany',
            u'International Summer University in Kassel, Germany',
            u'International Summer University in Marburg, Germany',
            u'International Winter University in Fulda, Germany',
            u'International Winter University in Kassel, Germany',
            u'Junior II Medical/Surgical Clinical in India',
            u'Kookmin Univeristy - Summer Language Program',
            u'Kookmin University - academic year',
            u'Kookmin University - semester',
            u'Language and Culture for Teachers (Costa Rica)',
            u'Languages Open Doors (Chile)',
            u'Leadership & Culture in Australia and New Zealand',
            u'Leadership & Culture in Australia',
            u'Lorenzo de'' Medici - Florence',
            u'Lorenzo de'' Medici - Rome',
            u'Lorenzo de'' Medici - Three Cities',
            u'Lorenzo de'' Medici - Tuscania',
            u'Los Angeles Connection (USA)',
            u'MBA Healthcare in India',
            u'MBA in China & Korea',
            u'Mathematics Education in China',
            u'Mathematics Education in Germany',
            u'Mathematics Education in Peru',
            u'Modern Democratic Politics in Europe',
            u'Modern European Politics and the Rise and Fall of European Facism',
            u'Nagasaki Junior College - semester',
            u'Nagasaki Junior College/USA Summer Camp Study & Internship Program',
            u'Nagasaki University of Foreign Studies, Japan (UW-Platteville academic year)',
            u'Nagasaki University of Foreign Studies, Japan (UW-Platteville semester)',
            u'National Student Exchange - academic year',
            u'National Student Exchange - semester',
            u'Nationalism and Internationalism in the Heart of Europe',
            u'Nicaragua: Gender, Poverty, and Activism',
            u'Ningbo University - academic year',
            u'Ningbo University - semester',
            u'Nursing Clinical Community & Families in Peru (Batch 1)',
            u'Nursing Clinical Community & Families in Peru (Batch 2)',
            u'Nursing Clinical Community and Families in Nicaragua',
            u'Nursing Clinical Rotations AND Nursing & Health Care in India (combined programs)',
            u'Nursing Clinical Rotations in Uganda',
            u'Nursing Community Health Clinical in India',
            u'Peruvian Business Travel Seminar in Lima',
            u'Politics and Political History in Great Britain',
            u'Quest III Literary Landscapes: Ireland',
            u'Quest III Migration, Culture, and Human Rights in the Americas in Nicaragua',
            u'Quest III in Panama',
            u'Quest III: Culture & Community Change in Costa Rica',
            u'Reading and Writing in Place: Ireland',
            u'Reason & Religion in 18th Century Scotland',
            u'Religious Studies in India & Nepal',
            u'Ritsumeikan Asia Pacific University Student Exchange - academic year',
            u'Ritsumeikan Asia Pacific University Student Exchange - semester',
            u'Seijo University Student Exchange (academic year)',
            u'Seijo University Student Exchange (semester)',
            u'Seminar on Globalization - Africas Experience in Kenya',
            u'Service-Learning in Malaysia',
            u'Social Work Study in Germany - Summer + Fall Semester',
            u'Social Work Study in Germany - Summer',
            u'Society and Culture in Greece & London',
            u'South Central University for Nationalities, China (UW-Platteville)',
            u'Spanish Language & Culture in Guanajuato, Mexico',
            u'Spanish and Economics Studies in Peru',
            u'Spanish-American Institute of International Education, Spain (UW-Platteville)',
            u'Spring Interim in Rome',
            u'St. Mary''s University College, England (academic year; UW-Platteville)',
            u'St. Mary''s University College, England (semester; UW-Platteville)',
            u'Student Consulting Practicum + European Business Travel Seminar',
            u'Student Consulting Practicum + Peruvian Business Travel Seminar',
            u'Student Consulting Practicum',
            u'Study in Lille, France',
            u'Study plus Intern or Teach in China',
            u'Study plus Intern or Volunteer in Australia',
            u'Summer Courses in Osnabrueck, Germany',
            u'Summer in England and Scotland',
            u'Survey of Special and Early Childhood Education in Belize',
            u'Sustainability & Globalization - Africas Experience in Uganda',
            u'THM Internship in Germany',
            u'Teach in China',
            u'Teacher Education in Korea',
            u'The Intern Group',
            u'The Jewish Question in European Politics in Poland and Germany',
            u'Travel Writing in Nicaragua',
            u'Travel and Documentary Photography in England',
            u'Traveling Through Literary and Artistic England',
            u'USA Summer Camp (Japan)',
            u'Universidad Bernardo O''Higgins Student Exchange (academic year)',
            u'Universidad Bernardo O''Higgins Student Exchange (semester)',
            u'Universidad Castilla-La Mancha (academic year)',
            u'Universidad del Pacifico Student Exchange - academic year',
            u'Universidad del Pacifico Student Exchange - semester',
            u'University Honors Program',
            u'University of Nagasaki Siebold - academic year',
            u'University of Nagasaki Siebold - semester',
            u'University of New Brunswick Student Exchange - academic year',
            u'University of New Brunswick Student Exchange - semester',
            u'University of Newcastle, Australia (UW-Platteville)',
            u'Viessmann Academy - Student Seminar in Sustainability in Germany',
            u'Viessmann Internship Program in Allendorf (summer)',
            u'Viessmann Internship Program in Schwandorf (summer)',
            u'Writing Across Cultures in Nicaragua',
            u'Youth Exchange Program in Japan',
            ),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    subjects = schema.Tuple(
        title=u'Subjects',
        default=(
            u'-- choose one --',
            u'AF AM ST',
            u'ANTHRO',
            u'ARABIC',
            u'ARAPAHO',
            u'ART',
            u'ASTRONY',
            u'BIOLOGY',
            u'BUSINESS',
            u'CHEM',
            u'COMM',
            u'COMP SCI',
            u'CRIM JUS',
            u'DFLL',
            u'ECON',
            u'ED FOUND',
            u'ED LDRSP',
            u'ELEM ED',
            u'eng-tech',
            u'ENGLISH',
            u'ENV STDS',
            u'EXT STDS',
            u'FL ELECT',
            u'FR ABRD',
            u'FRENCH',
            u'GEN ELEC',
            u'GEN STDS',
            u'GEOG',
            u'GEOLOGY',
            u'GERMAN',
            u'HEALTH',
            u'HISTORY',
            u'honors',
            u'HU ELECT',
            u'HUMAN SV',
            u'INTRDSCP',
            u'INTRNTL',
            u'JAPANESE',
            u'JOURNAL',
            u'KINESIOL',
            u'LIB SCI',
            u'LIB STDS',
            u'MATH',
            u'MED TECH',
            u'MIL SCI',
            u'MPA',
            u'MUSIC',
            u'NS ELECT',
            u'NURS-ACC',
            u'NURS-CNP',
            u'NURSING',
            u'PBIS',
            u'PHIL',
            u'PHYS AST',
            u'PHYS SCI',
            u'POLI SCI',
            u'PRAC ART',
            u'PROF COUNSELING',
            u'PRTGUESE',
            u'PSYCH',
            u'PUB ADM',
            u'PhysicalEducation',
            u'READING',
            u'RELSTDS',
            u'RUSSIAN',
            u'radio-tv-film',
            u'SEC ED',
            u'SHOSHONE',
            u'SOC WORK',
            u'social-justice',
            u'SOCIOLOGY',
            u'SPANISH',
            u'SPEC ED',
            u'SRVC CRS',
            u'SS ELECT',
            u'TBIS',
            u'THEATRE',
            u'URB REG',
            u'WOM STDS',
        ),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    ethnicities = schema.Tuple(
        title=u'Ethnicities',
        default=(
            u'no answer', 
            u'African-American', 
            u'Hispanic', 
            u'Native American', 
            u'Asian/Pacific Islander', 
            u'Other'
        ),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    marriage_statuses = schema.Tuple(
        title=u'Marriage Statuses',
        default=(u'Married', u'Single'),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    genders = schema.Tuple(
        title=u'Genders',
        default=(u'Male', u'Female', u'Other'),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    states_for_residency = schema.Tuple(
        title=u'States for Residency',
        default=(u'Wisconsin', u'Minnesota', u'Other'),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    citizenship = schema.Tuple(
        title=u'Citizenship',
        default=(u'U.S. Citizen', u'Permanent U.S. Resident', u'Other Citizenship'),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    session_hours = schema.Tuple(
        title=u'Session hours',
        default=(u'09:00-11:00', u'15:00-17:00'),
        missing_value=None,
        required=True,
        value_type=schema.TextLine()
    )

    first_day_of_spring_semester_classes = schema.Date(
        title=u'First day of Spring Semester Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_spring_semester_classes = schema.Date(
        title=u'Last day of Spring Semester Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    first_day_of_spring_interim_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_spring_interim_classes = schema.Date(
        title=u'Last day of Spring Interim Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    official_spring_graduation_date = schema.Date(
        title=u'official spring graduation date',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    first_day_of_summer_i_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_summer_i_classes = schema.Date(
        title=u'Last day of Summer I Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    first_day_of_summer_ii_classes = schema.Date(
        title=u'First day of Summer II Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_summer_ii_classes = schema.Date(
        title=u'Last day of Summer II Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    official_summer_graduation_date = schema.Date(
        title=u'Official Summer Graduation Date',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    first_day_of_fall_semester_classes = schema.Date(
        title=u'First day of Fall Semester Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_fall_semester_classes = schema.Date(
        title=u'Last day of Fall Semester Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    first_day_of_winter_interim_classes = schema.Date(
        title=u'First day of Winter Interim Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    last_day_of_winter_interim_classes = schema.Date(
        title=u'Last day of Winter Interim Classes',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    official_fall_graduation_date = schema.Date(
        title=u'Official Fall Graduation Date',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    spring_interim_summer_fall_semester_in_person_orientation = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester In-person Orientation',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    winter_interim_spring_semester_participant_orientation_deadline = schema.Date(
        title=u'Winter Interim & Spring Semester Participant Orientation Deadline',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    winter_interim_spring_semester_in_person_orientation = schema.Date(
        title=u'Winter Interim & Spring Semester In-person Orientation',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title=u'Spring Interim Payment Deadline 2',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    sunmmer_payment_deadline_2 = schema.Date(
        title=u'Sunmmer Payment Deadline 2',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title=u'Fall Semester Payment Deadline 2',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 1',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 2',
        required=True,
        default=date(2017,01,01),
#        value_type=schema.Date()
    )




class OIEStudyAbroadStudentControlPanelForm(RegistryEditForm):
    schema = IOIEStudyAbroadStudentControlPanel
    schema_prefix = "oiestudyabroadstudent"
    label = u'OIE Study Abroad Student Settings'


OIEStudyAbroadStudentControlPanelView = layout.wrap_form(
    OIEStudyAbroadStudentControlPanelForm, ControlPanelFormWrapper)
