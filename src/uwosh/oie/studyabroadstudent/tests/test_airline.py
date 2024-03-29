from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.airline import IOIEAirline
from uwosh.oie.studyabroadstudent.testing import \
    UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING as testing_layer  # noqa
from zope.component import createObject, queryUtility

import unittest


class OIEAirlineIntegrationTest(unittest.TestCase):

    layer = testing_layer

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIEAirline')
        schema = fti.lookupSchema()
        self.assertEqual(IOIEAirline, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIEAirline')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIEAirline')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEAirline.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIEAirline',
            id='OIEAirline',
        )
        self.assertTrue(IOIEAirline.providedBy(obj))
