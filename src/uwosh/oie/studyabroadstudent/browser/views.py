from Acquisition import aq_inner
from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.app.contenttypes.browser.folder import FolderView

class ApplicationView(DefaultView):
    pass

class ProgramView(DefaultView, FolderView):
    pass

class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        contact = self.context.primary_contact.to_object
        return '<a href="%s">%s, %s, %s, %s, %s, %s</a>' % (
            contact.absolute_url(),
            contact.title,
            contact.job_title,
            contact.telephone,
            contact.mobile,
            contact.email,
            contact.other,
        )

class ContactView(DefaultView):
    pass
