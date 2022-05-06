import numpy as np
import pandas as pd
import uuid
from pathlib import Path
from src.db.postgres import Postgres
from src.file_processor.file_process_func import FileProcessor


class Scotia_Preprocessor(FileProcessor):
    def __init__(self, file_path: str, columns):
        super().__init__(file_path)
        self.columns = columns

    def preprocess(self):
        df = self.load_file()
        df.columns = self.columns
        df = df.fillna(0)
        df["TransType"] = df["TransType"].str.strip()
        df["TransDetails"] = df["TransDetails"].str.strip()
        df["TransDetails"] = df["TransType"] + ", " + df["TransDetails"]
        df = df.drop("TransType", axis=1)
        df["Deposits"] = np.where(df["Withdrawals"] > 0, df["Withdrawals"], 0)
        df["Withdrawals"] = np.where(df["Withdrawals"] < 0, -df["Withdrawals"], 0)
        df["TransDate"] = pd.to_datetime(df.TransDate).astype(str)

        df["UUID"] = [uuid.uuid4() for _ in range(len(df.index))]
        df["Institution"] = ["Scotia"] * len(df.index)

        arrage_columns = [
            "UUID",
            "Institution",
            "TransDate",
            "TransDetails",
            "Withdrawals",
            "Deposits",
        ]
        df = df[arrage_columns]

        return df


# Chequing
def process_chequing_data(chequing_path, columns, table_name):
    data_path = project_root.joinpath(project_root, chequing_path)

    pc = Scotia_Preprocessor(file_path=data_path, columns=columns)
    chequing_df = pc.preprocess()
    print(chequing_df.head())

    pg = Postgres()
    pg.store_dataframe(chequing_df, table_name)


if __name__ == "__main__":
    project_root = Path(".")

    CHEQUING_PATH = "src/data/scotia-chequing.csv"
    CHEQUING_COLUMNS = [
        "TransDate",
        "Withdrawals",
        "Deposits",
        "TransType",
        "TransDetails",
    ]

    process_chequing_data(CHEQUING_PATH, CHEQUING_COLUMNS, "chequing")
