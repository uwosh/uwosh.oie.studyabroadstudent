# - 2017-05-20 read ISO8601 dates, workflow state, and all workflow transitions
#
# expects the extractoutput.py file or symlink to be in the folder
# /opt/Plone/zinstance/src/uwosh.oie.studyabroadstudent/src/uwosh/oie/studyabroadstudent

# invoke like this:
# bin/instance run importApplications.py

from datetime import date
from plone import api
from Products.CMFPlone.utils import getToolByName
from uwosh.oie.studyabroadstudent.extractoutput import app_data
from zope.component.hooks import getSite, setSite

import argparse
import DateTime
import transaction


MAX_COUNT = 100000  # stop after this many records

counter = 0
folder_id = 'applications'
workflow_id = 'OIEStudentApplicationWorkflow'
PORTAL_TYPE = 'OIEStudyAbroadStudentApplication'

parser = argparse.ArgumentParser(
    description='...')
parser.add_argument(
    '--site-id',
    dest='site_id',
    default='OIE',
    help='the ID of the site in which to create the applications; defaults to "OIE"',  # noqa
)
parser.add_argument(
    '--folder-id',
    dest='folder_id',
    default='applications',
    help='the ID of the folder within the site in which to create the applications; defaults to "applications"',  # noqa
)
parser.add_argument(
    '--skip-existing',
    dest='skip_existing',
    default=False,
    help='set to True to skip creating the application if an application with the same ID already exists in the site; defaults to False',  # noqa
)
args, _ = parser.parse_known_args()

# Sets the current site as the active site
site_id = args.site_id
setSite(app[site_id])  # noqa
site = getSite()  # noqa

# ensure folder exists
toplevel_items = site.items()
if 'applications' not in [id for id, obj in toplevel_items]:
    folder = api.content.create(
        container=site,
        type='Folder',
        id=folder_id,
        title='Applications',
    )

month_values = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

# Enable the context manager to switch the user
with api.env.adopt_user(username='admin'):
    # You're now posing as admin!

    workflow_tool = site.portal_workflow
    folder = app.unrestrictedTraverse("{0}/{1}".format(site_id, folder_id))  # noqa

    for values in app_data:  # noqa
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

        if created is not None and len(created):
            created = (DateTime.DateTime(created)).asdatetime()
        if modified is not None and len(modified):
            modified = (DateTime.DateTime(modified)).asdatetime()
        if DepartureDate is not None and len(DepartureDate):
            DepartureDate = (DateTime.DateTime(DepartureDate)).asdatetime().date()  # noqa
        if ReturnDate is not None and len(ReturnDate):
            ReturnDate = (DateTime.DateTime(ReturnDate)).asdatetime().date()
        if OrientationDate1 is not None and len(OrientationDate1):
            OrientationDate1 = (DateTime.DateTime(OrientationDate1)).asdatetime().date()  # noqa
        if OrientationDate2 is not None and len(OrientationDate2):
            OrientationDate2 = (DateTime.DateTime(OrientationDate2)).asdatetime().date()  # noqa
        if ConflictDate is not None and len(ConflictDate):
            ConflictDate = (DateTime.DateTime(ConflictDate)).asdatetime().date()  # noqa
        if CompletionDate is not None and len(CompletionDate):
            CompletionDate = (DateTime.DateTime(CompletionDate)).asdatetime().date()  # noqa

        # # skip if object with that ID already exists (commented out
        # # because it doesn't work right)
        #
        # existing = api.content.find(
        #                portal_type='OIEStudentApplicationWorkflow',
        #                id=id,
        #            )
        # if len(existing) > 0:
        #     print "Skipping existing object with ID", id
        #     next

        if str(DateOfBirth_year) == '11201972':
            DateOfBirth_year = '19721'
        if str(DateOfBirth_year) == '5191995':
            DateOfBirth_year = '1995'
        if str(DateOfBirth_year) == '19991':
            DateOfBirth_year = '1991'
        if str(DateOfBirth_year) == '4141989':
            DateOfBirth_year = '1989'
        if str(DateOfBirth_year) == '101389':
            DateOfBirth_year = '1989'
        if str(DateOfBirth_year) == '19997':
            DateOfBirth_year = '1997'
        if str(DateOfBirth_year) == '2171991':
            DateOfBirth_year = '1991'
        if str(DateOfBirth_year) == '5131997':
            DateOfBirth_year = '1997'
        if str(DateOfBirth_year) == '19992':
            DateOfBirth_year = '1992'
        if str(DateOfBirth_year) == '19996':
            DateOfBirth_year = '1996'
        if PassportExpDate_month == 'April' and PassportExpDate_day == '31':
            PassportExpDate_day = '30'
        try:
            dateOfBirth = date(
                int(
                    (DateOfBirth_year is not None) and
                    DateOfBirth_year or
                    '1900',
                ),
                month_values[
                    (
                        (DateOfBirth_month is not None) and
                        (DateOfBirth_month != '-- choose one --')
                    ) and
                    DateOfBirth_month or
                    'January'
                ],
                int(
                    (DateOfBirth_day is not None) and
                    (DateOfBirth_day != '-- choose one --') and
                    DateOfBirth_day or
                    1,
                ),
            )
        except Exception:  # noqa: B902
            import pdb;pdb.set_trace()  # noqa

        try:
            passportExpDate = date(
                int(
                    (
                        PassportExpDate_year is not None and
                        PassportExpDate_year != ''
                    ) and
                    PassportExpDate_year or
                    '1900',
                ),
                month_values[
                    (
                        PassportExpDate_month == '-- choose one --' or
                        PassportExpDate_month == ''
                    ) and
                    'January' or
                    PassportExpDate_month
                ],
                int(
                    (
                        PassportExpDate_day == '-- choose one --' or
                        PassportExpDate_day == ''
                    ) and
                    1 or
                    PassportExpDate_day,
                ),
            )
        except Exception:  # noqa: B902
            import pdb; pdb.set_trace()  # noqa: T100, E702

        if args.skip_existing:
            # try to look up an application by the same ID
            existing_apps = api.content.find(portal_type=PORTAL_TYPE, id=id)
            if len(existing_apps) > 0:
                print('Skipping existing application', id)  # noqa: T001
        else:
            obj = api.content.create(
                safe_id=True,
                container=folder,
                type=PORTAL_TYPE,
                id=id,
                title=f'{FirstName} {MiddleName} {LastName} {ProgramName} {ProgramYear}',
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
                dateOfBirth=dateOfBirth,
                placeOfBirth=PlaceOfBirth,
                gender=Gender,
                marriageStatus=MarriageStatus,
                ethnicity=Ethnicity,
                ethnicityOther=EthnicityOther,
                passportName=PassportName,
                passportNumber=PassportNumber,
                passportIssueOffice=PassportIssueOffice,
                passportExpDate=passportExpDate,
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

            # set review_state and review_history
            for h in review_history:
                workflow_tool.setStatusOf(workflow_id, obj, h)

            print('    ', id, Email)  # noqa

            # set some metadata (do this last)
            obj.setCreators(Creators)
            obj.creation_date = created
            obj.setModificationDate(modified)
            # reindexing these doesn't actually work correctly;
            #   instead, do a full catalog clear and rebuild at the end
            # obj.reindexObject(idxs=['modified', 'created', 'Creator'])

            counter += 1
            if counter >= MAX_COUNT:
                print('Stopping after reaching MAX_COUNT ', MAX_COUNT)  # noqa: T001
                break

        # commit every 100 objects
        if counter % 100 == 0:
            print(counter)  # noqa: T001
            # Commit transaction
            transaction.commit()
            # Perform ZEO client synchronization (if running in clustered mode)
            app._p_jar.sync()  # noqa: F821

print(counter)  # noqa: T001
# final commit transaction
transaction.commit()
# Perform ZEO client synchronization (if running in clustered mode)
app._p_jar.sync()  # noqa: F821

print('Rebuilding the catalog to update for modified dates, \
    creation dates, and creators. Will take a few minutes:')  # noqa: T001
catalog = getToolByName(site, 'portal_catalog', None)  # noqa: P001
if catalog:
    catalog.manage_catalogRebuild()
print('Catalog rebuild is done.')  # noqa: T001
print('Import is complete.')  # noqa: T001
