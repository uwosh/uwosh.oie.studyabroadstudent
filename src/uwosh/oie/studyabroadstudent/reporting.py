from plone import api


class ReportUtil(object):

    partipant_count_states = [
        'application-complete',
        'step-iv',
        'ready-to-travel',
        'traveling',
        'completing-program-evaluation',
        'program-completed',
    ]

    def __init__(self, program):
        cat = api.portal.get_tool('portal_catalog')
        self.program = program
        self.pbrains = cat(portal_type='OIEStudyAbroadParticipant',
                           programName=self.program.UID)
        self.high_school = 0
        self.uwo_freshman = 0
        self.uwo_sophomore = 0
        self.uwo_junior = 0
        self.uwo_senior = 0
        self.uwo_graduate = 0
        self.other_undergrad = 0
        self.other_graduate = 0
        self.program_leader = 0
        self.community_member = 0
        self.get_participant_counts()

    def get_participant_counts(self):
        high_school_levels = ['High School Junior', 'High School Senior']
        undergrad_levels = [
            'University Freshman',
            'University Sophomore',
            'University Junior',
            'University Senior',
        ]
        for pbrain in self.pbrains:
            if pbrain.review_state in self.partipant_count_states:
                if pbrain.educationLevel in high_school_levels:
                    self.high_school += 1
                elif pbrain.university == 'UW Oshkosh':
                    if pbrain.educationLevel == 'University Freshman':
                        self.uwo_freshman += 1
                    elif pbrain.educationLevel == 'University Sophomore':
                        self.uwo_sophomore += 1
                    elif pbrain.educationLevel == 'University Junior':
                        self.uwo_junior += 1
                    elif pbrain.educationLevel == 'University Senior':
                        self.uwo_senior += 1
                    elif pbrain.educationLevel == 'Graduate Student':
                        self.uwo_graduate += 1
                elif pbrain.educationLevel in undergrad_levels:
                    self.other_undergrad += 1
                elif pbrain.educationLevel == 'Graduate School':
                    self.other_graduate += 1

    def high_school_count(self):
        return self.high_school

    def uwo_freshman_count(self):
        return self.uwo_freshman

    def uwo_sophomore_count(self):
        return self.uwo_sophomore

    def uwo_junior_count(self):
        return self.uwo_junior

    def uwo_senior_count(self):
        return self.uwo_senior

    def uwo_graduate_count(self):
        return self.uwo_graduate

    def other_undergrad_count(self):
        return self.other_undergrad

    def other_graduate_count(self):
        return self.other_graduate

    def program_leader_count(self):
        return self.program_leader

    def community_member_count(self):
        return self.community_member
