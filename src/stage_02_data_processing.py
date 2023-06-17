import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import (
    read_yaml,
    create_directories,
    save_to_csv,
    generate_unique_name,
)
import random
from src.data_processing.data_preprocessing import RawDataPreProcessing
from configs.config import *
import pandas as pd

STAGE = "STAGE_NAME"  ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)


def main():
    ## read congfig files
    validated_and_transformed_data_file_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["DATABASE_DIR"]["SQL_DATABASE_DIR"],
        ARTIFACTS["DATABASE_DIR"]["SQL_TRAINING_FILE_DIR"],
        ARTIFACTS["DATABASE_DIR"]["SQL_TRAINING_FILE_NAME"],
    )
    final_data_dir_path_for_model_training = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["DATABASE_DIR"]["DATABASE"],
        ARTIFACTS["DATABASE_DIR"]["FINAL_EDA_DATA_DIR"],
    )
    initial_data_frame = pd.read_csv(validated_and_transformed_data_file_path)

    data_processing = RawDataPreProcessing(validated_and_transformed_data_file_path)
    # dropping unneccessary columns
    data_with_dropped_columns = data_processing.drop_unnecessary_columns(
        columns_to_drop=COLUMNS_TO_IGNORE_FOR_MODEL_TRAINING, data=initial_data_frame
    )
    # imputing categorical columns
    imputed_data = data_processing.imputing_empty_values_in_columns(
        columns_to_impute=COLUMNS_TO_IMPUTE_FOR_MODEL_TRAINING,
        data=data_with_dropped_columns,
    )
    # mapping and encoding the categorical columns
    mapped_encoded_data_frame = (
        data_processing.mapping_and_encoding_categorical_columns(
            mapping_config=MAPPING_CATEGORICAL_COLUMNS,
            data=imputed_data,
            columns_to_encode=COLUMNS_TO_ENCODE_FOR_MODEL_TRAINING,
        )
    )
    # performing some more EDA based on graphs
    final_data_dir_path = final_data_dir_path_for_model_training
    os.makedirs(final_data_dir_path, exist_ok=True)
    final_data_file_name = generate_unique_name(
        first_name="final_data_file", extension=".csv"
    )
    final_data_file_path = os.path.join(final_data_dir_path, final_data_file_name)
    save_to_csv(mapped_encoded_data_frame, file_path=final_data_file_path)


if __name__ == "__main__":
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
