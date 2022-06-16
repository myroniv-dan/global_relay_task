import os


# making sure path exist in 'ask forgiveness style'
def assure_path_exist(path: str):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
