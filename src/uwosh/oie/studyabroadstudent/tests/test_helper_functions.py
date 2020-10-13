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


def add_transition_tests(cls):
    
    def create_transition_to_state_test(state):
        def do_create_test(self):
            self._transition_to_state(obj=self.test_program, destination_state=state)
            self.assertEqual(api.content.get_state(self.test_program), state)
        return do_create_test

    def generate_tests(cls):    
        for state in STATES.keys():
            test_method = create_transition_to_state_test(state=state)
            test_name = 'test_transition_to_{}'.format(state)
            test_name = test_name.replace('-', '_')
            test_method.__name__ = test_name
            setattr(cls, test_method.__name__, test_method)
    
    generate_tests(cls)
    return cls
    


@add_transition_tests
class TestingHelperFunctions(OIEStudyAbroadContentBaseTest):

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # self.installer = api.portal.get_tool('portal_quickinstaller')

        self.calendar_year, self.calendar_year_uid = self.get_calendar_year_and_uid()
        self.test_program = self.create_test_program()
        # self.workflow_tool = getToolByName(self.portal, 'portal_workflow')
