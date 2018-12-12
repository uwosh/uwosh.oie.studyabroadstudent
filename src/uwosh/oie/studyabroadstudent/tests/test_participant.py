# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from uwosh.oie.studyabroadstudent.interfaces.participant import IOIEStudyAbroadParticipant  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class OIEStudyAbroadParticipantIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadParticipant')
        schema = fti.lookupSchema()
        self.assertEqual(IOIEStudyAbroadParticipant, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadParticipant')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='OIEStudyAbroadParticipant')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEStudyAbroadParticipant.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='OIEStudyAbroadParticipant',
            id='OIEStudyAbroadParticipant',
            state_of_wisconsin_need_based_travel_grant_form_link='',
            special_student_form_for_undergraduate_admissions_form_link='',
            disciplinary_clearance_form_link='',
        )
        self.assertTrue(IOIEStudyAbroadParticipant.providedBy(obj))
