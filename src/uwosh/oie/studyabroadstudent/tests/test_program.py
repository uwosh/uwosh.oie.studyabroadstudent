# -*- coding: utf-8 -*-
from . import OIEStudyAbroadContentBaseTest, TRANSITIONS, ROLES, STATES
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
from Products.CMFCore.utils import getToolByName

import unittest


def add_dynamic_tests(cls):
    
    def create_invalid_transition_test(start_state,
                                       transition,
                                       end_state):
        def do_create_test(self):
            self.test_program = self._transition_to_state(obj=self.test_program,
                                            destination_state=start_state)
            self._attempt_invalid_transition(obj=self.test_program,
                                                transition=transition,
                                                end_state=start_state)
        return do_create_test

    def create_transition_by_role_test(start_state,
                                       role,
                                       transition,
                                       end_state,
                                       is_authorized,
                                       fast=False):
        def do_create_test(self):
            self.test_program = self._transition_to_state(obj=self.test_program,
                                          destination_state=start_state)
            if is_authorized:
                self._verify_allowed_transition_by_role(obj=self.test_program,
                                                        initial_state=start_state,
                                                        role=role,
                                                        transition=transition,
                                                        destination_state=end_state,
                                                        end_state=end_state)
            else:
                self._verify_unauthorized_transition_by_role(obj=self.test_program,
                                                initial_state=start_state,
                                                role=role,
                                                transition=transition,
                                                end_state=start_state)
        return do_create_test

    def generate_tests(cls):    
        for state_id, state_info in STATES.items():
                for transition_name, transition in TRANSITIONS.items():
                    start_state = state_id
                    end_state = transition['new_state']
                    if transition_name not in state_info['exit_transitions']:
                        test_method = create_invalid_transition_test(
                                        start_state=start_state,
                                        transition=transition_name,
                                        end_state=end_state)
                        test_name = 'test_invalid_transition_{}_from_{}_to_{}'.format(
                            transition_name,
                            start_state,
                            end_state
                        )
                        test_name = test_name.replace('-', '_')
                        test_method.__name__ = test_name
                        setattr(cls, test_method.__name__, test_method)
                    else:
                        authorized_roles = transition['guard_roles']
                        for role in ROLES:
                            is_authorized = role in authorized_roles
                            test_method = create_transition_by_role_test(
                                            start_state=start_state,
                                            role=role,
                                            transition=transition_name,
                                            end_state=end_state,
                                            is_authorized=is_authorized)
                            can_or_cannot = 'can' if role in authorized_roles else 'cannot'
                            test_name = 'test_{}_{}_activate_{}_from_state_{}'.format(role,
                                                                        can_or_cannot,
                                                                        transition['transition_id'],
                                                                        state_id)
                            test_name = test_name.replace('-', '_')
                            test_method.__name__ = test_name
                            setattr(cls, test_method.__name__, test_method)
    
    generate_tests(cls)
    return cls
    


# @add_dynamic_tests
class OIEStudyAbroadProgramIntegrationTest(OIEStudyAbroadContentBaseTest):

  
    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        self.calendar_year, self.calendar_year_uid = self.get_calendar_year_and_uid()
        self.test_program = self.create_test_program()
        self.workflow_tool = getToolByName(self.portal, 'portal_workflow')

    
    


    
    ROLES_BY_TRANSITION = {
        'cancel': ['Site Administrator', 'Manager'],
        'suspend': ['Site Administrator', 'Mgmt_Provost', 'Manager'],
    }

    def test_verify_workflow(self):
        program = self.test_program
        workflow_chain = self.workflow_tool.getChainFor(program)
        self.assertEqual(len(workflow_chain), 1)
        program_workflow = workflow_chain[0]
        self.assertEqual(program_workflow, 'programmanagement')


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
        program = createObject(factory)
        self.assertTrue(IOIEStudyAbroadProgram.providedBy(program))

    def test_can_add_a_program(self):
        api.content.delete(self.test_program)
        program = self.create_test_program()
        self.assertTrue(IOIEStudyAbroadProgram.providedBy(program))

    def test_not_editable_by_anonymous(self):
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          'sample-program/@@edit')

    def test_correct_default_workflow(self):
        chains = dict(self.workflow_tool.listChainOverrides())
        default_chain = self.workflow_tool.getDefaultChain()
        program_chain = chains.get('OIEStudyAbroadProgram', default_chain)
        self.assertEqual(program_chain, ('programmanagement',))

    # workflow transitions from initial state

    def test_nonexistent_transition_by_manager(self):
        error_str = ''
        try:
            api.content.transition(obj=self.test_program,
                                   transition='this-transition-does-not-exist')
        except InvalidParameterError as e:
            error_str = e.message
        self.assertTrue('Invalid transition' in error_str)

    def test_cannot_transition_as_anonymous(self):
        login(self.portal, TEST_USER_NAME)
        logout()
        self.assertRaises(InvalidParameterError,
                          api.content.transition,
                          obj=self.test_program,
                          transition='submit-to-chair')

