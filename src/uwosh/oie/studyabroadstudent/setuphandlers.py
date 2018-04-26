# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone.app.textfield.value import RichTextValue
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


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


def create_toplevel_folder(portal, portal_ids, title, id, ftis):
    if id not in portal_ids:
        folder = api.content.create(type='Folder', title=title, id=id, container=portal)
    else:
        folder = portal[id]
    constrain_types(folder, ftis)


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    portal_items = portal.items()
    portal_ids = [id for id, obj in portal_items]

    # add folders and restrict addable types
    create_toplevel_folder(portal, portal_ids, 'Legacy Applications', 'legacy-applications', ['OIEStudyAbroadStudentApplication'])
    create_toplevel_folder(portal, portal_ids, 'Countries', 'countries', ['OIECountry'])
    create_toplevel_folder(portal, portal_ids, 'Participants', 'participants', ['OIEStudyAbroadParticipant'])
    create_toplevel_folder(portal, portal_ids, 'Programs', 'programs', ['OIEStudyAbroadProgram'])
    create_toplevel_folder(portal, portal_ids, 'People', 'people', ['OIEContact', 'OIELiaison', 'OIEProgramLeader'])
    create_toplevel_folder(portal, portal_ids, 'Partners', 'partners', ['OIECooperatingPartner'])
    create_toplevel_folder(portal, portal_ids, 'Years', 'years', ['OIECalendarYear'])
    create_toplevel_folder(portal, portal_ids, 'Airlines', 'airlines', ['OIEAirline'])
    create_toplevel_folder(portal, portal_ids, 'Forms', 'forms', ['File'])

    # populate countries
    country_folder = portal['countries']
    create_country('Australia', 'https://www.timeanddate.com/worldclock/results.html?query=australia', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/australia', 'https://travel.state.gov/content/passports/en/country/australia.html', country_folder)
    create_country('Austria', 'https://www.timeanddate.com/worldclock/austria', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/austria', 'https://travel.state.gov/content/passports/en/country/austria.html', country_folder)
    create_country('Belgium', 'https://www.timeanddate.com/worldclock/belgium', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/belgium', 'https://travel.state.gov/content/passports/en/country/belgium.html', country_folder)
    create_country('Belize', 'https://www.timeanddate.com/worldclock/belize', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/belize', 'https://travel.state.gov/content/passports/en/country/belize.html', country_folder)
    create_country('Bermuda', 'https://www.timeanddate.com/worldclock/bermuda', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/bermuda', 'https://travel.state.gov/content/passports/en/country/bermuda.html', country_folder)
    create_country('Canada', 'https://www.timeanddate.com/worldclock/canada', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/canada', 'https://travel.state.gov/content/passports/en/country/canada.html', country_folder)
    create_country('China', 'https://www.timeanddate.com/worldclock/results.html?query=china', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/china', 'https://travel.state.gov/content/passports/en/country/china.html', country_folder)
    create_country('Costa Rica', 'https://www.timeanddate.com/worldclock/costa-rica', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/costa-rica', 'https://travel.state.gov/content/passports/en/country/costa-rica.html', country_folder)
    create_country('Czech Rep.', 'https://www.timeanddate.com/worldclock/czech-republic', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/czech-republic', 'https://travel.state.gov/content/passports/en/country/czech-republic.html', country_folder)
    create_country('France', 'https://www.timeanddate.com/worldclock/france', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/france', 'https://travel.state.gov/content/passports/en/country/france.html', country_folder)
    create_country('Germany', 'https://www.timeanddate.com/worldclock/germany', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/germany', 'https://travel.state.gov/content/passports/en/country/germany.html', country_folder)
    create_country('Greece', 'https://www.timeanddate.com/worldclock/greece', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/greece', 'https://travel.state.gov/content/passports/en/country/greece.html', country_folder)
    create_country('Honduras', 'https://www.timeanddate.com/worldclock/honduras', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/honduras', 'https://travel.state.gov/content/passports/en/country/honduras.html', country_folder)
    create_country('Hong Kong, China', 'https://www.timeanddate.com/worldclock/hong-kong', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/hong-kong-sar', 'https://travel.state.gov/content/passports/en/country/hongkong.html', country_folder)
    create_country('Hungary', 'https://www.timeanddate.com/worldclock/hungary', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/hungary', 'https://travel.state.gov/content/passports/en/country/hungary.html', country_folder)
    create_country('India', 'https://www.timeanddate.com/worldclock/india', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/india', 'https://travel.state.gov/content/passports/en/country/india.html', country_folder)
    create_country('Ireland', 'https://www.timeanddate.com/worldclock/ireland', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/ireland', 'https://travel.state.gov/content/passports/en/country/ireland.html', country_folder)
    create_country('Italy', 'https://www.timeanddate.com/worldclock/italy', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/italy', 'https://travel.state.gov/content/passports/en/country/italy.html', country_folder)
    create_country('Jamaica', 'https://www.timeanddate.com/worldclock/jamaica', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/jamaica', 'https://travel.state.gov/content/passports/en/country/jamaica.html', country_folder)
    create_country('Japan', 'https://www.timeanddate.com/worldclock/japan', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/japan', 'https://travel.state.gov/content/passports/en/country/japan.html', country_folder)
    create_country('Kenya', 'https://www.timeanddate.com/worldclock/kenya', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/kenya', 'https://travel.state.gov/content/passports/en/country/kenya.html', country_folder)
    create_country('Korea, Rep.', 'https://www.timeanddate.com/worldclock/south-korea', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/south-korea', 'https://travel.state.gov/content/passports/en/country/korea-south.html', country_folder)
    create_country('Malaysia', 'https://www.timeanddate.com/worldclock/malaysia', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/malaysia', 'https://travel.state.gov/content/passports/en/country/malaysia.html', country_folder)
    create_country('Netherlands', 'https://www.timeanddate.com/worldclock/netherlands', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/netherlands', 'https://travel.state.gov/content/passports/en/country/netherlands.html', country_folder)
    create_country('New Zealand', 'https://www.timeanddate.com/worldclock/new-zealand', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/new-zealand', 'https://travel.state.gov/content/passports/en/country/new-zealand.html', country_folder)
    create_country('Nicaragua', 'https://www.timeanddate.com/worldclock/nicaragua', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/nicaragua', 'https://travel.state.gov/content/passports/en/country/nicaragua.html', country_folder)
    create_country('Oman', 'https://www.timeanddate.com/worldclock/oman', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/oman', 'https://travel.state.gov/content/passports/en/country/oman.html', country_folder)
    create_country('Peru', 'https://www.timeanddate.com/worldclock/peru', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/peru', 'https://travel.state.gov/content/passports/en/country/peru.html', country_folder)
    create_country('Poland', 'https://www.timeanddate.com/worldclock/poland', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/poland', 'https://travel.state.gov/content/passports/en/country/poland.html', country_folder)
    create_country('Portugal', 'https://www.timeanddate.com/worldclock/portugal', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/portugal', 'https://travel.state.gov/content/passports/en/country/Portugal.html', country_folder)
    create_country('Puerto Rico', 'https://www.timeanddate.com/worldclock/puerto-rico', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/puerto-rico', '', country_folder)
    create_country('Spain', 'https://www.timeanddate.com/worldclock/spain', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/spain', 'https://travel.state.gov/content/passports/en/country/spain.html', country_folder)
    create_country('Switzerland', 'https://www.timeanddate.com/worldclock/switzerland', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/switzerland', 'https://travel.state.gov/content/passports/en/country/switzerland-and-liechtenstein.html', country_folder)
    create_country('Tanzania', 'https://www.timeanddate.com/worldclock/tanzania', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/tanzania', 'https://travel.state.gov/content/passports/en/country/tanzania.html', country_folder)
    create_country('Uganda', 'https://www.timeanddate.com/worldclock/uganda', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/uganda', 'https://travel.state.gov/content/passports/en/country/uganda.html', country_folder)
    create_country('United Kingdom', 'https://www.timeanddate.com/worldclock/uk', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-kingdom', 'https://travel.state.gov/content/passports/en/country/united-kingdom.html', country_folder)
    create_country('United States', 'https://www.timeanddate.com/worldclock/usa', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-states', '', country_folder)
    create_country('Virgin Islands (U.S.)', 'https://www.timeanddate.com/worldclock/us-virgin', 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/usvirgin-islands', '', country_folder)

    # retract and hide Users
    if 'Members' in portal_ids:
        user_folder = portal['Members']
        wf_state = api.content.get_state(user_folder)
        if wf_state != 'private':
            api.content.transition(obj=user_folder, transition='retract')
        user_folder.exclude_from_nav = True

    # change front page text
    if 'front-page' in portal_ids:
        frontpage = portal['front-page']
        frontpage.title = 'Welcome to OIE'
        frontpage.description = 'You have reached the UW Oshkosh Office of International Education'
        frontpage.text = RichTextValue(
            u'Lorem ipsum',
            'text/plain',
            'text/html',
        )

    # add Link to OIE control panel
    if 'oie-settings' not in portal_ids:
        link = api.content.create(type='Link', title='OIE Settings', id='oie-settings', container=portal)
        link.remoteUrl = '${navigation_root_url}/@@oiestudyabroadstudent-controlpanel'

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

    # populate Cooperating Partners content items
    partner_folder = portal['partners']
    create_partner('Academic Programs International (API)', partner_folder)
    create_partner('Accent International', partner_folder)
    create_partner('American Institute for Foreign Study (AIFS)', partner_folder)
    create_partner('AMIDEAST', partner_folder)
    create_partner('Amizade Ltd.', partner_folder)
    create_partner('Anglo Educational Services', partner_folder)
    create_partner('Anytour International', partner_folder)
    create_partner('Beyond Borders International / Minds Abroad', partner_folder)
    create_partner('Cultural Experiences Abroad (CEA)', partner_folder)
    create_partner('Customized Educational Programs Abroad (CEPA)', partner_folder)
    create_partner('China Sense', partner_folder)
    create_partner('Council on International Educational Exchange (CIEE)', partner_folder)
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

    # TODO add tests for content type creation and reading


def create_airline(name, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIEAirline', id=id)
    if len(brains) < 1:
        api.content.create(type='OIEAirline', container=folder, title=name)


def create_partner(name, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIECooperatingPartner', id=id)
    if len(brains) < 1:
        api.content.create(type='OIECooperatingPartner', container=folder, title=name)


def create_country(name, timezone_url, cdc_info_url, state_dept_info_url, folder):
    util = queryUtility(IIDNormalizer)
    id = util.normalize(name)
    brains = api.content.find(portal_type='OIECountry', id=id)
    if len(brains) < 1:
        api.content.create(type='OIECountry', container=folder, title=name)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
