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

Scenario: As a site administrator I can add a OIEStudyAbroadStudentApplication
  Given a logged-in site administrator
    and an add oiestudyabroadstudentapplication form
   When I type 'My OIEStudyAbroadStudentApplication' into the title field
    and I submit the form
   Then a oiestudyabroadstudentapplication with the title 'My OIEStudyAbroadStudentApplication' has been created

Scenario: As a site administrator I can view a OIEStudyAbroadStudentApplication
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
  Create content  type=OIEStudyAbroadStudentApplication  id=my-oiestudyabroadstudentapplication  title=My OIEStudyAbroadStudentApplication


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the oiestudyabroadstudentapplication view
  Go To  ${PLONE_URL}/my-oiestudyabroadstudentapplication
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a oiestudyabroadstudentapplication with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the oiestudyabroadstudentapplication title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
