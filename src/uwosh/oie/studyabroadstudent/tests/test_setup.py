"""Setup tests for this package."""
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.testing import \
    UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING as test_layer

import unittest


student = 'uwosh.oie.studyabroadstudent'


class TestSetup(unittest.TestCase):
    f"""Test that {student} is properly installed."""

    layer = test_layer

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        f"""Test if {student} is installed."""
        self.assertTrue(self.installer.is_product_installed(student))

    def test_browserlayer(self):
        """Test that IUwoshOieStudyabroadstudentLayer is registered."""
        from wosh.oie.studyabroadstudent.interfaces import \
            IUwoshOieStudyabroadstudentLayer as layer  # noqa: I001
        from plone.browserlayer.utils import registered_layers  # noqa: I001
        self.assertIn(layer, registered_layers())
