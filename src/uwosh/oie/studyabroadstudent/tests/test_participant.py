from . import OIEStudyAbroadContentBaseTest
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.participant import IOIEStudyAbroadParticipant  # noqa
from zope.component import createObject, queryUtility


class OIEStudyAbroadParticipantIntegrationTest(OIEStudyAbroadContentBaseTest):

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = get_installer(self.portal)

        # add calendar year
        self.calendar_year, self.calendar_year_uid = self.get_calendar_year_and_uid()  # noqa

        # add a sample program

        self.program = self.create_test_program()
        # add a sample participant
        self.test_participant = self.create_test_participant()

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=self.participant_name)
        schema = fti.lookupSchema()
        self.assertEqual(IOIEStudyAbroadParticipant, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=self.participant_name)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=self.participant_name)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IOIEStudyAbroadParticipant.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type=self.participant_name,
            id=self.participant_name,
        )
        self.assertTrue(IOIEStudyAbroadParticipant.providedBy(obj))

    def test_correct_default_workflow(self):
        workflowTool = api.portal.get_tool('portal_workflow')
        chains = dict(workflowTool.listChainOverrides())
        defaultChain = workflowTool.getDefaultChain()
        participantChain = chains.get(self.participant_name,
                                      defaultChain)
        self.assertEqual(participantChain, ('participant',))

    # def test_cannot_transition_as_anonymous(self):
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     logout()
    #     self.assertRaises(InvalidParameterError,
    #                       api.content.transition,
    #                       obj=self.test_participant,
    #                       transition='submit')
    #
    # def test_can_transition_submit(self, fast=None):
    #     self.assertTrue('Manager' in getSecurityManager().getUser().getRolesInContext(self.portal))  # noqa
    #     initial_state = 'express-interest'
    #     transition = 'submit'
    #     end_state = 'step-i'
    #     authorized_roles = ['Manager',
    #                         'Mgmt_Admin',
    #                         'Mgmt_Liaison',
    #                         'Participant_Applicant']
    #     self._transition_and_or_roles_test(fast,
    #                                        initial_state,
    #                                        transition,
    #                                        end_state,
    #                                        authorized_roles)

    def test_transition_with_email_template(self):
        pass  # TODO # noqa: T000
