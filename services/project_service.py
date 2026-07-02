from datetime import datetime
import json
from ssl import create_default_context

from pandas.core.dtypes.generic import create_pandas_abc_type
from streamlit import status

from enterprise.project_registry import Project
from storage.project_store import ProjectStore


class ProjectService:

    @staticmethod
    def create_project(
        project_id,
        operator,
        rig,
        well,
        field="",
        county="",
        state="",
        country=""
    ):

        # Create project folders
        root = ProjectStore.initialize_project_structure(project_id)

        # Create Project object
        project = Project(
            project_id=project_id,
            operator=operator,
            rig=rig,
            well=well,
            field=field,
            county=county,
            state=state,
            country=country
        )

        return project
        project = Project(
            project_id=project_id,
            operator=operator,
            rig=rig,
            well=well,
            field=field,
            county=county,
            state=state,
            country=country
            created_at=create_at
            updated_at=updated_at
            status=status
            )

        metadata = {
            "project_id": project.project_id,
            "operator": project.operator,
            "rig": project.rig,
            "well": project.well,
            "field": project.field,
            "county": project.county,
            "state": project.state,
            "country": project.country,
            "status": project.status,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat()
        }

        metadata_file = root / "metadata" / "project.json"

        with open(metadata_file, "w") as f:
             json.dump(
                metadata,
                f,
                indent=4
            )
        return project