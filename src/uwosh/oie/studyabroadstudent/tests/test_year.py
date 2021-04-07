from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.calendaryear import IOIECalendarYear  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject, queryUtility

import unittest


class OIECalendarYearIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIECalendarYear')
        schema = fti.lookupSchema()
        self.assertEqual(IOIECalendarYear, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIECalendarYear')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIECalendarYear')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIECalendarYear.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIECalendarYear',
            id='OIECalendarYear',
        )
        self.assertTrue(IOIECalendarYear.providedBy(obj))

    def test_view_year_in_toplevel_folder(self):
        """test that we can view a year even if not a Manager"""
        year = api.content.create(
            container=self.portal,
            type='OIECalendarYear',
            id='OIECalendarYear',
        )
        setRoles(self.portal, TEST_USER_ID, ['Mgmt_Chair'])
        self.assertIsNotNone(year, 'unable to view year as Mgmt_Chair')
