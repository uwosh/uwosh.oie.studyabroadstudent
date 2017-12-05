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
