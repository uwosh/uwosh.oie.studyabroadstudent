# -*- coding: utf-8 -*-
from plone.app.contenttypes import indexers
from plone.indexer import indexer as indexer_wrapper
from plone.indexer.decorator import indexer
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant


concat = indexers._unicode_save_string_concat
SearchableText = indexers.SearchableText


def IndexerFactory(name):
    def func(obj):
        return getattr(obj, name, None)
    return func


participantIndexer = indexer_wrapper(IOIEStudyAbroadParticipant)
programName = participantIndexer(IndexerFactory('programName'))


@indexer(IOIEStudyAbroadParticipant)
def university(participant):
    import pdb; pdb.set_trace()  # if universityEnrolledUWO is Yes then this will be "UW Oshkosh", otherwise this is the value of universityEnrolledOther # noqa
