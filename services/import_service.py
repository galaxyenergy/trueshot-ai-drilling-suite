from pathlib import Path
from datetime import datetime

import pandas as pd

from core.approved_dataset import ApprovedDataset
from services.validation_service import ValidationService


class ImportService:

    @staticmethod
    def import_file(uploaded_file):

        if uploaded_file is None:
            return None

        extension = Path(uploaded_file.name).suffix.lower()
        uploaded_file.seek(0)
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(uploaded_file.tell())

        first_bytes = uploaded_file.read(300)

        print(first_bytes)

        uploaded_file.seek(0)   
        
        
        if extension in [".xlsx", ".xls"]:
            dataframe = pd.read_excel(uploaded_file)

        elif extension == ".csv":
            dataframe = pd.read_csv(uploaded_file)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        dataset = ImportService.build_dataset(dataframe)

        dataset.file_name = uploaded_file.name
        dataset.import_time = datetime.now()

        validator = ValidationService()

        try:
            report = validator.validate(dataset)

        except Exception as ex:

            print("VALIDATION FAILED")
            print(ex)

            report = {
                "status": "ERROR",
                "quality_score": 0,
                "issues": [str(ex)]
            }

        dataset.validation_report = report

        return dataset

    @staticmethod
    def build_dataset(dataframe):

        dataset = ApprovedDataset()

        # Original imported data
        dataset.raw_dataframe = dataframe

        # Working copy
        dataset.approved_dataframe = dataframe.copy()

        return dataset