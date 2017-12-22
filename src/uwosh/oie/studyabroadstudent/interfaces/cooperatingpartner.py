from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.supermodel import model
from plone.namedfile import field
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, month_vocabulary, dayofmonth_vocabulary, room_type_vocabulary, smoking_vocabulary, semester_vocabulary, student_type_vocabulary, bus_vocabulary, fly_vocabulary, orientation_conflict_vocabulary, hold_vocabulary, aware_vocabulary


class IOIECooperatingPartner(Interface):

    widget(
        'primary_contact',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['OIEContact']
        }
    )
    primary_contact = RelationChoice(
        title=_('Primary Contact'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    dexteritytextindexer.searchable('website')
    website = schema.URI(
        title=_(u'Partner Web Address'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_1')
    hq_address_1 = schema.TextLine(
        title=_(u'Address 1'),
        description=_(u'must be a real address, not a post office box or similar'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_2')
    hq_address_2 = schema.TextLine(
        title=_(u'Address 2'),
        description=_(u'must be a real address, not a post office box or similar'),
        required=False,
    )
    dexteritytextindexer.searchable('hq_city')
    hq_city = schema.TextLine(
        title=_(u'City'),
        description=_(u''),
        required=True,
    )
    dexteritytextindexer.searchable('hq_state')
    hq_state = schema.TextLine(
        title=_(u'State'),
        description=_(u'(or province or equivalent)'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_mailing_code')
    hq_mailing_code = schema.TextLine(
        title=_(u'Mailing Code'),
        description=_(u'Zip or Postal Code or equivalent'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_country')
    hq_country = schema.TextLine(
        title=_(u'Country'),
        description=_(u''),
        required=True,
    )