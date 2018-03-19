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

    def country_info(self):
        """Retrieve info for all countries associated with the program"""
        country_info_html = '<dl>'
        countries = self.context.countries
        portal = api.portal.get()
        for country_name in countries:
            brains = api.content.find(portal_type='OIECountry', Title=country_name)
            country = brains[0].getObject()
            country_url = country.absolute_url()
            timezone_url = country.timezone_url
            cdc_info_url = country.cdc_info_url
            state_dept_info_url = country.state_dept_info_url
            country_info_html += \
                '<dt><a href="%s">%s</a></dt>' \
                '<dd><a href="%s">CDC</a>, '\
                '<a href="%s">State Dept.</a>, '\
                '<a href="%s">time zone</a></dd>' % \
                (country_url, country_name, cdc_info_url, state_dept_info_url, timezone_url)
        country_info_html += '</dl>'
        return country_info_html


class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        primary_contact = getattr(self.context, 'primary_contact', None)
        if primary_contact:
            contact = primary_contact.to_object
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
        return ''


class ContactView(DefaultView):
    pass


class ParticipantView(DefaultView):
    pass
