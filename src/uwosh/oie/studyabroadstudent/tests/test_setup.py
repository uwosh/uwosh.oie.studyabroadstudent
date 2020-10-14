# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa

import unittest

oie_student = 'uwosh.oie.studyabroadstudent'

class TestSetup(unittest.TestCase):
    """Test that uwosh.oie.studyabroadstudent is properly installed."""

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if uwosh.oie.studyabroadstudent is installed."""
        self.assertTrue(self.installer.is_product_installed(oie_student))

    def test_browserlayer(self):
        """Test that IUwoshOieStudyabroadstudentLayer is registered."""
        from uwosh.oie.studyabroadstudent.interfaces import \
            IUwoshOieStudyabroadstudentLayer as layer
        from plone.browserlayer import utils
        self.assertIn(layer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        self.installer.uninstallProducts([oie_student])

    def test_product_uninstalled(self):
        """Test if uwosh.oie.studyabroadstudent is cleanly uninstalled."""
        is_installed = self.installer.is_product_installed(oie_student)
        self.assertFalse(is_installed)

    def test_browserlayer_removed(self):
        """Test that IUwoshOieStudyabroadstudentLayer is removed."""
        from uwosh.oie.studyabroadstudent.interfaces import \
            IUwoshOieStudyabroadstudentLayer as layer
        from plone.browserlayer import utils
        self.assertNotIn(layer, utils.registered_layers())
