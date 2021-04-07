from os.path import dirname, join
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.healthdocument import \
    IOIEHealthSafetySecurityDocument  # noqa : E501
from uwosh.oie.studyabroadstudent.testing import \
    UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING as test_layer  # noqa : E501
from zope.component import createObject, queryUtility

import unittest


class OIEHealthSafetySecurityDocumentIntegrationTest(unittest.TestCase):

    layer = test_layer

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

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
        path = join(dirname(__file__), 'notimage.doc')
        with open(path) as file:
            obj = api.content.create(
                container=self.portal,
                type='OIEHealthSafetySecurityDocument',
                id='OIEHealthSafetySecurityDocument',
                file=file,
            )
        self.assertTrue(IOIEHealthSafetySecurityDocument.providedBy(obj))
