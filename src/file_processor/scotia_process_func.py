import numpy as np
import pandas as pd
import uuid
import os
from pathlib import Path
from src.db.postgres import Postgres
from src.file_processor.file_process_func import FileProcessor


class Scotia_Preprocessor(FileProcessor):
    def __init__(self, file_path: str, columns):
        super().__init__(file_path)
        self.columns = columns

    def preprocess(self, file_type):
        df = self.load_file()
        df.columns = self.columns

        if file_type == "chequing":
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
            print(f'{df.shape[0]} rows processed...')

        if file_type == "credit":
            df["TransDetails"] = df["TransDetails"].str.strip()
            df["Credits"] = np.where(df["Debts"] > 0, df["Debts"], 0)
            df["Debts"] = np.where(df["Debts"] < 0, df["Debts"], 0)
            df["TransDate"] = pd.to_datetime(df.TransDate).astype(str)

            df["UUID"] = [uuid.uuid4() for _ in range(len(df.index))]
            df["Institution"] = ["Scotia"] * len(df.index)
            df["CardNumber"] = ["4538********7050"] * len(df.index)

            arrage_columns = [
                "UUID",
                "Institution",
                "TransDate",
                "TransDetails",
                "Debts",
                "Credits",
                "CardNumber"
            ]
            df = df[arrage_columns]
            print(f'{df.shape[0]} rows processed...')
            
        return df


def process_data(file_path, columns, table_name):
    
    pc = Scotia_Preprocessor(file_path=file_path, columns=columns)
    df = pc.preprocess(file_type=table_name)

    pg = Postgres()
    pg.store_dataframe(df, table_name)

def process_current_diretory(data_directory, credit_columns, chequing_columns):
    count = 0
    for filename in os.listdir(data_directory):
        file_path = os.path.join(data_directory, filename)
        if os.path.isfile(file_path):
            if filename.split("-")[0] == "credit":
                process_data(file_path, credit_columns, "credit")
                count += 1
                print("---------------*****--------------")
            if filename.split("-")[0] == "chequing":
                process_data(file_path, chequing_columns, "chequing")
                count += 1
                print("---------------*****--------------")

    print(
        f"A total of {count} files in current directory has been loaded to database..."
    )


if __name__ == "__main__":

    directory = os.getcwd()
    data_directory = directory + "/src/data/scotia"

    CREDIT_COLUMNS = ["TransDate", "TransDetails", "Debts"]
    CHEQUING_COLUMNS = [
        "TransDate",
        "Withdrawals",
        "Deposits",
        "TransType",
        "TransDetails",
    ]

    process_current_diretory(data_directory=data_directory,credit_columns=CREDIT_COLUMNS, chequing_columns=CHEQUING_COLUMNS)
