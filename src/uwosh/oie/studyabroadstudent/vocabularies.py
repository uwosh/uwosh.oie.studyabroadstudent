# -*- coding: utf-8 -*-
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

MAX_LENGTH = 250

@implementer(IVocabularyFactory)
class SubjectsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.subjects')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SubjectsVocabulary = SubjectsVocabularyFactory()

@implementer(IVocabularyFactory)
class MajorsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.majors')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

MajorsVocabulary = MajorsVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.programs')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramsVocabulary = ProgramsVocabularyFactory()

@implementer(IVocabularyFactory)
class SessionHoursVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.session_hours')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SessionHoursVocabulary = SessionHoursVocabularyFactory()

@implementer(IVocabularyFactory)
class EthnicitiesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.ethnicities')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

EthnicitiesVocabulary = EthnicitiesVocabularyFactory()

@implementer(IVocabularyFactory)
class MarriageStatusesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.marriage_statuses')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

MarriageStatusesVocabulary = MarriageStatusesVocabularyFactory()

@implementer(IVocabularyFactory)
class GendersVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.genders')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

GendersVocabulary = GendersVocabularyFactory()

@implementer(IVocabularyFactory)
class StatesForResidencyVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.states_for_residency')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

StatesForResidencyVocabulary = StatesForResidencyVocabularyFactory()

@implementer(IVocabularyFactory)
class CitizenshipVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.citizenship')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CitizenshipVocabulary = CitizenshipVocabularyFactory()

@implementer(IVocabularyFactory)
class CountriesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.countries')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CountriesVocabulary = CountriesVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramTypeVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.program_type')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramTypeVocabulary = ProgramTypeVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramComponentVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.program_component')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramComponentVocabulary = ProgramComponentVocabularyFactory()

@implementer(IVocabularyFactory)
class EquipmentAndSpaceVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.equipment_and_space')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

EquipmentAndSpaceVocabulary = EquipmentAndSpaceVocabularyFactory()

@implementer(IVocabularyFactory)
class GuestLecturesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.guest_lectures')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

GuestLecturesVocabulary = GuestLecturesVocabularyFactory()

@implementer(IVocabularyFactory)
class TermVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.term')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

TermVocabulary = TermVocabularyFactory()

@implementer(IVocabularyFactory)
class CollegeOrUnitVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.college_or_unit')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CollegeOrUnitVocabulary = CollegeOrUnitVocabularyFactory()

@implementer(IVocabularyFactory)
class SponsoringUnitOrDepartmentVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.sponsoring_unit_or_department')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SponsoringUnitOrDepartmentVocabulary = SponsoringUnitOrDepartmentVocabularyFactory()

@implementer(IVocabularyFactory)
class LanguageVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.language')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

LanguageVocabulary = LanguageVocabularyFactory()

@implementer(IVocabularyFactory)
class CreditsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.credits')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CreditsVocabulary = CreditsVocabularyFactory()

@implementer(IVocabularyFactory)
class ContactsVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        contact_brains = catalog(portal_type='OIEContact',
                                sort_on='sortable_title',
                                sort_order='ascending')
        terms = []
        for brain in contact_brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)

ContactsVocabulary = ContactsVocabularyFactory()
