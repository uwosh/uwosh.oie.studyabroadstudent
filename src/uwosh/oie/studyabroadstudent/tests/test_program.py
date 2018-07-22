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
        obj = self.program
        error_str = ''
        try:
            api.content.transition(obj=obj, transition='this-transition-does-not-exist')
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)

    def test_cannot_transition_as_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        obj = self.program
        logout()
        self.assertRaises(InvalidParameterError, api.content.transition, obj=obj, transition='submit-to-chair')

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
    def test_can_transition_by_manager_submit_to_chair(self):
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
        # by default, roles will be ['Manager', 'Authenticated']
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(self.portal))
        obj = self.program
        self.transition_to_state(obj, 'submit-to-chair', 'pending-chair-review')

        # send it back to the previous state
        self.transition_to_state(obj, 'return-to-initial', 'initial')
        # change to another authorized role, verify new role can execute the same transition: Mgmt_Admin
        self.switch_role(obj, 'Mgmt_Admin')
        api.content.transition(obj=obj, transition='submit-to-chair')
        self.assertEqual(api.content.get_state(obj=obj), 'pending-chair-review')

        # send it back to the previous state
        self.transition_to_state(obj, 'return-to-initial', 'initial')
        # change to another authorized role, verify new role can execute the same transition: Mgmt_Liaison
        self.switch_role(obj, 'Mgmt_Liaison')
        api.content.transition(obj=obj, transition='submit-to-chair')
        self.assertEqual(api.content.get_state(obj=obj), 'pending-chair-review')

        self.transition_to_state(obj, 'return-to-initial', 'initial')

        # verify can view the item
        # verify can view all viewable fields
        # verify can edit all editable fields

        # change to an unauthorized role: Mgmt_Manager
        self.switch_role(obj, 'Mgmt_Manager')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Coordinator
        self.switch_role(obj, 'Mgmt_Coordinator')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Financial
        self.switch_role(obj, 'Mgmt_Financial')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_OIEProfessional
        self.switch_role(obj, 'Mgmt_OIEProfessional')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Intern
        self.switch_role(obj, 'Mgmt_Intern')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_ProgramLeader
        self.switch_role(obj, 'Mgmt_ProgramLeader')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Dean
        self.switch_role(obj, 'Mgmt_Dean')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Chair
        self.switch_role(obj, 'Mgmt_Chair')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_Provost
        self.switch_role(obj, 'Mgmt_Provost')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_LeaderReview
        self.switch_role(obj, 'Mgmt_LeaderReview')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_CourseBuilder
        self.switch_role(obj, 'Mgmt_CourseBuilder')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Mgmt_RiskMgmt
        self.switch_role(obj, 'Mgmt_RiskMgmt')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Director
        self.switch_role(obj, 'Participant_Director')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Manager
        self.switch_role(obj, 'Participant_Manager')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Coordinator
        self.switch_role(obj, 'Participant_Coordinator')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Financial
        self.switch_role(obj, 'Participant_Financial')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_OIEProfessional
        self.switch_role(obj, 'Participant_OIEProfessional')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Intern
        self.switch_role(obj, 'Participant_Intern')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Liaison
        self.switch_role(obj, 'Participant_Liaison')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_ProgramLeader
        self.switch_role(obj, 'Participant_ProgramLeader')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_FinancialAid
        self.switch_role(obj, 'Participant_FinancialAid')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Provost
        self.switch_role(obj, 'Participant_Provost')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_DeanOfStudents
        self.switch_role(obj, 'Participant_DeanOfStudents')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Health
        self.switch_role(obj, 'Participant_Health')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_StudentAccounts
        self.switch_role(obj, 'Participant_StudentAccounts')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Reference
        self.switch_role(obj, 'Participant_Reference')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_RiskMgmt
        self.switch_role(obj, 'Participant_RiskMgmt')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Participant_Applicant
        self.switch_role(obj, 'Participant_Applicant')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # change to an unauthorized role: Anonymous
        self.switch_role(obj, 'Anonymous')
        self.attempt_invalid_transition(obj, 'submit-to-chair', 'initial')

        # verify cannot view item
        # verify cannot view certain fields
        # verify cannot edit certain fields
        # repeat for all authorized roles
        #
        # send it back to the previous state
        # change to an unauthorized transitioning role
        # verify cannot execute the same transition
        # repeat for all unauthorized transitioning roles

        # and finally return it to the intended state
        self.transition_to_state(obj, 'submit-to-chair', 'pending-chair-review')

    def attempt_invalid_transition(self, obj, transition, state):
        error_str = ''
        try:
            api.content.transition(obj=obj, transition=transition)
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)
        self.assertEqual(api.content.get_state(obj=obj), state)

    def switch_role(self, obj, role):
        setRoles(self.portal, TEST_USER_ID, [role])
        self.assertTrue(role in getSecurityManager().getUser().getRolesInContext(obj))

    def transition_to_state(self, obj, transition, state):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(obj))
        api.content.transition(obj=obj, transition=transition)
        self.assertEqual(api.content.get_state(obj=obj), state)

    def test_can_transition_by_manager_cancel_from_initial(self):
        """from initial"""
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_withdraw_application_from_initial(self):
        """from initial"""
        obj = self.program
        api.content.transition(obj=obj, transition='withdraw-application')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'withdrawn')

    def test_can_transition_by_manager_submit_sponsored_program(self):
        """from initial"""
        obj = self.program
        api.content.transition(obj=obj, transition='submit-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    def test_can_transition_by_manager_submit_non_sponsored_program(self):
        """from initial"""
        obj = self.program
        api.content.transition(obj=obj, transition='submit-non-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'application-intake-in-progress')

    def test_can_transition_by_manager_submit_to_dean(self):
        """from pending-chair-review"""
        self.test_can_transition_by_manager_submit_to_chair()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-to-dean')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-dean-unit-director-review')

    def test_can_transition_by_manager_decline_from_pending_chair_review(self):
        """from pending-chair-review"""
        self.test_can_transition_by_manager_submit_to_chair()
        obj = self.program
        api.content.transition(obj=obj, transition='decline')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'declined')

    def test_can_transition_by_manager_withdraw_application_from_pending_chair_review(self):
        """from pending-chair-review"""
        self.test_can_transition_by_manager_submit_to_chair()
        obj = self.program
        api.content.transition(obj=obj, transition='withdraw-application')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'withdrawn')

    def test_can_transition_by_manager_return_to_initial_from_pending_chair_review(self):
        """from pending-chair-review"""
        self.test_can_transition_by_manager_submit_to_chair()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_submit_to_oie(self):
        """from pending-dean-unit-director-review"""
        self.test_can_transition_by_manager_submit_to_dean()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-to-oie')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-oie-review')

    def test_can_transition_by_manager_decline_from_pending_dean_unit_director_review(self):
        """from pending-dean-unit-director-review"""
        self.test_can_transition_by_manager_submit_to_dean()
        obj = self.program
        api.content.transition(obj=obj, transition='decline')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'declined')

    def test_can_transition_by_manager_withdraw_application_from_pending_dean_unit_director_review(self):
        """from pending-dean-unit-director-review"""
        self.test_can_transition_by_manager_submit_to_dean()
        obj = self.program
        api.content.transition(obj=obj, transition='withdraw-application')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'withdrawn')

    def test_can_transition_by_manager_return_to_initial_from_pending_dean_unit_director_review(self):
        """from pending-dean-unit-director-review"""
        self.test_can_transition_by_manager_submit_to_dean()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_withdraw_application_from_pending_oie_review(self):
        """from pending-oie-review"""
        self.test_can_transition_by_manager_submit_to_oie()
        obj = self.program
        api.content.transition(obj=obj, transition='withdraw-application')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'withdrawn')

    def test_can_transition_by_manager_submit_to_provost(self):
        """from pending-oie-review"""
        self.test_can_transition_by_manager_submit_to_oie()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-to-provost')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-provost-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_oie_review(self):
        """from pending-oie-review"""
        self.test_can_transition_by_manager_submit_to_oie()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_approve_provosts_office(self):
        """from pending-provost-review"""
        self.test_can_transition_by_manager_submit_to_provost()
        obj = self.program
        api.content.transition(obj=obj, transition='approve-provosts-office')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-discussions-with-program-manager')

    def test_can_transition_by_manager_return_to_oie_review(self):
        """from pending-provost-review"""
        self.test_can_transition_by_manager_submit_to_provost()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-oie-review')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-oie-review')

    def test_can_transition_by_manager_suspend_from_pending_provost_review(self):
        """from pending-provost-review"""
        self.test_can_transition_by_manager_submit_to_provost()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_decline_from_pending_provost_review(self):
        """from pending-provost-review"""
        self.test_can_transition_by_manager_submit_to_provost()
        obj = self.program
        api.content.transition(obj=obj, transition='decline')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'declined')

    def test_can_transition_by_manager_withdraw_application_from_pending_provost_review(self):
        """from pending-provost-review"""
        self.test_can_transition_by_manager_submit_to_provost()
        obj = self.program
        api.content.transition(obj=obj, transition='withdraw-application')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'withdrawn')

    def test_can_transition_by_manager_develop_rfp(self):
        """from pending-discussions-with-program-manager"""
        self.test_can_transition_by_manager_approve_provosts_office()
        obj = self.program
        api.content.transition(obj=obj, transition='develop-rfp')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'request-for-proposals-under-development')

    def test_can_transition_by_manager_return_to_initial_from_pending_discussions_with_program_manager(self):
        """from pending-discussions-with-program-manager"""
        self.test_can_transition_by_manager_approve_provosts_office()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_cancel_from_pending_discussions_with_program_manager(self):
        """from pending-discussions-with-program-manager"""
        self.test_can_transition_by_manager_approve_provosts_office()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_discussions_with_program_manager(self):
        """from pending-discussions-with-program-manager"""
        self.test_can_transition_by_manager_approve_provosts_office()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_pending_provider_proposal(self):
        """from pending-discussions-with-program-manager"""
        self.test_can_transition_by_manager_approve_provosts_office()
        obj = self.program
        api.content.transition(obj=obj, transition='pending-provider-proposal')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    def test_can_transition_by_manager_submit_rfp_for_liaison_review(self):
        """from request-for-proposals-under-development"""
        self.test_can_transition_by_manager_develop_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-rfp-for-liaison-review')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'request-for-proposals-under-liaison-review')

    def test_can_transition_by_manager_return_to_initial_from_request_for_proposals_under_development(self):
        """from request-for-proposals-under-development"""
        self.test_can_transition_by_manager_develop_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_development(self):
        """from request-for-proposals-under-development"""
        self.test_can_transition_by_manager_develop_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_development(self):
        """from request-for-proposals-under-development"""
        self.test_can_transition_by_manager_develop_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_approve_rfp(self):
        """from request-for-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='approve-rfp')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-provider-responses')

    def test_can_transition_by_manager_return_rfp_to_program_manager(self):
        """from request-for-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='return-rfp-to-program-manager')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'request-for-proposals-under-development')

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_liaison_review(self):
        """from request-for-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_liaison_review(self):
        """from request-for-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_review_provider_proposals(self):
        """from pending-provider-responses"""
        self.test_can_transition_by_manager_approve_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='review-provider-proposals')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_cancel_from_pending_provider_responses(self):
        """from pending-provider-responses"""
        self.test_can_transition_by_manager_approve_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_provider_responses(self):
        """from pending-provider-responses"""
        self.test_can_transition_by_manager_approve_rfp()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_initial_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review"""
        self.test_can_transition_by_manager_review_provider_proposals()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_submit_proposal_to_liaison(self):
        """from provider-proposals-under-oie-review"""
        self.test_can_transition_by_manager_review_provider_proposals()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-proposal-to-liaison')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'provider-proposals-under-liaison-review')

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review"""
        self.test_can_transition_by_manager_review_provider_proposals()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_oie_review(self):
        """from provider-proposals-under-oie-review"""
        self.test_can_transition_by_manager_review_provider_proposals()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_oie(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-oie')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_liaison_review(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_liaison_review(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_approve_proposal(self):
        """from provider-proposals-under-liaison-review"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison()
        obj = self.program
        api.content.transition(obj=obj, transition='approve-proposal')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    def test_can_transition_by_manager_submit_fee_for_liaison_review(self):
        """from pending-program-fee-determination-by-oie"""
        self.test_can_transition_by_manager_approve_proposal()
        obj = self.program
        api.content.transition(obj=obj, transition='submit-fee-for-liaison-review')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-fee-under-liaison-review')

    def test_can_transition_by_manager_return_to_initial_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie"""
        self.test_can_transition_by_manager_approve_proposal()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-initial')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial')

    def test_can_transition_by_manager_cancel_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie"""
        self.test_can_transition_by_manager_approve_proposal()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_fee_determination_by_oie(self):
        """from pending-program-fee-determination-by-oie"""
        self.test_can_transition_by_manager_approve_proposal()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_return_to_oie(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='return-to-oie')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_suspend_from_program_fee_under_liaison_review(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_program_fee_under_liaison_review(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_approve_fee(self):
        """from program-fee-under-liaison-review"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review()
        obj = self.program
        api.content.transition(obj=obj, transition='approve-fee')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-fee-pending-publication')

    def test_can_transition_by_manager_publish_fee(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='publish-fee')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'application-intake-in-progress')

    def test_can_transition_by_manager_cancel_from_program_fee_pending_publication(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_program_fee_pending_publication(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_announce_programmatic_for_fee_change(self):
        """from program-fee-pending-publication"""
        self.test_can_transition_by_manager_approve_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='announce-programmatic-for-fee-change')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'applicants-considering-change')

    def test_can_transition_by_manager_confirm_to_run_from_applicants_considering_change(self):
        """from applicants-considering-change"""
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change()
        obj = self.program
        api.content.transition(obj=obj, transition='confirm-to-run')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial-payment-billing-in-progress')

    def test_can_transition_by_manager_cancel_after_change(self):
        """from applicants-considering-change"""
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel-after-change')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_confirm_to_run(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='confirm-to-run')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'initial-payment-billing-in-progress')

    def test_can_transition_by_manager_suspend_from_application_intake_in_progress(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_cancel_from_application_intake_in_progress(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_send_for_programmatic_change(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='send-for-programmatic-change')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'provider-proposals-under-oie-review')

    def test_can_transition_by_manager_send_for_fee_change(self):
        """from application-intake-in-progress"""
        self.test_can_transition_by_manager_publish_fee()
        obj = self.program
        api.content.transition(obj=obj, transition='send-for-fee-change')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-fee-determination-by-oie')

    # TODO provider-proposals-under-oie-review

    def test_can_transition_by_manager_send_bills_for_initial_payment(self):
        """from initial-payment-billing-in-progress"""
        self.test_can_transition_by_manager_confirm_to_run()
        obj = self.program
        api.content.transition(obj=obj, transition='send-bills-for-initial-payment')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-final-program-fee')

    def test_can_transition_by_manager_cancel_from_initial_payment_billing_in_progress(self):
        """from initial-payment-billing-in-progress"""
        self.test_can_transition_by_manager_confirm_to_run()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_initial_payment_billing_in_progress(self):
        """from initial-payment-billing-in-progress"""
        self.test_can_transition_by_manager_confirm_to_run()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_publish_final_fee(self):
        """from pending-final-program-fee"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        obj = self.program
        api.content.transition(obj=obj, transition='publish-final-fee')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'final-payment-billing-in-progress')

    def test_can_transition_by_manager_cancel_from_pending_final_program_fee(self):
        """from pending-final-program-fee"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_final_program_fee(self):
        """from pending-final-program-fee"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_bill_for_final_payment(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='bill-for-final-payment')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-leader-orientation')

    def test_can_transition_by_manager_cancel_from_final_payment_billing_in_progress(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_final_payment_billing_in_progress(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_bill_for_final_payment_programs_with_no_leader(self):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee()
        obj = self.program
        # TODO only for programs with no leader
        api.content.transition(obj=obj, transition='bill-for-final-payment-programs-with-no-leader')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_confirm_orientation_completed(self):
        """from pending-program-leader-orientation"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='confirm-orientation-completed')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-travel-advance')

    def test_can_transition_by_manager_cancel_from_pending_program_leader_orientation(self):
        """from pending-program-leader-orientation"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_leader_orientation(self):
        """from pending-program-leader-orientation"""
        self.test_can_transition_by_manager_bill_for_final_payment()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_travel_advance_ready(self):
        """from pending-travel-advance"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='travel-advance-ready')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'reviewing-final-program-details')

    def test_can_transition_by_manager_cancel_from_pending_travel_advance(self):
        """from pending-travel-advance"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_travel_advance(self):
        """from pending-travel-advance"""
        self.test_can_transition_by_manager_confirm_orientation_completed()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_schedule_operational_briefing(self):
        """from reviewing-final-program-details"""
        self.test_can_transition_by_manager_travel_advance_ready()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='schedule-operational-briefing')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-leader-operational-briefing')

    def test_can_transition_by_manager_cancel_from_reviewing_final_program_details(self):
        """from reviewing-final-program-details"""
        self.test_can_transition_by_manager_travel_advance_ready()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_reviewing_final_program_details(self):
        """from reviewing-final-program-details"""
        self.test_can_transition_by_manager_travel_advance_ready()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_confirm_briefing_completed(self):
        """from pending-program-leader-operational-briefing"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        obj = self.program
        # TODO only for programs with leader
        api.content.transition(obj=obj, transition='confirm-briefing-completed')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_cancel_from_pending_program_leader_operational_briefing(self):
        """from pending-program-leader-operational-briefing"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_leader_operational_briefing(self):
        """from pending-program-leader-operational-briefing"""
        self.test_can_transition_by_manager_schedule_operational_briefing()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_depart(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        obj = self.program
        # TODO only for programs with individuals
        api.content.transition(obj=obj, transition='depart')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_cancel_from_pending_program_departure(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        obj = self.program
        api.content.transition(obj=obj, transition='cancel')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'cancelled')

    def test_can_transition_by_manager_suspend_from_pending_program_departure(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_depart_sponsored_program(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='depart-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_depart_non_sponsored_program(self):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='depart-non-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-arrival-abroad')

    def test_can_transition_by_manager_suspend_from_pending_arrival_abroad(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        obj = self.program
        api.content.transition(obj=obj, transition='suspend')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'suspended')

    def test_can_transition_by_manager_confirm_safe_arrival(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        obj = self.program
        # TODO only for programs with individuals
        api.content.transition(obj=obj, transition='confirm-safe-arrival')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_confirm_travel_delay(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        obj = self.program
        # TODO only for programs with individuals
        api.content.transition(obj=obj, transition='confirm-travel-delay')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-program-departure')

    def test_can_transition_by_manager_arrive_sponsored_program(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='arrive-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_arrive_non_sponsored_program(self):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='arrive-non-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-in-progress')

    def test_can_transition_by_manager_confirm_return(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        obj = self.program
        api.content.transition(obj=obj, transition='confirm-return')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'travel-expense-report-student-evaluations-due-to')

    def test_can_transition_by_manager_returned_sponsored_program(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='returned-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-completed')

    def test_can_transition_by_manager_returned_non_sponsored_program(self):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival()
        obj = self.program
        # TODO only for programs with groups
        api.content.transition(obj=obj, transition='returned-non-sponsored-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-completed')

    def test_can_transition_by_manager_confirm_ter_received(self):
        """from travel-expense-report-student-evaluations-due-to"""
        self.test_can_transition_by_manager_confirm_return()
        obj = self.program
        api.content.transition(obj=obj, transition='confirm-ter-received')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'final-program-accounting-in-progress')

    def test_can_transition_by_manager_process_refunds(self):
        """from final-program-accounting-in-progress"""
        self.test_can_transition_by_manager_confirm_ter_received()
        obj = self.program
        api.content.transition(obj=obj, transition='process-refunds')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'process-refunds-budget-transfers')

    def test_can_transition_by_manager_archive_program(self):
        """from process-refunds-budget-transfers"""
        self.test_can_transition_by_manager_process_refunds()
        obj = self.program
        api.content.transition(obj=obj, transition='archive-program')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'program-completed')
