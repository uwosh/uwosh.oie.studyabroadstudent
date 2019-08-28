# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser import edit


class ParticipantEditForm(edit.DefaultEditForm):
    # if role is Participant_Student, make sure they are the owner of this form
    def __call__(self):
        current_user = api.user.get_current()
        roles = api.user.get_roles(user=current_user)
        if 'Participant_Applicant' in roles:
            owner = self.context.getOwner()
            if not current_user.getId() == owner.getId():
                msg = "You cannot edit an OIE Participant Application which you do not own."  # noqa
                return msg
        return super(ParticipantEditForm, self).__call__()
