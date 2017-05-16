# -*- coding: utf-8 -*-
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

MAX_LENGTH = 250

@implementer(IVocabularyFactory)
class SubjectsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.subjects')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i)) for i in values]
        return SimpleVocabulary.fromItems(items)

SubjectsVocabulary = SubjectsVocabularyFactory()

@implementer(IVocabularyFactory)
class MajorsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.majors')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i)) for i in values]
        return SimpleVocabulary.fromItems(items)

MajorsVocabulary = MajorsVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.programs')
        normalizer = queryUtility(IIDNormalizer)
        items = [(normalizer.normalize(i, max_length=MAX_LENGTH), i) for i in values]
        return SimpleVocabulary.fromItems(items)

ProgramsVocabulary = ProgramsVocabularyFactory()

@implementer(IVocabularyFactory)
class SessionHoursVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.session_hours')
        normalizer = queryUtility(IIDNormalizer)
        items = [(normalizer.normalize(i, max_length=MAX_LENGTH), i) for i in values]
        return SimpleVocabulary.fromItems(items)

SessionHoursVocabulary = SessionHoursVocabularyFactory()

@implementer(IVocabularyFactory)
class EthnicitiesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.ethnicities')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i, max_length=MAX_LENGTH)) for i in values]
        return SimpleVocabulary.fromItems(items)

EthnicitiesVocabulary = EthnicitiesVocabularyFactory()

@implementer(IVocabularyFactory)
class MarriageStatusesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.marriage_statuses')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i, max_length=MAX_LENGTH)) for i in values]
        return SimpleVocabulary.fromItems(items)

MarriageStatusesVocabulary = MarriageStatusesVocabularyFactory()

@implementer(IVocabularyFactory)
class GendersVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.genders')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i, max_length=MAX_LENGTH)) for i in values]
        return SimpleVocabulary.fromItems(items)

GendersVocabulary = GendersVocabularyFactory()

@implementer(IVocabularyFactory)
class StatesForResidencyVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.states_for_residency')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i, max_length=MAX_LENGTH)) for i in values]
        return SimpleVocabulary.fromItems(items)

StatesForResidencyVocabulary = StatesForResidencyVocabularyFactory()

@implementer(IVocabularyFactory)
class CitizenshipVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.citizenship')
        normalizer = queryUtility(IIDNormalizer)
        items = [(i, normalizer.normalize(i, max_length=MAX_LENGTH)) for i in values]
        return SimpleVocabulary.fromItems(items)

CitizenshipVocabulary = CitizenshipVocabularyFactory()
