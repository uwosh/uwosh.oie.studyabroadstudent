# -*- coding: utf-8 -*-
# from AccessControl import getSecurityManager  # noqa : P001
from plone.api import content
from plone.api.exc import InvalidParameterError
from plone.api.user import get_roles as get_user_roles
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from xml.etree import ElementTree

import os
import unittest


def get_roles():
    pathname = os.path.dirname(os.path.realpath(__file__))
    rolemap_tree = ElementTree.parse(pathname + '/../profiles/default/rolemap.xml') # noqa
    rolemap = rolemap_tree.getroot()
    roles_element = rolemap.find('roles')
    roles = set([role.attrib['name'] for role in list(roles_element)])
    roles.add('Anonymous')
    return roles


def get_transitions_and_states():
    pathname = os.path.dirname(os.path.realpath(__file__))
    workflow_tree = ElementTree.parse(pathname + '/../profiles/default/workflows/programmanagement/definition.xml') # noqa
    dc_workflow = workflow_tree.getroot()
    elements = list(dc_workflow)
    TRANSITIONS = {}
    STATES = {}
    for element in elements:
        tag = element.tag
        if tag == 'transition':
            transition = element
            id = transition.attrib['transition_id']
            TRANSITIONS[id] = transition.attrib
            sub_elements = list(transition)
            for sub_element in sub_elements:
                if sub_element.tag == 'guard':
                    guard_roles = [role.text for role in list(sub_element)]
                    TRANSITIONS[id]['guard_roles'] = guard_roles
                else:
                    TRANSITIONS[id][sub_element.tag] = sub_element.attrib
        elif tag == 'state':
            state = element
            id = state.attrib['state_id']
            STATES[id] = state.attrib
            STATES[id]['exit_transitions'] = []
            STATES[id]['permission_maps'] = []
            sub_elements = list(state)
            for sub_element in sub_elements:
                tag = sub_element.tag
                if tag == 'exit-transition':
                    exit_transition = sub_element
                    STATES[id]['exit_transitions'].append(
                        exit_transition.attrib['transition_id'],
                    )
                elif tag == 'permission-map':
                    permission_map = sub_element
                    attribs = permission_map.attrib
                    attrib_name = [role.text for role in list(permission_map)]
                    STATES[id]['permission_maps'].append(
                        {
                            attribs['name']: attrib_name,
                            'acquired': attribs['acquired'],
                        },
                    )
    return (TRANSITIONS, STATES)


ROLES = get_roles()
TRANSITIONS, STATES = get_transitions_and_states()
TRANSITIONS_FROM_INITIAL = {
        'applicants-considering-change': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-applicants-considering-change',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel-after-change',
        },
        'application-intake-in-progress': {
            'previous_state': None,
            'final_transition': 'submit-non-sponsored-program',
            # 'transition_to_initial_next_step': 'manager-return-to-initial',
        },
        'cancelled': {
            'previous_state': None,
            'final_transition': 'cancel',
            # 'transition_to_initial_next_step': 'manager-return-to-initial',
        },
        'declined': {
            'previous_state': 'pending-chair-review',
            'final_transition': 'decline',
            # 'transition_to_initial_next_step': 'manager-return-to-pending-chair-review',  # noqa : E501
        },
        'final-payment-billing-in-progress': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-final-payment-billing-in-progress',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'final-program-accounting-in-progress': {
            'previous_state': 'travel-expense-report-student-evaluations-due-to',  # noqa : E501
            'final_transition': 'confirm-ter-received',
            # 'transition_to_initial_next_step': 'manager-return-to-travel-expense-report-student-evaluations-due-to',  # noqa : E501
        },
        'incident-in-progress': {
            'previous_state': 'program-in-progress',
            'final_transition': 'report-incident',
            # 'transition_to_initial_next_step': 'end-incident',
        },
        'initial': {
            'previous_state': None,
            'final_transition': None,
            # 'transition_to_initial_next_step': None,
        },
        'initial-payment-billing-in-progress': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-initial-payment-billing-in-progress',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-arrival-abroad': {
            'previous_state': 'pending-program-departure',
            'final_transition': 'depart-sponsored-program',
            # 'transition_to_initial_next_step': 'manager-return-to-pending-program-departure',  # noqa : E501
        },
        'pending-chair-review': {
            'previous_state': None,
            'final_transition': 'submit-to-chair',
            # 'transition_to_initial_next_step': 'manager-return-to-initial',
        },
        'pending-dean-unit-director-review': {
            'previous_state': None,
            'final_transition': 'manager-return-to-pending-dean-unit-director-review',  # noqa : E501
            # 'transition_to_initial_next_step': 'return-to-initial',
        },
        'pending-discussions-with-program-manager': {
            'previous_state': None,
            'final_transition': 'manager-return-to-pending-discussions-with-program-manager',  # noqa : E501
            # 'transition_to_initial_next_step': 'return-to-initial',
        },
        'pending-final-program-fee': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-final-program-fee',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-oie-review': {
            'previous_state': None,
            'final_transition': 'manager-return-to-pending-oie-review',
            # 'transition_to_initial_next_step': 'return-to-initial',
        },
        'pending-program-departure': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-program-departure',
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-program-fee-determination-by-oie': {
            'previous_state': None,
            'final_transition': 'submit-sponsored-program',
            # 'transition_to_initial_next_step': 'manager-return-to-initial',
        },
        'pending-program-leader-operational-briefing': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-program-leader-operational-briefing',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-program-leader-orientation': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-program-leader-orientation',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-provider-responses': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-provider-responses',
            # 'transition_to_initial_next_step': 'cancel',
        },
        'pending-provost-review': {
            'previous_state': 'pending-oie-review',
            'final_transition': 'submit-to-provost',
            # 'transition_to_initial_next_step': 'manager-return-to-pending-oie-review',  # noqa : E501
        },
        'pending-travel-advance': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-pending-travel-advance',
            # 'transition_to_initial_next_step': 'cancel',
        },
        'process-refunds-budget-transfers': {
            'previous_state': 'final-program-accounting-in-progress',
            'final_transition': 'process-refunds',
            # 'transition_to_initial_next_step': 'manager-return-to-final-program-accounting-in-progress',  # noqa : E501
        },
        'program-completed': {
            'previous_state': 'process-refunds-budget-transfers',
            'final_transition': 'archive-program',
            # 'transition_to_initial_next_step': 'manager-return-to-process-refunds-budget-transfers',  # noqa : E501
        },
        'program-fee-pending-publication': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-program-fee-pending-publication',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'program-fee-under-liaison-review': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-program-fee-under-liaison-review',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'program-in-progress': {
            'previous_state': 'pending-arrival-abroad',
            'final_transition': 'confirm-safe-arrival',
            # 'transition_to_initial_next_step': 'manager-return-to-pending-arrival-abroad',  # noqa : E501
        },
        'provider-proposals-under-liaison-review': {
            'previous_state': None,
            'final_transition': 'manager-return-to-provider-proposals-under-liaison-review',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
            # 'to_initial_previous_state': 'cancelled',
        },
        'provider-proposals-under-oie-review': {
            'previous_state': None,
            'final_transition': 'manager-return-to-provider-proposals-under-oie-review',  # noqa : E501
            # 'transition_to_initial_next_step': 'return-to-initial',
        },
        'request-for-proposals-under-development': {
            'previous_state': None,
            'final_transition': 'manager-return-to-request-for-proposals-under-development',  # noqa : E501
            # 'transition_to_initial_next_step': 'return-to-initial',
        },
        'request-for-proposals-under-liaison-review': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-request-for-proposals-under-liaison-review',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'reviewing-final-program-details': {
            'previous_state': 'cancelled',
            'final_transition': 'manager-return-to-reviewing-final-program-details',  # noqa : E501
            # 'transition_to_initial_next_step': 'cancel',
        },
        'suspended': {
            'previous_state': 'application-intake-in-progress',
            'final_transition': 'suspend',
            # 'transition_to_initial_next_step': 'manager-return-to-application-intake-in-progress',  # noqa : E501
        },
        'travel-expense-report-student-evaluations-due-to': {
            'previous_state': 'program-in-progress',
            'final_transition': 'confirm-return',
            # 'transition_to_initial_next_step': 'manager-return-to-program-in-progress',  # noqa : E501
        },
        'withdrawn': {
            'previous_state': None,
            'final_transition': 'withdraw-application',
            # 'transition_to_initial_next_step': 'manager-return-to-initial',
        },
    }


class OIEStudyAbroadContentBaseTest(unittest.TestCase):
    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING
    participant_name = 'OIEStudyAbroadParticipant'
    program_name = 'OIEStudyAbroadProgram'

    def create_test_program(self, safe_id=True):
        return content.create(
            container=self.portal,
            type=self.program_name,
            id='sample-program',
            calendar_year=self.calendar_year_uid,
            term='1 Fall Interim',
            college_or_unit='B College of Business',
            countries=['Afghanistan'],
            safe_id=safe_id,
        )

    def create_test_participant(self):
        return content.create(
            container=self.portal,
            type=self.participant_name,
            id='sample-participant',
            programName=content.get_uuid(obj=self.program),
        )

    def get_calendar_year_and_uid(self):
        calendar_year = content.create(
            container=self.portal,
            type='OIECalendarYear',
            id='2020',
        )
        uid = content.get_uuid(obj=calendar_year)
        return (calendar_year, uid)

    def assertIsSubset(self, sub_list, super_list):
        return set(sub_list) <= set(super_list)
    # helper methods

    def _transition_and_or_roles_test(
        self,
        fast,
        initial_state,
        transition,
        end_state,
        authorized_roles,
    ):
        if fast:
            self.assertEqual(content.get_state(obj=self.test_obj),
                             initial_state)
            content.transition(obj=self.test_obj, transition=transition)
            self.assertEqual(content.get_state(obj=self.test_obj),
                             end_state)
        else:
            self._verify_transition_by_all_roles(
                obj=self.test_obj,
                initial_state=initial_state,
                authorized_roles=authorized_roles,
                transition=transition,
                destination_state=end_state,
                end_state=initial_state,
            )

    def _verify_transition_by_all_roles(
        self,
        obj=None,
        initial_state=None,
        authorized_roles=None,
        unauthorized_roles=None,
        transition=None,
        destination_state=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(initial_state, STATES.keys())
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(destination_state, STATES.keys())
        self.assertIn(end_state, STATES.keys())
        self.assertIsSubset(authorized_roles, ROLES)
        if unauthorized_roles is None:
            unauthorized_roles = list(ROLES - set(authorized_roles))
        self._verify_allowed_transition_by_roles(
            obj=obj,
            initial_state=initial_state,
            roles=authorized_roles,
            transition=transition,
            destination_state=destination_state,
            end_state=end_state,
        )
        # verify can view the item
        # verify can view viewable fields
        # verify can edit editable fields

        self._verify_unauthorized_transition_by_roles(
            obj=obj,
            initial_state=initial_state,
            roles=unauthorized_roles,
            transition=transition,
            end_state=end_state,
        )
        # verify cannot view item
        # verify cannot view certain fields
        # verify cannot edit certain fields

        # check if we have to get to the destination_state
        if content.get_state(obj=obj) != destination_state:
            self._switch_role(obj, 'Manager')
            self._transition_to_state(
                obj,
                transition=transition,
                state=destination_state,
            )

    def _verify_allowed_transition_by_roles(
        self,
        obj=None,
        initial_state=None,
        roles=None,
        transition=None,
        destination_state=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(initial_state, STATES.keys())
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(destination_state, STATES.keys())
        self.assertIn(end_state, STATES.keys())
        for role in roles:
            self._verify_allowed_transition_by_role(
                obj=obj,
                initial_state=initial_state,
                role=role,
                transition=transition,
                destination_state=destination_state,
                end_state=end_state,
            )

    def _verify_allowed_transition_by_role(
        self,
        obj=None,
        initial_state=None,
        role=None,
        transition=None,
        destination_state=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(initial_state, STATES.keys())
        self.assertIn(role, ROLES)
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(destination_state, STATES.keys())
        self.assertIn(end_state, STATES.keys())
        self.assertEqual(content.get_state(obj=obj), initial_state)
        self._switch_role(obj, role)
        content.transition(obj=obj, transition=transition)
        self.assertEqual(content.get_state(obj=obj), destination_state)
        # send it back to the end state
        self._transition_to_state(obj, destination_state=end_state)

    def _verify_unauthorized_transition_by_roles(
        self,
        obj=None,
        initial_state=None,
        roles=None,
        transition=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(initial_state, STATES.keys())
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(end_state, STATES.keys())
        for role in roles:
            self._verify_unauthorized_transition_by_role(
                obj=obj,
                initial_state=initial_state,
                role=role,
                transition=transition,
                end_state=end_state,
            )

    def _verify_unauthorized_transition_by_role(
        self,
        obj=None,
        initial_state=None,
        role=None,
        transition=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(initial_state, STATES.keys())
        self.assertIn(role, ROLES)
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(end_state, STATES.keys())
        self.assertEqual(content.get_state(obj=obj), initial_state)
        self._switch_role(obj, role)
        self._attempt_invalid_transition(
            obj,
            transition=transition,
            end_state=end_state,
        )

    def _attempt_invalid_transition(
        self,
        obj=None,
        transition=None,
        end_state=None,
    ):
        self.assertIsNotNone(obj)
        self.assertIn(transition, TRANSITIONS)
        self.assertIn(end_state, STATES.keys())
        error_str = ''
        try:
            content.transition(obj=obj, transition=transition)
        except InvalidParameterError as e:
            error_str = e.message
        found_expected_error = 'Invalid transition' in error_str
        self.assertTrue(found_expected_error)
        self.assertEqual(content.get_state(obj=obj), end_state)

    def _get_roles_in_context(self, obj):
        return get_user_roles(obj=obj)
        # getSecurityManager().getUser().getRolesInContext(obj)  # noqa

    def _switch_role(self, obj=None, role=None):
        self.assertIsNotNone(obj)
        self.assertIn(role, ROLES)
        setRoles(self.portal, TEST_USER_ID, [role])
        self.assertTrue(role in self._get_roles_in_context(obj))

    def _transition_to_state(self, obj=None, destination_state=None):
        self.assertIsNotNone(obj)
        self.assertIn(destination_state, STATES.keys())
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertTrue('Manager' in self._get_roles_in_context(obj))
        transition_steps = self._get_transition_steps_to_state(state=destination_state)  # noqa : E501
        obj = self._transition_to_initial(obj)
        self._recursive_transition_to_state(obj, transition_steps)
        self.assertEqual(content.get_state(obj=obj), destination_state)
        return obj

    def _transition_to_initial(self, obj):
        if content.get_state(obj=obj) == 'initial':
            return obj
        elif obj.portal_type == self.program_name:
            return self.create_test_program()
        elif obj.portal_type == self.participant_name:
            return self.create_test_participant()
        else:
            return

    def _get_transition_steps_to_state(self, state):
        previous_state = TRANSITIONS_FROM_INITIAL[state]['previous_state']
        final_transition = TRANSITIONS_FROM_INITIAL[state]['final_transition']
        if previous_state is not None:
            return (self._get_transition_steps_to_state(state=previous_state) +
                    [final_transition])
        else:
            transition = TRANSITIONS_FROM_INITIAL[state]['final_transition']
            return [transition] if transition is not None else []

    def _recursive_transition_to_state(self, obj, transition_steps):
        for transition in transition_steps:
            content.transition(obj=obj, transition=transition)
