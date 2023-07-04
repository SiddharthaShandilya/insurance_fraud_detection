import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import (
    create_directories,
    save_to_csv,
)
import random
from src.data_processing.data_preprocessing import RawDataPreProcessing
from src.db_operation.db_operations import DbOperations
from configs.config import ARTIFACTS
from params import *
import pandas as pd

STAGE = "stage_02_data_processing"  ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)


def main():
    ## read congfig files
    database_name = ARTIFACTS["DATABASE_DIR"]["SQL_TRAINING_DATABASE_NAME"]
    validated_data_raw_table_name = ARTIFACTS["DATABASE_DIR"][
        "SQL_TRAINING_VALIDATED_DATA_TABLE_NAME"
    ]
    validated_data_dir_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
        ARTIFACTS["LOCAL_DATA_DIR"]["VALIDATED_DATA_DIR"],
    )
    validated_data_file_name = ARTIFACTS["LOCAL_DATA_DIR"]["VALIDATED_DATA_FILE_NAME"]
    # fetching values for processed data directory
    processed_data_raw_table_name = ARTIFACTS["DATABASE_DIR"][
        "SQL_TRAINING_PROCESSED_DATA_TABLE_NAME"
    ]
    processed_data_dir_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
        ARTIFACTS["LOCAL_DATA_DIR"]["PROCESSED_DATA_DIR"],
    )
    processed_data_file_name = ARTIFACTS["LOCAL_DATA_DIR"]["PROCESSED_DATA_FILE_NAME"]
    validated_and_transformed_data_file_path = os.path.join(
        validated_data_dir_path, validated_data_file_name
    )
    processed_data_file_path = os.path.join(
        processed_data_dir_path, processed_data_file_name
    )
    db_ops = DbOperations()
    logging.info("Extracting csv file from table")
    # export data in table to csvfile
    db_ops.selecting_data_from_table_into_csv(
        database=database_name,
        table_name=validated_data_raw_table_name,
        data_file_dir_name=validated_data_dir_path,
        file_name=validated_data_file_name,
    )
    initial_data_frame = pd.read_csv(validated_and_transformed_data_file_path)

    data_processing = RawDataPreProcessing(validated_and_transformed_data_file_path)
    # dropping unneccessary columns
    data_with_dropped_columns: pd.DataFrame = data_processing.drop_unnecessary_columns(
        columns_to_drop=COLUMNS_TO_IGNORE_FOR_MODEL_TRAINING, data=initial_data_frame
    )
    # imputing categorical columns
    columns_to_impute = [
        column
        for column in data_with_dropped_columns.columns
        if data_with_dropped_columns[column].isnull().any()
    ]
    imputed_data: pd.DataFrame = data_processing.imputing_empty_values_in_columns(
        columns_to_impute=columns_to_impute,
        data=data_with_dropped_columns,
    )
    # mapping and encoding the categorical columns
    mapped_encoded_data_frame: pd.DataFrame = (
        data_processing.mapping_and_encoding_categorical_columns(
            mapping_config=MAPPING_CATEGORICAL_COLUMNS,
            data=imputed_data,
        )
    )
    os.makedirs(processed_data_dir_path, exist_ok=True)
    save_to_csv(mapped_encoded_data_frame, file_path=processed_data_file_path)
    # saving all the processed data in the database
    column_name_with_data_types = {}
    for column in mapped_encoded_data_frame.columns:
        column_name_with_data_types[column] = "Integer"
    db_ops.create_table_db(
        database_name=database_name,
        column_names_with_data_type=column_name_with_data_types,
        table_name=processed_data_raw_table_name,
    )
    logging.info("Table creation Completed!!")
    logging.info("Insertion of Data into Table started!!!!")
    # insert csv files in the table
    db_ops.insert_into_table(
        database_name=database_name,
        table_name=processed_data_raw_table_name,
        data_directory_path=processed_data_dir_path,
    )
    logging.info("Insertion of Data into Table Completed!!!!")


if __name__ == "__main__":
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
