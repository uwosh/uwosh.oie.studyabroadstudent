# -*- coding: utf-8 -*-

from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
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


class IOIETransition(Interface):
    form.mode(title="display")
    title = schema.TextLine(
        title=_(u'Transition Name'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )
    transitionDate = schema.Date(title=_(u'Transition Date'))
    destinationCity = schema.TextLine(title=_(u'Destination City'))
    destinationCountry = schema.Choice(title=_(u'Destination Country'),
                                       vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries')
    accommodation = schema.Choice(title=_(u'Accommodation'),
                                  vocabulary='uwosh.oie.studyabroadstudent.vocabularies.accommodation')
    accommodationRoomSizes = schema.List(
        title=_(u'Room Size(s)'),
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.room_size')
    )
    transitionType = schema.Choice(
        title=_(u'Transition Type'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.transition_type'
    )


