# -*- coding: utf-8 -*-
from . import OIEStudyAbroadContentBaseTest
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.dexterity.interfaces import IDexterityFTI
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgram  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility


class OIEStudyAbroadProgramIntegrationTest(OIEStudyAbroadContentBaseTest):

    ROLES_BY_TRANSITION = {
        'cancel': ['Mgmt_Admin', 'Manager'],
        'suspend': ['Mgmt_Admin', 'Mgmt_Provost', 'Manager'],
    }

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        # add calendar year
        self.calendar_year = api.content.create(
            container=self.portal,
            type='OIECalendarYear',
            id='2018',
        )
        self.calendar_year_uid = api.content.get_uuid(obj=self.calendar_year)

        # add a sample program
        self.test_obj = api.content.create(
            container=self.portal,
            type='OIEStudyAbroadProgram',
            id='sample-program',
            calendar_year=self.calendar_year_uid,
            term='1 Fall Interim',
            college_or_unit='B College of Business',
            countries=['Afghanistan'],
        )

    def test_is_addon_installed(self):
        self.assertTrue(
            self.installer.isProductInstalled('uwosh.oie.studyabroadstudent'),
        )

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
        self.assertRaises(Unauthorized,
                          portal.restrictedTraverse,
                          'sample-program/@@edit')

    def test_correct_default_workflow(self):
        workflowTool = api.portal.get_tool('portal_workflow')
        chains = dict(workflowTool.listChainOverrides())
        defaultChain = workflowTool.getDefaultChain()
        programChain = chains.get('OIEStudyAbroadProgram', defaultChain)
        self.assertEqual(programChain, ('programmanagement',))

    # workflow transitions from initial state

    def test_nonexistent_transition_by_manager(self):
        error_str = ''
        try:
            api.content.transition(obj=self.test_obj,
                                   transition='this-transition-does-not-exist')
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)

    def test_cannot_transition_as_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        logout()
        self.assertRaises(InvalidParameterError,
                          api.content.transition,
                          obj=self.test_obj,
                          transition='submit-to-chair')

    # all workflow transitions by manager

    # 1. Manager: Check that manager can execute this transition
    # 2. Authorized transitioners: Check each other role that can execute this
    #    transition
    # 3. Unauthorized transitions: Check that every other role CANNOT execute
    #    this transition
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
        # by default, roles will be ['Manager', 'Authenticated'] so
        # verify that we have Manager role
        self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(self.portal))  # noqa
        initial_state = 'initial'
        transition = 'submit-to-chair'
        end_state = 'pending-chair-review'
        authorized_roles = ['Manager', 'Mgmt_Admin', 'Mgmt_Liaison']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_initial(self, fast=None):
        """from initial Mgmt_Admin; Mgmt_Director; Manager"""
        initial_state = 'initial'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_withdraw_application_from_initial(
            self,
            fast=None,
    ):
        """from initial, Mgmt_Admin; Mgmt_Liaison; Manager"""
        initial_state = 'initial'
        transition = 'withdraw-application'
        end_state = 'withdrawn'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_sponsored_program(
            self,
            fast=None,
    ):
        """from initial, Mgmt_Coordinator; Mgmt_Admin; Manager"""
        initial_state = 'initial'
        transition = 'submit-sponsored-program'
        end_state = 'pending-program-fee-determination-by-oie'
        authorized_roles = ['Manager', 'Mgmt_Admin', 'Mgmt_Coordinator']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_non_sponsored_program(
            self,
            fast=None,
    ):
        """from initial, Mgmt_Coordinator; Mgmt_Admin; Manager"""
        initial_state = 'initial'
        transition = 'submit-non-sponsored-program'
        end_state = 'application-intake-in-progress'
        authorized_roles = ['Manager', 'Mgmt_Admin', 'Mgmt_Coordinator']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_to_dean(self, fast=None):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Chair; or
           Manager"""
        # get it to the correct state
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        initial_state = 'pending-chair-review'
        transition = 'submit-to-dean'
        end_state = 'pending-dean-unit-director-review'
        authorized_roles = ['Manager', 'Mgmt_Chair', 'Mgmt_Admin']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_decline_from_pending_chair_review(
            self,
            fast=None,
    ):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Dean;
        Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        initial_state = 'pending-chair-review'
        transition = 'decline'
        end_state = 'declined'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_withdraw_application_from_pending_chair_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Liaison;
        or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        initial_state = 'pending-chair-review'
        transition = 'withdraw-application'
        end_state = 'withdrawn'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_pending_chair_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-chair-review Requires role: Mgmt_Admin; Mgmt_Dean;
        Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_chair(fast=True)
        initial_state = 'pending-chair-review'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_to_oie(self, fast=None):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin;
        Mgmt_Dean; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        initial_state = 'pending-dean-unit-director-review'
        transition = 'submit-to-oie'
        end_state = 'pending-oie-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_decline_from_pending_dean_unit_director_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin;
        Mgmt_Dean; Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        initial_state = 'pending-dean-unit-director-review'
        transition = 'decline'
        end_state = 'declined'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_withdraw_application_from_pending_dean_unit_director_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin;
        Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        initial_state = 'pending-dean-unit-director-review'
        transition = 'withdraw-application'
        end_state = 'withdrawn'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_pending_dean_unit_director_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-dean-unit-director-review Requires role: Mgmt_Admin;
        Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_dean(fast=True)
        initial_state = 'pending-dean-unit-director-review'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_withdraw_application_from_pending_oie_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Liaison; or
        Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        initial_state = 'pending-oie-review'
        transition = 'withdraw-application'
        end_state = 'withdrawn'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_to_provost(self, fast=None):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Director;
        or Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        initial_state = 'pending-oie-review'
        transition = 'submit-to-provost'
        end_state = 'pending-provost-review'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_pending_oie_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-oie-review Requires role: Mgmt_Admin; Mgmt_Dean;
        Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_submit_to_oie(fast=True)
        initial_state = 'pending-oie-review'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_approve_provosts_office(
            self,
            fast=None,
    ):
        """from pending-provost-review Requires role: Mgmt_Admin;
        Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        initial_state = 'pending-provost-review'
        transition = 'approve-provosts-office'
        end_state = 'pending-discussions-with-program-manager'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Provost', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_oie_review(self, fast=None):
        """from pending-provost-review Requires role: Mgmt_Admin;
        Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        initial_state = 'pending-provost-review'
        transition = 'return-to-oie-review'
        end_state = 'pending-oie-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Provost', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_provost_review(
            self,
            fast=None,
    ):
        """from pending-provost-review Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        initial_state = 'pending-provost-review'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_decline_from_pending_provost_review(
            self,
            fast=None,
    ):
        """from pending-provost-review Requires role: Mgmt_Admin; Mgmt_Dean;
        Mgmt_Chair; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        initial_state = 'pending-provost-review'
        transition = 'decline'
        end_state = 'declined'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Provost', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_withdraw_application_from_pending_provost_review(  # noqa
            self,
            fast=None,
    ):
        """from pending-provost-review Requires role: Mgmt_Admin;
        Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_to_provost(fast=True)
        initial_state = 'pending-provost-review'
        transition = 'withdraw-application'
        end_state = 'withdrawn'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_develop_rfp(self, fast=None):
        """from pending-discussions-with-program-manager Requires role:
        Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        initial_state = 'pending-discussions-with-program-manager'
        transition = 'develop-rfp'
        end_state = 'request-for-proposals-under-development'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_pending_discussions_with_program_manager(  # noqa
            self,
            fast=None,
    ):
        """from pending-discussions-with-program-manager Requires role:
        Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or
        Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        initial_state = 'pending-discussions-with-program-manager'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_discussions_with_program_manager(  # noqa
            self,
            fast=None,
    ):
        """from pending-discussions-with-program-manager Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        initial_state = 'pending-discussions-with-program-manager'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_discussions_with_program_manager(  # noqa
            self,
            fast=None,
    ):
        """from pending-discussions-with-program-manager Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        initial_state = 'pending-discussions-with-program-manager'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_pending_provider_proposal(
            self,
            fast=None,
    ):
        """from pending-discussions-with-program-manager Requires role:
        Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_provosts_office(fast=True)
        initial_state = 'pending-discussions-with-program-manager'
        transition = 'pending-provider-proposal'
        end_state = 'pending-program-fee-determination-by-oie'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_rfp_for_liaison_review(
            self,
            fast=None,
    ):
        """from request-for-proposals-under-development Requires role:
        Mgmt_Admin; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        initial_state = 'request-for-proposals-under-development'
        transition = 'submit-rfp-for-liaison-review'
        end_state = 'request-for-proposals-under-liaison-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_request_for_proposals_under_development(  # noqa
            self,
            fast=None,
    ):
        """from request-for-proposals-under-development Requires role:
        Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or
        Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        initial_state = 'request-for-proposals-under-development'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_development(  # noqa
            self,
            fast=None,
    ):
        """from request-for-proposals-under-development Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        initial_state = 'request-for-proposals-under-development'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_development(  # noqa
            self,
            fast=None,
    ):
        """from request-for-proposals-under-development Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_develop_rfp(fast=True)
        initial_state = 'request-for-proposals-under-development'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_approve_rfp(
            self,
            fast=None,
    ):
        """from request-for-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(
            fast=True,
        )
        initial_state = 'request-for-proposals-under-liaison-review'
        transition = 'approve-rfp'
        end_state = 'pending-provider-responses'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_rfp_to_program_manager(
            self,
            fast=None,
    ):
        """from request-for-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(
            fast=True,
        )
        initial_state = 'request-for-proposals-under-liaison-review'
        transition = 'return-rfp-to-program-manager'
        end_state = 'request-for-proposals-under-development'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_request_for_proposals_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from request-for-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(
            fast=True,
        )
        initial_state = 'request-for-proposals-under-liaison-review'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_request_for_proposals_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from request-for-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_rfp_for_liaison_review(
            fast=True,
        )
        initial_state = 'request-for-proposals-under-liaison-review'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_review_provider_proposals(
            self,
            fast=None,
    ):
        """from pending-provider-responses Requires role: Mgmt_Admin;
        Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_approve_rfp(
            fast=True,
        )
        initial_state = 'pending-provider-responses'
        transition = 'review-provider-proposals'
        end_state = 'provider-proposals-under-oie-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_provider_responses(
            self,
            fast=None,
    ):
        """from pending-provider-responses Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_rfp(
            fast=True,
        )
        initial_state = 'pending-provider-responses'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_provider_responses(
            self,
            fast=None,
    ):
        """from pending-provider-responses Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_rfp(
            fast=True,
        )
        initial_state = 'pending-provider-responses'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_provider_proposals_under_oie_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin;
        Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals(
            fast=True,
        )
        initial_state = 'provider-proposals-under-oie-review'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_proposal_to_liaison(
            self,
            fast=None,
    ):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin;
        Mgmt_Manager; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals(
            fast=True,
        )
        initial_state = 'provider-proposals-under-oie-review'
        transition = 'submit-proposal-to-liaison'
        end_state = 'provider-proposals-under-liaison-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_oie_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals(
            fast=True,
        )
        initial_state = 'provider-proposals-under-oie-review'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_oie_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-oie-review Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_review_provider_proposals(
            fast=True,
        )
        initial_state = 'provider-proposals-under-oie-review'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_oie_from_provider_proposals_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison(
            fast=True,
        )
        initial_state = 'provider-proposals-under-liaison-review'
        transition = 'return-to-oie'
        end_state = 'provider-proposals-under-oie-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_provider_proposals_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison(
            fast=True,
        )
        initial_state = 'provider-proposals-under-liaison-review'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_provider_proposals_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from provider-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison(
            fast=True,
        )
        initial_state = 'provider-proposals-under-liaison-review'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_approve_proposal(
            self,
            fast=None,
    ):
        """from provider-proposals-under-liaison-review Requires role:
        Mgmt_Admin; Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_proposal_to_liaison(
            fast=True,
        )
        initial_state = 'provider-proposals-under-liaison-review'
        transition = 'approve-proposal'
        end_state = 'pending-program-fee-determination-by-oie'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_submit_fee_for_liaison_review(
            self,
            fast=None,
    ):
        """from pending-program-fee-determination-by-oie Requires role:
        Mgmt_Admin; Mgmt_Financial; or Manager"""
        self.test_can_transition_by_manager_approve_proposal(
            fast=True,
        )
        initial_state = 'pending-program-fee-determination-by-oie'
        transition = 'submit-fee-for-liaison-review'
        end_state = 'program-fee-under-liaison-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_initial_from_pending_program_fee_determination_by_oie(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-fee-determination-by-oie Requires role:
        Mgmt_Admin; Mgmt_Dean; Mgmt_Director; Mgmt_Chair; Mgmt_Manager; or
Manager"""
        self.test_can_transition_by_manager_approve_proposal(
            fast=True,
        )
        initial_state = 'pending-program-fee-determination-by-oie'
        transition = 'return-to-initial'
        end_state = 'initial'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Dean', 'Mgmt_Chair', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_program_fee_determination_by_oie(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-fee-determination-by-oie Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_proposal(
            fast=True,
        )
        initial_state = 'pending-program-fee-determination-by-oie'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_program_fee_determination_by_oie(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-fee-determination-by-oie Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_proposal(
            fast=True,
        )
        initial_state = 'pending-program-fee-determination-by-oie'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_return_to_oie_from_program_fee_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin;
        Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review(
            fast=True,
        )
        initial_state = 'program-fee-under-liaison-review'
        transition = 'return-to-oie'
        end_state = 'provider-proposals-under-oie-review'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_program_fee_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review(
            fast=True,
        )
        initial_state = 'program-fee-under-liaison-review'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_program_fee_under_liaison_review(  # noqa
            self,
            fast=None,
    ):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review(
            fast=True,
        )
        initial_state = 'program-fee-under-liaison-review'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_approve_fee(
            self,
            fast=None,
    ):
        """from program-fee-under-liaison-review Requires role: Mgmt_Admin;
        Mgmt_Liaison; or Manager"""
        self.test_can_transition_by_manager_submit_fee_for_liaison_review(
            fast=True,
        )
        initial_state = 'program-fee-under-liaison-review'
        transition = 'approve-fee'
        end_state = 'program-fee-pending-publication'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Liaison', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_publish_fee(
            self,
            fast=None,
    ):
        """from program-fee-pending-publication Requires role: Mgmt_Admin;
        Mgmt_Financial; or Manager"""
        self.test_can_transition_by_manager_approve_fee(
            fast=True,
        )
        initial_state = 'program-fee-pending-publication'
        transition = 'publish-fee'
        end_state = 'application-intake-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_program_fee_pending_publication(  # noqa
            self,
            fast=None,
    ):
        """from program-fee-pending-publication Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_approve_fee(
            fast=True,
        )
        initial_state = 'program-fee-pending-publication'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_program_fee_pending_publication(  # noqa
            self,
            fast=None,
    ):
        """from program-fee-pending-publication Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_approve_fee(
            fast=True,
        )
        initial_state = 'program-fee-pending-publication'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_announce_programmatic_for_fee_change(
            self,
            fast=None,
    ):
        """from program-fee-pending-publication Requires role:
        Mgmt_Coordinator; Mgmt_Admin; or Manager"""
        self.test_can_transition_by_manager_approve_fee(
            fast=True,
        )
        initial_state = 'program-fee-pending-publication'
        transition = 'announce-programmatic-or-fee-change'
        end_state = 'applicants-considering-change'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_to_run_from_applicants_considering_change(  # noqa
            self,
            fast=None,
    ):
        """from applicants-considering-change Requires role: Mgmt_Coordinator;
        Mgmt_Admin; or Manager"""
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change(  # noqa
            fast=True,
        )
        initial_state = 'applicants-considering-change'
        transition = 'confirm-to-run'
        end_state = 'initial-payment-billing-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_after_change(
            self,
            fast=None,
    ):
        """from applicants-considering-change Requires role: Mgmt_Coordinator;
        Mgmt_Admin; or Manager
        """
        self.test_can_transition_by_manager_announce_programmatic_for_fee_change(  # noqa
            fast=True,
        )
        initial_state = 'applicants-considering-change'
        transition = 'cancel-after-change'
        end_state = 'cancelled'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_to_run(
            self,
            fast=None,
    ):
        """from application-intake-in-progress Requires role:
        Mgmt_Coordinator; Mgmt_Admin; or Manager"""
        self.test_can_transition_by_manager_publish_fee(
            fast=True,
        )
        initial_state = 'application-intake-in-progress'
        transition = 'confirm-to-run'
        end_state = 'initial-payment-billing-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_application_intake_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from application-intake-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_publish_fee(
            fast=True,
        )
        initial_state = 'application-intake-in-progress'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_application_intake_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from application-intake-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_publish_fee(
            fast=True,
        )
        initial_state = 'application-intake-in-progress'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_send_for_programmatic_change(
            self,
            fast=None,
    ):
        """from application-intake-in-progress Requires role:
        Mgmt_Coordinator; Mgmt_Admin; or Manager"""
        self.test_can_transition_by_manager_publish_fee(
            fast=True,
        )
        initial_state = 'application-intake-in-progress'
        transition = 'send-for-programmatic-change'
        end_state = 'provider-proposals-under-oie-review'
        authorized_roles = ['Mgmt_Coordinator', 'Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_send_for_fee_change(
            self,
            fast=None,
    ):
        """from application-intake-in-progress Requires role:
        Mgmt_Coordinator; Mgmt_Admin; or Manager"""
        self.test_can_transition_by_manager_publish_fee(
            fast=True,
        )
        initial_state = 'application-intake-in-progress'
        transition = 'send-for-fee-change'
        end_state = 'pending-program-fee-determination-by-oie'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_send_bills_for_initial_payment(
            self,
            fast=None,
    ):
        """from initial-payment-billing-in-progress Requires role: Mgmt_Admin;
        Mgmt_Financial; or Manager"""
        self.test_can_transition_by_manager_confirm_to_run(
            fast=True,
        )
        initial_state = 'initial-payment-billing-in-progress'
        transition = 'send-bills-for-initial-payment'
        end_state = 'pending-final-program-fee'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_initial_payment_billing_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from initial-payment-billing-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_to_run(
            fast=True,
        )
        initial_state = 'initial-payment-billing-in-progress'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_initial_payment_billing_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from initial-payment-billing-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_to_run(
            fast=True,
        )
        initial_state = 'initial-payment-billing-in-progress'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_publish_final_fee(
            self,
            fast=None,
    ):
        """from pending-final-program-fee"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment(
            fast=True,
        )
        initial_state = 'pending-final-program-fee'
        transition = 'publish-final-fee'
        end_state = 'final-payment-billing-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_final_program_fee(
            self,
            fast=None,
    ):
        """from pending-final-program-fee Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment(
            fast=True,
        )
        initial_state = 'pending-final-program-fee'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_final_program_fee(
            self,
            fast=None,
    ):
        """from pending-final-program-fee Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_send_bills_for_initial_payment(
            fast=True,
        )
        initial_state = 'pending-final-program-fee'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_bill_for_final_payment(
            self,
            fast=None,
    ):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'final-payment-billing-in-progress'
        transition = 'bill-for-final-payment'
        end_state = 'pending-program-leader-orientation'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_final_payment_billing_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from final-payment-billing-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_publish_final_fee(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'final-payment-billing-in-progress'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_final_payment_billing_in_progress(  # noqa
            self,
            fast=None,
    ):
        """from final-payment-billing-in-progress Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_publish_final_fee(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'final-payment-billing-in-progress'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_bill_for_final_payment_programs_with_no_leader(  # noqa
            self,
            fast=None,
    ):
        """from final-payment-billing-in-progress"""
        self.test_can_transition_by_manager_publish_final_fee(
            fast=True,
        )
        # TODO only for programs with no leader  # noqa
        initial_state = 'final-payment-billing-in-progress'
        transition = 'bill-for-final-payment-programs-with-no-leader'
        end_state = 'pending-program-departure'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_orientation_completed(
            self,
            fast=None,
    ):
        """from pending-program-leader-orientation"""
        self.test_can_transition_by_manager_bill_for_final_payment(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-program-leader-orientation'
        transition = 'confirm-orientation-completed'
        end_state = 'pending-travel-advance'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_program_leader_orientation(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-leader-orientation Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_bill_for_final_payment(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-program-leader-orientation'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_program_leader_orientation(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-leader-orientation Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_bill_for_final_payment(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-program-leader-orientation'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_travel_advance_ready(
            self,
            fast=None,
    ):
        """from pending-travel-advance"""
        self.test_can_transition_by_manager_confirm_orientation_completed(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-travel-advance'
        transition = 'travel-advance-ready'
        end_state = 'reviewing-final-program-details'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_travel_advance(
            self,
            fast=None,
    ):
        """from pending-travel-advance Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_orientation_completed(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-travel-advance'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_travel_advance(
            self,
            fast=None,
    ):
        """from pending-travel-advance Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_orientation_completed(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-travel-advance'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_schedule_operational_briefing(
            self,
            fast=None,
    ):
        """from reviewing-final-program-details"""
        self.test_can_transition_by_manager_travel_advance_ready(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'reviewing-final-program-details'
        transition = 'schedule-operational-briefing'
        end_state = 'pending-program-leader-operational-briefing'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_reviewing_final_program_details(  # noqa
            self,
            fast=None,
    ):
        """from reviewing-final-program-details Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_travel_advance_ready(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'reviewing-final-program-details'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_reviewing_final_program_details(  # noqa
            self,
            fast=None,
    ):
        """from reviewing-final-program-details Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_travel_advance_ready(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'reviewing-final-program-details'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_briefing_completed(
            self,
            fast=None,
    ):
        """from pending-program-leader-operational-briefing"""
        self.test_can_transition_by_manager_schedule_operational_briefing(
            fast=True,
        )
        # TODO only for programs with leader  # noqa
        initial_state = 'pending-program-leader-operational-briefing'
        transition = 'confirm-briefing-completed'
        end_state = 'pending-program-departure'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Manager', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_program_leader_operational_briefing(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-leader-operational-briefing Requires role:
        Mgmt_Admin; Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_schedule_operational_briefing(
            fast=True,
        )
        initial_state = 'pending-program-leader-operational-briefing'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_program_leader_operational_briefing(  # noqa
            self,
            fast=None,
    ):
        """from pending-program-leader-operational-briefing Requires role:
        Mgmt_Admin; Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_schedule_operational_briefing(
            fast=True,
        )
        initial_state = 'pending-program-leader-operational-briefing'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_depart(
            self,
            fast=None,
    ):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed(
            fast=True,
        )
        # TODO only for programs with individuals  # noqa
        initial_state = 'pending-program-departure'
        transition = 'depart'
        end_state = 'pending-arrival-abroad'
        authorized_roles = ['Mgmt_Coordinator', 'Mgmt_Admin', 'Mgmt_Manager', 'Mgmt_ProgramLeader', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_cancel_from_pending_program_departure(
            self,
            fast=None,
    ):
        """from pending-program-departure Requires role: Mgmt_Admin;
        Mgmt_Director; or Manager"""
        self.test_can_transition_by_manager_confirm_briefing_completed(
            fast=True,
        )
        initial_state = 'pending-program-departure'
        transition = 'cancel'
        end_state = 'cancelled'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_program_departure(
            self,
            fast=None,
    ):
        """from pending-program-departure Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_confirm_briefing_completed(
            fast=True,
        )
        initial_state = 'pending-program-departure'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_depart_sponsored_program(
            self,
            fast=None,
    ):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'pending-program-departure'
        transition = 'depart-sponsored-program'
        end_state = 'pending-arrival-abroad'
        authorized_roles = ['Mgmt_Coordinator', 'Mgmt_Admin', 'Mgmt_Manager', 'Mgmt_ProgramLeader', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_depart_non_sponsored_program(
            self,
            fast=None,
    ):
        """from pending-program-departure"""
        self.test_can_transition_by_manager_confirm_briefing_completed(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'pending-program-departure'
        transition = 'depart-non-sponsored-program'
        end_state = 'pending-arrival-abroad'
        authorized_roles = ['Mgmt_Coordinator', 'Mgmt_Admin', 'Mgmt_Manager', 'Mgmt_ProgramLeader', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_suspend_from_pending_arrival_abroad(
            self,
            fast=None,
    ):
        """from pending-arrival-abroad Requires role: Mgmt_Admin;
        Mgmt_Director; Mgmt_Provost; or Manager"""
        self.test_can_transition_by_manager_depart_non_sponsored_program(
            fast=True,
        )
        initial_state = 'pending-arrival-abroad'
        transition = 'suspend'
        end_state = 'suspended'
        authorized_roles = self.ROLES_BY_TRANSITION[transition]
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_safe_arrival(
            self,
            fast=None,
    ):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program(
            fast=True,
        )
        # TODO only for programs with individuals  # noqa
        initial_state = 'pending-arrival-abroad'
        transition = 'confirm-safe-arrival'
        end_state = 'program-in-progress'
        authorized_roles = ['Mgmt_Coordinator', 'Mgmt_Admin', 'Mgmt_Manager', 'Mgmt_ProgramLeader', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_travel_delay(
            self,
            fast=None,
    ):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program(
            fast=True,
        )
        # TODO only for programs with individuals  # noqa
        initial_state = 'pending-arrival-abroad'
        transition = 'confirm-travel-delay'
        end_state = 'pending-program-departure'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_arrive_sponsored_program(
            self,
            fast=None,
    ):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'pending-arrival-abroad'
        transition = 'arrive-sponsored-program'
        end_state = 'program-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_arrive_non_sponsored_program(
            self,
            fast=None,
    ):
        """from pending-arrival-abroad"""
        self.test_can_transition_by_manager_depart_non_sponsored_program(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'pending-arrival-abroad'
        transition = 'arrive-non-sponsored-program'
        end_state = 'program-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_return(
            self,
            fast=None,
    ):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival(
            fast=True,
        )
        initial_state = 'program-in-progress'
        transition = 'confirm-return'
        end_state = 'travel-expense-report-student-evaluations-due-to'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Coordinator', 'Mgmt_Manager', 'Manager']  # noqa
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_returned_sponsored_program(
            self,
            fast=None,
    ):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'program-in-progress'
        transition = 'returned-sponsored-program'
        end_state = 'program-completed'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_returned_non_sponsored_program(
            self,
            fast=None,
    ):
        """from program-in-progress"""
        self.test_can_transition_by_manager_confirm_safe_arrival(
            fast=True,
        )
        # TODO only for programs with groups  # noqa
        initial_state = 'program-in-progress'
        transition = 'returned-non-sponsored-program'
        end_state = 'program-completed'
        authorized_roles = ['Mgmt_Admin', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_confirm_ter_received(
            self,
            fast=None,
    ):
        """from travel-expense-report-student-evaluations-due-to"""
        self.test_can_transition_by_manager_confirm_return(
            fast=True,
        )
        initial_state = 'travel-expense-report-student-evaluations-due-to'
        transition = 'confirm-ter-received'
        end_state = 'final-program-accounting-in-progress'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_process_refunds(
            self,
            fast=None,
    ):
        """from final-program-accounting-in-progress"""
        self.test_can_transition_by_manager_confirm_ter_received(
            fast=True,
        )
        initial_state = 'final-program-accounting-in-progress'
        transition = 'process-refunds'
        end_state = 'process-refunds-budget-transfers'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)

    def test_can_transition_by_manager_archive_program(
            self,
            fast=None,
    ):
        """from process-refunds-budget-transfers"""
        self.test_can_transition_by_manager_process_refunds(
            fast=True,
        )
        initial_state = 'process-refunds-budget-transfers'
        transition = 'archive-program'
        end_state = 'program-completed'
        authorized_roles = ['Mgmt_Admin', 'Mgmt_Financial', 'Manager']
        self._transition_and_or_roles_test(fast,
                                           initial_state,
                                           transition,
                                           end_state,
                                           authorized_roles)
