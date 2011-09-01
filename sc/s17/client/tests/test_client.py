# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from sc.s17.client.client import IClient
from sc.s17.client.testing import INTEGRATION_TESTING


class TestClientIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('sc.s17.client.client', 'obj')
        self.obj = self.folder['obj']

    def test_adding(self):
        self.folder.invokeFactory('sc.s17.client.client', 'client')
        client = self.folder['client']
        self.failUnless(IClient.providedBy(client))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.client.client')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.client.client')
        schema = fti.lookupSchema()
        self.assertEquals(IClient, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='sc.s17.client.client')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IClient.providedBy(new_object))

    def test_allowed_content_types(self):
        types = ['sc.s17.project.project']
        self.failUnlessEqual(self.obj.getLocallyAllowedTypes(), types)
        self.failUnlessEqual(self.obj.getImmediatelyAddableTypes(), types)
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')
        try:
            self.obj.invokeFactory('sc.s17.project.project', 'foo')
        except Unauthorized:
            self.fail()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)