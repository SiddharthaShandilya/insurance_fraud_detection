import argparse
import os
import logging
from configs.config import ARTIFACTS, SOURCE_DATA_DIR, VALID_FILE_SCHEMA_PATH
from src.data_processing.data_validation import RawDataValidation
from src.data_processing.data_transformation import RawDataTransformation
from src.db_operation.db_operations import DbOperations
from src.utils.common import delete_directory

STAGE = "stage_01_data_ingestion" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def data_validation(valid_data_schema_path,remote_data_path):
    """
        This method validates the input data file based on "Schema" file.

        Output:
            Bolean -> whether the data file is valid or not
            colName: List of col names extracted from given schema file

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        
    """
    data_validation = RawDataValidation(remote_data_path, valid_data_schema_path)
    filename_pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColName = data_validation.get_value_from_schema()
    logging.info(f"we are getting followign scehma {filename_pattern},{LengthOfDateStampInFile},{LengthOfTimeStampInFile},{NumberofColumns},{ColName}")
    
    onlyfiles = [f for f in os.listdir(remote_data_path)]
    
    for filename in onlyfiles:
        # Define a list of validation functions to be executed in sequence
        #here each lambda function wraps each validatin function with the required arguments
        validation_functions = [
        lambda filename=filename: data_validation.raw_file_validation(filename, LengthOfDateStampInFile, LengthOfTimeStampInFile),
        lambda: data_validation.raw_file_column_length_validation(NumberofColumns),
        lambda: data_validation.raw_file_column_name_validation(colName=ColName),
        lambda: data_validation.validate_missing_values_in_whole_column()
        ]
        # Execute each validation function in the list and store the results in a list
        validation_results = [func() for func in validation_functions]

        if all(result == 1 for result in validation_results):
            logging.info(f"Raw Data Validation Completed for {filename}")
            return True, ColName
        else:
            logging.info(f"Raw Data Validation Failed for {filename}")
            return False, None



def data_transformation():
    """
    This function performs raw data transformation by replacing missing values with null values.
    It uses the RawDataTransformation class to perform the transformation.

    Returns:
    None

   Example usage:
    >>> data_transformation()
    
    """
    data_transformation = RawDataTransformation()
    logging.info("Raw Data Transformation Started")
    data_transformation.replace_missing_with_null()
    logging.info("!!!Raw Data Transformation Completed !!!")

def storing_good_data_to_db_and_delete_dir(col_names, good_data_dir):
    """
    Store good data into the database table by creating the table and inserting data.

    Args:
    col_names: A list of column names for the table.

    Returns:
    None

    Raises:
    Any exceptions raised by the DbOperations methods.

    Example usage:
    >>> col_names = ['col1', 'col2', 'col3']
    >>> storing_good_data_to_db(col_names)
    """
    try:
        db_ops = DbOperations()
        raw_data_validation = RawDataValidation(SOURCE_DATA_DIR, VALID_FILE_SCHEMA_PATH)
        database_name = ARTIFACTS["DATABASE_DIR"]["SQL_TRAINING_DATABASE_NAME"]
        db_ops.create_table_db(database_name=database_name, column_names=col_names)
        logging.info("Table creation Completed!!")
        logging.info("Insertion of Data into Table started!!!!")
        # insert csv files in the table
        db_ops.insert_into_table_good_data(database=database_name)
        logging.info("Insertion in Table completed!!!")
        delete_directory(good_data_dir)
        logging.info("Good_Data folder deleted!!!")
        logging.debug("Moving bad files to Archive and deleting Bad_Data folder!!!")
        # Move the bad files to archive folder
        raw_data_validation.move_bad_files_to_archive_bad()
        logging.info( "Bad files moved to archive!! Bad folder Deleted!!")
        logging.info("Validation Operation completed!!")
        logging.info( "Extracting csv file from table")
        # export data in table to csvfile
        db_ops.selecting_data_from_table_into_csv(database=database_name)
    except Exception as e:
        logging.info(e)
        raise e
    

def main():
    ## read config files
    
    logging.info("Raw Data Validation Started")
    good_data_dir = os.path.join(ARTIFACTS["ARTIFACTS_DIR"],ARTIFACTS["DATABASE_DIR"]["DATABASE"],ARTIFACTS["DATABASE_DIR"]["GOOD_DATA_DIR"])

    valid_data, col_names = data_validation(VALID_FILE_SCHEMA_PATH,SOURCE_DATA_DIR)
    if valid_data:
        #Raw Data Transformation Started
        data_transformation()
        storing_good_data_to_db_and_delete_dir(col_names, good_data_dir)
        return 1


if __name__ == '__main__':
    
    try:
        logging.info("\n********************")
        logging.info(f">>>>>  {STAGE} started <<<<<")
        main()
        logging.info(f">>>>>  {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e