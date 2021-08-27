
from plone.autoform.directives import mode, widget
from plone.namedfile import field
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import validate_email  # noqa
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary, yes_no_vocabulary
from uwosh.oie.studyabroadstudent.widgets import SundayStartDateWidget
from zope import schema
from zope.interface import Interface


class IOIECourse(Interface):
    mode(title='hidden')
    title = schema.TextLine(
        title=_('Course Title'),
        required=False,
        default=_('will be auto-generated on save'),
    )
    course = schema.Choice(
        title=_('UW Oshkosh Course Subject & Number'),
        description=_(
            'Add all courses associated with your program, including courses '
            'that will be taught partially at UW Oshkosh and partially while '
            'away on the program.  Do not include courses that will be '
            'taught entirely at UWO, even when these courses are offered '
            'in preparation for the program away.  Contact the OIE to add '
            'a course (abroad@uwosh.edu).'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.course_subject_and_number'),
    )
    credits_earned = schema.Int(
        title=_('UW Oshkosh Credits Earned'),
        description=_(
            'Enter the number of credits that participants will earn for '
            'each individual course.  If you are offering a course that can '
            'be taught for a range of credits on your program (e.g. 3-5 '
            'credits), you must enter the course into this system multiple '
            'times, giving the course a different credit value each time '
            'that you enter it.'),
    )
    widget('class_start_date', SundayStartDateWidget)
    class_start_date = schema.Date(
        title=_('Class Start Date'),
        # TODO Auto-generate the first day of the term in which this program  # noqa: T000
        #  runs from the calendar?????  Maybe this isn't possible.
    )
    widget('class_end_date', SundayStartDateWidget)
    class_end_date = schema.Date(
        title=_('Class End Date'),
        # TODO If the "PeopleSoft Class End Date" is AFTER the Official  # noqa: T000
        #  Graduation Date, prompt the coursebuilder to complete the
        #  "Course End Date Extension Form".
    )
    min_credits = schema.Int(
        title=_('Course Prerequisites: minimum number of credits'),
        description=_(
            'If this course requires a minimum number of completed credits '
            'prior to the course start date, indicate this here'
        ),
        min=0,
        max=999,
        required=False,
    )
    gpa = schema.Int(
        title=_('Course Prerequisites: GPA'),
        description=_(
            'If this course requires a minimum GPA prior to the '
            'course start date, indicate this here.'
        ),
        min=0,
        max=999,
        required=False,
    )
    completed_courses = schema.Text(
        title=_('Course Prerequisites: completed courses'),
        description=_(
            'If this course requires that other courses be completed, or '
            'that a particular grade be earned in an earlier course, prior '
            'to the course start date, indicate this here.'
        ),
        required=False,
    )
    program_of_study = schema.Choice(
        title=_('Course Prerequisites: program of study'),
        description=_(
            'If this course requires admission to a particular program of '
            'study prior to the course start date, indicate this here.'
        ),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.program_of_study',
        ),
        required=False,
    )
    instruction_provided_by_host = schema.Choice(
        title=_('Instruction Provided by Host?'),
        description=_(
            'If the course is to be taught by a UW Oshkosh professor, select “NO”. '
            'If the course is to be provided by a partner, select “YES”.'
        ),
        vocabulary=yes_no_vocabulary,
    )
    instruction_provided_by = schema.Choice(
        title=_('Instruction Provided by (if not host)'),
        description=_(
            'Select the name of the person who will teach the course, if the '
            'course is to be taught by a UW Oshkosh professor.  Select '
            '"host" when instruction is provided by a partner.  Do not '
            'select the name of the "instructor-of-record" at UW Oshkosh '
            'when instruction is provided by a partner.'
        ),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
        required=False,
    )
    course_enrollment_at = schema.Choice(
        title=_('Course Enrollment at'),
        description=_(
            'Indicate the institution at which program participants will be '
            'enrolled for each individual course.'
        ),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.enrollment_institution',
        ),
        required=True,
    )
    foreign_institution = schema.Choice(
        title=_('Foreign Institution Name'),
        description=_(''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner',
        required=False,
        # TODO Oshkosh must be the first option on this dropdown list  # noqa: T000
    )
    foreign_course_number = schema.Text(
        title=_('Foreign Course Number'),
        description=_(''),
        required=False,
    )
    foreign_course_credits = schema.Int(
        title=_('Foreign Course Number of Credits'),
        description=_('max: 2 digits'),
        min=0,
        max=99,
        required=False,
    )
    widget('foreign_course_review_date', SundayStartDateWidget)
    foreign_course_review_date = schema.Date(
        title=_('Foreign Course Date of Most Recent Review'),
        description=_(''),
        required=False,
    )
    foreign_course_reviewer_info = schema.TextLine(
        title=_('Foreign Course Reviewer Name, Title & College'),
        description=_(''),
        required=False,
    )
    foreign_course_syllabus = field.NamedFile(
        title=_('Foreign Course Syllabus'),
        description=_('Upload the syllabus that corresponds to the most recent date of review'),
        required=False,
    )
    foreign_course_builder_email = schema.TextLine(
        title=_('PeopleSoft Course Builder'),
        description=_(
            'Enter the email address of the person in your department who '
            'will build your course/s in PeopleSoft.  If instruction is '
            'provided by the host institution, with no concurrent '
            'enrollment at UWO, enter OIE@uwosh.edu into the email address '
            'field.'
        ),
        constraint=validate_email,
        # TODO "A message should be generated to the course builder email  # noqa: T000
        #  addresses associated with each course.  Course builders should have
        #  access to all ""Course Subject & Number"" related fields and must
        #  have permission to edit greyed out fields in this section only.
        # TODO Course builders may request instructions on how to build study  # noqa: T000
        #  abroad/away sections in PeopleSoft by emailing OIE@uwosh.edu.
        #  Course builders enter the data requested below; Financial Services
        #  uses this data to properly set tuition & fees for each course."
    )
    ps_course_id = schema.Int(
        title=_('PeopleSoft Course ID'),
        min=0,
        required=False,
    )
    ps_class_id = schema.Int(
        title=_('PeopleSoft Class Number'),
        min=0,
        required=False,
    )
    ps_section_id = schema.Int(
        title=_('PeopleSoft Course Section Number'),
        min=0,
        required=False,
    )
    ps_section_letter = schema.TextLine(
        title=_('PeopleSoft Course Section Letter'),
        required=False,
        # TODO dropdown?  # noqa: T000
    )
    widget('ps_grade_by_date', SundayStartDateWidget)
    ps_grade_by_date = schema.Date(
        title=_('PeopleSoft "grade by" date'),
        required=False,
        # TODO Autogenerate the "PeopleSoft 'grade by' date" by adding 5  # noqa: T000
        #  calendar days to the "PeopleSoft Class End Date".
    )
    tuition_and_fees = schema.Choice(
        title=_('Tuition & Fees'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.tuition_and_fees',
        required=False,
    )
    ext_studies_graded = schema.Choice(
        title=_('External Studies Courses'),
        description=_('Confirm that any External Studies Courses have been graded.'),
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO This field must be associated with each Ext Studies Course  # noqa: T000
        #  listed in "Course Subject & Number".
    )
