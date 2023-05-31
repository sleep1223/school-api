# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from urllib import parse as urlparse

import time
from bs4 import BeautifulSoup
from requests import RequestException

from school_api.client.api.base import BaseSchoolApi
from school_api.exceptions import ScheduleException


class PlanSchedule(BaseSchoolApi):
    schedule_url = None
    payload = None
    grades = None
    facultys = None
    specialtys = None
    terms = None
    natures = None

    def getGrades(self):
        return self.grades

    def getFacultys(self):
        return self.facultys

    def getSpecialtys(self):
        return self.specialtys

    def getTerms(self):
        return self.terms

    def getNatures(self):
        return self.natures

    def get_schedule(self, xm=None, schedule_grade=None,
                     schedule_faculty=None,
                     schedule_specialty=None,
                     schedule_term=None,
                     schedule_nature=0, **kwargs):
        """ 课表信息 获取入口
        :param xm: 姓名
        :param schedule_grade: 年级
        :param schedule_faculty: 学院
        :param schedule_specialty: 专业
        :param schedule_term: 学期 0:全部 1 2 3 4 5 6 7 8
        :param schedule_nature: 0 全部 1 必修课 2 选修课 3 校公选课
        :return: 课表信息
        """
        self.schedule_url = self.school_url["SCHEDULE_URL"][2] + urlparse.quote(self.user.account.encode('gb2312')) + '&xm=' + urlparse.quote(
            xm.encode('gb2312'))

        if self.payload:
            self.payload.update({
                "schedule_grade": schedule_grade,
                "schedule_faculty": schedule_faculty,
                "schedule_specialty": schedule_specialty,
                "schedule_term": schedule_term,
                "schedule_nature": schedule_nature,
                'txtChoosePage': '1',
                "txtPageSize": '100',
            })
        data = self._update_payload(**kwargs)
        if not data:
            raise ScheduleException(self.school_code, '获取教务计划课表失败')
        return self.PlanScheduleParse(data.text)

    def _update_payload(self, **kwargs):
        # 更新提交参数 payload
        try:
            res = self._get_api(**kwargs)
        except ScheduleException:
            return None
        try:
            self.payload = self._get_payload(res.text)
        except AttributeError:
            return None
        # except Exception as e:
        #     time.sleep(2)
        #     return None
        return res

    def _get_payload(self, html):
        """ 获取课表提交参数 """
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(attrs={"name": "__VIEWSTATE"})['value']
        searchbox = pre_soup.find("div", {"class": "searchbox"})

        grades = searchbox.find(id='nj').find_all('option')
        facultys = searchbox.find(id='xymc').find_all('option')
        specialtys = searchbox.find(id='zymc').find_all('option')
        terms = searchbox.find(id='xq').find_all('option')
        natures = searchbox.find(id='kcxz').find_all('option')

        self.grades = [{"name": v.text, "value": v['value']} for v in grades if v.text and v['value']]
        self.facultys = [{"name": v.text, "value": v['value']} for v in facultys if v.text and v['value']]
        self.specialtys = [{"name": v.text, "value": v['value']} for v in specialtys if v.text and v['value']]
        self.terms = [{"name": v.text, "value": v['value']} for v in terms if v.text and v['value']]
        self.natures = [{"name": v.text, "value": v['value']} for v in natures if v.text and v['value']]
        payload = {'view_state': view_state}
        return payload

    def _get_api(self, **kwargs):
        """ 请求函数 """
        if self.payload:
            data = {
                "__EVENTTARGET": "nj",
                "nj": self.payload['schedule_grade'],
                "xymc": self.payload['schedule_faculty'],
                "zymc": self.payload['schedule_specialty'],
                "xq": '全部'.encode('gb2312') if self.payload['schedule_term'] == '0' else self.payload['schedule_term'],
                "kcxz": ['全部', '必修课', '选修课', '校公选课'][self.payload['schedule_nature']].encode('gb2312'),
                'dpDBGrid:txtChoosePage': self.payload['txtChoosePage'],
                "dpDBGrid:txtPageSize": self.payload['txtPageSize'],
                "__VIEWSTATE": self.payload['view_state'],
            }

            _request = self._post
        else:
            data = ""
            _request = self._get

        try:
            res = _request(self.schedule_url, data=data, **kwargs)
        except RequestException:
            raise ScheduleException(self.school_code, '获取教学计划课表失败')
        self._get_payload(res.text)
        return res

    @staticmethod
    def PlanScheduleParse(html):
        soup = BeautifulSoup(html, "html.parser")
        option_args = soup.find_all("option", {"selected": "selected"})
        if option_args:
            table = soup.find("table", {"id": "DBGrid"})
            rows = table.find_all('tr')
            # rows.pop(0)
            # print(rows)

            return [[x.text.strip() for x in row.find_all("td")] for row in rows]
