import os.path

from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d-%H-%M")


class Paths:
    DATA = os.path.join("data", now)
    METADATA = os.path.join(DATA, "metadata")
    WAVS = os.path.join(DATA, "wavs")
    VADS = os.path.join(DATA, "vads")
    LANG_CLAS = os.path.join(DATA, "lang_clas")


class Processing:
    SAMPLING_RATE = 16000
