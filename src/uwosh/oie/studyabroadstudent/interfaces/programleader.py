from collective import dexteritytextindexer
from plone.autoform.directives import mode
from plone.namedfile import field
from plone.supermodel import model
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid, checkEmailAddress
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import (
    RegistryValueVocabulary,
    load_or_overload,
    paid_by,
    rate_or_lump_sum,
    replacement_costs,
    salary_form,
    socialmediaservice,
    yes_no_vocabulary,
)
from zope import schema
from zope.interface import Interface
from zope.schema import ValidationError


class InvalidEmailAddress(ValidationError):
    """Invalid email address"""


def validate_email(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class IOIEProgramLeader(Interface):
    """The On-site Program Leader is responsible for providing leadership
    for the group and for overseeing group health and safety.  The On-site
    Program Leader may also teach one or more of the program courses.
    """

    # TODO "There may be only one Program Leader.  Most of the data fields  # noqa
    #   associated with the Program Leader are the same fields used for the
    #   Program Liaison and Program Co-leader/s.  Can the same fields be
    #   used for all three leadership roles?

    # TODO The Program Leader may also be the Program Liaison or one of  # noqa
    #   the Program Co-leaders.

    # TODO Some of these fields also need to be matched to "participant"  # noqa
    #   fields so that we can pull a roster that includes all participants,
    #   leaders and co-leaders. "
    dexteritytextindexer.searchable('title')
    mode(title='hidden')
    title = schema.TextLine(
        title=_('Full Name'),
        required=False,
        default=_('will be auto-generated on save'),
    )
    dexteritytextindexer.searchable('first_name')
    first_name = schema.TextLine(
        title=_('First Name'),
        required=True,
    )
    dexteritytextindexer.searchable('middle_name')
    middle_name = schema.TextLine(
        title=_('Middle Name'),
        required=False,
    )
    dexteritytextindexer.searchable('last_name')
    last_name = schema.TextLine(
        title=_('Last Name'),
        required=True,
    )
    dexteritytextindexer.searchable('job_title')
    job_title = schema.TextLine(
        title=_('Job Title'),
        required=True,
    )
    dexteritytextindexer.searchable('empid')
    empid = schema.TextLine(
        title=_('Employee ID'),
        required=True,
    )
    dexteritytextindexer.searchable('office_phone')
    office_phone = schema.TextLine(
        title=_('Office Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('mobile_phone_us')
    mobile_phone_us = schema.TextLine(
        title=_('Mobile Phone (US)'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('mobile_phone_int')
    mobile_phone_int = schema.TextLine(
        title=_('Mobile Phone (abroad)'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_('Email'),
        required=True,
        constraint=validate_email,
    )
    dexteritytextindexer.searchable('other_service')
    other_service = schema.Choice(
        title=_('e.g., Line, Skype, Viber, WeChat, WhatsApp'),
        required=False,
        vocabulary=socialmediaservice,
    )
    dexteritytextindexer.searchable('other_username')
    other_username = schema.TextLine(
        title=_('username or ID for the above service'),
        required=False,
    )
    dexteritytextindexer.searchable('office_building')
    office_building = schema.Choice(
        title=_('Office Building'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.building'),
    )
    dexteritytextindexer.searchable('office_room')
    office_room = schema.TextLine(
        title=_('Office Room'),
        required=True,
    )
    dexteritytextindexer.searchable('college_or_unit')
    college_or_unit = schema.Choice(
        title=_('College or Unit'),
        description=_(''),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.college_or_unit'),  # noqa
    )
    role_and_responsibility = field.NamedFile(
        title=_('Role & Responsibility'),
        description=_('Upload a signed Program Liaison Role & Responsibilities form'),  # noqa
    )
    dexteritytextindexer.searchable('emergency_contact_name')
    emergency_contact_name = schema.TextLine(
        title=_('Emergency Contact Name'),
        required=True,
    )
    dexteritytextindexer.searchable('emergency_contact_relationship')
    emergency_contact_relationship = schema.TextLine(
        title=_('Emergency Contact Relationship to You'),
        required=True,
    )
    dexteritytextindexer.searchable('emergency_contact_mobile_phone')
    emergency_contact_mobile_phone = schema.TextLine(
        title=_('Emergency Contact Mobile Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('emergency_contact_other_phone')
    emergency_contact_other_phone = schema.TextLine(
        title=_('Emergency Contact Other Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('emergency_contact_email')
    emergency_contact_email = schema.TextLine(
        title=_('Emergency Contact Email'),
        required=True,
        constraint=validate_email,
    )

    #######################################################
    # TODO move JavaScript over for compensation fields  # noqa
    # this appears to be the contents of programedit.js
    # which is currently set to load on the program rather than leader type
    model.fieldset(
        'compensation',
        label=_('Compensation'),
        fields=['load_or_overload', 'replacement_costs', 'paid_by',
                'rate_or_lump_sum', 'lump_sum_amount',
                'will_base_salary_change', 'salary_form_type'],
    )
    load_or_overload = schema.Choice(
        title=_('Load or Overload'),
        description=_('Choose whether payment is part of load or is overload'),  # noqa
        required=True,
        vocabulary=load_or_overload,
    )
    replacement_costs = schema.Choice(
        title=_('Replacement Costs'),
        description=_('Are replacement costs due to the College?'),
        required=False,
        vocabulary=replacement_costs,
    )
    paid_by = schema.Choice(
        title=_('Costs are paid by'),
        description=_('Choose who pays'),
        required=False,
        vocabulary=paid_by,
    )
    rate_or_lump_sum = schema.Choice(
        title=_('Payment Rate or Lump Sum'),
        description=_('Choose a payment rate or lump sum'),
        required=False,
        vocabulary=rate_or_lump_sum,
    )
    lump_sum_amount = schema.TextLine(
        title=_('Lump sum amount'),
        description=_('Enter the lump sum to be paid'),
        required=False,
    )
    will_base_salary_change = schema.Choice(
        title=_('Will this person''s base salary change prior to the date on which this program is scheduled to end?'),  # noqa
        description=_('If you check ''no'' and the base salary changes, any compensation due for this program will be calculated using the current base salary.'),  # noqa
        vocabulary=yes_no_vocabulary,
    )
    salary_form_type = schema.Choice(
        title=_('Salary Form Type'),
        vocabulary=salary_form,
        # TODO Applicant should not see this field.  This is for OIE.  It  # noqa
        #   would be better to put this on the "Program Finances" tab, but this
        #   field is specific to each Program Leader rather than to the
        #   program.
    )
    #######################################################
    model.fieldset(
        'Marketing Material',
        label=_('Marketing Material'),
        fields=['number_study_abroad_away_fair_flyers',
                'number_study_abroad_away_fair_posters',
                'number_study_abroad_away_fair_brochures'],
    )
    number_study_abroad_away_fair_flyers = schema.Int(
        title=_('Number of Study Abroad/Away Fair Flyers'),
        description=_('Indicate the number (max: 999) of flyers, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=999,
        default=0,
    )
    number_study_abroad_away_fair_posters = schema.Int(
        title=_('Number of Study Abroad/Away Fair Posters'),
        description=_('Indicate the number (max: 99) of posters, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=99,
        default=0,
    )
    number_study_abroad_away_fair_brochures = schema.Int(
        title=_('Number of Study Abroad/Away Fair Brochures'),
        description=_('Indicate the number (max: 999) of brochures, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=999,
        default=0,
    )
    #######################################################
    # TODO Either "passport" or "driver's license" should appear in place  # noqa
    #   of "See Comment" depending on the list of "countries" associated
    #   with the applicant's program.  (If the document name can't be
    #   generated based on other data in the system, add this text below
    #   "Travel Document": Complete the following using information from
    #   your unexpired passport (required for international travel) or with
    #   your unexpired driver's license (for domestic travel only). Can we
    #   use the same data fields as are used for the Participants in the
    #   "applicant" portal?
    model.fieldset(
        'Travel Document',
        label=_('Travel Document'),
        fields=['travel_document_last_name', 'travel_document_first_name',
                'travel_document_middle_name', 'date_of_birth', 'gender',
                'document_number', 'document_expiry_date'],
    )
    travel_document_first_name = schema.TextLine(
        title=_('Travel Document: First Name'),
        description=_('If you are flying to your destination, the name on your airline ticket must match the name on your ID exactly.  Type your first name exactly as it Appears on the ID.  IF MULTIPLE FIRST NAMES APPEAR ON THE ID, type all first names that appear on the ID in this field.  If typed incorrectly, you will be responsible for any name change fee charged by the airline or by the travel agency.'),  # noqa
        required=True,
    )
    travel_document_middle_name = schema.TextLine(
        title=_('Travel Document: Middle Name'),
        description=_('If you are flying to your destination, the name on your airline ticket must match the name on your ID exactly.  IF YOUR MIDDLE NAME APPEARS ON YOUR ID, you must type your middle name in this field exactly as it appears on the ID.  IF YOUR MIDDLE INITIAL APPEARS ON YOUR ID, you must type only your middle initial in this field.  IF MULTIPLE MIDDLE NAMES APPEAR ON YOUR ID, you must type all middle names that appear on your ID in this field.  IF YOUR MIDDLE NAME DOES NOT APPEAR ON YOUR ID, do not include your middle name in this field.  If typed incorrectly, you will be responsible for any name change fee charged by the airline or by the travel agency.'),  # noqa
        required=False,
    )
    travel_document_last_name = schema.TextLine(
        title=_('Travel Document: Last Name'),
        description=_('If you are flying to your destination, the name on your airline ticket must match the name on your ID exactly.  Type your last name exactly as it Appears on the ID.  IF MULTIPLE LAST NAMES APPEAR ON THE ID, type all last names that appear on the ID in this field.  If typed incorrectly, you will be responsible for any name change fee charged by the airline or by the travel agency.  '),  # noqa
        required=True,
    )
    date_of_birth = schema.Date(
        title=_('Travel Document: Date of Birth'),
        required=True,
    )
    gender = schema.Choice(
        title=_('Travel Document: Gender (Sex)'),
        description=_('Select the sex that is listed on your travel document.'),  # noqa
        source=RegistryValueVocabulary('oiestudyabroadstudent.genders'),
        required=True,
    )
    document_number = schema.TextLine(
        title=_('Travel Document: Document Number'),
        description=_(''),
        required=True,
    )
    document_expiry_date = schema.Date(
        title=_('Travel Document: Expiry Date'),
        description=_('You may not enter details for a document that is expired or for a document that will expire prior to the final travel return date for your program.'),  # noqa
        required=True,
    )
    #######################################################
    # TODO this fieldset should be hidden from the person adding their Leader profile.  Who is allowed to see it?  # noqa
    model.fieldset(
        'Office Use Only',
        label=_('Office Use Only'),
        fields=['orientation_completed_date', 'cash_advance_request',
                'cash_advance_distribution', 'hr_review_ok',
                'administrative_services_review_ok',
                'equal_opportunity_review_ok'],
    )
    orientation_completed_date = schema.Date(
        title=_('Program Leader Orientation Completed'),
        description=_('Confirm attendance at orientation'),
        required=False,
    )
    cash_advance_request = field.NamedFile(
        title=_('Cash Advance Request'),
        description=_('Upload the signed Cash Advance Form'),
        required=False,
    )
    cash_advance_distribution = schema.Date(
        title=_('Cash Advance Distribution'),
        description=_('Enter the date on which the cash advance was distributed to the Program Leader/Program Co-leader'),  # noqa
        required=False,
    )
    hr_review_ok = schema.Choice(
        title=_('HR Review'),
        description=_('There are no actions pending that may affect the Provost''s decision to approve this applicant as a Leader or Co-leader for a study abroad/away program'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO Or, is this its own workflow?  # noqa
    )
    administrative_services_review_ok = schema.Choice(
        title=_('Administrative Services Review'),
        description=_('This applicant does not have any past due travel or cash advances'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO Or, is this its own workflow?  # noqa
    )
    equal_opportunity_review_ok = schema.Choice(
        title=_('Office of Equal Opportunity & Access Review'),
        description=_('There are no actions pending that may affect the Provost''s decision to approve this applicant as a Leader or Co-leader for a study abroad/away program.'),  # noqa
        vocabulary=yes_no_vocabulary,
        required=False,
        # TODO Or, is this its own workflow?  # noqa
    )
