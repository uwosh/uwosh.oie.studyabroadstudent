# -*- coding: utf-8 -*-

from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface, implementer
from plone.supermodel import model
from plone.namedfile import field
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, \
    dayofmonth_vocabulary, hold_vocabulary, aware_vocabulary, program_cycle_vocabulary, seat_assignment_protocol
from plone.directives import form
from Products.CMFPlone.RegistrationTool import checkEmailAddress, EmailAddressInvalid
from zope.schema import ValidationError
from collective import dexteritytextindexer
from plone.formwidget.namedfile.widget import NamedFileFieldWidget
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import validate_email


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
