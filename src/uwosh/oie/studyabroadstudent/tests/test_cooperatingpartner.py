# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from uwosh.oie.studyabroadstudent.interfaces.cooperatingpartner import IOIECooperatingPartner  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class OIECooperatingPartnerIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIECooperatingPartner')
        schema = fti.lookupSchema()
        self.assertEqual(IOIECooperatingPartner, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIECooperatingPartner')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIECooperatingPartner')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIECooperatingPartner.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIECooperatingPartner',
            id='OIECooperatingPartner',
        )
        self.assertTrue(IOIECooperatingPartner.providedBy(obj))
