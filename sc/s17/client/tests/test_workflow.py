# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.WorkflowCore import WorkflowException

from sc.s17.client.testing import INTEGRATION_TESTING

ctype = 'sc.s17.client'
workflow_id = 'client_workflow'


class WorkflowTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow_tool = getattr(self.portal, 'portal_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_workflow_installed(self):
        ids = self.workflow_tool.getWorkflowIds()
        self.failUnless(workflow_id in ids)

    def test_default_workflow(self):
        chain = self.workflow_tool.getChainForPortalType(self.obj.portal_type)
        self.failUnless(len(chain) == 1)
        self.failUnless(chain[0] == workflow_id)

    def test_workflow_initial_state(self):
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'inactive')

    def test_workflow_transitions(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'activate')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'active')
        self.workflow_tool.doActionFor(self.obj, 'deactivate')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'inactive')

    def test_workflow_permissions(self):
        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'activate')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'activate')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'deactivate')
