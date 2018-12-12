# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import uwosh.oie.studyabroadstudent


class UwoshOieStudyabroadstudentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=uwosh.oie.studyabroadstudent)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'uwosh.oie.studyabroadstudent:default')


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
        z2.ZSERVER_FIXTURE,
    ),
    name='UwoshOieStudyabroadstudentLayer:AcceptanceTesting',
)
