from plone import api

def application_created(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    o.reindexObject()

def application_modified(o, event):
    o.title = '%s %s %s %s %s' % (o.firstName, o.middleName, o.lastName, o.programName, o.programYear)

def program_created(o, event):
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    o.program_code = program_code
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    # TODO copy all the dates
    for d in ['first_day_of_spring_semester_classes', 'last_day_of_spring_semester_classes',
              'first_day_of_spring_interim_classes', 'last_day_of_spring_interim_classes',
              'official_spring_graduation_date', 'first_day_of_summer_i_classes', 'last_day_of_summer_i_classes',
              'first_day_of_summer_ii_classes', 'last_day_of_summer_ii_classes',
              'official_summer_graduation_date', 'first_day_of_fall_semester_classes',
              'last_day_of_fall_semester_classes', 'first_day_of_winter_interim_classes',
              'last_day_of_winter_interim_classes', 'official_fall_graduation_date',
              'spring_interim_summer_fall_semester_participant_orientation_deadline',
              'spring_interim_summer_fall_semester_in_person_orientation',
              'winter_interim_spring_semester_participant_orientation_deadline',
              'winter_interim_spring_semester_in_person_orientation',
              'spring_interim_summer_fall_semester_payment_deadline_1', 'spring_interim_payment_deadline_2',
              'sunmmer_payment_deadline_2', 'fall_semester_payment_deadline_2',
              'winter_interim_spring_payment_deadline_1', 'winter_interim_spring_payment_deadline_2']:
        setattr(o, d, getattr(calendar_year_obj, d))
    o.reindexObject()

def program_modified(o, event):
    calendar_year_obj = api.content.get(UID=o.calendar_year)
    calendar_year = calendar_year_obj.title
    program_code = (calendar_year)[2:4] + (o.term)[0] + (o.college_or_unit)[0]
    for c in o.countries:
        program_code += c[0:3].upper()
    o.program_code = program_code
    # TODO copy all the dates
    for d in ['first_day_of_spring_semester_classes', 'last_day_of_spring_semester_classes',
              'first_day_of_spring_interim_classes', 'last_day_of_spring_interim_classes',
              'official_spring_graduation_date', 'first_day_of_summer_i_classes', 'last_day_of_summer_i_classes',
              'first_day_of_summer_ii_classes', 'last_day_of_summer_ii_classes',
              'official_summer_graduation_date', 'first_day_of_fall_semester_classes',
              'last_day_of_fall_semester_classes', 'first_day_of_winter_interim_classes',
              'last_day_of_winter_interim_classes', 'official_fall_graduation_date',
              'spring_interim_summer_fall_semester_participant_orientation_deadline',
              'spring_interim_summer_fall_semester_in_person_orientation',
              'winter_interim_spring_semester_participant_orientation_deadline',
              'winter_interim_spring_semester_in_person_orientation',
              'spring_interim_summer_fall_semester_payment_deadline_1', 'spring_interim_payment_deadline_2',
              'sunmmer_payment_deadline_2', 'fall_semester_payment_deadline_2',
              'winter_interim_spring_payment_deadline_1', 'winter_interim_spring_payment_deadline_2']:
        setattr(o, d, getattr(calendar_year_obj, d))

def contact_created(o, event):
    o.title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)
    new_id = o.title.lower().replace(' ', '-')
    o.id = str(new_id)
    o.reindexObject()

def contact_modified(o, event):
    o.title = '%s %s %s' % (o.first_name, o.middle_name, o.last_name)

