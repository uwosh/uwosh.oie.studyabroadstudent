# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

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
from uwosh.oie.studyabroadstudent.interfaces.airline import IOIEAirline
from uwosh.oie.studyabroadstudent.interfaces.calendaryear import IOIECalendarYear
from uwosh.oie.studyabroadstudent.interfaces.contact import IOIEContact
from uwosh.oie.studyabroadstudent.interfaces.cooperatingpartner import IOIECooperatingPartner
from uwosh.oie.studyabroadstudent.interfaces.country import IOIECountry
from uwosh.oie.studyabroadstudent.interfaces.course import IOIECourse
from uwosh.oie.studyabroadstudent.interfaces.liaison import IOIELiaison
from uwosh.oie.studyabroadstudent.interfaces.participant import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.interfaces.programleader import IOIEProgramLeader
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgram
from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication


class IUwoshOieStudyabroadstudentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
