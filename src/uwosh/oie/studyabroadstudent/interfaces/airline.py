from collective import dexteritytextindexer
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIEAirline(Interface):

    dexteritytextindexer.searchable('luggage_general')
    luggage_general = schema.URI(
        title=_(u'General luggage'),
        description=_(u'website address (URL)'),
        required=False,
    )

    dexteritytextindexer.searchable('luggage_carryon')
    luggage_carryon = schema.URI(
        title=_(u'Carry on luggage'),
        description=_(u'website address (URL)'),
        required=False,
    )

    dexteritytextindexer.searchable('luggage_checked')
    luggage_checked = schema.URI(
        title=_(u'Checked luggage'),
        description=_(u'website address (URL)'),
        required=False,
    )
