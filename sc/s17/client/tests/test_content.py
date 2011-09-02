# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFPlone.interfaces.constrains import IConstrainTypes

from sc.s17.client.content import IClient
from sc.s17.client.testing import INTEGRATION_TESTING

ctype = 'sc.s17.client.content'


class TestClientIntegration(unittest.TestCase):

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
        types = ['sc.s17.project.content']

        # test allowed content types
        allowed_types = [t.getId() for t in self.obj.allowedContentTypes()]
        for t in types:
            self.failUnless(t in allowed_types)

        # test addable content types on menu
        constrain = IConstrainTypes(self.obj, None)
        if constrain:
            immediately_addable_types = constrain.getLocallyAllowedTypes()
            for t in types:
                self.failUnless(t in immediately_addable_types)

        # trying to add any other content type raises an error
        self.assertRaises(ValueError,
                          self.obj.invokeFactory, 'Document', 'foo')

        try:
            self.obj.invokeFactory('sc.s17.project.content', 'foo')
        except Unauthorized:
            self.fail()


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
