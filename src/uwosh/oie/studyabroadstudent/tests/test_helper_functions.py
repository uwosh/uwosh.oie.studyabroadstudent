from . import STATES, OIEStudyAbroadContentBaseTest
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles


def add_transition_tests(cls):
    def create_transition_to_state_test(state):
        def do_create_test(self):
            self._transition_to_state(
                obj=self.test_program,
                destination_state=state,
            )
            self.assertEqual(
                api.content.get_state(self.test_program),
                state,
            )
        return do_create_test

    def generate_tests(cls):
        for state in STATES.keys():
            test_method = create_transition_to_state_test(state=state)
            test_name = f'test_transition_to_{state}'
            test_name = test_name.replace('-', '_')
            test_method.__name__ = test_name
            setattr(cls, test_method.__name__, test_method)

    generate_tests(cls)
    return cls


@add_transition_tests
class TestingHelperFunctions(OIEStudyAbroadContentBaseTest):

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.calendar_year, self.calendar_year_uid = self.get_calendar_year_and_uid()  # noqa : E501
        self.test_program = self.create_test_program()
