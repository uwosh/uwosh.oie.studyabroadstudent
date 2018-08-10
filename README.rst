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

This is how to export data from the legacy site then import it into a new site:

On the legacy site:

- Using the Management Interface, e.g. http://localhost:8080/OIE/manage_main, navigate to portal_skins/custom and
  create a Script (Python) called `listApplicationIDs` containing the code in the file `listApplicationIDs.py`

- Run the Script (Python) `listApplicationIDs`

- Save the output to a local file with the `.py` Python filename extension, e.g. `listApplicationIDsoutput.py`

- Using the Management Interface, create a Script (Python) in portal_skins/custom called `extractApplication`
  containing the code in the file `extractApplication.py` and add `id` to its parameter list

On the new site:

- Run the script `extractApplicationsRemotely.py` and save its output to a file, like this:
  `bin/instance run extractApplicationsRemotely.py > extractoutput.out`; this will take hours (to extract 8600 student
  applications it took over 3.5 hours over the internet). You can override default values with `--http-ok=yes`,
  `--remote-user`, `--remote-password`, `--remote-server`.

- If `extractApplicationsRemotely.py` did not finish running and extracted only a subset of the IDs, you can rerun it
  like this to skip the IDs it had previously read:
  `bin/instance run ./src/uwosh/oie/studyabroadstudent/scripts/extractApplicationsRemotely.py --http-ok=yes --skip-ids=yes --id-file=extractoutput.out > newextractoutput.out`

- If you ran the script more than once and have more than one output file, combine all the output files into one file,
  e.g. `cat extractoutput.out newextractoutput.out > combinedextractoutput.out`

- Massage the output file to turn it into a Python file: `./pythonify_extract.sh extractoutput.out > extractoutput.py`

- Run the script `importApplications.py` to import the applications locally into the site, where the add-on must
  already be installed: `bin/instance run importApplications.py` (this took almost one hour on a MacBook Air). If there
  is a problem with the data, such as a bad birthdate year, you will be dropped into a PDB prompt where you can inspect
  the values and make any changes needed before continuing. By default the import will try to create applications in the
  folder 'applications' of the site 'OIE' but you can override those values with `--site-id=Plone`
  and `--folder-id=another-folder-id`. The argument `--skip-existing` tells the script to check first if there is
  already an existing application object with the same ID before creating one.

    (Pdb) l
    329  	        try:
    330  	            dateOfBirth=date(int((DateOfBirth_year is not None) and DateOfBirth_year or '1900'), month_values[((DateOfBirth_month is not None) and (DateOfBirth_month != '-- choose one --')) and DateOfBirth_month or 'January'], int(((DateOfBirth_day is not None) and (DateOfBirth_day != '-- choose one --') and DateOfBirth_day or 1)))
    331  	        except:
    332  	            import pdb;pdb.set_trace()
    333
    334  ->	        try:
    335  	            passportExpDate=date(int((PassportExpDate_year is not None and PassportExpDate_year is not '') and PassportExpDate_year or '1900'), month_values[(PassportExpDate_month == '-- choose one --' or PassportExpDate_month == '') and 'January' or PassportExpDate_month], int((PassportExpDate_day == '-- choose one --' or PassportExpDate_day == '') and 1 or PassportExpDate_day))
    336  	        except:
    337  	            import pdb;pdb.set_trace()
    338
    339  	        obj = api.content.create(
    (Pdb) DateOfBirth_year
    19991
    (Pdb) DateOfBirth_month
    'January'
    (Pdb) DateOfBirth_day
    '8'
    (Pdb) DateOfBirth_year=1991
    (Pdb) dateOfBirth=date(int((DateOfBirth_year is not None) and DateOfBirth_year or '1900'), month_values[((DateOfBirth_month is not None) and (DateOfBirth_month != '-- choose one --')) and DateOfBirth_month or 'January'], int(((DateOfBirth_day is not None) and (DateOfBirth_day != '-- choose one --') and DateOfBirth_day or 1)))
    (Pdb) dateOfBirth
    datetime.date(1991, 1, 8)
    (Pdb) id
    'oiestuapp_howlettj1287342001'
    (Pdb) c

Using the ID of the application that had the error, you can go to the site, browse to that application (it will be at a
URL like https://app.oie.uwosh.edu/Members/howlettj12/oiestuapp_howlettj1287342001) and edit and save it to correct the
data error and prevent this particular data error in future extracts and imports.

To verify the import, on the new site:

- Using the Management Interface, create a Script (Python) in portal_skins/custom called `extractApplication`
  containing the code in the file `extractApplication.py` and add `id` to its parameter list

- Create and run the script `extractApplicationsLocally.py` and save its output to a file, like this:
  `bin/instance run extractApplicationsLocally.py > extractlocallyoutput.out`

- Compare the contents of that file to that of the one you created remotely before, e.g.
  `diff extractoutput.out extractlocallyoutput.out`

Legacy Time Zones
-----------------

Since Plone 2.5, the time zones database has changed: the time zones 'GMT-5' and 'GMT-6' have since been renamed
'Etc/GMT+5' and 'Etc/GMT+6' (see https://community.plone.org/t/unknowntimezoneerror-pytz-quirks/4255/4 for why the sign
change). Some DateTime values in legacy data use the old time zone designations, which causes an error in the
unpickler() method in the file tzinfo.py, part of the pytz-2015.7-py2.7.egg. This error prevents viewing of legacy
(migrated) OIEStudentApplication objects.

For the moment, the only way to get around this error is to patch the unpickler() method in tzinfo.py and add the
following lines right after line 525 (the comment "Raises a KeyError if zone no longer exists, which should never
happen and would be a bug.")::

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
