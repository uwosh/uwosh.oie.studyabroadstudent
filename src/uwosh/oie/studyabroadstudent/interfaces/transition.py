# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from plone.directives import form
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from zope import schema
from zope.interface import Interface


class IOIETransition(Interface):
    form.mode(title='display')
    title = schema.TextLine(
        title=_(u'Transition Name'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )

    transitionDate = schema.Date(
        title=_(u'Transition Date'),
        required=True,
    )

    dexteritytextindexer.searchable('destinationCity')
    destinationCity = schema.TextLine(
        title=_(u'Destination City'),
        required=True,
    )

    dexteritytextindexer.searchable('destinationCountry')
    destinationCountry = schema.Choice(
        title=_(u'Destination Country'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
    )

    transitionType = schema.Choice(
        title=_(u'Transition Type'),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.transition_type',
        ),
    )

    accommodation = schema.Choice(
        title=_(u'Accommodation'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.accommodation'),
    )

    accommodationRoomSizes = schema.List(
        title=_(u'Room Size(s)'),
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.room_size',
            ),
        ),
    )
