#! /Users/kim/PloneBuilds/Plone-5.0.4-unified-clean/zinstance/bin/python
#
# - 2017-05-20 read ISO8601 dates, workflow state, and all workflow transitions
#
# expects the extractoutput.py file or symlink to be in the folder
# /opt/Plone/zinstance/src/uwosh.oie.studyabroadstudent/src/uwosh/oie/studyabroadstudent

# invoke like this:
# bin/instance run importApplications.py

from datetime import datetime, date
import DateTime
from plone import api
from zope.component.hooks import setSite, getSite
import uwosh.oie.studyabroadstudent
import argparse
import transaction

from uwosh.oie.studyabroadstudent.extractoutput import app_data

MAX_COUNT = 100000 # stop after this many records

counter = 0
site_id = 'OIE'
folder_id = 'applications'
workflow_id = 'OIEStudentApplicationWorkflow'
PORTAL_TYPE = 'OIEStudyAbroadStudentApplication'

parser = argparse.ArgumentParser(
    description='...')
parser.add_argument('--site-id', dest='site_id', default='OIE')
parser.add_argument('--folder-id', dest='folder_id', default='applications')
args, _ = parser.parse_known_args()

# Sets the current site as the active site
setSite(app[site_id])
site = getSite()

# ensure folder exists 
toplevel_items = site.items() 
if 'applications' not in [id for id, obj in toplevel_items]:
    folder = api.content.create(
        container=site,
        type='Folder',
        id=folder_id,
        title='Applications',
    )

# Enable the context manager to switch the user
with api.env.adopt_user(username="admin"):
    # You're now posing as admin!
    #portal.restrictedTraverse("manage_propertiesForm")

    wtool = site.portal_workflow
    folder = app.unrestrictedTraverse("%s/%s" % (site_id, folder_id))

    for values in app_data:
        (id,
         review_state,
         Creators,
         created,
         modified,
         StudentID,
         FirstName,
         MiddleName,
         LastName,
         Email,
         LocalAddr1,
         LocalAddr2,
         LocalCity,
         LocalState,
         LocalZip,
         LocalCountry,
         LocalPhone,
         MobilePhone,
         HomeAddr1,
         HomeAddr2,
         HomeCity,
         HomeState,
         HomeZip,
         HomeCountry,
         HomePhone,
         Citizenship,
         CitizenshipOther,
         StateResidency,
         StateResidencyOther,
         DateOfBirth_year,
         DateOfBirth_month,
         DateOfBirth_day,
         PlaceOfBirth,
         Gender,
         MarriageStatus,
         Ethnicity,
         EthnicityOther,
         PassportName,
         PassportNumber,
         PassportIssueOffice,
         PassportExpDate_year,
         PassportExpDate_month,
         PassportExpDate_day,
         QuestionAcadCareerPlan,
         QuestionLangCulturalSkills,
         QuestionPrevTravel,
         QuestionWorkExp,
         QuestionEuroBizTravSem,
         QuestionStuExchComp,
         DoctorLastname,
         DoctorFirstname,
         DoctorPhone,
         MedicalInsuranceCompany,
         MedicalPolicyHolder,
         MedicalPolicyGroupNumber,
         FoodAllergies,
         HasDifficultyWalking,
         MaxWalkingDistance,
         MedicalReadStatement,
         MedicalHealthProblems,
         MedicalHealthProblems_takenMedication,
         MedicalHealthProblems_medications,
         MedicalHealthProblems_stable,
         MedicalHealthProblems_underCare,
         MedicalHealthProblems_whatCondition,
         MedicalHealthProblems_willingToPrescribe,
         MedicalHealthProblems_additionalInfo,
         MedicalMentalProblems,
         MedicalMentalProblems_takenMedication,
         MedicalMentalProblems_medications,
         MedicalMentalProblems_currentDose,
         MedicalMentalProblems_stable,
         MedicalMentalProblems_underCare,
         MedicalMentalProblems_condition,
         MedicalMentalProblems_enoughMedication,
         MedicalMentalProblems_additionalInfo,
         MedicalRegistered,
         MedicalRegistered_office,
         MedicalRegistered_accommodations,
         MedicalAccessOK,
         SmokingPreferred,
         IsVegetarian,
         AdditionalNeeds,
         Emerg1name,
         Emerg1addr1,
         Emerg1addr2,
         Emerg1city,
         Emerg1state,
         Emerg1zip,
         Emerg1country,
         Emerg1homePhone,
         Emerg1workPhone,
         Emerg1mobilePhone,
         Emerg1email,
         Emerg2name,
         Emerg2addr1,
         Emerg2addr2,
         Emerg2city,
         Emerg2state,
         Emerg2zip,
         Emerg2country,
         Emerg2homePhone,
         Emerg2workPhone,
         Emerg2mobilePhone,
         Emerg2email,
         Emerg3name,
         Emerg3addr1,
         Emerg3addr2,
         Emerg3city,
         Emerg3state,
         Emerg3zip,
         Emerg3country,
         Emerg3homePhone,
         Emerg3workPhone,
         Emerg3mobilePhone,
         Emerg3email,
         ProgramName,
         ProgramYear,
         ProgramSemester,
         StudentType,
         UniversityEnrolled,
         GraduationMonth,
         GraduationYear,
         CumulativeGPA,
         Major1,
         Major2,
         Minor1,
         Minor2,
         Emphasis1,
         Emphasis2,
         WillTakeBus,
         WillFlyWithGroup,
         DepartureDate,
         ReturnDate,
         AgreeToCosts,
         OrientationDate1,
         OrientationHours1,
         OrientationDate2,
         OrientationHours2,
         NumberOfGuests,
         OrientationConflict,
         ConflictDate,
         Subject1,
         Course1,
         Credits1,
         Subject2,
         Course2,
         Credits2,
         Subject3,
         Credits3,
         Subject4,
         Course4,
         Credits4,
         Subject5,
         Course5,
         Credits5,
         Subject6,
         Course6,
         Credits6,
         ReadSyllabus,
         EnrolledIS333,
         ApplyForAid,
         HoldApplication,
         FinancialAidGranted,
         RoomType,
         RoommateName1,
         RoommateName2,
         QuestionExpectations,
         AwareOfAllMaterials,
         _UWOshkoshRelease,
         Certification,
         SeatNumber,
         CompletionDate,
         ApplicationIsComplete,
         ApplicationFeeOK,
         _UWSystemStatementOK,
         _UWOshkoshStatementOK,
         WithdrawalRefund,
         TranscriptsOK,
         ProgramSpecificMaterialsRequired,
         ProgramSpecificMaterialsOK,
         SpecialStudentFormRequired,
         SpecialStudentFormOK,
         CreditOverloadFormRequired,
         CreditOverloadFormOK,
         MedicalOK,
         MedicalForm,
         PassportOK,
         MetPassportDeadline,
         ProgramSpecificMaterialsRequiredStepIII,
         ProgramSpecificMaterialsOKStepIII,
         AttendedOrientation,
         CisiDates,
         CisiNumberOfMonths,
         ProgramFee,
         TuitionPayment,
         DepositOnTime,
         Payment2OnTime,
         ApplicationFeeRefund,
         ForeignCourse1,
         ForeignCourse2,
         ForeignCourse3,
         ForeignCourse4,
         ForeignCourse5,
         ForeignCourse6,
         PapersOK,
         NoMoreMaterials,
         ProgramMaterials,
         ProgramFee2,
         review_history) = values

        if created and len(created):
            created = (DateTime.DateTime(created)).asdatetime()
        if modified and len(modified):
            modified = (DateTime.DateTime(modified)).asdatetime()
        if DepartureDate and len(DepartureDate):
            DepartureDate = (DateTime.DateTime(DepartureDate)).asdatetime().date()
        if ReturnDate and len(ReturnDate):
            ReturnDate = (DateTime.DateTime(ReturnDate)).asdatetime().date()
        if OrientationDate1 and len(OrientationDate1):
            OrientationDate1 = (DateTime.DateTime(OrientationDate1)).asdatetime().date()
        if OrientationDate2 and len(OrientationDate2):
            OrientationDate2 = (DateTime.DateTime(OrientationDate2)).asdatetime().date()
        if ConflictDate and len(ConflictDate):
            ConflictDate = (DateTime.DateTime(ConflictDate)).asdatetime().date()
        if CompletionDate and len(CompletionDate):
            CompletionDate = (DateTime.DateTime(CompletionDate)).asdatetime().date()

        # # skip if object with that ID already exists (commented out because it doesn't work right)
        # existing = api.content.find(portal_type='OIEStudentApplicationWorkflow', id=id)
        # if len(existing) > 0:
        #     print "Skipping existing object with ID", id
        #     next

        obj = api.content.create(
            safe_id=True,
            container=folder,
            type=PORTAL_TYPE,
            id=id,
            title="%s %s %s %s %s" % (FirstName, MiddleName, LastName, ProgramName, ProgramYear),
            studentID=StudentID,
            firstName=FirstName,
            middleName=MiddleName,
            lastName=LastName,
            email=Email,
            localAddr1=LocalAddr1,
            localAddr2=LocalAddr2,
            localCity=LocalCity,
            localState=LocalState,
            localZip=LocalZip,
            localCountry=LocalCountry,
            localPhone=LocalPhone,
            mobilePhone=MobilePhone,
            homeAddr1=HomeAddr1,
            homeAddr2=HomeAddr2,
            homeCity=HomeCity,
            homeState=HomeState,
            homeZip=HomeZip,
            homeCountry=HomeCountry,
            homePhone=HomePhone,
            citizenship=Citizenship,
            citizenshipOther=CitizenshipOther,
            stateResidency=StateResidency,
            stateResidencyOther=StateResidencyOther,
            dateOfBirth_year=DateOfBirth_year,
            dateOfBirth_month=DateOfBirth_month,
            dateOfBirth_day=DateOfBirth_day,
            placeOfBirth=PlaceOfBirth,
            gender=Gender,
            marriageStatus=MarriageStatus,
            ethnicity=Ethnicity,
            ethnicityOther=EthnicityOther,
            passportName=PassportName,
            passportNumber=PassportNumber,
            passportIssueOffice=PassportIssueOffice,
            passportExpDate_year=PassportExpDate_year,
            passportExpDate_month=PassportExpDate_month,
            passportExpDate_day=PassportExpDate_day,
            questionAcadCareerPlan=QuestionAcadCareerPlan,
            questionLangCulturalSkills=QuestionLangCulturalSkills,
            questionPrevTravel=QuestionPrevTravel,
            questionWorkExp=QuestionWorkExp,
            questionEuroBizTravSem=QuestionEuroBizTravSem,
            questionStuExchComp=QuestionStuExchComp,
            doctorLastname=DoctorLastname,
            doctorFirstname=DoctorFirstname,
            doctorPhone=DoctorPhone,
            medicalInsuranceCompany=MedicalInsuranceCompany,
            medicalPolicyHolder=MedicalPolicyHolder,
            medicalPolicyGroupNumber=MedicalPolicyGroupNumber,
            foodAllergies=FoodAllergies,
            hasDifficultyWalking=HasDifficultyWalking,
            maxWalkingDistance=MaxWalkingDistance,
            medicalReadStatement=MedicalReadStatement,
            medicalHealthProblems=MedicalHealthProblems,
            medicalHealthProblems_takenMedication=MedicalHealthProblems_takenMedication,
            medicalHealthProblems_medications=MedicalHealthProblems_medications,
            medicalHealthProblems_stable=MedicalHealthProblems_stable,
            medicalHealthProblems_underCare=MedicalHealthProblems_underCare,
            medicalHealthProblems_whatCondition=MedicalHealthProblems_whatCondition,
            medicalHealthProblems_willingToPrescribe=MedicalHealthProblems_willingToPrescribe,
            medicalHealthProblems_additionalInfo=MedicalHealthProblems_additionalInfo,
            medicalMentalProblems=MedicalMentalProblems,
            medicalMentalProblems_takenMedication=MedicalMentalProblems_takenMedication,
            medicalMentalProblems_medications=MedicalMentalProblems_medications,
            medicalMentalProblems_currentDose=MedicalMentalProblems_currentDose,
            medicalMentalProblems_stable=MedicalMentalProblems_stable,
            medicalMentalProblems_underCare=MedicalMentalProblems_underCare,
            medicalMentalProblems_condition=MedicalMentalProblems_condition,
            medicalMentalProblems_enoughMedication=MedicalMentalProblems_enoughMedication,
            medicalMentalProblems_additionalInfo=MedicalMentalProblems_additionalInfo,
            medicalRegistered=MedicalRegistered,
            medicalRegistered_office=MedicalRegistered_office,
            medicalRegistered_accommodations=MedicalRegistered_accommodations,
            medicalAccessOK=MedicalAccessOK,
            smokingPreferred=SmokingPreferred,
            isVegetarian=IsVegetarian,
            additionalNeeds=AdditionalNeeds,
            emerg1name=Emerg1name,
            emerg1addr1=Emerg1addr1,
            emerg1addr2=Emerg1addr2,
            emerg1city=Emerg1city,
            emerg1state=Emerg1state,
            emerg1zip=Emerg1zip,
            emerg1country=Emerg1country,
            emerg1homePhone=Emerg1homePhone,
            emerg1workPhone=Emerg1workPhone,
            emerg1mobilePhone=Emerg1mobilePhone,
            emerg1email=Emerg1email,
            emerg2name=Emerg2name,
            emerg2addr1=Emerg2addr1,
            emerg2addr2=Emerg2addr2,
            emerg2city=Emerg2city,
            emerg2state=Emerg2state,
            emerg2zip=Emerg2zip,
            emerg2country=Emerg2country,
            emerg2homePhone=Emerg2homePhone,
            emerg2workPhone=Emerg2workPhone,
            emerg2mobilePhone=Emerg2mobilePhone,
            emerg2email=Emerg2email,
            emerg3name=Emerg3name,
            emerg3addr1=Emerg3addr1,
            emerg3addr2=Emerg3addr2,
            emerg3city=Emerg3city,
            emerg3state=Emerg3state,
            emerg3zip=Emerg3zip,
            emerg3country=Emerg3country,
            emerg3homePhone=Emerg3homePhone,
            emerg3workPhone=Emerg3workPhone,
            emerg3mobilePhone=Emerg3mobilePhone,
            emerg3email=Emerg3email,
            programName=ProgramName,
            programYear=ProgramYear,
            programSemester=ProgramSemester,
            studentType=StudentType,
            universityEnrolled=UniversityEnrolled,
            graduationMonth=GraduationMonth,
            graduationYear=GraduationYear,
            cumulativeGPA=CumulativeGPA,
            major1=Major1,
            major2=Major2,
            minor1=Minor1,
            minor2=Minor2,
            emphasis1=Emphasis1,
            emphasis2=Emphasis2,
            willTakeBus=WillTakeBus,
            willFlyWithGroup=WillFlyWithGroup,
            departureDate=DepartureDate,
            returnDate=ReturnDate,
            agreeToCosts=AgreeToCosts,
            orientationDate1=OrientationDate1,
            orientationHours1=OrientationHours1,
            orientationDate2=OrientationDate2,
            orientationHours2=OrientationHours2,
            numberOfGuests=NumberOfGuests,
            orientationConflict=OrientationConflict,
            conflictDate=ConflictDate,
            subject1=Subject1,
            course1=Course1,
            credits1=Credits1,
            subject2=Subject2,
            course2=Course2,
            credits2=Credits2,
            subject3=Subject3,
            credits3=Credits3,
            subject4=Subject4,
            course4=Course4,
            credits4=Credits4,
            subject5=Subject5,
            course5=Course5,
            credits5=Credits5,
            subject6=Subject6,
            course6=Course6,
            credits6=Credits6,
            readSyllabus=ReadSyllabus,
            enrolledIS333=EnrolledIS333,
            applyForAid=ApplyForAid,
            holdApplication=HoldApplication,
            financialAidGranted=FinancialAidGranted,
            roomType=RoomType,
            roommateName1=RoommateName1,
            roommateName2=RoommateName2,
            questionExpectations=QuestionExpectations,
            awareOfAllMaterials=AwareOfAllMaterials,
            UWOshkoshRelease=_UWOshkoshRelease,
            certification=Certification,
            seatNumber=SeatNumber,
            completionDate=CompletionDate,
            applicationIsComplete=ApplicationIsComplete,
            applicationFeeOK=ApplicationFeeOK,
            UWSystemStatementOK=_UWSystemStatementOK,
            UWOshkoshStatementOK=_UWOshkoshStatementOK,
            withdrawalRefund=WithdrawalRefund,
            transcriptsOK=TranscriptsOK,
            programSpecificMaterialsRequired=ProgramSpecificMaterialsRequired,
            programSpecificMaterialsOK=ProgramSpecificMaterialsOK,
            specialStudentFormRequired=SpecialStudentFormRequired,
            specialStudentFormOK=SpecialStudentFormOK,
            creditOverloadFormRequired=CreditOverloadFormRequired,
            creditOverloadFormOK=CreditOverloadFormOK,
            medicalOK=MedicalOK,
            medicalForm=MedicalForm,
            passportOK=PassportOK,
            metPassportDeadline=MetPassportDeadline,
            programSpecificMaterialsRequiredStepIII=ProgramSpecificMaterialsRequiredStepIII,
            programSpecificMaterialsOKStepIII=ProgramSpecificMaterialsOKStepIII,
            attendedOrientation=AttendedOrientation,
            cisiDates=CisiDates,
            cisiNumberOfMonths=CisiNumberOfMonths,
            programFee=ProgramFee,
            tuitionPayment=TuitionPayment,
            depositOnTime=DepositOnTime,
            payment2OnTime=Payment2OnTime,
            applicationFeeRefund=ApplicationFeeRefund,
            foreignCourse1=ForeignCourse1,
            foreignCourse2=ForeignCourse2,
            foreignCourse3=ForeignCourse3,
            foreignCourse4=ForeignCourse4,
            foreignCourse5=ForeignCourse5,
            foreignCourse6=ForeignCourse6,
            papersOK=PapersOK,
            noMoreMaterials=NoMoreMaterials,
            programMaterials=ProgramMaterials,
            programFee2=ProgramFee2,
        )

        # set some metadata
        obj.creation_date=created
        obj.setModificationDate(modified)
        obj.setCreators(Creators)

        # set review_state and review_history
        for h in review_history:
            wtool.setStatusOf(workflow_id, obj, h)

        print "    ", id, Email


        counter += 1
        if counter >= MAX_COUNT:
            print "Stopping after reaching MAX_COUNT ", MAX_COUNT
            break

        # commit every 100 objects
        if counter % 100 == 0:
            print counter
            # Commit transaction
            transaction.commit()
            # Perform ZEO client synchronization (if running in clustered mode)
            app._p_jar.sync()

print counter
# final commit transaction
transaction.commit()
# Perform ZEO client synchronization (if running in clustered mode)
app._p_jar.sync()

