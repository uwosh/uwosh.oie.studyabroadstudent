from collective import dexteritytextindexer
from plone.autoform.directives import mode
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from zope import schema
from zope.interface import Interface


class IOIETransition(Interface):
    mode(title='hidden')
    title = schema.TextLine(
        title=_('Transition Name'),
        required=False,
        default=_('will be auto-generated on save'),
    )

    transitionDate = schema.Date(
        title=_('Transition Date'),
        required=True,
    )

    dexteritytextindexer.searchable('destinationCity')
    destinationCity = schema.TextLine(
        title=_('Destination City'),
        required=True,
    )

    dexteritytextindexer.searchable('destinationCountry')
    destinationCountry = schema.Choice(
        title=_('Destination Country'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.countries'),
    )

    transitionType = schema.Choice(
        title=_('Transition Type'),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.transition_type',
        ),
    )

    accommodation = schema.Choice(
        title=_('Accommodation'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.accommodation'),
    )

    accommodationRoomSizes = schema.List(
        title=_('Room Size(s)'),
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.room_size',
            ),
        ),
    )
