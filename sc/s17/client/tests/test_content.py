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


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_adding(self):
        self.failUnless(IClient.providedBy(self.obj))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        schema = fti.lookupSchema()
        self.assertEquals(IClient, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=ctype)
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IClient.providedBy(new_object))

    def test_allowed_content_types(self):
        # projects can only be added to an active client
        workflow_tool = getattr(self.portal, 'portal_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        workflow_tool.doActionFor(self.obj, 'activate')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        types = ['sc.s17.project']
        allowed_types = [t.getId() for t in self.obj.allowedContentTypes()]
        for t in types:
            self.failUnless(t in allowed_types)

        # trying to add any other content type raises an error
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')

        try:
            self.obj.invokeFactory('sc.s17.project', 'foo')
        except Unauthorized:
            self.fail()

    def test_view(self):
        view = self.obj.restrictedTraverse('@@view')
        projects = view.projects()
        self.assertEquals(0, len(projects))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
