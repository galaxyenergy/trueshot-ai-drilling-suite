from dataclasses import dataclass
from typing import Optional

from dataclasses import dataclass
from typing import Optional


@dataclass
class AppContext:

    current_project: Optional[str] = None
    current_operator: Optional[str] = None
    current_rig: Optional[str] = None
    current_well: Optional[str] = None
    current_bha: Optional[str] = None
    current_run: Optional[int] = None
    current_shift: Optional[str] = None
    current_engineer: Optional[str] = None
    active_project_id: Optional[str] = None


    connection_mode: str = "Periodic Synchronization"
    data_source: str = "WellData Export"

