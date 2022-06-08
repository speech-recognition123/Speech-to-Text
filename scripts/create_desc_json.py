"""
Where speaker.trans.txt has in each line, file_key
"""

from __future__ import absolute_import, division, print_function
from log_help import App_Logger


import argparse
import json
import os
import sys
import wave
import librosa
import json
import pandas as pd
import numpy as np
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))

app_logger = App_Logger("../logs/create_desc_json.log").get_app_logger()


class create_desc_json:

    def __init__(self):
        '''
        # init
        # @param self
        # return: None
        # @exception: None
        # @note: None
        # @example: None     
        '''
        self.logger = App_Logger(
            "../logs/create_desc_json.log").get_app_logger()

    def translation_loader(self, filename):
        '''
        # Load the transcriptions
        # @param filename: the path of the transcriptions
        # return: a dictionary of the transcriptions
        '''
        name_to_text = {}
        with open(filename, encoding="utf-8")as f:
            f.readline()
            for line in f:
                name = line.split("</s>")[1]
                name = name.replace('(', '')
                name = name.replace(')', '')
                name = name.replace('\n', '')
                name = name.replace(' ', '')
                text = line.split("</s>")[0]
                text = text.replace("<s>", "")
                name_to_text[name] = text
                self.logger.info(f"cleaning {filename} file")
            return name_to_text

    def meta_data(self, trans, path):
        '''
        # Extract the meta-data
        # @param trans: clean transcription
        # @param path: location for audio files
        # return: lists of the meta data
        '''
        target = []
        features = []
        filenames = []
        duration_of_recordings = []
        for k in trans:
            filename = path+k + ".wav"
            filenames.append(filename)
            audio, fs = librosa.load(filename, sr=None)
            duration_of_recordings.append(float(len(audio)/fs))
            lable = trans[k]
            target.append(lable)
            self.logger.info(
                f"Extract the meta-data from transcription {path}")
        return filenames, target, duration_of_recordings

    def convert_to_json(self, data: pd.DataFrame, path: str):
        '''
        # convert dataframe to json
        # @param data: dataframe
        # @param path: path to save json
        # return: None
        # @exception: None
        '''
        try:
            with open(path, 'w') as out_file:
                for i in range(len(data['key'])):
                    line = json.dumps({'key': data['key'][i], 'duration': data['duration'][i],
                                       'text': data['text'][i]})
                    out_file.write(line + '\n')
                    self.logger.info(
                        f"Convert the dataframe to json file {path}")
        except KeyError:
            var = 0
