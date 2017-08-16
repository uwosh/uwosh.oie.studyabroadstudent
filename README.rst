.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
uwosh.oie.studyabroadstudent
==============================================================================

Content types, workflows, and utilities for the Office of
International Education at the University of Wisconsin Oshkosh (http://uwosh.edu/oie).


Features
--------

- supports the submission, approval, publication, and management of study away programs
- supports the submission, approval, publication, and management of student applications for programs
- scripts to export legacy data from the first OIE workflow site (circa 2006, Archetypes-based, Plone 2.5) and import them to Plone 5 (Dexterity-based)



Examples
--------

This add-on can be seen in action at the following sites:
- (none yet)


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.


Translations
------------

None (yet)


Installation
------------

Install uwosh.oie.studyabroadstudent by adding it to your buildout::

    [buildout]

    ...

    eggs =
        uwosh.oie.studyabroadstudent


and then running ``bin/buildout``


Export / Import
---------------

Quick notes on how to export from the legacy site:

On the legacy site:

- using the Management Interface, e.g. http://localhost:8080/OIE/manage_main, navigate to portal_skins/custom and create a Script (Python) called `listApplicationIDs` containing the code in the file `listApplicationIDs.py` 
- run the Script (Python) `listApplicationIDs`
- save the output to a local file with the `.py` Python filename extension, e.g. `listApplicationIDsoutput.py`
- using the Management Interface, create a Script (Python) in portal_skins/custom called `extractApplication` containing the code in the file `extractApplication.py` and add `id` to its parameter list

On the new site:

- run the script `extractApplicationsRemotely.py` and save its output to a file, like this: `bin/instance run extractApplicationsRemotely.py > extractoutput.out`; this will take hours (to extract 8600 student applications it took over 3.5 hours over the internet)
- tweak that output file to create Python code: `./pythonify_extract.sh extractoutput.out > extractoutput.py`
- run the script `importApplications.py` to import the applications locally, like this: `bin/instance run importApplications.py` (this took almost one hour on a MacBook Air)

To verify the import, on the new site:

- using the Management Interface, create a Script (Python) in portal_skins/custom called `extractApplication` containing the code in the file `extractApplication.py` and add `id` to its parameter list
- create and run the script `extractApplicationsLocally.py` and save its output to a file, like this: `bin/instance run extractApplicationsLocally.py > extractlocallyoutput.out`
- compare the contents of that file to that of the one you created remotely before, e.g. `diff extractoutput.out extractlocallyoutput.out`

Legacy Time Zones
-----------------

Since Plone 2.5, the time zones database has changed: the time zones 'GMT-5' and 'GMT-6' have since been renamed 'Etc/GMT+5' and 'Etc/GMT+6' (see https://community.plone.org/t/unknowntimezoneerror-pytz-quirks/4255/4 for why the sign change). Some DateTime values in legacy data use the old time zone designations, which causes an error in the unpickler() method in the file tzinfo.py, part of the pytz-2015.7-py2.7.egg. This error prevents viewing of legacy (migrated) OIEStudentApplication objects. 

For the moment, the only way to get around this error is to patch the unpickler() method in tzinfo.py and add the following lines right after line 525 (the comment "Raises a KeyError if zone no longer exists, which should never happen and would be a bug.")::

    # Raises a KeyError if zone no longer exists, which should never happen
    # and would be a bug.
    newzone = zone
    if zone.find('GMT-') != -1:
        newzone = zone.replace('GMT-','Etc/GMT+')
    if zone.find('GMT+') != -1:
        import pdb;pdb.set_trace()
        newzone = zone.replace('GMT+','Etc/GMT-')
    if zone == 'GMT':
        newzone = 'Etc/GMT'
    if zone != newzone:
        logger.warn('fixing nonexistent timezone %s to %s' % (zone, newzone))
        zone = newzone
    tz = pytz.timezone(zone)


Contribute
----------

- Issue Tracker: https://github.com/uwosh/uwosh.oie.studyabroadstudent/issues
- Source Code: https://github.com/uwosh/uwosh.oie.studyabroadstudent
- Documentation: https://github.com/uwosh/uwosh.oie.studyabroadstudent/docs


Credits
-------

The project was paid for by the Office of International Education at the University of Wisconsin Oshkosh (http://uwosh.edu/oie).

Implementation by T. Kim Nguyen at Wildcard Corp. (https://wildcardcorp.com).


Support
-------

If you are having issues, please let us know.



License
-------

The project is licensed under the GPLv2.
