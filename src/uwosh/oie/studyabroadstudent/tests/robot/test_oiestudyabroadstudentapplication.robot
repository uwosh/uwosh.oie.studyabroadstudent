# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s uwosh.oie.studyabroadstudent -t test_oiestudyabroadstudentapplication.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src uwosh.oie.studyabroadstudent.testing.UWOSH_OIE_STUDYABROADSTUDENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_oiestudyabroadstudentapplication.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add an OIEStudyAbroadStudentApplication
  Given a logged-in site administrator
    and an add oiestudyabroadstudentapplication form
  When I enter fill out required fields
    and I submit the form
  Then a oiestudyabroadstudentapplication has been created

Scenario: As a site administrator I can view an OIEStudyAbroadStudentApplication
  Given a logged-in site administrator
    and a oiestudyabroadstudentapplication 'My OIEStudyAbroadStudentApplication'
   When I go to the oiestudyabroadstudentapplication view
   Then I can see the oiestudyabroadstudentapplication title 'My OIEStudyAbroadStudentApplication'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add oiestudyabroadstudentapplication form
  Go To  ${PLONE_URL}/++add++OIEStudyAbroadStudentApplication

a oiestudyabroadstudentapplication 'My OIEStudyAbroadStudentApplication'
  Create content  type=OIEStudyAbroadStudentApplication  id=my-oiestudyabroadstudentapplication


# --- WHEN -------------------------------------------------------------------

I enter fill out required fields
  Input Text  name=form.widgets.firstName  Fake
  Input Text  name=form.widgets.lastName  Student
  Input Text  name=form.widgets.email  fake.student@uwosh.edu
  Click Link  Addresses
  Input Text  name=form.widgets.homePhone  7151234567
  Input Text  name=form.widgets.localPhone  7152345678
  Input Text  name=form.widgets.localAddr1  123 Fake Place
  Input Text  name=form.widgets.localCity  Oshkosh
  Input Text  name=form.widgets.localState  Wisconsin
  Input Text  name=form.widgets.localZip  54901
  Input Text  name=form.widgets.localCountry  United States
  Input Text  name=form.widgets.homeAddr1  123 Not Real Avenue
  Input Text  name=form.widgets.homeCity  Steven's Point
  Input Text  name=form.widgets.homeState  Wisconsin
  Input Text  name=form.widgets.homeZip  54481
  Input Text  name=form.widgets.homeCountry  United States
  Click Link  Demographics
  Click Element  name=form.widgets.stateResidency
  # Input Text  name=form.widgets.stateResidency  Wisconsin
  # Input Text  name=form.widgets.citizenship  U.S. Citizen
  Input Text  name=form.widgets.dateOfBirth  May 10, 2001
  Input Text  name=form.widgets.placeOfBirth  Steven's Point, Wisconsin  54481
  Click Link  Passport
  Input Text  name=form.widgets.passportExpDate  May 10, 2021

I type '${title}' into the title field
  Input Text  name=form.widgets.description  ${title}

I submit the form
  Click Button  Save

I go to the oiestudyabroadstudentapplication view
  Go To  ${PLONE_URL}/my-oiestudyabroadstudentapplication
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a oiestudyabroadstudentapplication has been created
  Wait until page contains  Site Map
  Page should contain  Item created

I can see the oiestudyabroadstudentapplication title '${id}'
  Wait until page contains  Site Map
  Page should contain  ${id}
