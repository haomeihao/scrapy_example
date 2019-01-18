# coding=utf-8

import os

patent_dir = (os.path.dirname(os.path.abspath(__file__)))


class ProjectDeploy():

    def __init__(self, deploy_name, project_name):
        self.deploy_name = deploy_name
        self.project_name = project_name

    def deploy(self):
        # scrapyd-deploy.py local-20181202 -p scrapy_example
        command_list = ['scrapyd-deploy.py', self.deploy_name, '-p', self.project_name]
        command_str = ' '.join(command_list)
        print("> " + command_str)
        os.system(command_str)


if __name__ == '__main__':
    deploy_name = 'local-20181202'
    project_name = 'scrapy_example'
    project_deploy = ProjectDeploy(deploy_name, project_name)
    project_deploy.deploy()
