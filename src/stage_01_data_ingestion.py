import argparse
import os
import logging
from configs.config import ARTIFACTS, SOURCE_DATA_DIR, VALID_FILE_SCHEMA_PATH
from src.data_processing.data_validation import Raw_Data_Validation
from src.data_processing.data_transformation import RawDataTransformation


STAGE = "stage_01_data_ingestion" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def data_validation(valid_data_schema_path,remote_data_path):
    """
        Method Name: valid_data
        Description: This method validates the input data file based on "Schema" file.
        Output:Bolean -> whether the data file is valid or not
                                Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        
    """
    data_validation = Raw_Data_Validation(remote_data_path, valid_data_schema_path)
    filename_pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColName = data_validation.get_value_from_schema()
    logging.info(f"we are getting followign scehma {filename_pattern},{LengthOfDateStampInFile},{LengthOfTimeStampInFile},{NumberofColumns},{ColName}")
    
    onlyfiles = [f for f in os.listdir(remote_data_path)]
    
    for filename in onlyfiles:
        # Define a list of validation functions to be executed in sequence
        #here each lambda function wraps each validatin function with the required arguments
        validation_functions = [
        lambda: data_validation.raw_file_validation(filename, LengthOfDateStampInFile, LengthOfTimeStampInFile),
        lambda: data_validation.raw_file_column_length_validation(NumberofColumns),
        lambda: data_validation.raw_file_column_name_validation(colName=ColName),
        lambda: data_validation.validate_missing_values_in_whole_column()
        ]
        # Execute each validation function in the list and store the results in a list
        validation_results = [func() for func in validation_functions]

        if all(result == 1 for result in validation_results):
            logging.info(f"Raw Data Validation Completed for {filename}")
        else:
            logging.info(f"Raw Data Validation Failed for {filename}")



def data_transformation():
    data_transformation = RawDataTransformation()
    logging.info("Raw Data Transformation Started")
    data_transformation.replace_missing_with_null()
    logging.info("!!!Raw Data Transformation Completed !!!")

def main():
    ## read config files
    logging.info("Raw Data Validation Started")
    data_validation(VALID_FILE_SCHEMA_PATH,SOURCE_DATA_DIR)
    #Raw Data Transformation Started
    data_transformation()
    return 1


if __name__ == '__main__':
    
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e