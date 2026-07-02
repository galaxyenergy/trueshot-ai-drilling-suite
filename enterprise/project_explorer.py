from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Project:

    project_id: str

    operator: str

    rig: str

    well: str

    field: str = ""

    county: str = ""

    state: str = ""

    country: str = ""

    status: str = "Active"

    current_bha: Optional[str] = None

    current_run: Optional[int] = None

    current_shift: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)

    updated_at: datetime = field(default_factory=datetime.now)