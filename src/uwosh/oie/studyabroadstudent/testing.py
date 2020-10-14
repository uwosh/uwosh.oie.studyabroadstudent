# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE
from plone.testing import Layer, zope, zodb



class UwoshOieStudyabroadstudentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import uwosh.oie.studyabroadstudent
        self.loadZCML(package=uwosh.oie.studyabroadstudent)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'uwosh.oie.studyabroadstudent:default')


# from plone.app.testing import PloneWithPackageLayer
# import my.addon

# FIXTURE = PloneWithPackageLayer(
#     zcml_package=my.addon,
#     zcml_filename='configure.zcml',
#     gs_profile_id='my.addon:default',
#     name="MyAddonFixture"
# )

UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE = UwoshOieStudyabroadstudentLayer()


UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,),
    name='UwoshOieStudyabroadstudentLayer:IntegrationTesting',
)


UWOSH_OIE_STUDYABROADSTUDENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,),
    name='UwoshOieStudyabroadstudentLayer:FunctionalTesting',
)


UWOSH_OIE_STUDYABROADSTUDENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        ZSERVER_FIXTURE,
    ),
    name='UwoshOieStudyabroadstudentLayer:AcceptanceTesting',
)
