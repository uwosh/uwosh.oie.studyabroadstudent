# -*- coding: utf-8 -*-
from plone import api


class ReportUtil(object):

    def __init__(self):
        self.cat = api.portal.get_tool('portal_catalog')

    def high_school_count(self):
        pass

    def uwo_freshman_count(self):
        pass

    def uwo_sophomore_count(self):
        pass

    def uwo_junior_count(self):
        pass

    def uwo_senior_count(self):
        pass

    def uwo_graduate_count(self):
        pass

    def other_undergrad_count(self):
        pass

    def other_graduate_count(self):
        pass

    def program_leader_count(self):
        pass

    def community_member_count(self):
        pass
