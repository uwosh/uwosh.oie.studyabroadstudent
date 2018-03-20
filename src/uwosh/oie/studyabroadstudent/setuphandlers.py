# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from plone.app.textfield.value import RichTextValue


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
    # populate countries
    portal = api.portal.get()
    # if needed, add countries folder and populate it
    portal_items = portal.items()
    portal_ids = [id for id, obj in portal_items]
    if 'countries' not in portal_ids:
        country_folder = api.content.create(type='Folder', title='Countries', id='countries', container=portal)
        api.content.create(type='OIECountry', container=country_folder, title='Australia', timezone_url='https://www.timeanddate.com/worldclock/results.html?query=australia', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/australia', state_dept_info_url='https://travel.state.gov/content/passports/en/country/australia.html')
        api.content.create(type='OIECountry', container=country_folder, title='Austria', timezone_url='https://www.timeanddate.com/worldclock/austria', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/austria', state_dept_info_url='https://travel.state.gov/content/passports/en/country/austria.html')
        api.content.create(type='OIECountry', container=country_folder, title='Belgium', timezone_url='https://www.timeanddate.com/worldclock/belgium', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/belgium', state_dept_info_url='https://travel.state.gov/content/passports/en/country/belgium.html')
        api.content.create(type='OIECountry', container=country_folder, title='Belize', timezone_url='https://www.timeanddate.com/worldclock/belize', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/belize', state_dept_info_url='https://travel.state.gov/content/passports/en/country/belize.html')
        api.content.create(type='OIECountry', container=country_folder, title='Bermuda', timezone_url='https://www.timeanddate.com/worldclock/bermuda', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/bermuda', state_dept_info_url='https://travel.state.gov/content/passports/en/country/bermuda.html')
        api.content.create(type='OIECountry', container=country_folder, title='Canada', timezone_url='https://www.timeanddate.com/worldclock/canada', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/canada', state_dept_info_url='https://travel.state.gov/content/passports/en/country/canada.html')
        api.content.create(type='OIECountry', container=country_folder, title='China', timezone_url='https://www.timeanddate.com/worldclock/results.html?query=china', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/china', state_dept_info_url='https://travel.state.gov/content/passports/en/country/china.html')
        api.content.create(type='OIECountry', container=country_folder, title='Costa Rica', timezone_url='https://www.timeanddate.com/worldclock/costa-rica', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/costa-rica', state_dept_info_url='https://travel.state.gov/content/passports/en/country/costa-rica.html')
        api.content.create(type='OIECountry', container=country_folder, title='Czech Rep.', timezone_url='https://www.timeanddate.com/worldclock/czech-republic', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/czech-republic', state_dept_info_url='https://travel.state.gov/content/passports/en/country/czech-republic.html')
        api.content.create(type='OIECountry', container=country_folder, title='France', timezone_url='https://www.timeanddate.com/worldclock/france', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/france', state_dept_info_url='https://travel.state.gov/content/passports/en/country/france.html')
        api.content.create(type='OIECountry', container=country_folder, title='Germany', timezone_url='https://www.timeanddate.com/worldclock/germany', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/germany', state_dept_info_url='https://travel.state.gov/content/passports/en/country/germany.html')
        api.content.create(type='OIECountry', container=country_folder, title='Greece', timezone_url='https://www.timeanddate.com/worldclock/greece', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/greece', state_dept_info_url='https://travel.state.gov/content/passports/en/country/greece.html')
        api.content.create(type='OIECountry', container=country_folder, title='Honduras', timezone_url='https://www.timeanddate.com/worldclock/honduras', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/honduras', state_dept_info_url='https://travel.state.gov/content/passports/en/country/honduras.html')
        api.content.create(type='OIECountry', container=country_folder, title='Hong Kong, China', timezone_url='https://www.timeanddate.com/worldclock/hong-kong', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/hong-kong-sar', state_dept_info_url='https://travel.state.gov/content/passports/en/country/hongkong.html')
        api.content.create(type='OIECountry', container=country_folder, title='Hungary', timezone_url='https://www.timeanddate.com/worldclock/hungary', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/hungary', state_dept_info_url='https://travel.state.gov/content/passports/en/country/hungary.html')
        api.content.create(type='OIECountry', container=country_folder, title='India', timezone_url='https://www.timeanddate.com/worldclock/india', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/india', state_dept_info_url='https://travel.state.gov/content/passports/en/country/india.html')
        api.content.create(type='OIECountry', container=country_folder, title='Ireland', timezone_url='https://www.timeanddate.com/worldclock/ireland', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/ireland', state_dept_info_url='https://travel.state.gov/content/passports/en/country/ireland.html')
        api.content.create(type='OIECountry', container=country_folder, title='Italy', timezone_url='https://www.timeanddate.com/worldclock/italy', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/italy', state_dept_info_url='https://travel.state.gov/content/passports/en/country/italy.html')
        api.content.create(type='OIECountry', container=country_folder, title='Jamaica', timezone_url='https://www.timeanddate.com/worldclock/jamaica', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/jamaica', state_dept_info_url='https://travel.state.gov/content/passports/en/country/jamaica.html')
        api.content.create(type='OIECountry', container=country_folder, title='Japan', timezone_url='https://www.timeanddate.com/worldclock/japan', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/japan', state_dept_info_url='https://travel.state.gov/content/passports/en/country/japan.html')
        api.content.create(type='OIECountry', container=country_folder, title='Kenya', timezone_url='https://www.timeanddate.com/worldclock/kenya', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/kenya', state_dept_info_url='https://travel.state.gov/content/passports/en/country/kenya.html')
        api.content.create(type='OIECountry', container=country_folder, title='Korea, Rep.', timezone_url='https://www.timeanddate.com/worldclock/south-korea', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/south-korea', state_dept_info_url='https://travel.state.gov/content/passports/en/country/korea-south.html')
        api.content.create(type='OIECountry', container=country_folder, title='Malaysia', timezone_url='https://www.timeanddate.com/worldclock/malaysia', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/malaysia', state_dept_info_url='https://travel.state.gov/content/passports/en/country/malaysia.html')
        api.content.create(type='OIECountry', container=country_folder, title='Netherlands', timezone_url='https://www.timeanddate.com/worldclock/netherlands', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/netherlands', state_dept_info_url='https://travel.state.gov/content/passports/en/country/netherlands.html')
        api.content.create(type='OIECountry', container=country_folder, title='New Zealand', timezone_url='https://www.timeanddate.com/worldclock/new-zealand', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/new-zealand', state_dept_info_url='https://travel.state.gov/content/passports/en/country/new-zealand.html')
        api.content.create(type='OIECountry', container=country_folder, title='Nicaragua', timezone_url='https://www.timeanddate.com/worldclock/nicaragua', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/nicaragua', state_dept_info_url='https://travel.state.gov/content/passports/en/country/nicaragua.html')
        api.content.create(type='OIECountry', container=country_folder, title='Oman', timezone_url='https://www.timeanddate.com/worldclock/oman', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/oman', state_dept_info_url='https://travel.state.gov/content/passports/en/country/oman.html')
        api.content.create(type='OIECountry', container=country_folder, title='Peru', timezone_url='https://www.timeanddate.com/worldclock/peru', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/peru', state_dept_info_url='https://travel.state.gov/content/passports/en/country/peru.html')
        api.content.create(type='OIECountry', container=country_folder, title='Poland', timezone_url='https://www.timeanddate.com/worldclock/poland', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/poland', state_dept_info_url='https://travel.state.gov/content/passports/en/country/poland.html')
        api.content.create(type='OIECountry', container=country_folder, title='Portugal', timezone_url='https://www.timeanddate.com/worldclock/portugal', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/portugal', state_dept_info_url='https://travel.state.gov/content/passports/en/country/Portugal.html')
        api.content.create(type='OIECountry', container=country_folder, title='Puerto Rico', timezone_url='https://www.timeanddate.com/worldclock/puerto-rico', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/puerto-rico', state_dept_info_url='')
        api.content.create(type='OIECountry', container=country_folder, title='Spain', timezone_url='https://www.timeanddate.com/worldclock/spain', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/spain', state_dept_info_url='https://travel.state.gov/content/passports/en/country/spain.html')
        api.content.create(type='OIECountry', container=country_folder, title='Switzerland', timezone_url='https://www.timeanddate.com/worldclock/switzerland', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/switzerland', state_dept_info_url='https://travel.state.gov/content/passports/en/country/switzerland-and-liechtenstein.html')
        api.content.create(type='OIECountry', container=country_folder, title='Tanzania', timezone_url='https://www.timeanddate.com/worldclock/tanzania', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/tanzania', state_dept_info_url='https://travel.state.gov/content/passports/en/country/tanzania.html')
        api.content.create(type='OIECountry', container=country_folder, title='Uganda', timezone_url='https://www.timeanddate.com/worldclock/uganda', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/uganda', state_dept_info_url='https://travel.state.gov/content/passports/en/country/uganda.html')
        api.content.create(type='OIECountry', container=country_folder, title='United Kingdom', timezone_url='https://www.timeanddate.com/worldclock/uk', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-kingdom', state_dept_info_url='https://travel.state.gov/content/passports/en/country/united-kingdom.html')
        api.content.create(type='OIECountry', container=country_folder, title='United States', timezone_url='https://www.timeanddate.com/worldclock/usa', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/united-states', state_dept_info_url='')
        api.content.create(type='OIECountry', container=country_folder, title='Virgin Islands (U.S.)', timezone_url='https://www.timeanddate.com/worldclock/us-virgin', cdc_info_url='https://wwwnc.cdc.gov/travel/destinations/traveler/none/usvirgin-islands', state_dept_info_url='')
    else:
        country_folder = portal['countries']
    constrain_types(country_folder, ['OIECountry'])

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

    # add folders and restrict addable types
    create_toplevel_folder(portal, portal_ids, 'Applications', 'applications', ['OIEStudyAbroadStudentApplication'])
    create_toplevel_folder(portal, portal_ids, 'Participants', 'participants', ['OIEStudyAbroadParticipant'])
    create_toplevel_folder(portal, portal_ids, 'Programs', 'programs', ['OIEStudyAbroadProgram'])
    create_toplevel_folder(portal, portal_ids, 'People', 'people', ['OIEContact', 'OIELiaison', 'OIEProgramLeader'])
    create_toplevel_folder(portal, portal_ids, 'Partners', 'partners', ['OIECooperatingPartner'])
    create_toplevel_folder(portal, portal_ids, 'Years', 'years', ['OIECalendarYear'])
    create_toplevel_folder(portal, portal_ids, 'Airlines', 'airlines', ['OIEAirline'])
    create_toplevel_folder(portal, portal_ids, 'Forms', 'forms', ['File'])

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
    brains = api.content.find(portal_type='OIEAirline', sortable_title=name.lower())
    if len(brains) < 1:
        api.content.create(type='OIEAirline', container=folder, title=name)


def create_partner(name, folder):
    brains = api.content.find(portal_type='OIECooperatingPartner', sortable_title=name.lower())
    if len(brains) < 1:
        api.content.create(type='OIECooperatingPartner', container=folder, title=name)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
