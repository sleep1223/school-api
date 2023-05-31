#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

from school_api import SchoolClient
import unittest


class TestStudent(unittest.TestCase):
    conf = {
        'name': '湖北师范大学文理学院',
        'exist_verify': True
    }

    GdstApi = SchoolClient('http://221.233.125.126:8096', **conf)
    student = GdstApi.user_login('2021415210101', 'hsyqwe123', timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.student.get_schedule(schedule_year='2017-2018', schedule_term='1')
        schedule_data = self.student.get_schedule(schedule_year='2017-2018', schedule_term='1', schedule_type=1)
        print(schedule_data)

    def test_score(self):
        score_data = self.student.get_score(score_year='2017-2018', score_term='1', use_api=2, timeout=5)
        score_data = self.student.get_score(score_year='2017-2018', score_term='1', timeout=5)
        print(score_data)

    def test_info(self):
        info_data = self.student.get_info(timeout=5)
        print(info_data)


if __name__ == '__main__':
    unittest.main()
