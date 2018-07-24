# -*- coding: utf-8 -*-
from AccessControl import Unauthorized, getSecurityManager
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login, logout
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class OIEStudyAbroadProgramIntegrationTest(unittest.TestCase):
    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    ALL_ROLES = set(
        ['Mgmt_Admin', 'Manager', 'Mgmt_Coordinator', 'Mgmt_Manager', 'Mgmt_Liaison', 'Mgmt_Dean', 'Mgmt_Chair',
         'Mgmt_Provost', 'Mgmt_Financial', 'Mgmt_OIEProfessional', 'Mgmt_Intern', 'Mgmt_ProgramLeader',
         'Mgmt_LeaderReview', 'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt', 'Participant_Director', 'Participant_Manager',
         'Participant_Coordinator', 'Participant_Financial', 'Participant_Financial', 'Participant_Intern',
         'Participant_Liaison', 'Participant_ProgramLeader', 'Participant_FinancialAid', 'Participant_Provost',
         'Participant_DeanOfStudents', 'Participant_Health', 'Participant_Health', 'Participant_Reference',
         'Participant_RiskMgmt', 'Participant_Applicant', 'Anonymous']
    )

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        # add calendar year
        self.calendar_year = api.content.create(
            container=self.portal,
            type='OIECalendarYear',
            id='2018'
        )
        self.calendar_year_uid = api.content.get_uuid(obj=self.calendar_year)

        # add a sample program
        self.program = api.content.create(
            container=self.portal,
            type='OIEStudyAbroadProgram',
            id='sample-program',
            calendar_year=self.calendar_year_uid,
            term='1 Fall Interim',
            college_or_unit='B College of Business',
            countries=['Afghanistan'],
        )

    # helper methods

    def _verify_transition_by_all_roles(self, obj=None, initial_state=None, authorized_roles=None,
                                        unauthorized_roles=None, transition=None, destination_state=None,
                                        return_transition=None, end_state=None):
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
        self._verify_allowed_transition_by_roles(obj=obj, initial_state=initial_state, roles=authorized_roles,
                                                 transition=transition, destination_state=destination_state,
                                                 return_transition=return_transition, end_state=end_state)
        # verify can view the item
        # verify can view viewable fields
        # verify can edit editable fields

        self._verify_unauthorized_transition_by_roles(obj=obj, initial_state=initial_state, roles=unauthorized_roles,
                                                      transition=transition, end_state=end_state)
        # verify cannot view item
        # verify cannot view certain fields
        # verify cannot edit certain fields

        # check if we have to get to the destination_state
        if api.content.get_state(obj=obj) != destination_state:
            self._switch_role(obj, 'Manager')
            self._transition_to_state(obj, transition=transition, state=destination_state)

    def _verify_allowed_transition_by_roles(self, obj=None, initial_state=None, roles=None, transition=None,
                                            destination_state=None,
                                            return_transition=None, end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(roles)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(destination_state)
        self.assertIsNotNone(return_transition)
        self.assertIsNotNone(end_state)
        for role in roles:
            self._verify_allowed_transition_by_role(obj=obj, initial_state=initial_state, role=role,
                                                    transition=transition, destination_state=destination_state,
                                                    return_transition=return_transition, end_state=end_state)

    def _verify_allowed_transition_by_role(self, obj=None, initial_state=None, role=None, transition=None,
                                           destination_state=None,
                                           return_transition=None, end_state=None):
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
        self._transition_to_state(obj, transition=return_transition, state=end_state)

    def _verify_unauthorized_transition_by_roles(self, obj=None, initial_state=None, roles=None, transition=None,
                                                 end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(roles)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        for role in roles:
            self._verify_unauthorized_transition_by_role(obj=obj, initial_state=initial_state, role=role,
                                                         transition=transition,
                                                         end_state=end_state)

    def _verify_unauthorized_transition_by_role(self, obj=None, initial_state=None, role=None, transition=None,
                                                end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(initial_state)
        self.assertIsNotNone(role)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        self.assertEqual(api.content.get_state(obj=obj), initial_state)
        self._switch_role(obj, role)
        self._attempt_invalid_transition(obj, transition=transition, end_state=end_state)

    def _attempt_invalid_transition(self, obj=None, transition=None, end_state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(end_state)
        error_str = ''
        try:
            api.content.transition(obj=obj, transition=transition)
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)
        self.assertEqual(api.content.get_state(obj=obj), end_state)

    def _switch_role(self, obj=None, role=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(role)
        setRoles(self.portal, TEST_USER_ID, [role])
        self.assertTrue(role in getSecurityManager().getUser().getRolesInContext(obj))

    def _transition_to_state(self, obj=None, transition=None, state=None):
        self.assertIsNotNone(obj)
        self.assertIsNotNone(transition)
        self.assertIsNotNone(state)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(obj))
        api.content.transition(obj=obj, transition=transition)
        self.assertEqual(api.content.get_state(obj=obj), state)

    # actual tests

    def test_is_addon_installed(self):
        self.assertTrue(self.installer.isProductInstalled('uwosh.oie.studyabroadstudent'))

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadProgram')
        schema = fti.lookupSchema()
        self.assertEqual(IOIEStudyAbroadProgram, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadProgram')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadProgram')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEStudyAbroadProgram.providedBy(obj))

    def test_can_add_a_program(self):
        obj = api.content.create(
            container=self.portal,
            type='OIEStudyAbroadProgram',
            id='sample-program-test-can-add-a-program',
            calendar_year=self.calendar_year_uid,
            term='1 Fall Interim',
            college_or_unit='B College of Business',
            countries=['Afghanistan'],
        )
        self.assertTrue(IOIEStudyAbroadProgram.providedBy(obj))

    def test_not_editable_by_anonymous(self):
        portal = self.layer['portal']
        logout()
        self.assertRaises(Unauthorized, portal.restrictedTraverse, 'sample-program/@@edit')

    def test_correct_default_workflow(self):
        portal = self.layer['portal']
        workflowTool = getToolByName(portal, 'portal_workflow')
        chains = dict(workflowTool.listChainOverrides())
        defaultChain = workflowTool.getDefaultChain()
        programChain = chains.get('OIEStudyAbroadProgram', defaultChain)
        self.assertEqual(programChain, ('programmanagement',))

    # workflow transitions from initial state

    def test_nonexistent_transition_by_manager(self):
        error_str = ''
        try:
            api.content.transition(obj=self.program, transition='this-transition-does-not-exist')
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)

    def test_cannot_transition_as_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        logout()
        self.assertRaises(InvalidParameterError, api.content.transition, obj=self.program,
                          transition='submit-to-chair')

    # all workflow transitions by manager

    # 1. Manager: Check that manager can execute this transition
    # 2. Authorized transitioners: Check each other role that can execute this transition
    # 3. Unauthorized transitions: Check that every other role CANNOT execute this transition
    # 4. Authorized viewers of the item
    # 5. Unauthorized viewers of the item
    # 6. Authorized viewers of the field values (list viewable fields)
    # 7. Unuthorized viewers of the field values (list viewable fields)
    # 8. Authorized editors of the field values (list editable fields)
    # 9. Unuthorized editors of the field values (list editable fields)
    def test_can_transition_by_manager_submit_to_chair(self, fast=None):
        """from initial
        1. Manager can transition
        2. authorized to transition: Mgmt_Admin; Mgmt_Liaison; Manager
        3. unauthorized to transition: everyone else!
        4. authorized item viewers
        5. unauthorized item viewers
        6. authorized field viewers (which fields?)
        7. unauthorized field viewers
        8. authorized field editors (which fields?)
        9. unauthorized field editors
        """
        # by default, roles will be ['Manager', 'Authenticated'] so verify that we have Manager role
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(self.portal))
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='submit-to-chair')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-chair-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='initial',
                                                 authorized_roles=['Manager', 'Mgmt_Admin', 'Mgmt_Liaison'],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Coordinator', 'Mgmt_Financial',
                                                 #                     'Mgmt_OIEProfessional', 'Mgmt_Intern',
                                                 #                     'Mgmt_ProgramLeader', 'Mgmt_Dean', 'Mgmt_Chair',
                                                 #                     'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder',
                                                 #                     'Mgmt_RiskMgmt', 'Participant_Director',
                                                 #                     'Participant_Manager', 'Participant_Coordinator',
                                                 #                     'Participant_Financial', 'Participant_Financial',
                                                 #                     'Participant_Intern', 'Participant_Liaison',
                                                 #                     'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid',
                                                 #                     'Participant_Provost', 'Participant_DeanOfStudents',
                                                 #                     'Participant_Health', 'Participant_Health',
                                                 #                     'Participant_Reference', 'Participant_RiskMgmt',
                                                 #                     'Participant_Applicant', 'Anonymous'],
                                                 transition='submit-to-chair', destination_state='pending-chair-review',
                                                 return_transition='return-to-initial', end_state='initial')

    def test_can_transition_by_manager_cancel_from_initial(self, fast=None):
        """from initial Mgmt_Admin; Mgmt_Director; Manager"""
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='cancel')
            self.assertEqual(api.content.get_state(obj=self.program), 'cancelled')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='initial',
                                                 authorized_roles=['Manager', 'Mgmt_Admin'],
                                                 # unauthorized_roles=['Mgmt_Liaison', 'Mgmt_Manager', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader', 'Mgmt_Dean',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='cancel', destination_state='cancelled',
                                                 return_transition='manager-return-to-initial',
                                                 end_state='initial')

    def test_can_transition_by_manager_withdraw_application_from_initial(self, fast=None):
        """from initial, Mgmt_Admin; Mgmt_Liaison; Manager"""
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='withdraw-application')
            self.assertEqual(api.content.get_state(obj=self.program), 'withdrawn')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='initial',
                                                 authorized_roles=['Manager', 'Mgmt_Admin', 'Mgmt_Liaison'],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader', 'Mgmt_Dean',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='withdraw-application', destination_state='withdrawn',
                                                 return_transition='manager-return-to-initial',
                                                 end_state='initial')

    def test_can_transition_by_manager_submit_sponsored_program(self, fast=None):
        """from initial, Mgmt_Coordinator; Mgmt_Admin; Manager"""
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='submit-sponsored-program')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='initial',
                                                 authorized_roles=['Manager', 'Mgmt_Admin', 'Mgmt_Coordinator'],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader', 'Mgmt_Dean',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-sponsored-program',
                                                 destination_state='pending-program-fee-determination-by-oie',
                                                 return_transition='manager-return-to-initial',
                                                 end_state='initial')

    def test_can_transition_by_manager_submit_non_sponsored_program(self, fast=None):
        """from initial, Mgmt_Coordinator; Mgmt_Admin; Manager"""
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='submit-non-sponsored-program')
            self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='initial',
                                                 authorized_roles=['Manager', 'Mgmt_Admin', 'Mgmt_Coordinator'],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader', 'Mgmt_Dean',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-non-sponsored-program',
                                                 destination_state='application-intake-in-progress',
                                                 return_transition='manager-return-to-initial',
                                                 end_state='initial')

    def test_can_transition_by_manager_submit_to_dean(self, fast=None):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Chair; or Manager"""
        # get it to the correct state
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-chair-review')
            api.content.transition(obj=self.program, transition='submit-to-dean')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-dean-unit-director-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-chair-review',
                                                 authorized_roles=['Manager', 'Mgmt_Chair', 'Mgmt_Admin', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader', 'Mgmt_Dean',
                                                 #                     'Mgmt_Provost', 'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-to-dean',
                                                 destination_state='pending-dean-unit-director-review',
                                                 return_transition='manager-return-to-pending-chair-review',
                                                 end_state='pending-chair-review')

    def test_can_transition_by_manager_decline_from_pending_chair_review(self, fast=None):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
            api.content.transition(obj=self.program, transition='decline')
            self.assertEqual(api.content.get_state(obj=self.program), 'declined')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-chair-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='decline',
                                                 destination_state='declined',
                                                 return_transition='manager-return-to-pending-chair-review',
                                                 end_state='pending-chair-review')

    def test_can_transition_by_manager_withdraw_application_from_pending_chair_review(self, fast=None):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-chair-review')
            api.content.transition(obj=self.program, transition='withdraw-application')
            self.assertEqual(api.content.get_state(obj=self.program), 'withdrawn')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-chair-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='withdraw-application',
                                                 destination_state='withdrawn',
                                                 return_transition='manager-return-to-pending-chair-review',
                                                 end_state='pending-chair-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_chair_review(self, fast=None):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-chair-review')
            api.content.transition(obj=self.program, transition='return-to-initial')
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-chair-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview', 'Mgmt_Provost',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-initial',
                                                 destination_state='initial',
                                                 return_transition='manager-return-to-pending-chair-review',
                                                 end_state='pending-chair-review')

    def test_can_transition_by_manager_submit_to_oie(self, fast=None):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin; Mgmt_Dean; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-dean-unit-director-review')
            api.content.transition(obj=self.program, transition='submit-to-oie')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-oie-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-dean-unit-director-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-to-oie',
                                                 destination_state='pending-oie-review',
                                                 return_transition='manager-return-to-pending-dean-unit-director-review',
                                                 end_state='pending-dean-unit-director-review')

    def test_can_transition_by_manager_decline_from_pending_dean_unit_director_review(self, fast=None):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-dean-unit-director-review')
            api.content.transition(obj=self.program, transition='decline')
            self.assertEqual(api.content.get_state(obj=self.program), 'declined')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-dean-unit-director-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost','Manager', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='decline',
                                                 destination_state='declined',
                                                 return_transition='manager-return-to-pending-dean-unit-director-review',
                                                 end_state='pending-dean-unit-director-review')

    def test_can_transition_by_manager_withdraw_application_from_pending_dean_unit_director_review(self, fast=None):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-dean-unit-director-review')
            api.content.transition(obj=self.program, transition='withdraw-application')
            self.assertEqual(api.content.get_state(obj=self.program), 'withdrawn')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-dean-unit-director-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Manager', 'Mgmt_Coordinator','Mgmt_Dean',
                                                 #                     'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='withdraw-application',
                                                 destination_state='withdrawn',
                                                 return_transition='manager-return-to-pending-dean-unit-director-review',
                                                 end_state='pending-dean-unit-director-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_dean_unit_director_review(self, fast=None):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-dean-unit-director-review')
            api.content.transition(obj=self.program, transition='return-to-initial')
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-dean-unit-director-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Liaison', 'Mgmt_Coordinator',
                                                 #                     'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-initial',
                                                 destination_state='initial',
                                                 return_transition='manager-return-to-pending-dean-unit-director-review',
                                                 end_state='pending-dean-unit-director-review')

    def test_can_transition_by_manager_withdraw_application_from_pending_oie_review(self, fast=None):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-oie-review')
            api.content.transition(obj=self.program, transition='withdraw-application')
            self.assertEqual(api.content.get_state(obj=self.program), 'withdrawn')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-oie-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator',
                                                 #                     'Mgmt_Provost', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='withdraw-application',
                                                 destination_state='withdrawn',
                                                 return_transition='manager-return-to-pending-oie-review',
                                                 end_state='pending-oie-review')

    def test_can_transition_by_manager_submit_to_provost(self, fast=None):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-oie-review')
            api.content.transition(obj=self.program, transition='submit-to-provost')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-oie-review',
                                                 authorized_roles=['Mgmt_Admin', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Provost', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-to-provost',
                                                 destination_state='pending-provost-review',
                                                 return_transition='manager-return-to-pending-oie-review',
                                                 end_state='pending-oie-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_oie_review(self, fast=None):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-oie-review')
            api.content.transition(obj=self.program, transition='return-to-initial')
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-oie-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-initial',
                                                 destination_state='initial',
                                                 return_transition='manager-return-to-pending-oie-review',
                                                 end_state='pending-oie-review')

    def test_can_transition_by_manager_approve_provosts_office(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
            api.content.transition(obj=self.program, transition='approve-provosts-office')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-provost-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='approve-provosts-office',
                                                 destination_state='pending-discussions-with-program-manager',
                                                 return_transition='manager-return-to-pending-provost-review',
                                                 end_state='pending-provost-review')

    def test_can_transition_by_manager_return_to_oie_review(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
            api.content.transition(obj=self.program, transition='return-to-oie-review')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-oie-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-provost-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-oie-review',
                                                 destination_state='pending-oie-review',
                                                 return_transition='manager-return-to-pending-provost-review',
                                                 end_state='pending-provost-review')

    def test_can_transition_by_manager_suspend_from_pending_provost_review(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
            api.content.transition(obj=self.program, transition='suspend')
            self.assertEqual(api.content.get_state(obj=self.program), 'suspended')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-provost-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='suspend',
                                                 destination_state='suspended',
                                                 return_transition='manager-return-to-pending-provost-review',
                                                 end_state='pending-provost-review')

    def test_can_transition_by_manager_decline_from_pending_provost_review(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
            api.content.transition(obj=self.program, transition='decline')
            self.assertEqual(api.content.get_state(obj=self.program), 'declined')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-provost-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='decline',
                                                 destination_state='declined',
                                                 return_transition='manager-return-to-pending-provost-review',
                                                 end_state='pending-provost-review')

    def test_can_transition_by_manager_withdraw_application_from_pending_provost_review(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provost-review')
            api.content.transition(obj=self.program, transition='withdraw-application')
            self.assertEqual(api.content.get_state(obj=self.program), 'withdrawn')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-provost-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Provost',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='withdraw-application',
                                                 destination_state='withdrawn',
                                                 return_transition='manager-return-to-pending-provost-review',
                                                 end_state='pending-provost-review')

    def test_can_transition_by_manager_develop_rfp(self, fast=None):
        """from pending-discussions-with-program-manager Requires role: Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
            api.content.transition(obj=self.program, transition='develop-rfp')
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-discussions-with-program-manager',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='develop-rfp',
                                                 destination_state='request-for-proposals-under-development',
                                                 return_transition='manager-return-to-pending-discussions-with-program-manager',
                                                 end_state='pending-discussions-with-program-manager')

    def test_can_transition_by_manager_return_to_initial_from_pending_discussions_with_program_manager(self, fast=None):
        """from pending-discussions-with-program-manager Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
            api.content.transition(obj=self.program, transition='return-to-initial')
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-discussions-with-program-manager',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-initial',
                                                 destination_state='initial',
                                                 return_transition='manager-return-to-pending-discussions-with-program-manager',
                                                 end_state='pending-discussions-with-program-manager')

    def test_can_transition_by_manager_cancel_from_pending_discussions_with_program_manager(self, fast=None):
        """from pending-discussions-with-program-manager Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
            api.content.transition(obj=self.program, transition='cancel')
            self.assertEqual(api.content.get_state(obj=self.program), 'cancelled')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-discussions-with-program-manager',
                                                 authorized_roles=['Mgmt_Admin', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison', 'Mgmt_Manager',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='cancel',
                                                 destination_state='cancelled',
                                                 return_transition='manager-return-to-pending-discussions-with-program-manager',
                                                 end_state='pending-discussions-with-program-manager')

    def test_can_transition_by_manager_suspend_from_pending_discussions_with_program_manager(self, fast=None):
        """from pending-discussions-with-program-manager Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
            api.content.transition(obj=self.program, transition='suspend')
            self.assertEqual(api.content.get_state(obj=self.program), 'suspended')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-discussions-with-program-manager',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='suspend',
                                                 destination_state='suspended',
                                                 return_transition='manager-return-to-pending-discussions-with-program-manager',
                                                 end_state='pending-discussions-with-program-manager')

    def test_can_transition_by_manager_pending_provider_proposal(self, fast=None):
        """from pending-discussions-with-program-manager Requires role: Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-discussions-with-program-manager')
            api.content.transition(obj=self.program, transition='pending-provider-proposal')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='pending-discussions-with-program-manager',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='pending-provider-proposal',
                                                 destination_state='pending-program-fee-determination-by-oie',
                                                 return_transition='manager-return-to-pending-discussions-with-program-manager',
                                                 end_state='pending-discussions-with-program-manager')

    def test_can_transition_by_manager_submit_rfp_for_liaison_review(self, fast=None):
        """from request-for-proposals-under-development Requires role: Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
            api.content.transition(obj=self.program, transition='submit-rfp-for-liaison-review')
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-liaison-review')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-development',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='submit-rfp-for-liaison-review',
                                                 destination_state='request-for-proposals-under-liaison-review',
                                                 return_transition='manager-return-to-request-for-proposals-under-development',
                                                 end_state='request-for-proposals-under-development')

    def test_can_transition_by_manager_return_to_initial_from_request_for_proposals_under_development(self, fast=None):
        """from request-for-proposals-under-development Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
            api.content.transition(obj=self.program, transition='return-to-initial')
            self.assertEqual(api.content.get_state(obj=self.program), 'initial')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-development',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-to-initial',
                                                 destination_state='initial',
                                                 return_transition='manager-return-to-request-for-proposals-under-development',
                                                 end_state='request-for-proposals-under-development')

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_development(self, fast=None):
        """from request-for-proposals-under-development Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
            api.content.transition(obj=self.program, transition='cancel')
            self.assertEqual(api.content.get_state(obj=self.program), 'cancelled')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-development',
                                                 authorized_roles=['Mgmt_Admin', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison', 'Mgmt_Manager',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='cancel',
                                                 destination_state='cancelled',
                                                 return_transition='manager-return-to-request-for-proposals-under-development',
                                                 end_state='request-for-proposals-under-development')

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_development(self, fast=None):
        """from request-for-proposals-under-development Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
            api.content.transition(obj=self.program, transition='suspend')
            self.assertEqual(api.content.get_state(obj=self.program), 'suspended')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-development',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Provost', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='suspend',
                                                 destination_state='suspended',
                                                 return_transition='manager-return-to-request-for-proposals-under-development',
                                                 end_state='request-for-proposals-under-development')

    def test_can_transition_by_manager_approve_rfp(self, fast=None):
        """from request-for-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-liaison-review')
            api.content.transition(obj=self.program, transition='approve-rfp')
            self.assertEqual(api.content.get_state(obj=self.program), 'pending-provider-responses')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-liaison-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Manager',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='approve-rfp',
                                                 destination_state='pending-provider-responses',
                                                 return_transition='manager-return-to-request-for-proposals-under-liaison-review',
                                                 end_state='request-for-proposals-under-liaison-review')

    def test_can_transition_by_manager_return_rfp_to_program_manager(self, fast=None):
        """from request-for-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-liaison-review')
            api.content.transition(obj=self.program, transition='return-rfp-to-program-manager')
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-development')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-liaison-review',
                                                 authorized_roles=['Mgmt_Admin', 'Mgmt_Liaison', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Manager',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='return-rfp-to-program-manager',
                                                 destination_state='request-for-proposals-under-development',
                                                 return_transition='manager-return-to-request-for-proposals-under-liaison-review',
                                                 end_state='request-for-proposals-under-liaison-review')

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_liaison_review(self, fast=None):
        """from request-for-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(fast=True)
        if fast:
            self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-liaison-review')
            api.content.transition(obj=self.program, transition='cancel')
            self.assertEqual(api.content.get_state(obj=self.program), 'cancelled')
        else:
            self._verify_transition_by_all_roles(obj=self.program, initial_state='request-for-proposals-under-liaison-review',
                                                 authorized_roles=['Mgmt_Admin', 'Manager', ],
                                                 # unauthorized_roles=['Mgmt_Coordinator', 'Mgmt_Manager', 'Mgmt_Liaison',
                                                 #                     'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost',
                                                 #                     'Mgmt_Financial', 'Mgmt_OIEProfessional',
                                                 #                     'Mgmt_Intern', 'Mgmt_ProgramLeader',
                                                 #                     'Mgmt_LeaderReview',
                                                 #                     'Mgmt_CourseBuilder', 'Mgmt_RiskMgmt',
                                                 #                     'Participant_Director', 'Participant_Manager',
                                                 #                     'Participant_Coordinator', 'Participant_Financial',
                                                 #                     'Participant_Financial', 'Participant_Intern',
                                                 #                     'Participant_Liaison', 'Participant_ProgramLeader',
                                                 #                     'Participant_FinancialAid', 'Participant_Provost',
                                                 #                     'Participant_DeanOfStudents', 'Participant_Health',
                                                 #                     'Participant_Health', 'Participant_Reference',
                                                 #                     'Participant_RiskMgmt', 'Participant_Applicant',
                                                 #                     'Anonymous'],
                                                 transition='cancel',
                                                 destination_state='cancelled',
                                                 return_transition='manager-return-to-request-for-proposals-under-liaison-review',
                                                 end_state='request-for-proposals-under-liaison-review')

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_liaison_review(self, fast=None):
        """from request-for-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(fast=True)
        self.assertEqual(api.content.get_state(obj=self.program), 'request-for-proposals-under-liaison-review')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_review_provider_proposals(self):
        """from pending-provider-responses"""
        self.test_can_transition_by_manager_approve_rfp()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-provider-responses')
        api.content.transition(obj=self.program, transition='review-provider-proposals')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_cancel_from_pending_provider_responses(self):
        """from pending-provider-responses Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_rfp()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-provider-responses')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_provider_responses(self):
        """from pending-provider-responses Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_rfp()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-provider-responses')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_initial_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-oie-review')
        api.content.transition(obj=self.program, transition='return-to-initial')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_submit_proposal_to_liaison(self):
        """from provider-proposals-under-oie-review"""
        self.test_can_transition_by_manager_review_provider_proposals()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-oie-review')
        api.content.transition(obj=self.program, transition='submit-proposal-to-liaison')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'provider-proposals-under-liaison-review')

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-oie-review')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-oie-review')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_oie(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-liaison-review')
        api.content.transition(obj=self.program, transition='return-to-oie')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_liaison_review(self):
        """from provider-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-liaison-review')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_liaison_review(self):
        """from provider-proposals-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-liaison-review')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_approve_proposal(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        self.assertEqual(api.content.get_state(obj=self.program), 'provider-proposals-under-liaison-review')
        api.content.transition(obj=self.program, transition='approve-proposal')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    def test_can_transition_by_manager_submit_fee_for_liaison_review(self):
        """from pending-program-fee-determination-by-oie"""
        self.test_can_transition_by_manager_approve_proposal()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        api.content.transition(obj=self.program, transition='submit-fee-for-liaison-review')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-fee-under-liaison-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie Requires role: Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_proposal()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        api.content.transition(obj=self.program, transition='return-to-initial')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_cancel_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_proposal()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_proposal()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-fee-determination-by-oie')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_oie(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-under-liaison-review')
        api.content.transition(obj=self.program, transition='return-to-oie')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_suspend_from_program_fee_under_liaison_review(self):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-under-liaison-review')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_program_fee_under_liaison_review(self):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-under-liaison-review')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_approve_fee(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-under-liaison-review')
        api.content.transition(obj=self.program, transition='approve-fee')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-fee-pending-publication')

    def test_can_transition_by_manager_publish_fee(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-pending-publication')
        api.content.transition(obj=self.program, transition='publish-fee')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'application-intake-in-progress')

    def test_can_transition_by_manager_cancel_from_program_fee_pending_publication(self):
        """from program-fee-pending-publication Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-pending-publication')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_program_fee_pending_publication(self):
        """from program-fee-pending-publication Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-pending-publication')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_announce_programmatic_for_fee_change(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-fee-pending-publication')
        api.content.transition(obj=self.program, transition='announce-programmatic-for-fee-change')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'applicants-considering-change')

    def test_can_transition_by_manager_confirm_to_run_from_applicants_considering_change(self):
        """from applicants-considering-change"""
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change()
        self.assertEqual(api.content.get_state(obj=self.program), 'applicants-considering-change')
        api.content.transition(obj=self.program, transition='confirm-to-run')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'initial-payment-billing-in-progress')

    def test_can_transition_by_manager_cancel_after_change(self):
        """from applicants-considering-change"""
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change()
        self.assertEqual(api.content.get_state(obj=self.program), 'applicants-considering-change')
        api.content.transition(obj=self.program, transition='cancel-after-change')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_confirm_to_run(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        api.content.transition(obj=self.program, transition='confirm-to-run')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'initial-payment-billing-in-progress')

    def test_can_transition_by_manager_suspend_from_application_intake_in_progress(self):
        """from application-intake-in-progress Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_publish_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_application_intake_in_progress(self):
        """from application-intake-in-progress Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_publish_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_send_for_programmatic_change(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        api.content.transition(obj=self.program, transition='send-for-programmatic-change')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_send_for_fee_change(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'application-intake-in-progress')
        api.content.transition(obj=self.program, transition='send-for-fee-change')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    # TODO provider-proposals-under-oie-review

    def test_can_transition_by_manager_send_bills_for_initial_payment(self):
        """from initial-payment-billing-in-progress"""
        self.test_can_transition_by_manager_confirm_to_run()
        self.assertEqual(api.content.get_state(obj=self.program), 'initial-payment-billing-in-progress')
        api.content.transition(obj=self.program, transition='send-bills-for-initial-payment')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-final-program-fee')

    def test_can_transition_by_manager_cancel_from_initial_payment_billing_in_progress(self):
        """from initial-payment-billing-in-progress Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_to_run()
        self.assertEqual(api.content.get_state(obj=self.program), 'initial-payment-billing-in-progress')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_initial_payment_billing_in_progress(self):
        """from initial-payment-billing-in-progress Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_to_run()
        self.assertEqual(api.content.get_state(obj=self.program), 'initial-payment-billing-in-progress')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_publish_final_fee(self):
        """from pending-final-program-fee"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-final-program-fee')
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-final-program-fee')
        api.content.transition(obj=self.program, transition='publish-final-fee')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'final-payment-billing-in-progress')

    def test_can_transition_by_manager_cancel_from_pending_final_program_fee(self):
        """from pending-final-program-fee Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-final-program-fee')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_final_program_fee(self):
        """from pending-final-program-fee Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-final-program-fee')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_bill_for_final_payment(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'final-payment-billing-in-progress')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='bill-for-final-payment')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-leader-orientation')

    def test_can_transition_by_manager_cancel_from_final_payment_billing_in_progress(self):
        """from final-payment-billing-in-progress Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_publish_final_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'final-payment-billing-in-progress')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_final_payment_billing_in_progress(self):
        """from final-payment-billing-in-progress Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_publish_final_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'final-payment-billing-in-progress')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_bill_for_final_payment_programs_with_no_leader(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        self.assertEqual(api.content.get_state(obj=self.program), 'final-payment-billing-in-progress')
        # TODO only for programs with no leader
        api.content.transition(obj=self.program, transition='bill-for-final-payment-programs-with-no-leader')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_confirm_orientation_completed(self):
        """from pending-program-leader-orientation"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-orientation')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='confirm-orientation-completed')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-travel-advance')

    def test_can_transition_by_manager_cancel_from_pending_program_leader_orientation(self):
        """from pending-program-leader-orientation Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-orientation')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_leader_orientation(self):
        """from pending-program-leader-orientation Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-orientation')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_travel_advance_ready(self):
        """from pending-travel-advance"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-travel-advance')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='travel-advance-ready')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'reviewing-final-program-details')

    def test_can_transition_by_manager_cancel_from_pending_travel_advance(self):
        """from pending-travel-advance Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-travel-advance')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_travel_advance(self):
        """from pending-travel-advance Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-travel-advance')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_schedule_operational_briefing(self):
        """from reviewing-final-program-details"""
        self.test_can_transition_by_manager_travel_advance_ready()
        self.assertEqual(api.content.get_state(obj=self.program), 'reviewing-final-program-details')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='schedule-operational-briefing')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-leader-operational-briefing')

    def test_can_transition_by_manager_cancel_from_reviewing_final_program_details(self):
        """from reviewing-final-program-details Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_travel_advance_ready()
        self.assertEqual(api.content.get_state(obj=self.program), 'reviewing-final-program-details')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_reviewing_final_program_details(self):
        """from reviewing-final-program-details Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_travel_advance_ready()
        self.assertEqual(api.content.get_state(obj=self.program), 'reviewing-final-program-details')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_confirm_briefing_completed(self):
        """from pending-program-leader-operational-briefing"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-operational-briefing')
        # TODO only for programs with leader
        api.content.transition(obj=self.program, transition='confirm-briefing-completed')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_cancel_from_pending_program_leader_operational_briefing(self):
        """from pending-program-leader-operational-briefing Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-operational-briefing')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_leader_operational_briefing(self):
        """from pending-program-leader-operational-briefing Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-leader-operational-briefing')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_depart(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-departure')
        # TODO only for programs with individuals
        api.content.transition(obj=self.program, transition='depart')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_cancel_from_pending_program_departure(self):
        """from pending-program-departure Requires role: Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-departure')
        api.content.transition(obj=self.program, transition='cancel')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_departure(self):
        """from pending-program-departure Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-departure')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_depart_sponsored_program(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-departure')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='depart-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_depart_non_sponsored_program(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-program-departure')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='depart-non-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_suspend_from_pending_arrival_abroad(self):
        """from pending-arrival-abroad Requires role: Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-arrival-abroad')
        api.content.transition(obj=self.program, transition='suspend')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_confirm_safe_arrival(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-arrival-abroad')
        # TODO only for programs with individuals
        api.content.transition(obj=self.program, transition='confirm-safe-arrival')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_confirm_travel_delay(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-arrival-abroad')
        # TODO only for programs with individuals
        api.content.transition(obj=self.program, transition='confirm-travel-delay')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_arrive_sponsored_program(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-arrival-abroad')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='arrive-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_arrive_non_sponsored_program(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        self.assertEqual(api.content.get_state(obj=self.program), 'pending-arrival-abroad')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='arrive-non-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_confirm_return(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-in-progress')
        api.content.transition(obj=self.program, transition='confirm-return')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'travel-expense-report-student-evaluations-due-to')

    def test_can_transition_by_manager_returned_sponsored_program(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-in-progress')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='returned-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-completed')

    def test_can_transition_by_manager_returned_non_sponsored_program(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        self.assertEqual(api.content.get_state(obj=self.program), 'program-in-progress')
        # TODO only for programs with groups
        api.content.transition(obj=self.program, transition='returned-non-sponsored-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-completed')

    def test_can_transition_by_manager_confirm_ter_received(self):
        """from travel-expense-report-student-evaluations-due-to"""
        self.test_can_transition_by_manager_confirm_return()
        self.assertEqual(api.content.get_state(obj=self.program), 'travel-expense-report-student-evaluations-due-to')
        api.content.transition(obj=self.program, transition='confirm-ter-received')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'final-program-accounting-in-progress')

    def test_can_transition_by_manager_process_refunds(self):
        """from final-program-accounting-in-progress"""
        self.test_can_transition_by_manager_confirm_ter_received()
        self.assertEqual(api.content.get_state(obj=self.program), 'final-program-accounting-in-progress')
        api.content.transition(obj=self.program, transition='process-refunds')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'process-refunds-budget-transfers')

    def test_can_transition_by_manager_archive_program(self):
        """from process-refunds-budget-transfers"""
        self.test_can_transition_by_manager_process_refunds()
        self.assertEqual(api.content.get_state(obj=self.program), 'process-refunds-budget-transfers')
        api.content.transition(obj=self.program, transition='archive-program')
        state = api.content.get_state(obj=self.program)
        self.assertEqual(state, 'program-completed')
