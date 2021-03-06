# -*- coding: utf-8 -*-
from plone.app.contenttypes import indexers
from plone.app.uuid.utils import uuidToObject
from plone.indexer import indexer as indexer_wrapper
from plone.indexer.decorator import indexer
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadProgram

import json


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
    if participant.universityEnrollowedUWO:
        return 'UW Oshkosh'
    return participant.universityEnrolledOther


# Program Indexers
programIndexer = indexer_wrapper(IOIEStudyAbroadProgram)
program_type = programIndexer(IndexerFactory('program_type'))


@indexer(IOIEStudyAbroadProgram)
def calendar_year(program):
    cal = uuidToObject(program.calendar_year)
    return cal.title


@indexer(IOIEStudyAbroadProgram)
def countries(program):
    return json.dumps(program.countries)


@indexer(IOIEStudyAbroadProgram)
def image(program):
    try:
        if (
                getattr(program, 'image', None) and
                program.image.size > 0
        ):
            return '{0}/@@images/image'.format(program.absolute_url())
    except TypeError:
        return
