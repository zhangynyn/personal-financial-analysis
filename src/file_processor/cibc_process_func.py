import pandas as pd
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

        return df


def process_credit_data(credit_path, columns, table_name):
    data_path = project_root.joinpath(project_root, credit_path)

    pc = Cibc_Preprocessor(file_path=data_path, columns=columns)
    credit_df = pc.preprocess()

    pg = Postgres()
    pg.store_dataframe(credit_df, table_name)


# Chequing
def process_chequing_data(chequing_path, columns, table_name):
    data_path = project_root.joinpath(project_root, chequing_path)

    pc = Cibc_Preprocessor(file_path=data_path, columns=columns)
    chequing_df = pc.preprocess()
    print(chequing_df.head())

    pg = Postgres()
    pg.store_dataframe(chequing_df, table_name)


if __name__ == "__main__":
    project_root = Path(".")

    CREDIT_COLUMNS = ["TransDate", "TransDetails", "Debits", "Credits", "CardNumber"]
    CREDIT_PATH = "src/data/cibc-credit.csv"
    process_credit_data(CREDIT_PATH, CREDIT_COLUMNS, "cibc_credit")

    CHEQUING_COLUMNS = ["TransDate", "TransDetails", "Withdrawals", "Deposits"]
    CHEQUING_PATH = "src/data/cibc-chequing.csv"
    process_chequing_data(CHEQUING_PATH, CHEQUING_COLUMNS, "chequing")
