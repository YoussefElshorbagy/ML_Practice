import os
import sys
import pickle

from src.misc.exceptions import CustomException
from src.misc.logger import logging


def save_object(file_path, obj):
    try:

        dir = os.path.dirname(file_path)
        os.makedirs(dir, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info(f"Saved pickle object at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            pickle.load(file_path)

        logging.info(f"Loaded pickle object from {file_path}")

    except Exception as e:
        raise CustomException(e, sys)