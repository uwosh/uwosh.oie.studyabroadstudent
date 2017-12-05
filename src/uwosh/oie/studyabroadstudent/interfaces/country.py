# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from collective import dexteritytextindexer


class IOIECountry(Interface):

    dexteritytextindexer.searchable('timezone')
    # TODO vocabulary of time zones
    timezone = schema.Choice(
        title=_(u'Time Zone'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timezone',
        required=True,
    )
    dexteritytextindexer.searchable('cdc_info')
    cdc_info = schema.URI(
        title=_(u'Centers for Disease Control Country Information URL'),
        description=_(u''),
        required=True,
    )
    dexteritytextindexer.searchable('state_dept_info')
    state_dept_info = schema.URI(
        title=_(u'US State Department Country Information URL'),
        description=_(u''),
        required=True,
    )
