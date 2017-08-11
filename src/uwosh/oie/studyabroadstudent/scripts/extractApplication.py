# Prints out the attribute values of the OIEStudentApplication object having the specified ID.
# Invoked remotely via XML-RPC
#
# Using the Management Interface, save the contents of this script as a Script (Python) in the portal_skins/custom of the site.

import DateTime
wtool = context.portal_workflow
catalog = context.portal_catalog
results = catalog.searchResults(portal_type='OIEStudentApplication', id=id)
for r in results:
    o = r.getObject()
    (created, modified, getDepartureDate, getReturnDate, getOrientationDate1, getOrientationDate2, getConflictDate, getCompletionDate) = (o.created(), o.modified(), o.getDepartureDate(), o.getReturnDate(), o.getOrientationDate1(), o.getOrientationDate2(), o.getConflictDate(), o.getCompletionDate())
    if created is not None and created != '':
        created = created.ISO8601()
    if modified is not None and modified != '':
        modified = modified.ISO8601()
    if getDepartureDate is not None and getDepartureDate != '':
        getDepartureDate = getDepartureDate.ISO8601()
    if getReturnDate is not None and getReturnDate != '':
        getReturnDate = getReturnDate.ISO8601()
    if getOrientationDate1 is not None and getOrientationDate1 != '':
        getOrientationDate1 = getOrientationDate1.ISO8601()
    if getOrientationDate2 is not None and getOrientationDate2 != '':
        getOrientationDate2 = getOrientationDate2.ISO8601()
    if getConflictDate is not None and getConflictDate != '':
        getConflictDate = getConflictDate.ISO8601()
    if getCompletionDate is not None and getCompletionDate != '':
        getCompletionDate = getCompletionDate.ISO8601()
    getProgramName = o.getProgramName()
    if getProgramName is not None and getProgramName != '':
        getProgramName = getProgramName.Title()
    review_history = wtool.getInfoFor(o, 'review_history', [])
    for h in review_history:
        h['time'] = h['time'].ISO8601()
    print [o.id, r.review_state, o.Creators(), created, modified, o.getStudentID(), o.getFirstName(), o.getMiddleName(), o.getLastName(), o.getEmail(), o.getLocalAddr1(), o.getLocalAddr2(), o.getLocalCity(), o.getLocalState(), o.getLocalZip(), o.getLocalCountry(), o.getLocalPhone(), o.getMobilePhone(), o.getHomeAddr1(), o.getHomeAddr2(), o.getHomeCity(), o.getHomeState(), o.getHomeZip(), o.getHomeCountry(), o.getHomePhone(), o.getCitizenship(), o.getCitizenshipOther(), o.getStateResidency(), o.getStateResidencyOther(), o.getDateOfBirth_year(), o.getDateOfBirth_month(), o.getDateOfBirth_day(), o.getPlaceOfBirth(), o.getGender(), o.getMarriageStatus(), o.getEthnicity(), o.getEthnicityOther(), o.getPassportName(), o.getPassportNumber(), o.getPassportIssueOffice(), o.getPassportExpDate_year(), o.getPassportExpDate_month(), o.getPassportExpDate_day(), o.getQuestionAcadCareerPlan(), o.getQuestionLangCulturalSkills(), o.getQuestionPrevTravel(), o.getQuestionWorkExp(), o.getQuestionEuroBizTravSem(), o.getQuestionStuExchComp(), o.getDoctorLastname(), o.getDoctorFirstname(), o.getDoctorPhone(), o.getMedicalInsuranceCompany(), o.getMedicalPolicyHolder(), o.getMedicalPolicyGroupNumber(), o.getFoodAllergies(), o.getHasDifficultyWalking(), o.getMaxWalkingDistance(), o.getMedicalReadStatement(), o.getMedicalHealthProblems(), o.getMedicalHealthProblems_takenMedication(), o.getMedicalHealthProblems_medications(), o.getMedicalHealthProblems_stable(), o.getMedicalHealthProblems_underCare(), o.getMedicalHealthProblems_whatCondition(), o.getMedicalHealthProblems_willingToPrescribe(), o.getMedicalHealthProblems_additionalInfo(), o.getMedicalMentalProblems(), o.getMedicalMentalProblems_takenMedication(), o.getMedicalMentalProblems_medications(), o.getMedicalMentalProblems_currentDose(), o.getMedicalMentalProblems_stable(), o.getMedicalMentalProblems_underCare(), o.getMedicalMentalProblems_condition(), o.getMedicalMentalProblems_enoughMedication(), o.getMedicalMentalProblems_additionalInfo(), o.getMedicalRegistered(), o.getMedicalRegistered_office(), o.getMedicalRegistered_accommodations(), o.getMedicalAccessOK(), o.getSmokingPreferred(), o.getIsVegetarian(), o.getAdditionalNeeds(), o.getEmerg1name(), o.getEmerg1addr1(), o.getEmerg1addr2(), o.getEmerg1city(), o.getEmerg1state(), o.getEmerg1zip(), o.getEmerg1country(), o.getEmerg1homePhone(), o.getEmerg1workPhone(), o.getEmerg1mobilePhone(), o.getEmerg1email(), o.getEmerg2name(), o.getEmerg2addr1(), o.getEmerg2addr2(), o.getEmerg2city(), o.getEmerg2state(), o.getEmerg2zip(), o.getEmerg2country(), o.getEmerg2homePhone(), o.getEmerg2workPhone(), o.getEmerg2mobilePhone(), o.getEmerg2email(), o.getEmerg3name(), o.getEmerg3addr1(), o.getEmerg3addr2(), o.getEmerg3city(), o.getEmerg3state(), o.getEmerg3zip(), o.getEmerg3country(), o.getEmerg3homePhone(), o.getEmerg3workPhone(), o.getEmerg3mobilePhone(), o.getEmerg3email(), getProgramName, o.getProgramYear(), o.getProgramSemester(), o.getStudentType(), o.getUniversityEnrolled(), o.getGraduationMonth(), o.getGraduationYear(), o.getCumulativeGPA(), o.getMajor1(), o.getMajor2(), o.getMinor1(), o.getMinor2(), o.getEmphasis1(), o.getEmphasis2(), o.getWillTakeBus(), o.getWillFlyWithGroup(), getDepartureDate, getReturnDate, o.getAgreeToCosts(), getOrientationDate1, o.getOrientationHours1(), getOrientationDate2, o.getOrientationHours2(), o.getNumberOfGuests(), o.getOrientationConflict(), getConflictDate, o.getSubject1(), o.getCourse1(), o.getCredits1(), o.getSubject2(), o.getCourse2(), o.getCredits2(), o.getSubject3(), o.getCredits3(), o.getSubject4(), o.getCourse4(), o.getCredits4(), o.getSubject5(), o.getCourse5(), o.getCredits5(), o.getSubject6(), o.getCourse6(), o.getCredits6(), o.getReadSyllabus(), o.getEnrolledIS333(), o.getApplyForAid(), o.getHoldApplication(), o.getFinancialAidGranted(), o.getRoomType(), o.getRoommateName1(), o.getRoommateName2(), o.getQuestionExpectations(), o.getAwareOfAllMaterials(), o.getUWOshkoshRelease(), o.getCertification(), o.getSeatNumber(), getCompletionDate, o.getApplicationIsComplete(), o.getApplicationFeeOK(), o.getUWSystemStatementOK(), o.getUWOshkoshStatementOK(), o.getWithdrawalRefund(), o.getTranscriptsOK(), o.getProgramSpecificMaterialsRequired(), o.getProgramSpecificMaterialsOK(), o.getSpecialStudentFormRequired(), o.getSpecialStudentFormOK(), o.getCreditOverloadFormRequired(), o.getCreditOverloadFormOK(), o.getMedicalOK(), o.getMedicalForm(), o.getPassportOK(), o.getMetPassportDeadline(), o.getProgramSpecificMaterialsRequiredStepIII(), o.getProgramSpecificMaterialsOKStepIII(), o.getAttendedOrientation(), o.getCisiDates(), o.getCisiNumberOfMonths(), o.getProgramFee(), o.getTuitionPayment(), o.getDepositOnTime(), o.getPayment2OnTime(), o.getApplicationFeeRefund(), o.getForeignCourse1(), o.getForeignCourse2(), o.getForeignCourse3(), o.getForeignCourse4(), o.getForeignCourse5(), o.getForeignCourse6(), o.getPapersOK(), o.getNoMoreMaterials(), o.getProgramMaterials(), o.getProgramFee2(), review_history]
return printed