# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from uwosh.oie.studyabroadstudent.exceptions import StateError
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_IN_STATE_KEY  # noqa
from uwosh.oie.studyabroadstudent.interfaces.directives import REQUIRED_VALUE_IN_STATE_KEY  # noqa
from zLOG import ERROR
from zLOG import INFO
from zLOG import LOG


DEFAULT_NOTIFICATION_EMAIL_ADDRESS = 'tknguyen+oie@mac.com'


def pre_submit_to_chair(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_to_chair(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_to_dean(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_to_dean(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_announce_programmatic_for_fee_change(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_announce_programmatic_for_fee_change(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_approve_fee(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_approve_fee(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_approve_proposal(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_approve_proposal(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_approve_provosts_office(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_approve_provosts_office(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_approve_rfp(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_approve_rfp(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_archive_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_archive_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_arrive_non_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_arrive_non_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_arrive_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_arrive_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_bill_for_final_payment(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_bill_for_final_payment(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_bill_for_final_payment_programs_with_no_leader(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_bill_for_final_payment_programs_with_no_leader(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_cancel(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_cancel(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_cancel_after_change(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_cancel_after_change(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_briefing_completed(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_briefing_completed(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_orientation_completed(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_orientation_completed(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_return(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_return(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_safe_arrival(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_safe_arrival(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_ter_received(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_ter_received(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_to_run(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_to_run(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_confirm_travel_delay(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_confirm_travel_delay(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_decline(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_decline(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_depart(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_depart(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_depart_non_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_depart_non_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_depart_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_depart_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_develop_rfp(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_develop_rfp(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_end_incident(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_end_incident(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_pending_approval_of_alternate_course(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_pending_approval_of_alternate_course(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_pending_provider_proposal(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_pending_provider_proposal(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_process_refunds(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_process_refunds(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_publish_fee(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_publish_fee(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_publish_final_fee(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_publish_final_fee(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_report_incident(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_report_incident(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_return_rfp_to_program_manager(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_return_rfp_to_program_manager(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_return_to_initial(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_return_to_initial(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_initial(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_initial(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_return_to_oie(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_return_to_oie(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_return_to_oie_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_return_to_oie_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_return_to_rfp_under_development(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_return_to_rfp_under_development(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_returned_non_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_returned_non_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_returned_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_returned_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_review_provider_proposals(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_review_provider_proposals(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_schedule_operational_briefing(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_schedule_operational_briefing(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_send_bills_for_initial_payment(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_send_bills_for_initial_payment(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_send_for_fee_change(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_send_for_fee_change(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_send_for_programmatic_change(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_send_for_programmatic_change(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_fee_for_liaison_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_fee_for_liaison_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_non_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_non_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_proposal_to_liaison(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_proposal_to_liaison(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_rfp_for_liaison_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_rfp_for_liaison_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_sponsored_program(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_sponsored_program(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_to_oie(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_to_oie(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_submit_to_provost(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_submit_to_provost(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_suspend(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_suspend(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_travel_advance_ready(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_travel_advance_ready(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_withdraw_application(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_withdraw_application(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_applicants_considering_change(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_applicants_considering_change(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_application_intake_in_progress(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_application_intake_in_progress(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_cancelled(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_cancelled(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_declined(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_declined(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_final_payment_billing_in_progress(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_final_payment_billing_in_progress(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_final_program_accounting_in_progress(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_final_program_accounting_in_progress(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_incident_in_progress(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_incident_in_progress(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_initial_payment_billing_in_progress(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_initial_payment_billing_in_progress(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_arrival_abroad(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_arrival_abroad(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_chair_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_chair_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_dean_unit_director_review(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_dean_unit_director_review(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_discussions_with_program_manager(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_discussions_with_program_manager(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_final_program_fee(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_final_program_fee(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_oie_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_oie_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_program_departure(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_program_departure(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_program_fee_determination_by_oie(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_program_fee_determination_by_oie(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_program_leader_operational_briefing(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_program_leader_operational_briefing(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_program_leader_orientation(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_program_leader_orientation(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_provider_responses(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_provider_responses(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_provost_review(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_provost_review(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_pending_travel_advance(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_pending_travel_advance(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_process_refunds_budget_transfers(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_process_refunds_budget_transfers(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_program_completed(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_program_completed(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_program_fee_pending_publication(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_program_fee_pending_publication(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_program_fee_under_liaison_review(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_program_fee_under_liaison_review(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_program_in_progress(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_program_in_progress(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_provider_proposals_under_liaison_review(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_provider_proposals_under_liaison_review(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_provider_proposals_under_oie_review(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_provider_proposals_under_oie_review(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_request_for_proposals_under_development(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_request_for_proposals_under_development(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_request_for_proposals_under_liaison_review(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_request_for_proposals_under_liaison_review(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_reviewing_final_program_details(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_reviewing_final_program_details(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_suspended(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_suspended(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_travel_expense_report_student_evaluations_due_to(self, state_change, **kw):  # noqa
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_travel_expense_report_student_evaluations_due_to(self, state_change, **kw):  # noqa
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def pre_manager_return_to_withdrawn(self, state_change, **kw):
    check_program_for_required_values_by_state(self, state_change, {})
    check_program_for_required_specific_values_by_state(self, state_change, {})


def post_manager_return_to_withdrawn(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)


def afterTransition(application, state_id):
    pass


def getEmailMessageTemplate(self, transition, onFailure=False):
    # LOG ('getEmailMessageTemplate', INFO, "called with onFailure='%s'" % (onFailure))  # noqa
    if onFailure:
        onFailure = True
    else:
        onFailure = False
    # LOG ('getEmailMessageTemplate', INFO, "reinterpreted onFailure='%s'" % (onFailure))  # noqa

    templates = self.queryCatalog({
        'portal_type': 'UWOshOIEEmailTemplate',
        'getTransition': transition,
        # 'getSendEmailOnFailure': onFailure, # this does NOT work so must filter below  # noqa
        'sort_on': 'modified',
    })
    # the queryCatalog() does not return correctly based on getSendEmailOnFailure filter value passed in  # noqa
    retlist = []
    for t in templates:
        obj = t.getObject()
        if obj.getSendEmailOnFailure() == onFailure:
            retlist.append(obj)
    # LOG ('getEmailMessageTemplate', INFO, "templates='%s', length=%s" % (templates, len(templates)))  # noqa

    if len(retlist) > 0:
        retval = retlist[0]
        LOG('getEmailMessageTemplate', INFO, 'returning ''%s''' % (retval))  # noqa
        return retval
    else:
        LOG('getEmailMessageTemplate', INFO, 'returning None')
        return None


def intializeMissingValues(missingValues, key):
    if key not in missingValues:
        missingValues[key] = []


def getCreatorInfo(self, application):
    pmtool = getToolByName(self, 'portal_membership', None)  # noqa
    creator = application.Creator()
    member = pmtool.getMemberById(creator)  # noqa

    return {
        'member': member,
        'id': member.getId(),
        'fullname': member.getProperty('fullname', 'Fullname missing'),
        'email': member.getProperty('email', None),
    }


def getReviewerInfo(self, application):
    pmtool = getToolByName(self, 'portal_membership', None)  # noqa
    wftool = getToolByName(self, 'portal_workflow', None)  # noqa

    actorid = wftool.getInfoFor(application, 'actor')  # noqa
    actor = pmtool.getMemberById(actorid)  # noqa

    reviewer = {
        'member': actor,
        'id': actor.getId(),
        'fullname': actor.getProperty('fullname', 'Fullname missing'),
        'email': actor.getProperty('email', None),
    }

    return reviewer


# cc will be faculty on that transition
def getToAddresses(application, emailTemplate, cc=[]):
    addresses = []

    # student email
    # addresses.append(application.getEmail())

    # if emailTemplate:
    #    # custom specified emails sent
    #    addresses.extend(emailTemplate.getFormattedCCAddresses())

    if cc is not None:
        addresses.extend(cc)

    return addresses


def assembleEmailMessage(self, application, wftool, emailTemplate, onFailure):
    mMsg = """

Your UW Oshkosh Office of International Education study abroad program has been updated.

Name: %s
Program Name: %s
Program Year: %s

%s

You can view your program here: %s

Comment: %s

%s
""" % (  # noqa
        application.getFirstName() + ' ' + application.getLastName(),
        application.getProgramNameAsString(),
        application.getProgramYear(),
        emailTemplate.getFormattedEmailText(),
        application.absolute_url(),
        wftool.getInfoFor(application, 'comments'),  # noqa
        getAssembledErrorMessage(onFailure),
    )

    return mMsg


def sendTransitionMessage(self, state_change, cc=[], onFailure=False):
    portal = getToolByName(self, 'portal_url').getPortalObject()  # noqa
    wftool = getToolByName(self, 'portal_workflow', None)  # noqa

    application = state_change.object
    emailTemplate = getEmailMessageTemplate(self, state_change.transition.id, onFailure)  # noqa
    history = state_change.getHistory()  # noqa

    old_state_id = state_change.old_state.id
    new_state_id = state_change.new_state.id

    creator = getCreatorInfo(self, application)  # noqa
    reviewer = getReviewerInfo(self, application)

    mTo = getToAddresses(application, emailTemplate, cc)
    mFrom = reviewer['email']

    # If the owner is performing action, this will prevent them from sending an email to themselves  # noqa
    if mFrom in mTo:
        mFrom = DEFAULT_NOTIFICATION_EMAIL_ADDRESS

    mSubj = 'Your study abroad program update (UW Oshkosh Office of International Education)'  # noqa

    state_msg = None
    if old_state_id != new_state_id:
        state_msg = "Its state has changed from '" + old_state_id + "' to '" + new_state_id + "'.\n\n"  # noqa

    canSendEmail = emailTemplate and emailTemplate.canSendEmail(onFailure)
    if emailTemplate and canSendEmail:
        LOG('sendTransitionMessage', INFO,
            "Sending transition email for transition %s to %s, subject '%s', onFailure = '%s', emailTemplate = '%s', canSendEmail = '%s'" % (  # noqa
            state_change.transition.id, mTo, mSubj, onFailure, emailTemplate, canSendEmail))  # noqa
        mMsg = assembleEmailMessage(self, application, wftool, emailTemplate, onFailure)  # noqa

        # only for debugging
        # if DEBUG_MODE or DevelopmentMode:
        #    DEBUG_MAIL_HOST.secureSend(mMsg, mTo, mFrom, mSubj)
        # else:
        portal.MailHost.secureSend(mMsg, mTo, mFrom, mSubj)
    else:
        LOG('sendTransitionMessage', INFO,
            "Not sending transition email for transition %s to %s, subject '%s', onFailure = '%s', emailTemplate = '%s', canSendEmail = '%s'" % (  # noqa
            state_change.transition.id, mTo, mSubj, onFailure, emailTemplate, canSendEmail))  # noqa


def check_program_for_required_values_by_state(
        self,
        state_change,
        alreadyMissingValues={}):
    """Find all fields that must have values before
       we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    missingValues = {}
    if len(alreadyMissingValues) > 0:
        missingValues = alreadyMissingValues

    requiredFields = []
    required_in_state = IOIEStudyAbroadProgram.queryTaggedValue(REQUIRED_IN_STATE_KEY)  # noqa
    if required_in_state:
        required_fields = required_in_state.keys()
    else:
        required_fields = None

    if not required_fields:
        return

    for f in required_fields:
        state = required_in_state[f]
        if new_state_id == state:
            requiredFields.append(f)

    for f in requiredFields:
        value = getattr(obj, f, None)
        field = IOIEStudyAbroadProgram.get(f)
        field_title = field.title
        if not value:
            message = "the field '%s' is required for state '%s' but has no value" % (field_title, new_state_id)  # noqa
            LOG('check_for_required_values_by_state', ERROR, message)
            intializeMissingValues(missingValues, f)
            missingValues[f].append(
                {
                    'expected': 'N/A',
                    'current_value': value,
                    'field': field_title,
                    'message': 'You are missing this required field',
                },
            )
            raise StateError, message  # noqa


def check_program_for_required_specific_values_by_state(
        self,
        state_change,
        alreadyMissingValues={}):
    """Find all fields that must have specific values before
       we can move into the new state"""
    obj = state_change.object
    new_state_id = state_change.new_state.id

    missingValues = {}
    if len(alreadyMissingValues) > 0:
        missingValues = alreadyMissingValues

    requiredValueFields = []
    required_value_in_state = IOIEStudyAbroadProgram.queryTaggedValue(REQUIRED_VALUE_IN_STATE_KEY)  # noqa
    if required_value_in_state:
        required_value_fields = required_value_in_state.keys()
    else:
        required_value_fields = None

    if not required_value_fields:
        return

    for f in required_value_fields:
        if isinstance(required_value_in_state[f][0], tuple):
            for must_be, state in required_value_in_state[f]:
                if new_state_id == state:
                    requiredValueFields.append([f, must_be])
        else:
            must_be, state = required_value_in_state[f]
            if new_state_id == state:
                requiredValueFields.append([f, must_be])

    for f, must_be in requiredValueFields:
        value = getattr(obj, f, None)
        field = IOIEStudyAbroadProgram.get(f)
        field_title = field.title
        if isinstance(must_be, str):
            # e.g., to handle DateTimes
            value = str(value)
        if value != must_be:
            message = "the field '%s' is required to have the value '%s' for state '%s' but has the value '%s'" % (field_title, must_be, new_state_id, value)  # noqa
            LOG('check_for_required_values_by_state', ERROR, message)
            intializeMissingValues(missingValues, f)
            missingValues[f].append(
                {
                    'expected': must_be,
                    'current_value': value,
                    'field': field_title,
                    'message': 'This field does not have the required value',
                },
            )
            raise StateError, message  # noqa

#         must_not_be = getattr(f, 'must_not_be', None)
#
#         if aValue == None or str(
#             aValue) == '':  # have to cast to a string to handle Products.Archetypes.Field.TextField values  # noqa
#             if must_be is None:
#                 must_be = "Any Value"
#             intializeMissingValues(missingValues, f.schemata)
#             missingValues[f.schemata].append({'expected': must_be,
#                                               'current_value': str(aValue),
#                                               'field': f.widget.label,
#                                               'message': 'You are missing this required field'})  # noqa
#             break
#
#         if must_be is not None and aValue != must_be and (aValue != None or len(str(aValue)) == 0):  # noqa
#             intializeMissingValues(missingValues, f.schemata)
#             missingValues[f.schemata].append({'expected': str(must_be),
#                                               'current_value': str(aValue),
#                                               'field': f.widget.label,
#                                               'message': 'You have entered or are missing information that makes the application invalid'})  # noqa
#             break
#
#         if must_not_be is not None and aValue == must_not_be and aValue != None:  # noqa
#             intializeMissingValues(missingValues, f.schemata)
#             missingValues[f.schemata].append({'expected': 'NOT  ' + str(must_not_be),  # noqa
#                                               'current_value': str(aValue),
#                                               'field': f.widget.label,
#                                               'message': 'You are missing or have entered information that makes the application invalid'})  # noqa
#
#     if len(missingValues) > 0:
#         sendTransitionMessage(self, state_change, None, missingValues)
#
#         raise StateError, missingValues


def getAssembledErrorMessage(errorMessage):
    if errorMessage:

        message = ''
        for key in errorMessage.keys():
            message += '\n\n Section: ' + key + '\n'
            for error in errorMessage[key]:
                message += 'Field: ' \
                           + error['field'] \
                           + ',\tExplanation: ' \
                           + error['message'] \
                           + '\n'

        return message

    else:
        return ''
