import re

import pandas as pd


class TranscriptionCleaner:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.df = dataframe.copy()

    def get_dataframe(self) -> pd.DataFrame:
        return self.df

    def trim_spaces(self, text_column_name: str) -> None:
        self.df[text_column_name] = self.df[text_column_name].apply(
            lambda transcription_text: transcription_text.strip()
        )

    def remove_double_spaces(self, text_column_name: str) -> None:
        self.df[text_column_name] = self.df[text_column_name].apply(
            lambda transcription_text: re.sub(" +", " ", transcription_text)
        )
