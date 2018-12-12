# -*- coding: utf-8 -*-
#
# useful for printing out the field values of one or more objects you
# specify by ID
#
# parameter list: idstr
#
# pass in a value like this:
# oiestuapp_youngi441411072925,oiestuapp_volpr331411074761
#
# the separator is the comma
#
# do not use spaces or other characters (they will be considered part of an ID)
#
# a constructed URL would look like this:
# https://app.oie.uwosh.edu/listApplicationsByID?idstr=oiestuapp_youngi441411072925%2Coiestuapp_volpr331411074761
#
# use this URL to get all the application IDs (must be logged in as a Manager)
# https://app.oie.uwosh.edu/printApplicationsByIDs

wtool = context.portal_workflow  # noqa
catalog = context.portal_catalog  # noqa

ids = []
acc = ''
for c in idstr:  # noqa
    if c == ',':
        ids.append(acc)
        acc = ''
    else:
        acc += c
if acc != '':
    ids.append(acc)
    acc = ''
print '# len of ids is ', len(ids)  # noqa
print 'ids = ', ids  # noqa

new_style = False  # set to False if looking at legacy site

print 'application_data = ['  # noqa
for id in ids:  # noqa
    results = catalog.searchResults(portal_type='OIEStudentApplication', id=id)  # noqa
    if len(results) == 0:
        results = catalog.searchResults(portal_type='OIEStudyAbroadStudentApplication', id=id)  # noqa
        new_style = True
    if len(results) > 1:
        print 'too many catalog query results ({0}) for ID {1}'.format(len(results), id)  # noqa
        return printed  # noqa
    if len(results) != 1:
        print 'no catalog query results for ID {0}'.format(id)  # noqa
        return printed  # noqa
    r = results[0]
    o = r.getObject()
    if not new_style:
        (
          created,
          modified,
          getDepartureDate,
          getReturnDate,
          getOrientationDate1,
          getOrientationDate2,
          getConflictDate,
          getCompletionDate,
        ) = (
          o.created(),
          o.modified(),
          o.getDepartureDate(),
          o.getReturnDate(),
          o.getOrientationDate1(),
          o.getOrientationDate2(),
          o.getConflictDate(),
          o.getCompletionDate(),
        )
    else:
        (
          created,
          modified,
          getDepartureDate,
          getReturnDate,
          getOrientationDate1,
          getOrientationDate2,
          getConflictDate,
          getCompletionDate,
        ) = (
          o.created(),
          o.modified(),
          o.departureDate,
          o.returnDate,
          o.orientationDate1,
          o.orientationDate2,
          o.conflictDate,
          o.completionDate,
        )
    if created is not None and created != '':
        created = (
          getattr(created, 'ISO8601', None) and
          created.ISO8601() or
          created
        )
    if modified is not None and modified != '':
        modified = (
          getattr(modified, 'ISO8601', None) and
          modified.ISO8601() or
          modified
        )
    if getDepartureDate is not None and getDepartureDate != '':
        getDepartureDate = (
          getattr(getDepartureDate, 'ISO8601', None) and
          getDepartureDate.ISO8601() or
          getDepartureDate
        )
    if getReturnDate is not None and getReturnDate != '':
        getReturnDate = (
          getattr(getReturnDate, 'ISO8601', None) and
          getReturnDate.ISO8601() or
          getReturnDate
        )
    if getOrientationDate1 is not None and getOrientationDate1 != '':
        getOrientationDate1 = (
          getattr(getOrientationDate1, 'ISO8601', None) and
          getOrientationDate1.ISO8601() or
          getOrientationDate1
        )
    if getOrientationDate2 is not None and getOrientationDate2 != '':
        getOrientationDate2 = (
          getattr(getOrientationDate2, 'ISO8601', None) and
          getOrientationDate2.ISO8601() or
          getOrientationDate2
        )
    if getConflictDate is not None and getConflictDate != '':
        getConflictDate = (
          getattr(getConflictDate, 'ISO8601', None) and
          getConflictDate.ISO8601() or
          getConflictDate
        )
    if getCompletionDate is not None and getCompletionDate != '':
        getCompletionDate = (
          getattr(getCompletionDate, 'ISO8601', None) and
          getCompletionDate.ISO8601() or
          getCompletionDate
        )
    getProgramName = (
      getattr(o, 'getProgramName', None) and
      o.getProgramName() or
      o.programName
    )
    if getProgramName is not None and getProgramName != '':
        getProgramName = (
          getattr(getProgramName, 'Title', None) and
          getProgramName.Title() or
          getProgramName
        )
    review_history = wtool.getInfoFor(o, 'review_history', [])  # noqa
    for h in review_history:
        h['time'] = h['time'].ISO8601()
    if not new_style:
        print [o.id, r.review_state, o.Creators(), created, modified,  # noqa
               o.getStudentID(), o.getFirstName(), o.getMiddleName(),
               o.getLastName(), o.getEmail(), o.getLocalAddr1(),
               o.getLocalAddr2(), o.getLocalCity(), o.getLocalState(),
               o.getLocalZip(), o.getLocalCountry(), o.getLocalPhone(),
               o.getMobilePhone(), o.getHomeAddr1(), o.getHomeAddr2(),
               o.getHomeCity(), o.getHomeState(), o.getHomeZip(),
               o.getHomeCountry(), o.getHomePhone(), o.getCitizenship(),
               o.getCitizenshipOther(), o.getStateResidency(),
               o.getStateResidencyOther(), o.getDateOfBirth_year(),
               o.getDateOfBirth_month(), o.getDateOfBirth_day(),
               o.getPlaceOfBirth(), o.getGender(), o.getMarriageStatus(),
               o.getEthnicity(), o.getEthnicityOther(), o.getPassportName(),
               o.getPassportNumber(), o.getPassportIssueOffice(),
               o.getPassportExpDate_year(), o.getPassportExpDate_month(),
               o.getPassportExpDate_day(), o.getQuestionAcadCareerPlan(),
               o.getQuestionLangCulturalSkills(), o.getQuestionPrevTravel(),
               o.getQuestionWorkExp(), o.getQuestionEuroBizTravSem(),
               o.getQuestionStuExchComp(), o.getDoctorLastname(),
               o.getDoctorFirstname(), o.getDoctorPhone(),
               o.getMedicalInsuranceCompany(), o.getMedicalPolicyHolder(),
               o.getMedicalPolicyGroupNumber(), o.getFoodAllergies(),
               o.getHasDifficultyWalking(), o.getMaxWalkingDistance(),
               o.getMedicalReadStatement(), o.getMedicalHealthProblems(),
               o.getMedicalHealthProblems_takenMedication(),
               o.getMedicalHealthProblems_medications(),
               o.getMedicalHealthProblems_stable(),
               o.getMedicalHealthProblems_underCare(),
               o.getMedicalHealthProblems_whatCondition(),
               o.getMedicalHealthProblems_willingToPrescribe(),
               o.getMedicalHealthProblems_additionalInfo(),
               o.getMedicalMentalProblems(),
               o.getMedicalMentalProblems_takenMedication(),
               o.getMedicalMentalProblems_medications(),
               o.getMedicalMentalProblems_currentDose(),
               o.getMedicalMentalProblems_stable(),
               o.getMedicalMentalProblems_underCare(),
               o.getMedicalMentalProblems_condition(),
               o.getMedicalMentalProblems_enoughMedication(),
               o.getMedicalMentalProblems_additionalInfo(),
               o.getMedicalRegistered(), o.getMedicalRegistered_office(),
               o.getMedicalRegistered_accommodations(),
               o.getMedicalAccessOK(), o.getSmokingPreferred(),
               o.getIsVegetarian(), o.getAdditionalNeeds(),
               o.getEmerg1name(), o.getEmerg1addr1(), o.getEmerg1addr2(),
               o.getEmerg1city(), o.getEmerg1state(), o.getEmerg1zip(),
               o.getEmerg1country(), o.getEmerg1homePhone(),
               o.getEmerg1workPhone(), o.getEmerg1mobilePhone(),
               o.getEmerg1email(), o.getEmerg2name(), o.getEmerg2addr1(),
               o.getEmerg2addr2(), o.getEmerg2city(), o.getEmerg2state(),
               o.getEmerg2zip(), o.getEmerg2country(),
               o.getEmerg2homePhone(), o.getEmerg2workPhone(),
               o.getEmerg2mobilePhone(), o.getEmerg2email(),
               o.getEmerg3name(), o.getEmerg3addr1(), o.getEmerg3addr2(),
               o.getEmerg3city(), o.getEmerg3state(), o.getEmerg3zip(),
               o.getEmerg3country(), o.getEmerg3homePhone(),
               o.getEmerg3workPhone(), o.getEmerg3mobilePhone(),
               o.getEmerg3email(), getProgramName, o.getProgramYear(),
               o.getProgramSemester(), o.getStudentType(),
               o.getUniversityEnrolled(), o.getGraduationMonth(),
               o.getGraduationYear(), o.getCumulativeGPA(), o.getMajor1(),
               o.getMajor2(), o.getMinor1(), o.getMinor2(), o.getEmphasis1(),
               o.getEmphasis2(), o.getWillTakeBus(), o.getWillFlyWithGroup(),
               getDepartureDate, getReturnDate, o.getAgreeToCosts(),
               getOrientationDate1, o.getOrientationHours1(),
               getOrientationDate2, o.getOrientationHours2(),
               o.getNumberOfGuests(), o.getOrientationConflict(),
               getConflictDate, o.getSubject1(), o.getCourse1(),
               o.getCredits1(), o.getSubject2(), o.getCourse2(),
               o.getCredits2(), o.getSubject3(), o.getCredits3(),
               o.getSubject4(), o.getCourse4(), o.getCredits4(),
               o.getSubject5(), o.getCourse5(), o.getCredits5(),
               o.getSubject6(), o.getCourse6(), o.getCredits6(),
               o.getReadSyllabus(), o.getEnrolledIS333(), o.getApplyForAid(),
               o.getHoldApplication(), o.getFinancialAidGranted(),
               o.getRoomType(), o.getRoommateName1(), o.getRoommateName2(),
               o.getQuestionExpectations(), o.getAwareOfAllMaterials(),
               o.getUWOshkoshRelease(), o.getCertification(),
               o.getSeatNumber(), getCompletionDate,
               o.getApplicationIsComplete(), o.getApplicationFeeOK(),
               o.getUWSystemStatementOK(), o.getUWOshkoshStatementOK(),
               o.getWithdrawalRefund(), o.getTranscriptsOK(),
               o.getProgramSpecificMaterialsRequired(),
               o.getProgramSpecificMaterialsOK(),
               o.getSpecialStudentFormRequired(),
               o.getSpecialStudentFormOK(),
               o.getCreditOverloadFormRequired(),
               o.getCreditOverloadFormOK(), o.getMedicalOK(),
               o.getMedicalForm(), o.getPassportOK(),
               o.getMetPassportDeadline(),
               o.getProgramSpecificMaterialsRequiredStepIII(),
               o.getProgramSpecificMaterialsOKStepIII(),
               o.getAttendedOrientation(), o.getCisiDates(),
               o.getCisiNumberOfMonths(), o.getProgramFee(),
               o.getTuitionPayment(), o.getDepositOnTime(),
               o.getPayment2OnTime(), o.getApplicationFeeRefund(),
               o.getForeignCourse1(), o.getForeignCourse2(),
               o.getForeignCourse3(), o.getForeignCourse4(),
               o.getForeignCourse5(), o.getForeignCourse6(), o.getPapersOK(),
               o.getNoMoreMaterials(), o.getProgramMaterials(),
               o.getProgramFee2(), review_history]
    else:
        print [o.id, r.review_state, o.listCreators(), created,  # noqa
               modified, o.studentID, o.firstName, o.middleName, o.lastName,
               o.email, o.localAddr1, o.localAddr2, o.localCity,
               o.localState, o.localZip, o.localCountry, o.localPhone,
               o.mobilePhone, o.homeAddr1, o.homeAddr2, o.homeCity,
               o.homeState, o.homeZip, o.homeCountry, o.homePhone,
               o.citizenship, o.citizenshipOther, o.stateResidency,
               o.stateResidencyOther, o.dateOfBirth_year,
               o.dateOfBirth_month, o.dateOfBirth_day, o.placeOfBirth,
               o.gender, o.marriageStatus, o.ethnicity, o.ethnicityOther,
               o.passportName, o.passportNumber, o.passportIssueOffice,
               o.passportExpDate, o.passportExpDate, o.passportExpDate,
               o.questionAcadCareerPlan, o.questionLangCulturalSkills,
               o.questionPrevTravel, o.questionWorkExp,
               o.questionEuroBizTravSem, o.questionStuExchComp,
               o.doctorLastname, o.doctorFirstname, o.doctorPhone,
               o.medicalInsuranceCompany, o.medicalPolicyHolder,
               o.medicalPolicyGroupNumber, o.foodAllergies,
               o.hasDifficultyWalking, o.maxWalkingDistance,
               o.medicalReadStatement, o.medicalHealthProblems,
               o.medicalHealthProblems_takenMedication,
               o.medicalHealthProblems_medications,
               o.medicalHealthProblems_stable,
               o.medicalHealthProblems_underCare,
               o.medicalHealthProblems_whatCondition,
               o.medicalHealthProblems_willingToPrescribe,
               o.medicalHealthProblems_additionalInfo,
               o.medicalMentalProblems,
               o.medicalMentalProblems_takenMedication,
               o.medicalMentalProblems_medications,
               o.medicalMentalProblems_currentDose,
               o.medicalMentalProblems_stable,
               o.medicalMentalProblems_underCare,
               o.medicalMentalProblems_condition,
               o.medicalMentalProblems_enoughMedication,
               o.medicalMentalProblems_additionalInfo, o.medicalRegistered,
               o.medicalRegistered_office,
               o.medicalRegistered_accommodations, o.medicalAccessOK,
               o.smokingPreferred, o.isVegetarian, o.additionalNeeds,
               o.emerg1name, o.emerg1addr1, o.emerg1addr2, o.emerg1city,
               o.emerg1state, o.emerg1zip, o.emerg1country,
               o.emerg1homePhone, o.emerg1workPhone, o.emerg1mobilePhone,
               o.emerg1email, o.emerg2name, o.emerg2addr1, o.emerg2addr2,
               o.emerg2city, o.emerg2state, o.emerg2zip, o.emerg2country,
               o.emerg2homePhone, o.emerg2workPhone, o.emerg2mobilePhone,
               o.emerg2email, o.emerg3name, o.emerg3addr1, o.emerg3addr2,
               o.emerg3city, o.emerg3state, o.emerg3zip, o.emerg3country,
               o.emerg3homePhone, o.emerg3workPhone, o.emerg3mobilePhone,
               o.emerg3email, getProgramName, o.programYear,
               o.programSemester, o.studentType, o.universityEnrolled,
               o.graduationMonth, o.graduationYear, o.cumulativeGPA,
               o.major1, o.major2, o.minor1, o.minor2, o.emphasis1,
               o.emphasis2, o.willTakeBus, o.willFlyWithGroup,
               getDepartureDate, getReturnDate, o.agreeToCosts,
               getOrientationDate1, o.orientationHours1, getOrientationDate2,
               o.orientationHours2, o.numberOfGuests, o.orientationConflict,
               getConflictDate, o.subject1, o.course1, o.credits1,
               o.subject2, o.course2, o.credits2, o.subject3, o.credits3,
               o.subject4, o.course4, o.credits4, o.subject5, o.course5,
               o.credits5, o.subject6, o.course6, o.credits6, o.readSyllabus,
               o.enrolledIS333, o.applyForAid, o.holdApplication,
               o.financialAidGranted, o.roomType, o.roommateName1,
               o.roommateName2, o.questionExpectations,
               o.awareOfAllMaterials, o.UWOshkoshRelease, o.certification,
               o.seatNumber, getCompletionDate, o.applicationIsComplete,
               o.applicationFeeOK, o.UWSystemStatementOK,
               o.UWOshkoshStatementOK, o.withdrawalRefund, o.transcriptsOK,
               o.programSpecificMaterialsRequired,
               o.programSpecificMaterialsOK, o.specialStudentFormRequired,
               o.specialStudentFormOK, o.creditOverloadFormRequired,
               o.creditOverloadFormOK, o.medicalOK, o.medicalForm,
               o.passportOK, o.metPassportDeadline,
               o.programSpecificMaterialsRequiredStepIII,
               o.programSpecificMaterialsOKStepIII, o.attendedOrientation,
               o.cisiDates, o.cisiNumberOfMonths, o.programFee,
               o.tuitionPayment, o.depositOnTime, o.payment2OnTime,
               o.applicationFeeRefund, o.foreignCourse1, o.foreignCourse2,
               o.foreignCourse3, o.foreignCourse4, o.foreignCourse5,
               o.foreignCourse6, o.papersOK, o.noMoreMaterials,
               o.programMaterials, o.programFee2, review_history]
    print ','  # noqa
print ']'  # noqa
return printed  # noqa
