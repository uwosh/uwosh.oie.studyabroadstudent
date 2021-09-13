from plone.app.uuid.utils import uuidToObject
from plone import api


def get_object_from_uid(uid='wont_be_found'):
    one = uuidToObject(uid)
    return (
        one
        if one
        else api.content.get(UID=uid)
    )
