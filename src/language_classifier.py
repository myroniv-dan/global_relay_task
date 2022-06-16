import logging
import os

import numpy as np
import pandas as pd
import torch

from config import Processing, Paths
from utils import assure_path_exist


class LanguageClassifier:

    def run(self):

        torch.backends.quantized.engine = 'qnnpack'

        model, lang_dict, lang_group_dict, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                                                  model='silero_lang_detector_95',
                                                                  force_reload=True)

        get_language_and_group, read_audio = utils

        for lang in os.listdir(Paths.METADATA):

            language = lang[0:-4]

            df = pd.DataFrame(columns=['file', 'language', 'language_group', 'error'])

            for file in os.listdir(os.path.join(Paths.WAVS, language)):

                logging.info(f'Running language classifier for {file}')

                try:
                    wav = read_audio(os.path.join(Paths.WAVS, language, file), sampling_rate=Processing.SAMPLING_RATE)
                    languages, language_groups = get_language_and_group(wav, model, lang_dict, lang_group_dict, top_n=2)

                    data = {
                        'file': [file],
                        'language': [languages],
                        'language_group': [language_groups],
                        'error': [None]
                    }

                except Exception as e:

                    data = {
                        'file': [file],
                        'language': [np.nan],
                        'language_group': [np.nan],
                        'error': [e]
                    }

                    logging.error(e)

                df = pd.concat([df, pd.DataFrame(data=data)], axis=0)

            logging.info(f'Saving language classified for {language}')

            assure_path_exist(Paths.LANG_CLAS)

            df.reset_index(inplace=True)
            df.to_csv(os.path.join(Paths.LANG_CLAS, f'{language}.csv'))
