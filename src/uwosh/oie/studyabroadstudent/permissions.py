from Products.CMFCore import permissions as CMFCorePermissions
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles


study_abroad_roles = [
    'Access arbitrary user session data',
    'Access contents information',
    'Access inactive portal content',
    'Access session data',
    'Add portal content',
    'Add portal folders',
    'Add portal member',
    'Allow sendto',
    'Change local roles',
    'Content rules: Manage rules',
    'Copy or Move',
    'Delete comments',
    'Delete objects',
    'Delete own comments',
    'Edit comments',
    'FTP access',
    'List folder contents',
    'List portal members',
    'List undoable changes',
    'Mail forgotten password',
    'Manage properties',
    'Modify portal content',
    'Modify view template',
    'Reply to item',
    'Request review',
    'Review comments',
    'Review portal content',
    'ZCatalog',
    'Set own password',
    'Set own properties',
    'Undo changes',
    'Use mailhost services',
    'Use version control',
    'View',
    'View Groups',
    'View management screens',
    'WebDAV Lock items',
    'WebDAV Unlock items',
    'WebDAV access',
]

security = ModuleSecurityInfo('uwosh.oie.studyabroadstudent')
for role in study_abroad_roles:
    security.declarePublic(role)
    setDefaultRoles(role, ())