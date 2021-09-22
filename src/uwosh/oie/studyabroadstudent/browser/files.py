from plone import api
from plone.namedfile.browser import Download
from plone.api.exc import InvalidParameterError
from zope.publisher.interfaces import NotFound
from ZODB.POSException import POSKeyError
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedFile


class DownloadablePDF(Download):
    def __init__(self, context, request):
        '''prevents super.__init__ from stripping filename,
        which can cause some issues in certain situations
        '''
        filename = getattr(self, 'filename', 'file.ext')
        super().__init__(context, request)
        self.filename = filename

    def get_form(self):
        form_key = getattr(self, 'form_key', 'fake_key')
        registry_key = f'oiestudyabroadstudent.{ form_key }'
        try:
            return api.portal.get_registry_record(registry_key)
        except InvalidParameterError:
            return None

    @property
    def NotFound():
        return NotFound(
            self,
            self.fieldname,
            self.request,
        )

    def _getFile(self):
        form = self.get_form()
        if form is not None:
            try:
                filename, data = b64decode_file(form)
                self.filename = filename
                return NamedFile(
                    contentType='application/pdf',
                    filename=filename,
                    data=data,
                )
            except Exception:
                raise self.NotFound
        else:
            raise self.NotFound

    def __call__(self):
        try:
            file = self._getFile()
            self.set_headers(file)
            return super().__call__()
        except (POSKeyError, SystemError):
            raise self.NotFound

class DisciplinaryClearanceFormDownload(DownloadablePDF):
    filename = 'DisciplinaryClearanceForm'
    form_key = 'disciplinary_clearance_form'


class NeedBasedTravelGrantFormDownload(DownloadablePDF):
    filename = 'StateOfWisconsinNeedBasedTravelGrantForm'
    form_key = 'state_of_wisconsin_need_based_travel_grant_form'


class SpecialStudentUndergraduateAdmissionsFormDownload(DownloadablePDF):
    filename = 'SpecialStudentFormForUndergraduateAdmissions'
    form_key = 'special_student_form_for_undergraduate_admissions'
