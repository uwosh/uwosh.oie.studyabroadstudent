# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa

import unittest


class OIEStudyAbroadContentBaseTest(unittest.TestCase):
    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    ALL_ROLES = set(
        ['Mgmt_Admin', 'Manager', 'Mgmt_Coordinator', 'Mgmt_Manager',
         'Mgmt_Liaison', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
         'Mgmt_Financial', 'Mgmt_OIEProfessional', 'Mgmt_Intern',
         'Mgmt_ProgramLeader', 'Mgmt_LeaderReview',
         'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
         'Participant_Director', 'Participant_Manager',
         'Participant_Coordinator', 'Participant_Financial',
         'Participant_Financial', 'Participant_Intern',
         'Participant_Liaison', 'Participant_ProgramLeader',
         'Participant_FinancialAid', 'Participant_Provost',
         'Participant_DeanOfStudents', 'Participant_Health',
         'Participant_Health', 'Participant_Reference',
         'Participant_RiskMgmt', 'Participant_Applicant', 'Anonymous'],
    )

    # helper methods

    def _transition_and_or_roles_test(self, fast, initial_state, transition,
                                      end_state, authorized_roles):
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program),
                             initial_state)
            api.content.transition(obj=self.program, transition=transition)
            self.assertEqual(api.content.get_state(obj=self.program),
                             end_state)
        else:
            self._verify_transition_by_all_roles(
                obj=self.program,
                initial_state=initial_state,
                authorized_roles=authorized_roles,
                transition=transition,
                destination_state=end_state,
                return_transition='manager-return-to-{0}'.format(initial_state),  # noqa
                end_state=initial_state,
            )

    def _verify_transition_by_all_roles(self,
                                        obj=None,
                                        initial_state=None,
                                        authorized_roles=None,
                                        unauthorized_roles=None,
                                        transition=None,
                                        destination_state=None,
                                        return_transition=None,
                                        end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(authorized_roles)
        if unauthorized_roles is None:
            unauthorized_roles = list(self.ALL_ROLES - set(authorized_roles))
        # self.assertIsNotNone(unauthorized_roles)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(destination_state)
        self.assertIsNotNone(return_transition)
        self.assertIsNotNone(end_state)
        self._verify_allowed_transition_by_roles(
            obj=obj,
            initial_state=initial_state,
            roles=authorized_roles,
            transition=transition,
            destination_state=destination_state,
            return_transition=return_transition,
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
        if api.content.get_state(obj=obj) != destination_state:
            self._switch_role(obj, 'Manager')
            self._transition_to_state(obj,
                                      transition=transition,
                                      state=destination_state)

    def _verify_allowed_transition_by_roles(self,
                                            obj=None,
                                            initial_state=None,
                                            roles=None,
                                            transition=None,
                                            destination_state=None,
                                            return_transition=None,
                                            end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(roles)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(destination_state)
        self.assertIsNotNone(return_transition)
        self.assertIsNotNone(end_state)
        for role in roles:
            self._verify_allowed_transition_by_role(
                obj=obj,
                initial_state=initial_state,
                role=role,
                transition=transition,
                destination_state=destination_state,
                return_transition=return_transition,
                end_state=end_state,
            )

    def _verify_allowed_transition_by_role(self,
                                           obj=None,
                                           initial_state=None,
                                           role=None, transition=None,
                                           destination_state=None,
                                           return_transition=None,
                                           end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(role)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(destination_state)
        self.assertIsNotNone(return_transition)
        self.assertIsNotNone(end_state)
        self.assertEqual(api.content.get_state(obj=obj), initial_state)
        self._switch_role(obj, role)
        api.content.transition(obj=obj, transition=transition)
        self.assertEqual(api.content.get_state(obj=obj), destination_state)
        # send it back to the end state
        self._transition_to_state(obj,
                                  transition=return_transition,
                                  state=end_state)

    def _verify_unauthorized_transition_by_roles(self,
                                                 obj=None,
                                                 initial_state=None,
                                                 roles=None,
                                                 transition=None,
                                                 end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(roles)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        for role in roles:
            self._verify_unauthorized_transition_by_role(
                obj=obj,
                initial_state=initial_state,
                role=role,
                transition=transition,
                end_state=end_state,
            )

    def _verify_unauthorized_transition_by_role(self,
                                                obj=None,
                                                initial_state=None,
                                                role=None,
                                                transition=None,
                                                end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(role)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        self.assertEqual(api.content.get_state(obj=obj), initial_state)
        self._switch_role(obj, role)
        self._attempt_invalid_transition(obj,
                                         transition=transition,
                                         end_state=end_state)

    def _attempt_invalid_transition(self,
                                    obj=None,
                                    transition=None,
                                    end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        error_str = ''
        try:
            api.content.transition(obj=obj, transition=transition)
        except InvalidParameterError as e:
            error_str = e.message
        found_expected_error = 'Invalid transition' in error_str
        if not found_expected_error:
            import pdb;pdb.set_trace()  # noqa
        self.assertTrue(found_expected_error)
        self.assertEqual(api.content.get_state(obj=obj), end_state)

    def _switch_role(self, obj=None, role=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(role)
        setRoles(self.portal, TEST_USER_ID, [role])
        self.assertTrue(role in getSecurityManager().getUser().getRolesInContext(obj))  # noqa

    def _transition_to_state(self, obj=None, transition=None, state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(state)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(obj))  # noqa
        api.content.transition(obj=obj, transition=transition)
        self.assertEqual(api.content.get_state(obj=obj), state)
