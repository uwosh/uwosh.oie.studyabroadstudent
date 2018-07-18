# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
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
            id='sample-program-test_adding',
            calendar_year=self.calendar_year_uid,
            term='1 Fall Interim',
            college_or_unit='B College of Business',
            countries=['Afghanistan'],
        )
        self.assertTrue(IOIEStudyAbroadProgram.providedBy(obj))

    def test_can_transition_by_manager(self):
        obj = self.program
        api.content.transition(obj=obj, transition='submit-to-chair')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'pending-chair-review')

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
