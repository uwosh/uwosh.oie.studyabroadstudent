# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface, implementer
from plone.namedfile import field
from plone.directives import form


class IOIEHealthSafetySecurityDocument(Interface):
    form.mode(title="display")
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )
    file = field.NamedFile(
        title=_(u'Health, Safety, Security Document'),
        required=True,
    )
