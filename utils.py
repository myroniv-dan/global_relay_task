import os


# https://stackoverflow.com/questions/12265451/ask-forgiveness-not-permission-explain
def assure_path_exist(path: str):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
