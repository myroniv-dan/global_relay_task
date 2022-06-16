import os.path


class Paths:
    DATA = "data"
    METADATA = os.path.join(DATA, "metadata")
    WAVS = os.path.join(DATA, "wavs")
    VADS = os.path.join(DATA, "vads")
    LANG_CLAS = os.path.join(DATA, "lang_clas")


class Processing:
    SAMPLING_RATE = 16000
