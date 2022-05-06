import pandas as pd
import os
import uuid
from pathlib import Path
from src.db.postgres import Postgres
from src.file_processor.file_process_func import FileProcessor


class Cibc_Preprocessor(FileProcessor):
    def __init__(self, file_path: str, columns):
        super().__init__(file_path)
        self.columns = columns

    def preprocess(self):
        df = self.load_file()
        df.columns = self.columns

        df = df.fillna(0)
        df["UUID"] = [uuid.uuid4() for _ in range(len(df.index))]
        df["Institution"] = ["CIBC"] * len(df.index)
        arrage_columns = ["UUID", "Institution"] + self.columns
        df = df[arrage_columns]
        print(f'{df.shape[0]} rows processed...')

        return df


def process_data(file_path, columns, table_name):

    pc = Cibc_Preprocessor(file_path=file_path, columns=columns)
    df = pc.preprocess()

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

    CREDIT_COLUMNS = ["TransDate", "TransDetails", "Debts", "Credits", "CardNumber"]
    CHEQUING_COLUMNS = ["TransDate", "TransDetails", "Withdrawals", "Deposits"]

    directory = os.getcwd()
    data_directory = directory + "/src/data/cibc"

    process_current_diretory(data_directory=data_directory,credit_columns=CREDIT_COLUMNS, chequing_columns=CHEQUING_COLUMNS)
