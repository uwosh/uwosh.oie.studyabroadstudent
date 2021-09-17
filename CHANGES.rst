Changelog
=========


1.0.12 (2021-09-17)
-------------------

- Fix Participant permissions
- Get functioning ux for applying with login and register
- add my applications portal tab functionality
- bring portal tabs into code


1.0.11 (2021-09-13)
-------------------

- Discover programs view changes to simplify semantics and use css grid


1.0.10 (2021-09-13)
-------------------

- changes to allow unauthenticated users to view necessary info associated with,
  but not directly contained within discoverable programs (via a uid linking to another object)
- start using get_object_from_uid
- refactor discover programs form to fetch data from endpoint
- discover programs paging tweak
- various and multiple formatting changes
- upgrade step to reindex programs
- reset currentPage of discover programs form if out of bounds after updating filter


1.0.9 (2021-09-10)
------------------

- additional manager-role permission for associated program view content items
- with_manager_permissions util decorator


1.0.8 (2021-09-09)
------------------

- fix permissions for loading programsearch details while anonymous
- fix programview.pt to handle missing attributes


1.0.7 (2021-09-09)
------------------

- fix programsearch typo


1.0.6 (2021-09-09)
------------------

- change program_leader on discoverprograms to be a last name instead of UID
- remove pt reference to folder_listing for cooperatingpartnerview and reformat
- change default site title


1.0.5 (2021-09-08)
------------------

- Made permission changes for programs in discoverable state to be able to be viewed anonymously
- Upgrade step and create anonymous user for impersonator


1.0.4 (2021-08-27)
------------------

- Second deployment update
- added OIEHomePage to show /discover on root
- made changes to discover programs filtering and rewrote programsearch.js
- changes in some required fields and add STATES_FOR_DISPLAYING_PROGRAMS


1.0.0 (2021-08-06)
------------------

- Initial release.
  [tkimnguyen]
