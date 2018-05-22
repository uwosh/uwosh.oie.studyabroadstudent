# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
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
