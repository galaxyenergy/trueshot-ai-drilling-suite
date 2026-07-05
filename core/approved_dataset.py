from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd


@dataclass
class ApprovedDataset:

    raw_dataframe: Optional[pd.DataFrame] = None

    approved_dataframe: Optional[pd.DataFrame] = None

    validation_report = None

    project_id: str = ""

    operator: str = ""

    rig: str = ""

    well: str = ""

    run: Optional[int] = None

    shift: str = ""
    
    file_name: str = ""
    
    import_time: datetime = field(default_factory=datetime.now)

    quality_score: float = 0

    engineering_confidence: float = 0

    approved: bool = False