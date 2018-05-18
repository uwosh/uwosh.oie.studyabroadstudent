# from Acquisition import aq_inner
# from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.app.contenttypes.behaviors.leadimage import ILeadImage

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
            if brains:
                country = brains[0].getObject()
                country_url = country.absolute_url()
                if country_url is None:
                    country_url_atag = '(missing country URL)'
                else:
                    country_url_atag = '<a href="%s">%s</a>' % (country_url, country_name)
                timezone_url = country.timezone_url
                if timezone_url is None:
                    timezone_url_atag = '(missing timezone URL)'
                else:
                    timezone_url_atag = '<a href="%s">time zone</a>' % timezone_url
                cdc_info_url = country.cdc_info_url
                if cdc_info_url is None:
                    cdc_info_url_atag = '(missing CDC URL)'
                else:
                    cdc_info_url_atag = '<a href="%s">CDC</a>' % cdc_info_url
                state_dept_info_url = country.state_dept_info_url
                if state_dept_info_url is None:
                    state_dept_info_url_atag = '(missing State Dept URL)'
                else:
                    state_dept_info_url_atag = '<a href="%s">State Dept.</a>' % state_dept_info_url
                country_info_html += \
                    '<dt>%s</dt><dd>%s, %s, %s</dd>' % \
                    (country_url_atag, cdc_info_url_atag, state_dept_info_url_atag, timezone_url_atag)
            else:
                country_info_html += '<dt>%s (missing country info)</dt>' % country_name
        country_info_html += '</dl>'
        return country_info_html

    def uwo_logo_url(self):
        uwo_logo_uid = api.portal.get_registry_record('oiestudyabroadstudent.uwo_logo')
        uwo_logo = uuidToObject(uwo_logo_uid)
        return uwo_logo.absolute_url()

    def footer_info(self):
        footer_text = api.portal.get_registry_record('oiestudyabroadstudent.program_view_footer')
        return footer_text

    def liaison (self):
        liaison = None
        if self.context.liaison:
            liaison = uuidToObject(self.context.liaison)
        return liaison

    def leader(self):
        leader = None
        if self.context.program_leader:
            leader = uuidToObject(self.context.program_leader)
        return leader

    def coleaders(self):
        coleaders = []
        if self.context.program_coleaders and len(self.context.program_coleaders) > 0:
            coleaders = [uuidToObject(coleader['coleader']) for coleader in self.context.program_coleaders]
        return coleaders

    def calendar_year(self):
        year_uid = self.context.calendar_year
        if year_uid:
            year = api.content.get(UID=year_uid)
            if year:
                return year

    def housing(self):
        travelDatesTransitionsAndDestinations = self.context.travelDatesTransitionsAndDestinations
        return [location['accommodation'] for location in travelDatesTransitionsAndDestinations]

    def has_lead_image(self):
        bdata = ILeadImage(self.context)
        if hasattr(bdata, 'image') and bdata.image is not None and bdata.image.size > 0:
            return True

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
