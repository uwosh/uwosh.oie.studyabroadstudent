# -*- coding: utf-8 -*-

from plone.autoform.directives import mode
from plone.namedfile import field
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIEHealthSafetySecurityDocument(Interface):
    mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )
    file = field.NamedFile(
        title=_(u'Health, Safety, Security Document'),
        required=True,
    )
