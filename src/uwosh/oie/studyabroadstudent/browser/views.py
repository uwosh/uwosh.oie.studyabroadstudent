from io import StringIO
from plone import api
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.autoform.interfaces import OMITTED_KEY
from plone.dexterity.browser.view import DefaultView
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedImage
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from time import time
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadParticipant
from uwosh.oie.studyabroadstudent.reporting import ReportUtil
from zope.interface import Interface, alsoProvides

import csv
import json
import logging
import Missing
import os


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
        return 'Manager' in roles or 'Site Administrator' in roles

    def country_info(self):
        """Retrieve info for all countries associated with the program"""
        country_info_html = '<dl>'
        countries = self.context.countries
        for country_name in countries:
            brains = api.content.find(
                portal_type='OIECountry',
                Title=country_name,
            )
            if brains:
                country = brains[0].getObject()
                country_url = country.absolute_url()
                if country_url is None:
                    country_url_atag = '(missing country URL)'
                else:
                    country_url_atag = f'<a href="{country_url}">{country_name}</a>'
                timezone_url = country.timezone_url
                if timezone_url is None:
                    timezone_url_atag = '(missing timezone URL)'
                else:
                    timezone_url_atag = f'<a href="{timezone_url}">time zone</a>'
                cdc_info_url = country.cdc_info_url
                if cdc_info_url is None:
                    cdc_info_url_atag = '(missing CDC URL)'
                else:
                    cdc_info_url_atag = f'<a href="{cdc_info_url}">CDC</a>'
                state_dept_info_url = country.state_dept_info_url
                if state_dept_info_url is None:
                    state_dept_info_url_atag = '(missing State Dept URL)'
                else:
                    state_dept_info_url_atag = f'<a href="{state_dept_info_url}">State Dept.</a>'
                country_info_html += \
                    f'<dt>{country_url_atag}</dt><dd>{cdc_info_url_atag}, ' + \
                    f'{state_dept_info_url_atag}, {timezone_url_atag}</dd>'
            else:
                country_info_html += f'<dt>{country_name} (missing country info)</dt>'
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
            coleaders = [
                uuidToObject(coleader['coleader'])
                for coleader
                in self.context.program_coleaders
            ]
        return coleaders

    def calendar_year(self):
        year_uid = self.context.calendar_year
        if year_uid:
            year = api.content.get(UID=year_uid)
            if year:
                return year

    def housing(self):
        brains = api.content.find(
            context=self.context,
            portal_type='OIETransition',
        )
        locations = [brain.getObject() for brain in brains]
        return set([location.accommodation for location in locations])

    def has_lead_image(self):
        try:
            if (
                getattr(self.context, 'image', None) and
                self.context.image.size > 0
            ):
                return True
        except TypeError:
            return False

    def get_detailed_view_link(self):
        return self.context.absolute_url() + '/manager_view'


class ProgramSearchView(BrowserView):

    def get_program_data(self):
        programs = []
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            portal_type='OIEStudyAbroadProgram',
            review_state='application-intake-in-progress',
        )
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
                logger.warning(
                    f'Excluding program {brain.Title} from search view, '
                    'not all searchable fields were indexed.'
                )
        return json.dumps(programs, default=handle_missing)


class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        primary_contact = getattr(self.context, 'primary_contact', None)
        if primary_contact:
            contact = primary_contact.to_object
            url = contact.absolute_url()
            title = getattr(contact, 'title', None)
            job = getattr(contact, 'job_title', None)
            tel = getattr(contact, 'telephone', None)
            mob = getattr(contact, 'mobile', None)
            email = getattr(contact, 'email', None)
            serv = getattr(contact, 'other_service', None)
            user = getattr(contact, 'other_username', None)
            return f'<a href="{url}">{title}, {job}, {tel}, {mob}, {email}, {serv} : {user}</a>'
        return ''


class ContactView(DefaultView):
    pass


class ParticipantView(DefaultView, FolderView):
    # This can be the view for reviewers/etc of the application

    @property
    def permissions(self):
        if not getattr(self, '_permissions', None):
            self._permissions = self._get_permissions(
                self.user_roles,
                self.transition_state,
            )
        return self._permissions

    @property
    def transition_state(self):
        if not getattr(self, '_transition_state', None):
            # try:
            self._transition_state = api.content.get_state(self.context)
            # except KeyError:
            #    self._transition_state = None
        return self._transition_state

    @property
    def user_roles(self):
        if not getattr(self, '_user_roles', None):
            # self._user_roles = api.user.get_current().getRoles()  # noqa : P001
            self._user_roles = []
        return self._user_roles

    def _get_permissions(self, user_roles, transition_state):
        relative_path = '../static/json/optimized_participant_permissions.json'
        absolute_path = os.path.join(os.path.dirname(__file__), relative_path)
        field_permissions = {}
        # try:
        with open(absolute_path, 'r') as infile:
            permission_map = json.load(infile)
        # except Exception:
        #     return field_permissions
        for role in user_roles:
            role_permissions = (
                permission_map[role]['default_permissions'],
                permission_map[role][transition_state],
            )
            for permissions in role_permissions:
                for read_write_none in permissions:
                    for field in permissions[read_write_none]:
                        field_permissions[field] = self._highest_permission(
                            field_permissions.get(field, None),
                            read_write_none,
                        )
        return field_permissions

    def show_error_page(self):
        return False

    def updateFieldsFromSchemata(self):
        IOIEStudyAbroadParticipant.setTaggedValue(
            OMITTED_KEY,
            [
                (Interface, field, 'true')
                for field in self.permissions
                if self.permissions[field] == 'none'
            ]
        )
        super().updateFieldsFromSchemata()

    def _highest_permission(self, *permissions):
        ranked = [None, 'none', 'read', 'read_write']
        tmp = {
            permission: ranked.index(permission)
            for permission in set(permissions)
        }
        return max(tmp, key=tmp.get)

    def _get_show_these(self):
        show_these = {'fields': {}, 'groups': {}}
        for group in self.groups:
            show_these['groups'][group.label] = False
            for widget in group.widgets.values():
                if self.can_view_field(widget.label):
                    show_these['groups'][group.label] = True
                    break

        for field in self.widgets.values():
            if self._can_view_field(field.label):
                show_these['fields'][field.label] = True
            else:
                show_these['fields'][field.label] = False

        return show_these

    def _can_view_field(self, field_name):
        return field_name in self.permissions['read'] + self.permissions['read_write']

    def show_widget(self, widget):
        disallowed = (
            'IBasic.title',
            'IBasic.description',
            'title',
            'description',
        )
        # if not self._permissions:
        #     self.call()
        return widget.__name__ not in disallowed and \
            self._permissions['fields'][widget.label] in ('read', 'read_write')


class ParticipantEditUtilView(DefaultView):
    def _get_payment_deadlines(self, program):
        return [
            {
                'label': 'Spring Interim, Summer & Fall Semester Payment Deadline 1',
                'date': str(program.spring_interim_summer_fall_semester_payment_deadline_1),
            },
            {
                'label': 'Spring Interim Payment Deadline 2',
                'date': str(program.spring_interim_payment_deadline_2),
            },
            {
                'label': 'Summer Payment Deadline 2',
                'date': str(program.summer_payment_deadline_2),
            },
            {
                'label': 'Fall Semester Payment Deadline 2',
                'date': str(program.fall_semester_payment_deadline_2),
            },
            {
                'label': 'Winter Interim & Spring Semester Payment Deadline 1',
                'date': str(program.winter_interim_spring_payment_deadline_1),
            },
            {
                'label': 'Winter Interim & Spring Semester Payment Deadline 2',
                'date': str(program.winter_interim_spring_payment_deadline_2),
            },
        ]

    def _get_orientation_deadlines(self, program):
        return [
            {
                'label': 'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
                'date': str(program.spring_interim_summer_fall_semester_participant_orientation_deadline),
            },
            {
                'label': 'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
                'date': str(program.winter_interim_spring_semester_participant_orientation_deadline),
            },
        ]

    def __call__(self):
        program = uuidToObject(self.context.programName)
        return {
            'individualInterview': program.individualInterview,
            'orientationDeadlines': self._get_orientation_deadlines(program),
            'paymentDeadlines': self._get_payment_deadlines(program),
            'pretravelStart': str(program.pretravel_dates[0]['pretravel_start_datetime']),
            'pretravelEnd': str(program.pretravel_dates[0]['pretravel_end_datetime']),
        }


class ApplyView(DefaultView):
    pass


class CreatedView(DefaultView):

    created = False

    def __call__(self):
        if self.request.method == 'POST':
            alsoProvides(self.request, IDisableCSRFProtection)
            self.created = self.create_participant()
            if not self.created:
                pass  # Show some error message
        return super().__call__()

    def create_participant(self):
        program_name = self.context.title
        first = self.request.get('first', None)
        last = self.request.get('last', None)
        email = self.request.get('email', None)
        fields = [program_name, first, last, email]
        if all(fields):
            try:
                site = api.portal.get()
                participants_folder = site['participants']
                data = {
                    'firstName': first,
                    'lastName': last,
                    'email': email,
                    'programName': program_name,
                }
                with api.env.adopt_roles(roles='Manager'):
                    obj = api.content.create(
                        type='OIEStudyAbroadParticipant',
                        container=participants_folder,
                        title=f'{first} {last}',
                        **data,
                    )
                    api.content.transition(obj, 'submit')  # go ahead to step I
                return f'{obj.absolute_url()}/edit'
            except Exception as e:  # noqa: B902
                logger.warning('Could not create partipant application.')
                logger.warning(e)
        return False


class AttemptTransitionsPeriodicallyView(DefaultView):

    def __call__(self, *args, **kwargs):
        """execute certain workflow transitions which should use their guard
        expressions before proceeding
        """
        logger = logging.getLogger(__class__)
        logger.info('transition has been attempted')


class ReportingView(DefaultView):

    def __call__(self):
        if 'csv' in self.request.form:
            util = self.getReportUtil()

            output = StringIO()
            writer = csv.writer(output)

            writer.writerow([
                'Participant Type',
                'Count for this Program',
            ])
            writer.writerow([
                'High School Participants',
                util.high_school_count(),
            ])
            writer.writerow([
                'UWO Freshman Participants',
                util.uwo_freshman_count(),
            ])
            writer.writerow([
                'UWO Sophomore Participants',
                util.uwo_sophomore_count(),
            ])
            writer.writerow([
                'UWO Junior Participants',
                util.uwo_junior_count(),
            ])
            writer.writerow([
                'UWO Senior Participants',
                util.uwo_senior_count(),
            ])
            writer.writerow([
                'UWO Graduate Participants',
                util.uwo_graduate_count(),
            ])
            writer.writerow([
                'Other Undergraduate Participants',
                util.other_undergrad_count(),
            ])
            writer.writerow([
                'Other Graduate Participants',
                util.other_graduate_count(),
            ])

            resp = self.request.response
            filename = f'{self.context.Title()}-report.csv'
            resp.setHeader(
                'Content-Disposition',
                f'attachment; filename={filename}',
            )
            resp.setHeader('Content-Type', 'text/csv')
            output.seek(0)
            return output.read()
        else:
            return super().__call__()

    def getReportUtil(self):
        return ReportUtil(self.context)


class ProgramEditUtilView(DefaultView):
    def __call__(self):
        util_data = {}

        util_data['portalState'] = api.content.get_state(self.context)

        return json.dumps(util_data)
