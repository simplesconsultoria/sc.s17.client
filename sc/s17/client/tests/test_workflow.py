# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from sc.s17.client.content import IClient
from sc.s17.client.testing import INTEGRATION_TESTING

ctype = 'sc.s17.client'

class TestClientIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = self.portal['portal_workflow']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_workflow_client_installed(self):
        workflow_id = 'client_workflow'
        workflows_ids = self.workflow.getWorkflowIds()
        self.failUnless(workflow_id in workflows_ids)

    def test_workflow_client_applied(self):
        workflow_id = 'client_workflow'
        self.failUnless(workflow_id in self.workflow.getWorkflowsFor(self.obj)[0].id)

    def test_workflow_client_transitions(self):
        trans = self.workflow.getTransitionsFor(self.obj)
        self.assertEqual(len(trans), 1)

    def test_workflow_client_states(self):
        wf_names = ['client_workflow',]
        workflows = self.workflow.getChainFor(self.obj)
        for wf_name in wf_names:
            self.failUnless(wf_name in workflows)