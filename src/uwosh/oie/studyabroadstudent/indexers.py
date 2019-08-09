# -*- coding: utf-8 -*-
from plone.app.contenttypes import indexers
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
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
    import pdb; pdb.set_trace()  # if universityEnrolledUWO is Yes then this will be "UW Oshkosh", otherwise this is the value of universityEnrolledOther # noqa


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
    bdata = ILeadImage(program)
    if (
            getattr(bdata, 'image', None) and
            bdata.image is not None and
            bdata.image.size > 0
    ):
        return '{0}/@@images/image'.format(program.absolute_url())
