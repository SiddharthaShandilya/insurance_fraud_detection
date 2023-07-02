import json, re, shutil, argparse, logging, random, os
from tqdm import tqdm
from src.utils.common import read_yaml, create_directories, save_to_csv
from params import COLUMNS_WITH_STRING_DATATYPE
import pandas as pd
from sklearn.impute import SimpleImputer
from typing import List
import numpy as np


class RawDataPreProcessing:

    """
    This class shall be used for Pre-processing the Training Data before loading it in Database for model training!!.

    Written By: Siddhartha Shandilya
    Version: 1.0
    Revisions: None

    """

    def __init__(self, file_path_for_eda):
        """
        Pass the path of the fiel that is to be used for EDA
        """
        self.file_path_for_eda = file_path_for_eda

    def drop_unnecessary_columns(
        self, columns_to_drop: List[str], data
    ) -> pd.DataFrame:
        """
        Method Name: drop_unnecessary_columns
        Description: This method drops/removes the columns which cannot be used for model training

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None

        """

        try:
            # Get a data for model training in the directory
            logging.info("drop_unnecessary_columns function is called")
            # data = pd.read_csv(self.file_path_for_eda)
            data.drop(columns=columns_to_drop, inplace=True)
            logging.info("Sucessfully Dropped unnecessary columns !!!")
            # status = save_to_csv(dataframe = data, file_path = self.file_path_for_eda )
            return data
        except FileNotFoundError as e:
            logging.info(f"Dropping Columns failed because::{e}")
            # log_file.write("Current Date :: %s" %date +"\t" +"Current time:: %s" % current_time + "\t \t" + "Data Transformation failed because:: %s" % e + "\n")
            raise Exception(e)

    def imputing_empty_values_in_columns(
        self, columns_to_impute: List[str], data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Method Name: imputes categorical columns with missing values columns
        Description: This method imputes the columns which are having missing values be used for model training

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None

        """

        try:
            # Get a data for model training in the directory
            logging.info("imputing_empty_values_in_columns function is called")
            # replacing all the "?" with nan values
            data.replace("?", np.nan, inplace=True)
            # imputing columns
            for column in columns_to_impute:
                if data[column].dtype == "object":
                    imputer = SimpleImputer(strategy="most_frequent")
                else:
                    imputer = SimpleImputer(strategy="mean")

                data[f"{column}"] = imputer.fit_transform(
                    np.array(data[f"{column}"]).reshape(-1, 1)
                )
            logging.info("Sucessfully imputed unnecessary columns !!!")
            return data
        except Exception as e:
            logging.info(f"Dropping Columns failed because::{e}")
            raise Exception

    def mapping_and_encoding_categorical_columns(
        self, mapping_config, data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Map categorical columns in a DataFrame using a configuration dictionary.

        Args:
            dataframe (pandas.DataFrame): The DataFrame to perform the mapping on.
            mapping_config (dict): The configuration dictionary containing column mappings.
            columns_to_encode (List) : List of column names for encoding
        Returns:
            pandas.DataFrame: The DataFrame with mapped categorical columns.
        """
        logging.info("mapping_and_encoding_categorical_columns function is called")
        # dataframe = pd.read_csv(self.file_path_for_eda)

        mapped_df = (
            data.copy()
        )  # Create a copy of the DataFrame to avoid modifying the original
        cat_df = pd.DataFrame()
        columns_to_encode = data.select_dtypes(include=["object"]).columns.tolist()
        try:
            for column, mapping in mapping_config.items():
                mapped_df[column] = mapped_df[column].map(mapping)
            logging.info("Succesfully mapped categorical_columns")
            for col in columns_to_encode:
                encoded_df = pd.get_dummies(mapped_df[col], prefix=col, drop_first=True)
                cat_df = pd.concat([cat_df, encoded_df], axis=1)
            # getting columns with numerical values
            num_df = data.select_dtypes(include=["int64"]).copy()
            # concatinating both the encode columns and integer columns in to a single dataframe
            final_df = pd.concat([num_df, cat_df], axis=1)
            logging.info("Succesfully encoded categorical columns function")
            return final_df

        except KeyError as e:
            raise KeyError(
                f"Column '{column}' not found in DataFrame. Please check the column names and the configuration dictionary."
            ) from e

        except Exception as e:
            raise Exception(
                "An error occurred while mapping categorical columns."
            ) from e

        return mapped_df
