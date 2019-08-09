# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.browser.view import DefaultView
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedImage
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from uwosh.oie.studyabroadstudent.reporting import ReportUtil
from uwosh.oie.studyabroadstudent.vocabularies import NewProgramsVocabulary
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

import base64
import json
import logging
import Missing


logger = logging.getLogger('uwosh.oie.studyabroadstudent')


def handle_missing(obj):
    if obj == Missing.Value:
        return None
    return obj


class ApplicationView(DefaultView):
    # this is for the legacy applications
    pass


class ProgramView(DefaultView, FolderView):
    def can_edit(self):
        """Determine whether to show the 'public' information only or the
        actual contents of the Program
        """
        if api.user.is_anonymous():
            return False
        current = api.user.get_current()
        roles = api.user.get_roles(username=current.id)
        if 'Manager' in roles or 'Site Administrator' in roles:
            return True
        return False

    def country_info(self):
        """Retrieve info for all countries associated with the program"""
        country_info_html = '<dl>'
        countries = self.context.countries
        for country_name in countries:
            brains = api.content.find(portal_type='OIECountry',
                                      Title=country_name)
            if brains:
                country = brains[0].getObject()
                country_url = country.absolute_url()
                if country_url is None:
                    country_url_atag = '(missing country URL)'
                else:
                    country_url_atag = '<a href="{0}">{1}</a>'.format(
                        country_url,
                        country_name,
                    )
                timezone_url = country.timezone_url
                if timezone_url is None:
                    timezone_url_atag = '(missing timezone URL)'
                else:
                    timezone_url_atag = '<a href="{0}">time zone</a>'.format(
                        timezone_url)
                cdc_info_url = country.cdc_info_url
                if cdc_info_url is None:
                    cdc_info_url_atag = '(missing CDC URL)'
                else:
                    cdc_info_url_atag = '<a href="{0}">CDC</a>'.format(
                        cdc_info_url,
                    )
                state_dept_info_url = country.state_dept_info_url
                if state_dept_info_url is None:
                    state_dept_info_url_atag = '(missing State Dept URL)'
                else:
                    state_dept_info_url_atag = '<a href="{0}">State Dept.</a>'.format(  # noqa
                        state_dept_info_url,
                    )
                country_info_html += \
                    '<dt>{0}</dt><dd>{1}, {2}, {3}</dd>'.format(
                        country_url_atag,
                        cdc_info_url_atag,
                        state_dept_info_url_atag,
                        timezone_url_atag)
            else:
                country_info_html += '<dt>{0} (missing country info)</dt>'.format(  # noqa
                    country_name,
                )
        country_info_html += '</dl>'
        return country_info_html

    def uwo_logo(self):
        uwo_logo_data = api.portal.get_registry_record(
            'oiestudyabroadstudent.uwo_logo',
        )
        if uwo_logo_data is None or len(uwo_logo_data) == 0:
            return None
        filename, data = b64decode_file(uwo_logo_data)
        image = NamedImage(data=data, filename=filename)
        return image

    def footer_info(self):
        footer_text = api.portal.get_registry_record(
            'oiestudyabroadstudent.program_view_footer',
        )
        return footer_text

    def liaison(self):
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
        if (
                self.context.program_coleaders and
                len(self.context.program_coleaders) > 0
        ):
            coleaders = [uuidToObject(coleader['coleader'])
                         for coleader in self.context.program_coleaders]
        return coleaders

    def calendar_year(self):
        year_uid = self.context.calendar_year
        if year_uid:
            year = api.content.get(UID=year_uid)
            if year:
                return year

    def housing(self):
        brains = api.content.find(context=self.context,
                                  portal_type='OIETransition')
        locations = [b.getObject() for b in brains]
        return set([l.accommodation for l in locations])

    def has_lead_image(self):
        bdata = ILeadImage(self.context)
        if (
                getattr(bdata, 'image', None) and
                bdata.image is not None and
                bdata.image.size > 0
        ):
            return True

    def get_detailed_view_link(self):
        return self.context.absolute_url() + '/manager_view'


class ProgramSearchView(BrowserView):

    def get_program_data(self):
        programs = []
        catalog = api.portal.get_tool('portal_catalog')
        # TODO brains = catalog(portal_type='OIEStudyAbroadProgram',  # noqa
        #                 review_state='application-intake-in-progress')
        brains = catalog(portal_type='OIEStudyAbroadProgram')
        for brain in brains:
            try:
                program = {
                            'title': brain.Title,
                            'description': brain.Description,
                            'uid': brain.UID,
                            'url': brain.getURL(),
                            'type': brain.program_type,
                            'calendarYear': brain.calendar_year,
                            'countries': json.loads(brain.countries),
                            'image': brain.image,
                           }
                programs.append(program)
            except AttributeError:
                logger.warn('Excluding program {0} from '
                            'search view, not all searchable fields were '
                            'indexed.'.format(brain.Title))

        string = json.dumps(programs, default=handle_missing)
        encoded = base64.b64encode(string)
        return encoded


class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        primary_contact = getattr(self.context, 'primary_contact', None)
        if primary_contact:
            contact = primary_contact.to_object
            return '<a href="{url}">{title}, {job}, {tel}, {mob}, {email}, {serv} : {user}</a>'.format(  # noqa
                url=contact.absolute_url(),
                title=getattr(contact, 'title', None),
                job=getattr(contact, 'job_title', None),
                tel=getattr(contact, 'telephone', None),
                mob=getattr(contact, 'mobile', None),
                email=getattr(contact, 'email', None),
                serv=getattr(contact, 'other_service', None),
                user=getattr(contact, 'other_username', None),
            )
        return ''


class ContactView(DefaultView):
    pass


class ParticipantView(DefaultView, FolderView):
    # This can be the view for reviewers/etc of the application
    pass


class ParticipantEditUtilView(DefaultView):
    # participantedit.js will call this, it will return data that will help
    # accomplish remaining TODO items for edit for customization  # noqa
    # such as adding relevant dates to field text dynamically
    # and checking conditions which might cause a field to be hidden
    pass


class ApplyView(DefaultView):

    def get_programs(self):
        programs = []
        vocab = NewProgramsVocabulary(self.context)
        for program_term in vocab:
            program = {'name': program_term.title,
                       'uid': program_term.value,
                       'selected': False}
            if program_term.value == self.context.UID():
                program['selected'] = True
            programs.append(program)
        string = json.dumps(programs, default=handle_missing)
        encoded = base64.b64encode(string)
        return encoded


class CreatedView(DefaultView):

    created = False

    def __call__(self):
        if self.request.method == 'POST':
            alsoProvides(self.request, IDisableCSRFProtection)
            self.created = self.create_participant()
            if not self.created:
                pass  # Show some error message
        return super(CreatedView, self).__call__()

    def create_participant(self):
        program_ID = self.context.UID()
        first = self.request.get('first', None)
        last = self.request.get('last', None)
        email = self.request.get('email', None)
        fields = [program_ID, first, last, email]
        if all(fields):
            try:
                site = api.portal.get()
                participants_folder = site['participants']
                data = {
                    'firstName': first,
                    'lastName': last,
                    'email': email,
                    'programName': program_ID,
                }
                obj = api.content.create(
                    type='OIEStudyAbroadParticipant',
                    container=participants_folder,
                    title='{0} {1}'.format(first, last),
                    **data)
                api.content.transition(obj, 'submit')  # go ahead to step I
                return '{0}/edit'.format(obj.absolute_url())
            except Exception:
                logger.warn('Could not create partipant application.')
        return False


class AttemptTransitionsPeriodicallyView(DefaultView):

    def __call__(self, *args, **kwargs):
        """execute certain workflow transitions which should use their guard
        expressions before proceeding
        """
        logger = logging.getLogger(__class__)  # noqa
        logger.info("'transition has been attempted")


class ReportingView(DefaultView):

    def getReportUtil(self):
        return ReportUtil(self.context)
