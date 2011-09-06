# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from five import grok

from plone.directives import form, dexterity
from plone.namedfile.field import NamedBlobImage

from Products.CMFPlone.utils import getToolByName

from sc.s17.client import MessageFactory as _
from sc.s17.project.content import IProject


class IClient(form.Schema):

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(''),
        required=False,
        )


class View(dexterity.DisplayForm):
    grok.context(IClient)
    grok.require('zope2.View')

    def projects(self):
        """Return a catalog search result of projects to show.
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        projects = catalog(object_provides=IProject.__identifier__,
                           path='/'.join(context.getPhysicalPath()),
                           sort_on='getObjPositionInParent')

        projects = [brain.getObject() for brain in projects]
        projects = [{'title': obj.Title(),
                     'description': obj.Description(),
                     'url': obj.remoteUrl} for obj in projects]
        return projects
