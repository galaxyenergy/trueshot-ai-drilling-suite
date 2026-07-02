from pathlib import Path
import json


class ProjectStore:

    ROOT = Path("projects")

    @classmethod
    def initialize(cls):
        cls.ROOT.mkdir(exist_ok=True)

    @classmethod
    def project_path(cls, project_id):
        return cls.ROOT / project_id

    @classmethod
    def create_project_folder(cls, project_id):

        folder = cls.project_path(project_id)

        folder.mkdir(parents=True, exist_ok=True)

        return folder
    
    @classmethod
    def initialize_project_structure(cls, project_id):

        root = cls.create_project_folder(project_id)

        folders = [
            "metadata",
            "imports",
            "reports",
            "surveys",
            "tool_dumps",
            "analytics"
        ]

        for folder in folders:
            (root / folder).mkdir(exist_ok=True)

        return root
