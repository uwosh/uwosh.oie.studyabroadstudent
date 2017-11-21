def application_created(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    o.reindexObject()

def application_modified(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)

def program_created(o, event):
    program_code = (o.calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    o.program_code = program_code
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    o.reindexObject()

def program_modified(o, event):
    program_code = (o.calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    o.program_code = program_code

def contact_created(o, event):
    o.title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    o.reindexObject()

def contact_modified(o, event):
    o.title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)


