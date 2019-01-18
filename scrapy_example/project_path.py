# coding = utf-8

import os


def get_project_path():
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_path.endswith('egg'):
        project_dir = project_path.split('.')[0]
        return os.path.join(os.path.dirname(project_path), project_dir)
    return project_path


if __name__ == '__main__':
    print(get_project_path())
