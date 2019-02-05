# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from uwosh.oie.studyabroadstudent.browser.programview_role_restricted import VIEWABILITY  # noqa
from uwosh.oie.studyabroadstudent.testing import UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING  # noqa

import unittest


PROGRAM_WORKFLOW_ID = 'programmanagement'


class OIEViewabilityCoverageIntegrationTest(unittest.TestCase):

    layer = UWOSH_OIE_STUDYABROADSTUDENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.wftool = api.portal.get_tool('portal_workflow')

    def test_coverage(self):
        """Check that we have all the workflow roles and states covered in the
           VIEWABILITY configuration constant"""

        # get the workflow
        wftool = self.wftool
        assert(wftool is not None)
        program_workflow = wftool[PROGRAM_WORKFLOW_ID]

        # get all the workflow states
        states = program_workflow.states.items()
        workflow_state_ids = [id for id, state in states]

        # get all the workflow roles
        workflow_roles = program_workflow.getRoles()  # noqa
        # for some reason, that gets all roles on the site
        # so must remove the participant workflow roles
        workflow_roles = [
            r for r in workflow_roles if not r.startswith('Participant_')
        ]

        # get all the roles defined in VIEWABILITY
        viewability_roles = VIEWABILITY.keys()

        # get all the states defined in VIEWABILITY
        viewability_states = set()
        for role in viewability_roles:
            viewability_states |= set(VIEWABILITY[role].keys())

        # check counts are the same
        self.assertEqual(len(viewability_states), len(workflow_state_ids))
        self.assertEqual(len(viewability_roles), len(workflow_roles))

        # ensure all states in VIEWABILITY are defined in the workflow
        for viewability_state in viewability_states:
            self.assertIn(viewability_state, workflow_state_ids)

        # ensure all states in the workflow are defined in VIEWABILITY
        for workflow_state_id in workflow_state_ids:
            self.assertIn(workflow_state_id, viewability_states)

        # ensure all roles in VIEWABILITY are defined in the workflow
        for viewability_role in viewability_roles:
            self.assertIn(viewability_role, workflow_roles)

        # ensure all roles in the workflow are defined in VIEWABILITY
        for workflow_role in workflow_roles:
            self.assertIn(workflow_role, viewability_roles)
