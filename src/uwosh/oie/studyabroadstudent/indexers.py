from plone.app.contenttypes import indexers
from plone.app.uuid.utils import uuidToObject
from plone.indexer import indexer as indexer_wrapper
from plone.indexer.decorator import indexer
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant, IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.utils import get_object_from_uid

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
    cal = get_object_from_uid(program.calendar_year)
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
            return f'{program.absolute_url()}/@@images/image'
    except TypeError:
        return
