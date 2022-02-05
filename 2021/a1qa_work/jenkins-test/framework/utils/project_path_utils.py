import os
from pathlib import Path


class ProjectPathUtils(object):

    @staticmethod
    def get_path_to_project_dir(dirname, name=""):
        utils_dir = os.path.dirname(__file__)
        project_dir = Path(utils_dir).parent.parent.absolute()
        filename = os.path.join(project_dir, dirname)
        filename = os.path.join(filename, name)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(filename)
        return filename
