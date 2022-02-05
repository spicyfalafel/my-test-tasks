import os
from pathlib import Path


class ProjectPathUtils(object):
    @staticmethod
    def get_project_path():
        utils_dir = os.path.dirname(__file__)
        return Path(utils_dir).parent.parent.absolute()

    @staticmethod
    def get_path_to_project_dir(dirname, filename=""):
        project_dir = ProjectPathUtils.get_project_path()
        dir_path = os.path.join(project_dir, dirname)
        file_path = os.path.join(dir_path, filename)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(file_path)
        return file_path

    @staticmethod
    def get_path_relative_to_project_dir(path):
        parts = os.path.split(path)
        res_path = ProjectPathUtils.get_project_path()
        for part in parts:
            res_path = os.path.join(res_path, part)
        return res_path
