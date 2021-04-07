
from collective import dexteritytextindexer
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface


class IOIECountry(Interface):

    dexteritytextindexer.searchable('timezone_url')
    timezone_url = schema.URI(
        title=_(u'Time Zone URL'),
        required=False,
    )
    dexteritytextindexer.searchable('cdc_info_url')
    cdc_info_url = schema.URI(
        title=_(u'Centers for Disease Control Country Information URL'),
        description=_(u''),
        required=False,
    )
    dexteritytextindexer.searchable('state_dept_info_url')
    state_dept_info_url = schema.URI(
        title=_(u'US State Department Country Information URL'),
        description=_(u''),
        required=False,
    )
