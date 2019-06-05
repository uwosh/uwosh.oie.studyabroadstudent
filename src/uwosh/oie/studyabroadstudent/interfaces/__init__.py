# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from uwosh.oie.studyabroadstudent.interfaces.airline import IOIEAirline  # noqa
from uwosh.oie.studyabroadstudent.interfaces.calendaryear import IOIECalendarYear  # noqa
from uwosh.oie.studyabroadstudent.interfaces.contact import IOIEContact  # noqa
from uwosh.oie.studyabroadstudent.interfaces.cooperatingpartner import IOIECooperatingPartner  # noqa
from uwosh.oie.studyabroadstudent.interfaces.country import IOIECountry  # noqa
from uwosh.oie.studyabroadstudent.interfaces.course import IOIECourse  # noqa
from uwosh.oie.studyabroadstudent.interfaces.emailtemplate import IOIEEmailTemplate  # noqa
from uwosh.oie.studyabroadstudent.interfaces.liaison import IOIELiaison  # noqa
from uwosh.oie.studyabroadstudent.interfaces.participant import IOIEStudyAbroadParticipant  # noqa
from uwosh.oie.studyabroadstudent.interfaces.programleader import IOIEProgramLeader  # noqa
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgram  # noqa
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import IOIEStudyAbroadProgramsFolder  # noqa
from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication  # noqa
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUwoshOieStudyabroadstudentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
