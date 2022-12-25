import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random

class DataLoading:
    """
    class Name: DataLoading
    Description: This class handles loading the data from source/validated before moving it to local file storage.
    """
    def __init__(self, source_dir, local_dir):
        self.source_dir=source_dir
        self.local_dir=local_dir

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source and moves it to local file storage.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

        Written By: siddhartha shandilya
        Version: 1.0
        Revisions: None

        """

        pass
        

