# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from collective import dexteritytextindexer


class IOIECountry(Interface):

    dexteritytextindexer.searchable('timezone_url')
    timezone_url = schema.URI(
        title=_(u'Time Zone URL'),
        required=False,
    )

    # or use vocabulary of time zones
    dexteritytextindexer.searchable('timezone')
    timezone = schema.List(
        title=_(u'Time Zone(s)'),
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timezone'),
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