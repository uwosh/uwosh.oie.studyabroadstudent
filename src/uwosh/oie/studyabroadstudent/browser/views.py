from Acquisition import aq_inner
from uwosh.oie.studyabroadstudent.interfaces import IOIEStudyAbroadStudentApplication
from plone import api
# from Products.Five import BrowserView


# class ApplicationView(BrowserView):

#     def sessions(self):
#         """Return a catalog search result of sessions to show."""

#         context = aq_inner(self.context)
#         catalog = api.portal.get_tool(name='portal_catalog')

#         return catalog(
#             object_provides=ISession.__identifier__,
#             path='/'.join(context.getPhysicalPath()),
#             sort_on='sortable_title')

from plone.dexterity.browser.view import DefaultView

class ApplicationView(DefaultView):

    pass
