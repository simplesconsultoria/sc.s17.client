# -*- coding: utf-8 -*-

from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.namedfile.field import NamedBlobImage

from sc.s17.client import MessageFactory as _


class IClient(form.Schema):

    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(""),
        required=False,
        )
