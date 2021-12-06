from plone import api
from plone.dexterity.browser import add, edit
from Products.CMFPlone.resources import add_resource_on_request
from uwosh.oie.studyabroadstudent.browser.views import ParticipantPermissionsMixin

class ParticipantEditForm(ParticipantPermissionsMixin, edit.DefaultEditForm):
    _participant_form_mode = 'input'

    # if role is Participant_Applicant, make sure they are the owner of this form
    def __call__(self, *args, **kwargs):
        add_resource_on_request(self.request, 'untitled-js')
        current_user = api.user.get_current()
        roles = api.user.get_roles(user=current_user)
        if 'Participant_Applicant' in roles:
            owner = self.context.getOwner()
            if not current_user.getId() == owner.getId():
                msg = 'You cannot edit an OIE Participant Application which you do not own.'
                return msg
        return super().__call__(*args, **kwargs)

    @property
    def label(self):
        first_name = self.context.firstName
        last_name = self.context.lastName
        program = self.context.programName
        courses = self.context.courses
        formatted_courses = ", ".join([f"{c}" for c in courses])
        return (f'Edit {first_name} {last_name} | Program: {program} | Course(s): {formatted_courses}')


class ParticipantAddForm(add.DefaultAddForm):
    portal_type = 'OIEStudyAbroadParticipant'

    def __call__(self, *args, **kw):
        add_resource_on_request(self.request, 'untitled-js')
        super().__call__(*args, **kw)
        # current_user = api.user.get_current()


class ParticipantAddView(add.DefaultAddView):
    form = ParticipantAddForm
