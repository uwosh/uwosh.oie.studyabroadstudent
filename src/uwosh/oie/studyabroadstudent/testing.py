from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing.z2 import ZSERVER_FIXTURE


layer_name = 'UwoshOieStudyabroadstudentLayer'


class UwoshOieStudyabroadstudentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import uwosh.oie.studyabroadstudent as student
        self.loadZCML(package=student)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'uwosh.oie.studyabroadstudent:default')


UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE = UwoshOieStudyabroadstudentLayer()


UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,),
    name=f'{layer_name}:IntegrationTesting',
)


UWOSH_OIE_STUDYABROADSTUDENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,),
    name=f'{layer_name}:FunctionalTesting',
)


UWOSH_OIE_STUDYABROADSTUDENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        UWOSH_OIE_STUDYABROADSTUDENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        ZSERVER_FIXTURE,
    ),
    name=f'{layer_name}:AcceptanceTesting',
)
