# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.transition import IOIETransition
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class OIETransitionIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIETransition')
        schema = fti.lookupSchema()
        self.assertEqual(IOIETransition, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIETransition')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIETransition')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIETransition.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIETransition',
            id='OIETransition',
        )
        self.assertTrue(IOIETransition.providedBy(obj))
