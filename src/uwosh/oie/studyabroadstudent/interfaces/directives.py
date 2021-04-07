
from plone.supermodel.directives import MetadataDictDirective


REQUIRED_IN_STATE_KEY = u'uwosh.oie.studyabroadstudent.required-in-state'
REQUIRED_VALUE_IN_STATE_KEY = u'uwosh.oie.studyabroadstudent.required-value-in-state'  # noqa
V_PROGRAM_CODE_FS = 'uwosh.oie.studyabroadstudent.view.program_code_fieldset'
E_PROGRAM_CODE_FS = 'uwosh.oie.studyabroadstudent.edit.program_code_fieldset'
E_PROGRAM_DESCRIPTION = 'uwosh.oie.studyabroadstudent.edit.program_description'
E_SYLLABUS_AND_SUPPORTING_DOCS = 'uwosh.oie.studyabroadstudent.edit.syllabus_and_supporting_docs'  # noqa
V_ACADEMIC_PROGRAM_FS = 'uwosh.oie.studyabroadstudent.view.academic_program_fieldset'  # noqa
E_ACADEMIC_PROGRAM_FS = 'uwosh.oie.studyabroadstudent.edit.academic_program_fieldset'  # noqa
V_DATES_DESTINATIONS_FS = 'uwosh.oie.studyabroadstudent.view.dates_destinations_fieldset'  # noqa
E_DATES_DESTINATIONS_FS = 'uwosh.oie.studyabroadstudent.edit.dates_destinations_fieldset'  # noqa
V_DEPARTURE_FLIGHT_FS = 'uwosh.oie.studyabroadstudent.view.departure_flight_fieldset'  # noqa
E_DEPARTURE_FLIGHT_FS = 'uwosh.oie.studyabroadstudent.edit.departure_flight_fieldset'  # noqa
V_DEPARTURE_FROM_OSHKOSH_FS = 'uwosh.oie.studyabroadstudent.view.departure_from_oshkosh_fieldset'  # noqa
E_DEPARTURE_FROM_OSHKOSH_FS = 'uwosh.oie.studyabroadstudent.edit.departure_from_oshkosh_fieldset'  # noqa
V_RETURN_FLIGHT_FS = 'uwosh.oie.studyabroadstudent.view.return_flight_fieldset'
E_RETURN_FLIGHT_FS = 'uwosh.oie.studyabroadstudent.edit.return_flight_fieldset'
V_RETURN_TO_OSHKOSH_FS = 'uwosh.oie.studyabroadstudent.view.return_to_oshkosh_fieldset'  # noqa
E_RETURN_TO_OSHKOSH_FS = 'uwosh.oie.studyabroadstudent.edit.return_to_oshkosh_fieldset'  # noqa
V_PARTICIPANT_SELECTION_FS = 'uwosh.oie.studyabroadstudent.view.participant_selection_fieldset'  # noqa
E_PARTICIPANT_SELECTION_FS = 'uwosh.oie.studyabroadstudent.edit.participant_selection_fieldset'  # noqa
V_LIAISON_AND_LEADERSHIP_FS = 'uwosh.oie.studyabroadstudent.view.liaison_and_leadership_fieldset'  # noqa
E_LIAISON_AND_LEADERSHIP_FS = 'uwosh.oie.studyabroadstudent.edit.liaison_and_leadership_fieldset'  # noqa
V_COURSES_FS = 'uwosh.oie.studyabroadstudent.view.courses_fieldset'
E_COURSES_FS = 'uwosh.oie.studyabroadstudent.edit.courses_fieldset'
V_CONTRIBUTIONS_FS = 'uwosh.oie.studyabroadstudent.view.contributions_fieldset'
E_CONTRIBUTIONS_FS = 'uwosh.oie.studyabroadstudent.edit.contributions_fieldset'
V_REVIEWERS_FS = 'uwosh.oie.studyabroadstudent.view.reviewers_fieldset'
E_REVIEWERS_FS = 'uwosh.oie.studyabroadstudent.edit.reviewers_fieldset'
V_OIE_REVIEW_FS = 'uwosh.oie.studyabroadstudent.view.oie_review_fieldset'
E_OIE_REVIEW_FS = 'uwosh.oie.studyabroadstudent.edit.oie_review_fieldset'
V_PROPOSALS_FS = 'uwosh.oie.studyabroadstudent.view.proposals_fieldset'
E_PROPOSALS_FS = 'uwosh.oie.studyabroadstudent.edit.proposals_fieldset'
V_FINANCES_FS = 'uwosh.oie.studyabroadstudent.view.finances_fieldset'
E_FINANCES_FS = 'uwosh.oie.studyabroadstudent.edit.finances_fieldset'
V_PRE_DEPARTURE_FS = 'uwosh.oie.studyabroadstudent.view.pre_departure_fieldset'
E_PRE_DEPARTURE_FS = 'uwosh.oie.studyabroadstudent.edit.pre_departure_fieldset'
E_REPORTING_FS = 'uwosh.oie.studyabroadstudent.edit.reporting_fieldset'
V_REPORTING_FS = 'uwosh.oie.studyabroadstudent.view.reporting_fieldset'
E_PROGRAM_DATES_FS = 'uwosh.oie.studyabroadstudent.edit.program_dates_fieldset'
V_PROGRAM_DATES_FS = 'uwosh.oie.studyabroadstudent.view.program_dates_fieldset'


class required_in_state(MetadataDictDirective):
    """Directive used to set a field to be required in a given workflow state
    """
    key = REQUIRED_IN_STATE_KEY

    def factory(self, **kw):
        return kw


class required_value_in_state(MetadataDictDirective):
    """Directive to specify the required value of a field for a state
    """
    key = REQUIRED_VALUE_IN_STATE_KEY

    def factory(self, **kw):
        return kw
