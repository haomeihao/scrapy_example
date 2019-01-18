# coding=utf-8

import os
import requests

patent_dir = (os.path.dirname(os.path.abspath(__file__)))


class ProjectSchedule():

    def __init__(self, project_name):
        self.schedule_url = 'http://localhost:6800/schedule.json'
        self.cancel_url = 'http://localhost:6800/cancel.json'
        self.project_name = project_name

    def schedule(self, spider_name_list):
        # method: POST
        # curl http://localhost:6800/schedule.json -d project=scrapy_example -d spider=woaiwojia_list
        for spider_name in spider_name_list:
            data = {'project': self.project_name, 'spider': spider_name}
            result = requests.post(self.schedule_url, data)
            print("> curl " + self.schedule_url + " -d project=" + self.project_name + " -d spider=" + spider_name)
            print(result.text)

    def cancel(self, job_id):
        # method: POST
        # curl http://localhost:6800/cancel.json -d project=scrapy_example -d job=70509948e87311e8817f38baf86d1cb1
        data = {'project': self.project_name, 'job': job_id}
        result = requests.post(self.cancel_url, data)
        print("> curl " + self.cancel_url + " -d project=" + self.project_name + " -d job=" + job_id)
        print(result.text)


if __name__ == '__main__':
    project_name = 'scrapy_example'
    project_schedule = ProjectSchedule(project_name)
    # schedule
    # spider_name_list = ['woaiwojia_list']
    # project_schedule.schedule(spider_name_list)
    # cancel
    # job_id = '66eacb80f86e11e898c738baf86d1cb1'
    # project_schedule.cancel(job_id)
