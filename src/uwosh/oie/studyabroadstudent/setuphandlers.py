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
    create_toplevel_folder(portal, portal_ids, 'Providers', 'providers', ['OIEProvider'])

    # add Link to OIE control panel
    if 'oie-settings' not in portal_ids:
        link = api.content.create(type='Link', title='OIE Settings', id='oie-settings', container=portal)
        link.remoteUrl = '${navigation_root_url}/@@oiestudyabroadstudent-controlpanel'

    # TODO add tests for content type creation and reading


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
