import pandas as pd
from abc import ABC, abstractmethod
from typing import List


class FileProcessor(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_file(self):
        df = pd.read_csv(self.file_path, header=None)
        return df

    @abstractmethod
    def preprocess(self, df: pd.DataFrame, columns: List[str]):
        pass