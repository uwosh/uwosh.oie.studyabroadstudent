# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING as test_layer  # noqa

import unittest


student = 'uwosh.oie.studyabroadstudent'


class TestUninstall(unittest.TestCase):

    layer = test_layer

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        self.installer.uninstallProducts([student])

    def test_product_uninstalled(self):
        f"""Test if {student} is cleanly uninstalled."""
        is_installed = self.installer.is_product_installed(student)
        self.assertFalse(is_installed)

    def test_browserlayer_removed(self):
        """Test that IUwoshOieStudyabroadstudentLayer is removed."""
        from uwosh.oie.studyabroadstudent.interfaces import \
            IUwoshOieStudyabroadstudentLayer as layer  # noqa : I001
        from plone.browserlayer import utils
        self.assertNotIn(layer, utils.registered_layers())  # noqa : I005
