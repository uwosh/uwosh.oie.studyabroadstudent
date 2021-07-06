from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IMarkupSchema
from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.utils import safe_unicode
from zope.component import getUtility

import logging
import six

OIE_PREFIX = 'oiestudyabroadstudent'

def migrate_control_panel_files_from_ascii_to_bytes(context):
    """zope.schema.ASCII inherits from NativeString.
    With Python 2 this is the same as Bytes, but with Python 3 not:
    you get a WrongType error when saving the site-controlpanel.
    """
    from plone.registry import field
    from plone.registry import Record

    registry = getUtility(IRegistry)
    for file_title in [
        'state_of_wisconsin_need_based_travel_grant_form',
        'special_student_form_for_undergraduate_admissions',
        'disciplinary_clearance_form',
        'uwo_logo', 
    ]:
        record_key = f'{OIE_PREFIX}.{file_title}'
        record = registry.records[record_key]
        if not isinstance(record.field, field.ASCII):
            # All is well.
            registry.registerInterface(ISiteSchema, prefix=OIE_PREFIX)
            continue
        # Keep the original value so we can restore it.
        original_value = record.value
        # Delete the bad record.
        del registry.records[record_key]
        # Make sure the site schema is fully registered again.
        # This should recreate the field correctly.
        registry.registerInterface(ISiteSchema, prefix=OIE_PREFIX)
        if original_value is None:
            # Nothing left to do.
            continue
        new_record = registry.records[record_key]
        if isinstance(original_value, six.text_type):
            # fromUnicode could be called from Text in Python 3.
            new_value = new_record.field.fromUnicode(original_value)
        elif isinstance(original_value, bytes):
            # Unlikely, but let's be careful.
            new_value = original_value
        else:
            # Anything else is broken.
            continue
        # Save the new value.
        new_record.value = new_value
        logger.info(f'Replaced {record_key} ASCII (native string) field with Bytes field.')
