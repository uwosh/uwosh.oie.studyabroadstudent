from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadStudentApplication  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject, queryUtility

import unittest


class OIEStudyAbroadStudentApplicationIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEStudyAbroadStudentApplication')
        schema = fti.lookupSchema()
        self.assertEqual(IOIEStudyAbroadStudentApplication, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEStudyAbroadStudentApplication')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI,
                           name='OIEStudyAbroadStudentApplication')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEStudyAbroadStudentApplication.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIEStudyAbroadStudentApplication',
            id='OIEStudyAbroadStudentApplication',
        )
        self.assertTrue(IOIEStudyAbroadStudentApplication.providedBy(obj))
