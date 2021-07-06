"""Module where all interfaces, events and exceptions live."""

from uwosh.oie.studyabroadstudent.interfaces.airline import IOIEAirline  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.calendaryear import IOIECalendarYear  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.contact import IOIEContact  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.cooperatingpartner import IOIECooperatingPartner  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.country import IOIECountry  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.course import IOIECourse  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.emailtemplate import (  # noqa: F401
    IOIEParticipantEmailTemplate,
    IOIEProgramEmailTemplate,
)
from uwosh.oie.studyabroadstudent.interfaces.liaison import IOIELiaison  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.participant import IOIEStudyAbroadParticipant  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.programleader import IOIEProgramLeader  # noqa: F401
from uwosh.oie.studyabroadstudent.interfaces.studyabroadprogram import (  # noqa: F401
    IOIEStudyAbroadProgram,
    IOIEStudyAbroadProgramsFolder,
)
from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import (  # noqa: F401
    IOIEStudyAbroadStudentApplication,
)
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUwoshOieStudyabroadstudentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
