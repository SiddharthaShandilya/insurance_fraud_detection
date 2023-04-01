import json, re, shutil, argparse, logging, random, os
from tqdm import tqdm
from src.utils.common import read_yaml, create_directories
from params import COLUMNS_WITH_STRING_DATATYPE
from configs.config import ARTIFACTS
import pandas as pd


class RawDataTransformation:

     """
               This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

               Written By: Siddhartha Shandilya
               Version: 1.0
               Revisions: None

               """

     def __init__(self):
        self.good_data_dir = os.path.join(ARTIFACTS["ARTIFACTS_DIR"],ARTIFACTS["DATABASE_DIR"]["DATABASE"],ARTIFACTS["DATABASE_DIR"]["GOOD_DATA_DIR"])
        self.bad_data_dir = os.path.join(ARTIFACTS["ARTIFACTS_DIR"],ARTIFACTS["DATABASE_DIR"]["DATABASE"],ARTIFACTS["DATABASE_DIR"]["BAD_DATA_DIR"])



     def replace_missing_with_null(self):
          """
                                           Method Name: replaceMissingWithNull
                                           Description: This method replaces the missing values in columns with "NULL" to
                                                        store in the table. We are using substring in the first column to
                                                        keep only "Integer" data for ease up the loading.
                                                        This column is anyways going to be removed during training.

                                            Written By: Siddhartha Shandilya
                                           Version: 1.0
                                           Revisions: None

                                                   """

          try:
                # Get a list of files in the directory
               onlyfiles = [f for f in os.listdir(self.good_data_dir)]
                # Loop through each file and modify the data
               for file in onlyfiles:
                    # Read the CSV file into a pandas DataFrame
                    data = pd.read_csv(os.path.join(self.good_data_dir, file))

                    for col in COLUMNS_WITH_STRING_DATATYPE:
                         # Replace missing values in columns with "NULL"
                         data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                    
                     # Write the modified data back to the same CSV file
                    data.to_csv(os.path.join(self.good_data_dir, file), index=None, header=True)
                    logging.info(f" Quotes added successfully!! : {file}")
               #log_file.write("Current Date :: %s" %date +"\t" + "Current time:: %s" % current_time + "\t \t" +  + "\n")
          except Exception as e:
               logging.info(f"Data Transformation failed because::{e}")
               #log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data Transformation failed because:: %s" % e + "\n")
               
