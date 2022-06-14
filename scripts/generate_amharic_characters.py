"""

This module is supposed to read the target
transcriptions and generate the corresponding 
index => character mapping. 

Jun-3-2022

author: Henok
"""


import pandas as pd


class GenerateCharacters:
    def __init__(self) -> None:
        self.characters = []
        self.md_path = None

    def generate_md(self):
        if self.md_path.endswith('.json'):
            with open(self.md_path, 'r') as f:
                md = json.load(f)
                self.df = pd.DataFrame(md)
        elif self.md_path.endswith('.csv'):
          self.df = pd.read_csv(self.md_path)
        # print(self.df['text'].values)
        for ele in self.df['text'].values:
            yield ele

    def get_texts(self, target_text):
        
        target_text = list(target_text)
        # print(target_text)
        for char in target_text:
            self.characters.append(char)

    def generate(self):
        for data in self.generate_md():
            # print(data)
            self.get_texts(data)

    def get_characters(self, md_path):
        self.md_path = md_path
        self.generate()
        self.characters = sorted(self.characters)
        return list(set((self.characters)))


