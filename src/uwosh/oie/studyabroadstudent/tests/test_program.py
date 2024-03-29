from . import (
    ROLES,
    STATES,
    TRANSITIONS,
    OIEStudyAbroadContentBaseTest,
)
from AccessControl import Unauthorized
from plone.api.content import delete as content_delete
from plone.api.content import transition as content_transition
from plone.api.exc import InvalidParameterError
from plone.api.portal import get_tool
from plone.app.testing import (
    TEST_USER_ID,
    TEST_USER_NAME,
    login,
    logout,
    setRoles,
)
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgram as IProgram
from zope.component import createObject, queryUtility


def add_dynamic_tests(cls):
    def create_invalid_transition_test(start_state,
                                       transition,
                                       end_state):
        def do_create_test(self):
            self.test_program = self._transition_to_state(
                obj=self.test_program,
                destination_state=start_state,
            )
            self._attempt_invalid_transition(
                obj=self.test_program,
                transition=transition,
                end_state=start_state,
            )
        return do_create_test

    def create_transition_by_role_test(
        start_state,
        role,
        transition,
        end_state,
        is_authorized,
        fast=False,
    ):
        def do_create_test(self):
            self.test_program = self._transition_to_state(
                obj=self.test_program,
                destination_state=start_state,
            )
            if is_authorized:
                self._verify_allowed_transition_by_role(
                    obj=self.test_program,
                    initial_state=start_state,
                    role=role,
                    transition=transition,
                    destination_state=end_state,
                    end_state=end_state,
                )
            else:
                self._verify_unauthorized_transition_by_role(
                    obj=self.test_program,
                    initial_state=start_state,
                    role=role,
                    transition=transition,
                    end_state=start_state,
                )
        return do_create_test

    def generate_tests(cls):
        for state_id, state_info in STATES.items():
            for transition_name, transition in TRANSITIONS.items():
                start_state = state_id
                end_state = transition['new_state']
                if transition_name not in state_info['exit_transitions']:
                    test_method = create_invalid_transition_test(
                        start_state=start_state,
                        transition=transition_name,
                        end_state=end_state)
                    test_name = f'test_invalid_transition_{transition_name}_from_{start_state}_to_{end_state}'  # noqa
                    test_name = test_name.replace('-', '_')
                    test_method.__name__ = test_name
                    setattr(cls, test_method.__name__, test_method)
                else:
                    authorized_roles = transition['guard_roles']
                    for role in ROLES:
                        is_authorized = role in authorized_roles
                        test_method = create_transition_by_role_test(
                            start_state=start_state,
                            role=role,
                            transition=transition_name,
                            end_state=end_state,
                            is_authorized=is_authorized)
                        can_or_cannot = 'can' if role in authorized_roles else 'cannot'  # noqa
                        test_name = f'test_{role}_{can_or_cannot}_activate_{transition["transition_id"]}_from_state_{state_id}'  # noqa
                        test_name = test_name.replace('-', '_')
                        test_method.__name__ = test_name
                        setattr(cls, test_method.__name__, test_method)
    generate_tests(cls)
    return cls


# @add_dynamic_tests
class OIEStudyAbroadProgramIntegrationTest(OIEStudyAbroadContentBaseTest):

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.installer = get_installer(self.portal)

        self.calendar_year, self.calendar_year_uid = self.get_calendar_year_and_uid()  # noqa
        self.test_program = self.create_test_program()
        self.workflow_tool = get_tool('portal_workflow')

    ROLES_BY_TRANSITION = {
        'cancel': ['Site Administrator', 'Manager'],
        'suspend': ['Site Administrator', 'Mgmt_Provost', 'Manager'],
    }

    def test_verify_workflow(self):
        program = self.test_program
        workflow_chain = self.workflow_tool.getChainFor(program)
        self.assertEqual(len(workflow_chain), 1)
        program_workflow = workflow_chain[0]
        self.assertEqual(program_workflow, 'programmanagement')

    def test_is_addon_installed(self):
        package = 'uwosh.oie.studyabroadstudent'
        is_installed = self.installer.is_product_installed(package)
        self.assertTrue(is_installed)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=self.program_name)
        schema = fti.lookupSchema()
        self.assertEqual(IProgram, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=self.program_name)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=self.program_name)
        factory = fti.factory
        program = createObject(factory)
        self.assertTrue(IProgram.providedBy(program))

    def test_can_add_a_program(self):
        content_delete(self.test_program)
        program = self.create_test_program()
        self.assertTrue(IProgram.providedBy(program))

    def test_not_editable_by_anonymous(self):
        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            'sample-program/@@edit',
        )

    def test_correct_default_workflow(self):
        chains = dict(self.workflow_tool.listChainOverrides())
        default_chain = self.workflow_tool.getDefaultChain()
        program_chain = chains.get(self.program_name, default_chain)
        self.assertEqual(program_chain, ('programmanagement',))

    # workflow transitions from initial state

    def test_nonexistent_transition_by_manager(self):
        try:
            content_transition(
                obj=self.test_program,
                transition='this-transition-does-not-exist',
            )
        except InvalidParameterError as e:
            self.assertTrue('Invalid transition' in str(e))

    def test_cannot_transition_as_anonymous(self):
        login(self.portal, TEST_USER_NAME)
        logout()
        self.assertRaises(
            InvalidParameterError,
            content_transition,
            obj=self.test_program,
            transition='submit-to-chair',
        )
