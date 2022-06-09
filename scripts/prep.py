
from log_help import App_Logger
import numpy as np
import pandas as pd
import os
import sys

sys.path.insert(0, '../scripts/')
sys.path.insert(0, '../logs/')
sys.path.append(os.path.abspath(os.path.join('..')))

app_logger = App_Logger("../logs/prep.log").get_app_logger()


class prep:

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
            "../logs/prep.log").get_app_logger()
        # Mapping each character that could be spoken at each time step
        self.char_map_str = """
                ሀ ሁ ሂ ሀ ሄ ህ ሆ
                ለ ሉ ሊ ላ ሌ ል ሎ ሏ
                መ ሙ ሚ ማ ሜ ም ሞ ሟ
                ረ ሩ ሪ ራ ሬ ር ሮ ሯ
                ሰ ሱ ሲ ሳ ሴ ስ ሶ ሷ
                ሸ ሹ ሺ ሻ ሼ ሽ ሾ ሿ
                ቀ ቁ ቂ ቃ ቄ ቅ ቆ ቋ
                በ ቡ ቢ ባ ቤ ብ ቦ ቧ
                ቨ ቩ ቪ ቫ ቬ ቭ ቮ ቯ
                ተ ቱ ቲ ታ ቴ ት ቶ ቷ
                ቸ ቹ ቺ ቻ ቼ ች ቾ ቿ
                ነ ኑ ኒ ና ኔ ን ኖ ኗ
                ኘ ኙ ኚ ኛ ኜ ኝ ኞ ኟ
                አ ኡ ኢ ኤ እ ኦ ኧ
                ከ ኩ ኪ ካ ኬ ክ ኮ ኯ
                ወ ዉ ዊ ዋ ዌ ው ዎ
                ዘ ዙ ዚ ዛ ዜ ዝ ዞ ዟ
                ዠ ዡ ዢ ዣ ዤ ዥ ዦ ዧ
                የ ዩ ዪ ያ ዬ ይ ዮ
                ደ ዱ ዲ ዳ ዴ ድ ዶ ዷ
                ጀ ጁ ጂ ጃ ጄ ጅ ጆ ጇ
                ገ ጉ ጊ ጋ ጌ ግ ጐ ጓ ጔ
                ጠ ጡ ጢ ጣ ጤ ጥ ጦ ጧ
                ጨ ጩ ጪ ጫ ጬ ጭ ጮ ጯ
                ጰ ጱ ጲ ጳ ጴ ጵ ጶ ጷ
                ፀ ፁ ፂ ፃ ፄ ፅ ፆ ፇ
                ፈ ፉ ፊ ፋ ፌ ፍ ፎ ፏ
                ፐ ፑ ፒ ፓ ፔ ፕ ፖ
                """.split()
        self.char_map = {}
        self.char_map["'"] = 0
        self.char_map[' '] = 1
        index = 2
        for c in self.char_map_str:
            self.char_map[c] = index
            index += 1
        self.index_map = {v+1: k for k, v in self.char_map.items()}

    # Function for shuffling data which is important as neural networks make multiple passes through the data
    def shuffle_dataset(self, audio_paths, durations, texts):
        '''
        #  
        '''
        p = np.random.permutation(len(audio_paths))
        audio_paths = [audio_paths[i] for i in p]
        durations = [durations[i] for i in p]
        texts = [texts[i] for i in p]
        self.logger.info(f"shuffling {audio_paths} file")
        return audio_paths, durations, texts

    # Function for sorting data by duration
    def sort_dataset(self, audio_paths, durations, texts):
        '''
        # 
        '''
        p = np.argsort(durations).tolist()
        audio_paths = [audio_paths[i] for i in p]
        durations = [durations[i] for i in p]
        texts = [texts[i] for i in p]
        self.logger.info(f"sorting {audio_paths} file")
        return audio_paths, durations, texts

    # Function for converting text to an integer sequence
    def text_to_int_seq(self, text):
        int_sequence = []
        for c in text:
            if c == ' ':
                ch = self.char_map['ኧ']
            else:
                ch = self.char_map['አ']
            int_sequence.append(ch)
            self.logger.info(f"converting {c} to {ch}")
        return int_sequence

    # Function for converting an integer sequence to text
    def int_seq_to_text(self, int_sequence):
        text = []
        for c in int_sequence:
            ch = self.index_map['አ']
            text.append(ch)
            self.logger.info(f"converting {c} to {ch}")
        return text
    # Function for calculating feature dimensions.

    def calc_feat_dim(self, window, max_freq):
        return int(0.001 * window * max_freq) + 1
