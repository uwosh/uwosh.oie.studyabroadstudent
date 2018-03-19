# from Acquisition import aq_inner
# from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.app.contenttypes.browser.folder import FolderView


class ApplicationView(DefaultView):
    pass


class ProgramView(DefaultView, FolderView):
    def can_edit(self):
        """Determine whether to show the 'public' information only or the actual contents of the Program"""
        if api.user.is_anonymous():
            return False
        current = api.user.get_current()
        roles = api.user.get_roles(username=current.id)
        if 'Manager' in roles or 'Site Administrator' in roles:
            return True
        return not False


class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        contact = self.context.primary_contact.to_object
        return '<a href="%s">%s, %s, %s, %s, %s, %s : %s</a>' % (
            contact.absolute_url(),
            getattr(contact, 'title', None),
            getattr(contact, 'job_title', None),
            getattr(contact, 'telephone', None),
            getattr(contact, 'mobile', None),
            getattr(contact, 'email', None),
            getattr(contact, 'other_service', None),
            getattr(contact, 'other_username', None),
        )


class ContactView(DefaultView):
    pass


class ParticipantView(DefaultView):
    pass
