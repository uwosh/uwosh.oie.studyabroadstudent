from plone import api
from plone.dexterity.browser import add, edit
from Products.CMFPlone.resources import add_resource_on_request


class ParticipantEditForm(edit.DefaultEditForm):
    # if role is Participant_Student, make sure they are the owner of this form
    def __call__(self, *args, **kwargs):
        add_resource_on_request(self.request, 'untitled-js')
        current_user = api.user.get_current()
        roles = api.user.get_roles(user=current_user)
        if 'Participant_Applicant' in roles:
            owner = self.context.getOwner()
            if not current_user.getId() == owner.getId():
                msg = "You cannot edit an OIE Participant Application which you do not own."  # noqa
                return msg
        return super(ParticipantEditForm, self).__call__(*args, **kwargs)


class ParticipantAddForm(add.DefaultAddForm):
    portal_type = 'OIEStudyAbroadParticipant'

    def __call__(self, *args, **kw):
        add_resource_on_request(self.request, 'untitled-js')
        super(ParticipantAddForm, self).__call__(*args, **kw)
        # current_user = api.user.get_current()


class ParticipantAddView(add.DefaultAddView):
    form = ParticipantAddForm
