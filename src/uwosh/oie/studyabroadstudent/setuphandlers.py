# -*- coding: utf-8 -*-
from plone import api
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.app.textfield.value import RichTextValue
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from zope.component import queryUtility
from zope.interface import implementer

import random
import string


PASSWORD_LENGTH = 50


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'uwosh.oie.studyabroadstudent:uninstall',
        ]


def constrain_types(folder, ftis):
    aspect = ISelectableConstrainTypes(folder)
    aspect.setConstrainTypesMode(1)
    aspect.setLocallyAllowedTypes(ftis)
    aspect.setImmediatelyAddableTypes(ftis)


def create_toplevel_folder(portal,
                           portal_ids,
                           title,
                           id,
                           ftis,
                           publish_but_exclude=False):
    if id not in portal_ids:
        folder = api.content.create(
            type='Folder',
            title=title, id=id,
            container=portal,
        )
    else:
        folder = portal[id]
    constrain_types(folder, ftis)
    if publish_but_exclude:
        if folder.exclude_from_nav is not True:
            folder.exclude_from_nav = True
        if api.content.get_state(folder) != 'published':
            api.content.transition(folder, transition='publish')


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    portal_items = portal.items()
    portal_ids = [id for id, obj in portal_items]

    populate_toplevel_folders(portal, portal_ids)
    populate_repositories(portal, portal_ids)
    populate_countries(portal)
    populate_years(portal)
    hide_users_folder(portal, portal_ids)
    set_front_page_text(portal, portal_ids)

    populate_airlines(portal)
    populate_partners(portal)
    enable_commenting()
    create_generic_accounts(portal)

    grant_permissions_toplevel_folders(portal)


def create_generic_accounts(portal):
    _create_account('kim.nguyen+Site_Admin@wildcardcorp.com',
                    'Site_Admin', ['Site_Admin', 'SiteAdministrator'])

    # program management workflow
    _create_account('kim.nguyen+Mgmt_Director@wildcardcorp.com',
                    'Mgmt_Director', ['Mgmt_Director', 'SiteAdministrator'])
    _create_account('kim.nguyen+Mgmt_Admin@wildcardcorp.com',
                    'Mgmt_Admin', ['Mgmt_Admin'])
    _create_account('kim.nguyen+Mgmt_Manager@wildcardcorp.com',
                    'Mgmt_Manager', ['Mgmt_Manager'])
    _create_account('kim.nguyen+Mgmt_Coordinator@wildcardcorp.com',
                    'Mgmt_Coordinator', ['Mgmt_Coordinator'])
    _create_account('kim.nguyen+Mgmt_Financial@wildcardcorp.com',
                    'Mgmt_Financial', ['Mgmt_Financial'])
    _create_account('kim.nguyen+Mgmt_OIEProfessional@wildcardcorp.com',
                    'Mgmt_OIEProfessional', ['Mgmt_OIEProfessional'])
    # TODO duplicate?  # noqa
    _create_account('kim.nguyen+Mgmt_OIE@wildcardcorp.com',
                    'Mgmt_OIE', ['Mgmt_OIE'])
    # TODO not in workflow roles  # noqa
    _create_account('kim.nguyen+Mgmt_Intern@wildcardcorp.com',
                    'Mgmt_Intern', ['Mgmt_Intern'])
    _create_account('kim.nguyen+Mgmt_Liaison@wildcardcorp.com',
                    'Mgmt_Liaison', ['Mgmt_Liaison'])
    _create_account('kim.nguyen+Mgmt_ProgramLeader@wildcardcorp.com',
                    'Mgmt_ProgramLeader', ['Mgmt_ProgramLeader'])
    _create_account('kim.nguyen+Mgmt_Dean@wildcardcorp.com',
                    'Mgmt_Dean', ['Mgmt_Dean'])
    # TODO duplicate?  # noqa
    _create_account('kim.nguyen+Mgmt_DeanDirector@wildcardcorp.com',
                    'Mgmt_DeanDirector', ['Mgmt_DeanDirector'])
    _create_account('kim.nguyen+Mgmt_Chair@wildcardcorp.com',
                    'Mgmt_Chair', ['Mgmt_Chair'])
    _create_account('kim.nguyen+Mgmt_Provost@wildcardcorp.com',
                    'Mgmt_Provost', ['Mgmt_Provost'])
    _create_account('kim.nguyen+Mgmt_HR@wildcardcorp.com',
                    'Mgmt_HR', ['Mgmt_HR'])
    _create_account('kim.nguyen+Mgmt_Access@wildcardcorp.com',
                    'Mgmt_Access', ['Mgmt_Access'])
    _create_account('kim.nguyen+Mgmt_Emergency@wildcardcorp.com',
                    'Mgmt_Emergency', ['Mgmt_Emergency'])
    _create_account('kim.nguyen+Mgmt_CourseBuilder@wildcardcorp.com',
                    'Mgmt_CourseBuilder', ['Mgmt_CourseBuilder'])
    _create_account('kim.nguyen+Mgmt_AdminServices@wildcardcorp.com',
                    'Mgmt_AdminServices', ['Mgmt_AdminServices'])
    _create_account('kim.nguyen+Mgmt_LeaderReview@wildcardcorp.com',
                    'Mgmt_LeaderReview', ['Mgmt_LeaderReview'])
    _create_account('kim.nguyen+Mgmt_CourseBuilder@wildcardcorp.com',
                    'Mgmt_CourseBuilder', ['Mgmt_CourseBuilder'])
    _create_account('kim.nguyen+Mgmt_RiskMgmt@wildcardcorp.com',
                    'Mgmt_RiskMgmt', ['Mgmt_RiskMgmt'])

    # participant workflow
    _create_account('kim.nguyen+Participant_Director@wildcardcorp.com',
                    'Participant_Director', ['Participant_Director'])
    _create_account('kim.nguyen+Participant_Manager@wildcardcorp.com',
                    'Participant_Manager', ['Participant_Manager'])
    _create_account('kim.nguyen+Participant_Coordinator@wildcardcorp.com',
                    'Participant_Coordinator', ['Participant_Coordinator'])
    _create_account('kim.nguyen+Participant_Financial@wildcardcorp.com',
                    'Participant_Financial', ['Participant_Financial'])
    _create_account('kim.nguyen+Participant_OIEProfessional@wildcardcorp.com',
                    'Participant_OIEProfessional',
                    ['Participant_OIEProfessional'])
    _create_account('kim.nguyen+Participant_Intern@wildcardcorp.com',
                    'Participant_Intern', ['Participant_Intern'])
    _create_account('kim.nguyen+Participant_Liaison@wildcardcorp.com',
                    'Participant_Liaison', ['Participant_Liaison'])
    _create_account('kim.nguyen+Participant_ProgramLeader@wildcardcorp.com',
                    'Participant_ProgramLeader', ['Participant_ProgramLeader'])
    _create_account('kim.nguyen+Participant_FinancialAid@wildcardcorp.com',
                    'Participant_FinancialAid', ['Participant_FinancialAid'])
    _create_account('kim.nguyen+Participant_Provost@wildcardcorp.com',
                    'Participant_Provost', ['Participant_Provost'])
    _create_account('kim.nguyen+Participant_DeanOfStudents@wildcardcorp.com',
                    'Participant_DeanOfStudents',
                    ['Participant_DeanOfStudents'])
    _create_account('kim.nguyen+Participant_Health@wildcardcorp.com',
                    'Participant_Health', ['Participant_Health'])
    _create_account('kim.nguyen+Participant_StudentAccounts@wildcardcorp.com',
                    'Participant_StudentAccounts',
                    ['Participant_StudentAccounts'])
    _create_account('kim.nguyen+Participant_Reference@wildcardcorp.com',
                    'Participant_Reference', ['Participant_Reference'])
    _create_account('kim.nguyen+Participant_RiskMgmt@wildcardcorp.com',
                    'Participant_RiskMgmt', ['Participant_RiskMgmt'])
    _create_account('kim.nguyen+Participant_Applicant@wildcardcorp.com',
                    'Participant_Applicant', ['Participant_Applicant'])


def _generatePassword(length):
    return ''.join(
        random.choice(
            string.ascii_letters + string.digits + string.punctuation,
        ) for x in range(length)
    )


def _create_account(email, username, roles, password=None):
    # check if account already exists before trying to create
    user = api.user.get(username=username)
    if not user:
        if password is None:
            password = _generatePassword(PASSWORD_LENGTH)
        try:
            user = api.user.create(
                email=email,
                username=username,
                password=password,
            )
            api.user.grant_roles(username=user.id, roles=roles)
        except Exception:
            pass


def set_front_page_text(portal, portal_ids):
    # change front page text
    if 'front-page' in portal_ids:
        frontpage = portal['front-page']
        frontpage.title = 'Welcome to OIE'
        frontpage.description = \
            'You have reached the UW Oshkosh Office of International Education'
        frontpage.text = RichTextValue(
            u'Lorem ipsum',
            'text/plain',
            'text/html',
        )


def hide_users_folder(portal, portal_ids):
    # retract and hide Users
    if 'Members' in portal_ids:
        user_folder = portal['Members']
        wf_state = api.content.get_state(user_folder)
        if wf_state != 'private':
            api.content.transition(obj=user_folder, transition='retract')
        user_folder.exclude_from_nav = True


def populate_repositories(portal, portal_ids):
    # create and hide repositories
    create_toplevel_folder(
        portal,
        portal_ids,
        'Images',
        'image-repository',
        ['Image'],
    )
    images = portal['image-repository']
    images.exclude_from_nav = True
    wf_state = api.content.get_state(images)
    if wf_state != 'published':
        api.content.transition(obj=images, transition='publish')
    create_toplevel_folder(
        portal,
        portal_ids,
        'Files',
        'file-repository',
        ['File'],
    )
    files = portal['file-repository']
    files.exclude_from_nav = True
    wf_state = api.content.get_state(files)
    if wf_state != 'published':
        api.content.transition(obj=files, transition='publish')


def grant_permissions_toplevel_folders(portal):
    # programs folder
    api.group.create(groupname='liaison', title='Liaison')
    api.group.add_user(groupname='liaison', username='Mgmt_Liaison')
    folder = portal.programs
    folder.manage_addLocalRoles('liaison', ['Contributor'])


def populate_toplevel_folders(portal, portal_ids):
    # add folders and restrict addable types
    create_toplevel_folder(portal, portal_ids, 'Legacy Applications',
                           'legacy-applications',
                           ['OIEStudyAbroadStudentApplication'])
    create_toplevel_folder(portal, portal_ids, 'Countries', 'countries',
                           ['OIECountry'], publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Participants', 'participants',
                           ['OIEStudyAbroadParticipant'],
                           publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Programs', 'programs',
                           ['OIEStudyAbroadProgram'],
                           publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'People', 'people',
                           ['OIEContact', 'OIELiaison', 'OIEProgramLeader'],
                           publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Partners', 'partners',
                           ['OIECooperatingPartner'],
                           publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Years', 'years',
                           ['OIECalendarYear'], publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Airlines', 'airlines',
                           ['OIEAirline'], publish_but_exclude=True)
    create_toplevel_folder(portal, portal_ids, 'Forms', 'forms', ['File'])


def enable_commenting():
    # enable commenting/discussion
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IDiscussionSettings, check=False)  # noqa
    if not settings.globally_enabled:
        settings.globally_enabled = True
    if not settings.moderation_enabled:
        settings.moderation_enabled = True
    if not settings.edit_comment_enabled:
        settings.edit_comment_enabled = True
    if not settings.delete_own_comment_enabled:
        settings.delete_own_comment_enabled = True
    if not settings.moderator_notification_enabled:
        settings.moderator_notification_enabled = True
    if not settings.moderator_email:
        settings.moderator_email = 'oie@uwosh.edu'
    if not settings.user_notification_enabled:
        settings.user_notification_enabled = True


def populate_years(portal):
    # populate Calendar Year content items
    years_folder = portal['years']
    create_year('2018', years_folder)
    create_year('2019', years_folder)
    create_year('2020', years_folder)


def populate_partners(portal):
    # populate Cooperating Partners content items
    partner_folder = portal['partners']
    create_partner('Academic Programs International (API)', partner_folder)
    create_partner('Accent International', partner_folder)
    create_partner('American Institute for Foreign Study (AIFS)',
                   partner_folder)
    create_partner('AMIDEAST', partner_folder)
    create_partner('Amizade Ltd.', partner_folder)
    create_partner('Anglo Educational Services', partner_folder)
    create_partner('Anytour International', partner_folder)
    create_partner('Beyond Borders International / Minds Abroad',
                   partner_folder)
    create_partner('Cultural Experiences Abroad (CEA)', partner_folder)
    create_partner('Customized Educational Programs Abroad (CEPA)',
                   partner_folder)
    create_partner('China Sense', partner_folder)
    create_partner('Council on International Educational Exchange (CIEE)',
                   partner_folder)
    create_partner('CISabroad', partner_folder)
    create_partner('Destination Partners', partner_folder)
    create_partner('Educators Abroad Ltd', partner_folder)
    create_partner('EF College Study Tours', partner_folder)
    create_partner('EIL Intercultural Learning', partner_folder)
    create_partner('Fellowship Travel', partner_folder)
    create_partner('Global Academic Ventures', partner_folder)
    create_partner('Global Engagement Institute', partner_folder)
    create_partner('Happy Tours - Peru', partner_folder)
    create_partner('Inspiration India', partner_folder)
    create_partner('International Studies Abroad (ISA)', partner_folder)
    create_partner('International Study Programs (ISP)', partner_folder)
    create_partner('International Volunteer HQ (IVHQ)', partner_folder)
    create_partner('Operation Groundswell', partner_folder)
    create_partner('Palace Travel', partner_folder)
    create_partner('Rama Tours', partner_folder)
    create_partner('Select Travel Study', partner_folder)
    create_partner('Seminars International', partner_folder)
    create_partner('Spanish Learning', partner_folder)
    create_partner('Vesna Tours', partner_folder)
    create_partner('VIDA Volunteer', partner_folder)
    create_partner('World Endeavors', partner_folder)
    create_partner('Worldstrides Capstone', partner_folder)


def populate_airlines(portal):
    # populate airlines
    airline_folder = portal['airlines']
    create_airline('Adria Airways', airline_folder)
    create_airline('Aegean', airline_folder)
    create_airline('Aer Lingus', airline_folder)
    create_airline('Aeroflot-Russian Airlines', airline_folder)
    create_airline('AeroGal', airline_folder)
    create_airline('Aerolineas Argentinas', airline_folder)
    create_airline('Aeromar Airlines', airline_folder)
    create_airline('Aeromexico', airline_folder)
    create_airline('Aerosvit Airlines', airline_folder)
    create_airline('AirAsia', airline_folder)
    create_airline('Air Astana', airline_folder)
    create_airline('Air Baltic', airline_folder)
    create_airline('Air Botswana', airline_folder)
    create_airline('Air Canada', airline_folder)
    create_airline('Air Caraibes', airline_folder)
    create_airline('Air China', airline_folder)
    create_airline('Air Corsica', airline_folder)
    create_airline('Air Europa', airline_folder)
    create_airline('Air France', airline_folder)
    create_airline('Air India', airline_folder)
    create_airline('Air Inuit', airline_folder)
    create_airline('Air Malta', airline_folder)
    create_airline('Air Mauritius', airline_folder)
    create_airline('Air New Zealand', airline_folder)
    create_airline('Air North', airline_folder)
    create_airline('Air Pacific', airline_folder)
    create_airline('Air Tahiti Nui', airline_folder)
    create_airline('Air Transat', airline_folder)
    create_airline('airberlin', airline_folder)
    create_airline('AirTran Airways', airline_folder)
    create_airline('Alaska Airlines', airline_folder)
    create_airline('Alitalia', airline_folder)
    create_airline('All Nippon Airways', airline_folder)
    create_airline('American Airlines', airline_folder)
    create_airline('Aserca Airlines', airline_folder)
    create_airline('Asiana Airlines', airline_folder)
    create_airline('Austrian Airlines', airline_folder)
    create_airline('AviancaTaca', airline_folder)
    create_airline('Bangkok Airways', airline_folder)
    create_airline('Bearskin Airlines', airline_folder)
    create_airline('British Airways', airline_folder)
    create_airline('Brussels Airlines', airline_folder)
    create_airline('Cape Air', airline_folder)
    create_airline('Caribbean Airlines', airline_folder)
    create_airline('Carpatair', airline_folder)
    create_airline('Cathay Pacific', airline_folder)
    create_airline('Cayman Airways', airline_folder)
    create_airline('China Airlines', airline_folder)
    create_airline('China Eastern', airline_folder)
    create_airline('China Southern Airlines', airline_folder)
    create_airline('Condor', airline_folder)
    create_airline('Copa', airline_folder)
    create_airline('Corsairfly', airline_folder)
    create_airline('Czech Airlines', airline_folder)
    create_airline('Darwin Airline', airline_folder)
    create_airline('Delta', airline_folder)
    create_airline('Egyptair', airline_folder)
    create_airline('El Al', airline_folder)
    create_airline('Emirates', airline_folder)
    create_airline('Estonian Air', airline_folder)
    create_airline('Ethiopian Airlines', airline_folder)
    create_airline('Etihad Airways', airline_folder)
    create_airline('EVA Airways', airline_folder)
    create_airline('Finnair', airline_folder)
    create_airline('Flybe', airline_folder)
    create_airline('Frontier Airlines', airline_folder)
    create_airline('Garuda', airline_folder)
    create_airline('GOL', airline_folder)
    create_airline('Gulf Air', airline_folder)
    create_airline('Hainan Air', airline_folder)
    create_airline('Hawaiian Airlines', airline_folder)
    create_airline('Hong Kong Airlines', airline_folder)
    create_airline('Iberia', airline_folder)
    create_airline('Iceland Air', airline_folder)
    create_airline('Island Air', airline_folder)
    create_airline('Insel Air International', airline_folder)
    create_airline('Interjet', airline_folder)
    create_airline('Japan Airlines', airline_folder)
    create_airline('Jet Airways', airline_folder)
    create_airline('JetBlue Airways', airline_folder)
    create_airline('Jetstar', airline_folder)
    create_airline('Kenya Airways', airline_folder)
    create_airline('KLM', airline_folder)
    create_airline('Korean Air', airline_folder)
    create_airline('LACSA', airline_folder)
    create_airline('LAN Airlines', airline_folder)
    create_airline('LAN Argentina', airline_folder)
    create_airline('LAN Ecuador', airline_folder)
    create_airline('LAN Peru', airline_folder)
    create_airline('LAO Airlines', airline_folder)
    create_airline('LOT-Polish Airlines', airline_folder)
    create_airline('Lufthansa', airline_folder)
    create_airline('Luxair', airline_folder)
    create_airline('Malaysia Airlines', airline_folder)
    create_airline('Meridiana fly', airline_folder)
    create_airline('Middle East Airlines', airline_folder)
    create_airline('Mokulele Airlines', airline_folder)
    create_airline('Niki', airline_folder)
    create_airline('Olympic', airline_folder)
    create_airline('Oman Air', airline_folder)
    create_airline('Openskies', airline_folder)
    create_airline('Pacific Wings', airline_folder)
    create_airline('Pakistan International', airline_folder)
    create_airline('PenAir', airline_folder)
    create_airline('Philippine Airlines', airline_folder)
    create_airline('Porter Airlines', airline_folder)
    create_airline('PrecisionAir', airline_folder)
    create_airline('Proflight Commuter', airline_folder)
    create_airline('Qantas Airways', airline_folder)
    create_airline('Qatar Airways', airline_folder)
    create_airline('Royal Air Maroc', airline_folder)
    create_airline('Royal Brunei Airlines', airline_folder)
    create_airline('Royal Jordanian', airline_folder)
    create_airline('S7 Airlines', airline_folder)
    create_airline('Santa Barbara Airlines', airline_folder)
    create_airline('SAS', airline_folder)
    create_airline('SATA Internacional', airline_folder)
    create_airline('Saudi Arabian Airlines', airline_folder)
    create_airline('Seaborne Airlines', airline_folder)
    create_airline('Shandong Airlines', airline_folder)
    create_airline('Shenzen Airlines', airline_folder)
    create_airline('Silver Airways', airline_folder)
    create_airline('Singapore Airlines', airline_folder)
    create_airline('South African Airways', airline_folder)
    create_airline('Spirit', airline_folder)
    create_airline('Sri Lankan', airline_folder)
    create_airline('Sun Country Airlines', airline_folder)
    create_airline('Sunwing', airline_folder)
    create_airline('Surinam Airways', airline_folder)
    create_airline('Swiss International Air Lines', airline_folder)
    create_airline('TAAG Angola', airline_folder)
    create_airline('TACA', airline_folder)
    create_airline('TAM Airlines', airline_folder)
    create_airline('TAP Portugal', airline_folder)
    create_airline('Tarom-Romanian Air Transport', airline_folder)
    create_airline('Thai Air International', airline_folder)
    create_airline('Transaero Airlines', airline_folder)
    create_airline('Turkish Airlines', airline_folder)
    create_airline('Ukraine International Airlines', airline_folder)
    create_airline('United', airline_folder)
    create_airline('US Airways', airline_folder)
    create_airline('Utair Aviation', airline_folder)
    create_airline('Vietnam Airlines', airline_folder)
    create_airline('Virgin America', airline_folder)
    create_airline('Virgin Atlantic', airline_folder)
    create_airline('Virgin Australia', airline_folder)
    create_airline('Vision Airlines', airline_folder)
    create_airline('Volaris', airline_folder)
    create_airline('WestJet', airline_folder)
    create_airline('Xiamen Airlines', airline_folder)
    create_airline('XL Airways', airline_folder)


def populate_countries(portal):
    # populate countries
    country_folder = portal['countries']
    create_country(
        'Australia',
        'https://www.timeanddate.com/worldclock/results.html?query=australia',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/australia',
        'https://travel.state.gov/content/passports/en/country/australia.html',
        country_folder,
    )
    create_country(
        'Austria',
        'https://www.timeanddate.com/worldclock/austria',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/austria',
        'https://travel.state.gov/content/passports/en/country/austria.html',
        country_folder,
    )
    create_country(
        'Belgium',
        'https://www.timeanddate.com/worldclock/belgium',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/belgium',
        'https://travel.state.gov/content/passports/en/country/belgium.html',
        country_folder,
    )
    create_country(
        'Belize',
        'https://www.timeanddate.com/worldclock/belize',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/belize',
        'https://travel.state.gov/content/passports/en/country/belize.html',
        country_folder,
    )
    create_country(
        'Bermuda',
        'https://www.timeanddate.com/worldclock/bermuda',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/bermuda',
        'https://travel.state.gov/content/passports/en/country/bermuda.html',
        country_folder,
    )
    create_country(
        'Canada',
        'https://www.timeanddate.com/worldclock/canada',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/canada',
        'https://travel.state.gov/content/passports/en/country/canada.html',
        country_folder,
    )
    create_country(
        'China',
        'https://www.timeanddate.com/worldclock/results.html?query=china',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/china',
        'https://travel.state.gov/content/passports/en/country/china.html',
        country_folder,
    )
    create_country(
        'Costa Rica',
        'https://www.timeanddate.com/worldclock/costa-rica',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/costa-rica',
        'https://travel.state.gov/content/passports/en/country/costa-rica.html',  # noqa
        country_folder,
    )
    create_country(
        'Czech Rep.',
        'https://www.timeanddate.com/worldclock/czech-republic',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/czech-republic',  # noqa
        'https://travel.state.gov/content/passports/en/country/czech-republic.html',  # noqa
        country_folder,
    )
    create_country(
        'France',
        'https://www.timeanddate.com/worldclock/france',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/france',
        'https://travel.state.gov/content/passports/en/country/france.html',
        country_folder,
    )
    create_country(
        'Germany',
        'https://www.timeanddate.com/worldclock/germany',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/germany',
        'https://travel.state.gov/content/passports/en/country/germany.html',
        country_folder,
    )
    create_country(
        'Greece',
        'https://www.timeanddate.com/worldclock/greece',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/greece',
        'https://travel.state.gov/content/passports/en/country/greece.html',
        country_folder,
    )
    create_country(
        'Honduras',
        'https://www.timeanddate.com/worldclock/honduras',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/honduras',
        'https://travel.state.gov/content/passports/en/country/honduras.html',
        country_folder,
    )
    create_country(
        'Hong Kong, China',
        'https://www.timeanddate.com/worldclock/hong-kong',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/hong-kong-sar',  # noqa
        'https://travel.state.gov/content/passports/en/country/hongkong.html',
        country_folder,
    )
    create_country(
        'Hungary',
        'https://www.timeanddate.com/worldclock/hungary',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/hungary',
        'https://travel.state.gov/content/passports/en/country/hungary.html',
        country_folder,
    )
    create_country(
        'India',
        'https://www.timeanddate.com/worldclock/india',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/india',
        'https://travel.state.gov/content/passports/en/country/india.html',
        country_folder,
    )
    create_country(
        'Ireland',
        'https://www.timeanddate.com/worldclock/ireland',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/ireland',
        'https://travel.state.gov/content/passports/en/country/ireland.html',
        country_folder,
    )
    create_country(
        'Italy',
        'https://www.timeanddate.com/worldclock/italy',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/italy',
        'https://travel.state.gov/content/passports/en/country/italy.html',
        country_folder,
    )
    create_country(
        'Jamaica',
        'https://www.timeanddate.com/worldclock/jamaica',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/jamaica',
        'https://travel.state.gov/content/passports/en/country/jamaica.html',
        country_folder,
    )
    create_country(
        'Japan',
        'https://www.timeanddate.com/worldclock/japan',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/japan',
        'https://travel.state.gov/content/passports/en/country/japan.html',
        country_folder,
    )
    create_country(
        'Kenya',
        'https://www.timeanddate.com/worldclock/kenya',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/kenya',
        'https://travel.state.gov/content/passports/en/country/kenya.html',
        country_folder,
    )
    create_country(
        'Korea, Rep.',
        'https://www.timeanddate.com/worldclock/south-korea',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/south-korea',
        'https://travel.state.gov/content/passports/en/country/korea-south.html',  # noqa
        country_folder,
    )
    create_country(
        'Malaysia',
        'https://www.timeanddate.com/worldclock/malaysia',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/malaysia',
        'https://travel.state.gov/content/passports/en/country/malaysia.html',
        country_folder,
    )
    create_country(
        'Netherlands',
        'https://www.timeanddate.com/worldclock/netherlands',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/netherlands',
        'https://travel.state.gov/content/passports/en/country/netherlands.html',  # noqa
        country_folder,
    )
    create_country(
        'New Zealand',
        'https://www.timeanddate.com/worldclock/new-zealand',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/new-zealand',
        'https://travel.state.gov/content/passports/en/country/new-zealand.html',  # noqa
        country_folder,
    )
    create_country(
        'Nicaragua',
        'https://www.timeanddate.com/worldclock/nicaragua',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/nicaragua',
        'https://travel.state.gov/content/passports/en/country/nicaragua.html',
        country_folder,
    )
    create_country(
        'Oman',
        'https://www.timeanddate.com/worldclock/oman',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/oman',
        'https://travel.state.gov/content/passports/en/country/oman.html',
        country_folder,
    )
    create_country(
        'Peru',
        'https://www.timeanddate.com/worldclock/peru',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/peru',
        'https://travel.state.gov/content/passports/en/country/peru.html',
        country_folder,
    )
    create_country(
        'Poland',
        'https://www.timeanddate.com/worldclock/poland',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/poland',
        'https://travel.state.gov/content/passports/en/country/poland.html',
        country_folder,
    )
    create_country(
        'Portugal',
        'https://www.timeanddate.com/worldclock/portugal',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/portugal',
        'https://travel.state.gov/content/passports/en/country/Portugal.html',
        country_folder,
    )
    create_country(
        'Puerto Rico',
        'https://www.timeanddate.com/worldclock/puerto-rico',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/puerto-rico',
        '',
        country_folder,
    )
    create_country(
        'Spain',
        'https://www.timeanddate.com/worldclock/spain',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/spain',
        'https://travel.state.gov/content/passports/en/country/spain.html',
        country_folder,
    )
    create_country(
        'Switzerland',
        'https://www.timeanddate.com/worldclock/switzerland',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/switzerland',
        'https://travel.state.gov/content/passports/en/country/switzerland-and-liechtenstein.html',  # noqa
        country_folder,
    )
    create_country(
        'Tanzania',
        'https://www.timeanddate.com/worldclock/tanzania',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/tanzania',
        'https://travel.state.gov/content/passports/en/country/tanzania.html',
        country_folder,
    )
    create_country(
        'Uganda',
        'https://www.timeanddate.com/worldclock/uganda',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/uganda',
        'https://travel.state.gov/content/passports/en/country/uganda.html',
        country_folder,
    )
    create_country(
        'United Kingdom',
        'https://www.timeanddate.com/worldclock/uk',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-kingdom',  # noqa
        'https://travel.state.gov/content/passports/en/country/united-kingdom.html',  # noqa
        country_folder,
    )
    create_country(
        'United States',
        'https://www.timeanddate.com/worldclock/usa',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-states',  # noqa
        '',
        country_folder,
    )
    create_country(
        'Virgin Islands (U.S.)',
        'https://www.timeanddate.com/worldclock/us-virgin',
        'https://wwwnc.cdc.gov/travel/destinations/traveler/none/usvirgin-islands',  # noqa
        '',
        country_folder,
    )


def create_airline(name, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIEAirline', id=id)
    if len(brains) < 1:
        api.content.create(type='OIEAirline', container=folder, title=name)


def create_year(name, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIECalendarYear', id=id)
    if len(brains) < 1:
        api.content.create(type='OIECalendarYear', container=folder,
                           title=name)


def create_partner(name, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIECooperatingPartner', id=id)
    if len(brains) < 1:
        api.content.create(type='OIECooperatingPartner', container=folder,
                           title=name)


def create_country(name, timezone_url, cdc_info_url, state_dept_info_url,
                   folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIECountry', id=id)
    if len(brains) < 1:
        api.content.create(type='OIECountry', container=folder, title=name)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
