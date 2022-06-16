import logging
import os

import numpy as np
import pandas as pd
import torch

from config import Processing, Paths
from utils import assure_path_exist


class VAD:
    def detect(self):

        # setting up Silero Voice Activity Detector model
        model, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad", force_reload=True)
        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

        for lang in os.listdir(Paths.METADATA):

            language = lang[0:-4]

            df = pd.DataFrame(columns=["file", "has_speech", "error"])

            for file in os.listdir(os.path.join(Paths.WAVS, language)):

                # there is problem with reading one wav file and vad model fails
                # american_vad.csv -> OSR_us_000_0058_8k.wav (WAVE: RIFF header not found)

                logging.info(f"Running VAD for {file}")

                try:
                    wav = read_audio(os.path.join(Paths.WAVS, language, file), sampling_rate=Processing.SAMPLING_RATE)
                    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=Processing.SAMPLING_RATE)

                    data = {"file": [file], "has_speech": [bool(speech_timestamps)], "error": [None]}

                except Exception as e:
                    data = {"file": [file], "has_speech": [np.nan], "error": [e]}
                    logging.error(e)

                df = pd.concat([df, pd.DataFrame(data=data)], axis=0)

            logging.info(f"Saving VAD for {language}")

            assure_path_exist(Paths.VADS)
            df.reset_index(inplace=True)
            df.to_csv(os.path.join(Paths.VADS, f"{language}.csv"))
