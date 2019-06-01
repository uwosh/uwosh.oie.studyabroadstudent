# -*- coding: utf-8 -*-
from plone.app.contenttypes import indexers
from plone.indexer import indexer as indexer_wrapper
from plone.indexer.decorator import indexer
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadProgram


concat = indexers._unicode_save_string_concat
SearchableText = indexers.SearchableText


def IndexerFactory(name):
    def func(obj):
        return getattr(obj, name, None)
    return func


# Participant Indexers
participantIndexer = indexer_wrapper(IOIEStudyAbroadParticipant)
programName = participantIndexer(IndexerFactory('programName'))
educationLevel = participantIndexer(IndexerFactory('educationLevel'))


@indexer(IOIEStudyAbroadParticipant)
def university(participant):
    import pdb; pdb.set_trace()  # if universityEnrolledUWO is Yes then this will be "UW Oshkosh", otherwise this is the value of universityEnrolledOther # noqa


# Program Indexers
programIndexer = indexer_wrapper(IOIEStudyAbroadProgram)
program_type = indexer_wrapper(IndexerFactory('program_type'))
calendar_year = indexer_wrapper(IndexerFactory('calendar_year'))
