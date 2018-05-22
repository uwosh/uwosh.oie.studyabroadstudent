# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from plone.directives import form
from collective import dexteritytextindexer


class IOIETransition(Interface):
    form.mode(title="display")
    title = schema.TextLine(
        title=_(u'Transition Name'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )

    transitionDate = schema.Date(title=_(u'Transition Date'))

    dexteritytextindexer.searchable('destinationCity')
    destinationCity = schema.TextLine(title=_(u'Destination City'))

    dexteritytextindexer.searchable('destinationCountry')
    destinationCountry = schema.Choice(title=_(u'Destination Country'),
                                       source=RegistryValueVocabulary('oiestudyabroadstudent.countries'))

    accommodation = schema.Choice(title=_(u'Accommodation'),
                                  source=RegistryValueVocabulary('oiestudyabroadstudent.accommodation'))

    accommodationRoomSizes = schema.List(
        title=_(u'Room Size(s)'),
        value_type=schema.Choice(source=RegistryValueVocabulary('oiestudyabroadstudent.room_size'))
    )

    transitionType = schema.Choice(
        title=_(u'Transition Type'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.transition_type'),
    )


