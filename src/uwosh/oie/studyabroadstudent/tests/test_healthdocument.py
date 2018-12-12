# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.tests.base import getFile
from uwosh.oie.studyabroadstudent.interfaces.healthdocument import IOIEHealthSafetySecurityDocument  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class OIEHealthSafetySecurityDocumentIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEHealthSafetySecurityDocument')
        schema = fti.lookupSchema()
        self.assertEqual(IOIEHealthSafetySecurityDocument, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEHealthSafetySecurityDocument')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEHealthSafetySecurityDocument')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEHealthSafetySecurityDocument.providedBy(obj))

    def test_adding(self):
        file = getFile('notimage.doc')
        obj = api.content.create(
            container=self.portal,
            type='OIEHealthSafetySecurityDocument',
            id='OIEHealthSafetySecurityDocument',
            file=file,
        )
        self.assertTrue(IOIEHealthSafetySecurityDocument.providedBy(obj))
