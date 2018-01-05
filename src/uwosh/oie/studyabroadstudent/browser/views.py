from Acquisition import aq_inner
from uwosh.oie.studyabroadstudent.interfaces.studyabroadstudentapplication import IOIEStudyAbroadStudentApplication
from plone import api
from plone.dexterity.browser.view import DefaultView
#from plone.app.contenttypes.browser.folder import FolderView
from Products.CMFPlone.PloneBatch import Batch
from zope.component import getMultiAdapter
from plone.app.contenttypes import _

class ApplicationView(DefaultView):
    pass

class ProgramView(DefaultView):

    def __init__(self, context, request):
        super(DefaultView, self).__init__(context, request)

        self.plone_view = getMultiAdapter(
            (context, request), name=u"plone")
        self.portal_state = getMultiAdapter(
            (context, request), name=u"plone_portal_state")
        self.pas_member = getMultiAdapter(
            (context, request), name=u"pas_member")

        self.text_class = None

        limit_display = getattr(self.request, 'limit_display', None)
        limit_display = int(limit_display) if limit_display is not None else 20
        b_size = getattr(self.request, 'b_size', None)
        self.b_size = int(b_size) if b_size is not None else limit_display
        b_start = getattr(self.request, 'b_start', None)
        self.b_start = int(b_start) if b_start is not None else 0

    def results(self, **kwargs):
        """Return a content listing based result set with contents of the
        folder.

        :param **kwargs: Any keyword argument, which can be used for catalog
                         queries.
        :type  **kwargs: keyword argument

        :returns: plone.app.contentlisting based result set.
        :rtype: ``plone.app.contentlisting.interfaces.IContentListing`` based
                sequence.
        """
        # Extra filter
        kwargs.update(self.request.get('contentFilter', {}))
        if 'object_provides' not in kwargs:  # object_provides is more specific
            kwargs.setdefault('portal_type', self.friendly_types)
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        listing = aq_inner(self.context).restrictedTraverse(
            '@@folderListing', None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results

    def batch(self):
        batch = Batch(
            self.results(),
            size=self.b_size,
            start=self.b_start,
            orphan=1
        )
        return batch

    @property
    def friendly_types(self):
        return self.portal_state.friendly_types()

    @property
    def no_items_message(self):
        return _(
            'description_no_items_in_folder',
            default=u"There are currently no items in this folder."
        )


class CooperatingPartnerView(DefaultView):
    def primary_contact(self):
        contact = self.context.primary_contact.to_object
        return '<a href="%s">%s, %s, %s, %s, %s, %s</a>' % (
            contact.absolute_url(),
            contact.title,
            contact.job_title,
            contact.telephone,
            contact.mobile,
            contact.email,
            contact.other,
        )

class ContactView(DefaultView):
    pass
