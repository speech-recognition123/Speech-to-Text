import sys
import os
import librosa as lb
from librosa.core import audio
import pandas as pd
import numpy as np
# Add the local_modules directory to the set of paths
# Python uses to look for imports.
import sys
sys.path.append('scripts')
sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))
app_logger = App_Logger("audio_loader.log").get_app_logger()


class AudioLoader:

	def __init__(self) -> None:
	        self.logger = App_Logger(
	            "audio_loader.log").get_app_logger()
		
	def tran_loader(self, filename):
	  	name_to_text = {}
	  	with open (filename, encoding="utf-8")as f:
	  	  f.readline()
		    for line in f:
		      name=line.split("</s>")[1]
		      name=name.replace('(', '')
		      name=name.replace(')', '')
		      name=name.replace('\n','')
		      name=name.replace(' ','')
		      text=line.split("</s>")[0]
		      text=text.replace("<s>","")
		      name_to_text[name]=text
		self.logger.info(f"train data loaded")
	    return name_to_text