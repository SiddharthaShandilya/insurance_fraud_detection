import os
import yaml
import logging
import time
import pandas as pd
import json
import shutil, sqlite3, csv

from datetime import datetime


def read_yaml(path_to_yaml: str) -> dict:
    """
    Reads Yaml at the given path.

    :param
        path_to_yaml(str): The path of the directory to delete.
    :return:
        Content (Dict): It contins the data present in the given Yaml file
    """
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content


def create_directories(path_to_directories: list) -> None:
    """
    Creates a directory at the given path.

    :param
        path(str): The path of the directory to delete.
    :return:
        None
    """
    logging.info("create_dictionry function is called ")
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict) -> None:
    """
    Saves a Data into json at the given path.

    :param
        path (str): The path of the directory to store json.
        data (Dict): Data that need to be stored in json
    :return:
         None
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")


def delete_directory(path: str) -> None:
    """
    Deletes a directory at the given path.

    :param
        path(str): The path of the directory to delete.
    :return:
        None
    """
    try:
        shutil.rmtree(path)
        logging.info(f"Directory at path {path} has been deleted.")
    except OSError as e:
        logging.exception(f"Error: {path} : {e.strerror}")


def export_database_to_csv(database_file, table_name, output_file):
    """
    Export data from a database table to a CSV file.

    Args:
        database_file (str): The path to the SQLite database file.
        table_name (str): The name of the table to export.
        output_file (str): The path to the output CSV file.
    """
    try:
        logging.info("export_database_to_csv from utils is called")
        # Connect to the database
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Fetch data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        # Write data to CSV file
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(data)

        logging.info(
            f"file from {table_name} table is succesfully stored at {output_file}"
        )
    except sqlite3.Error as e:
        logging.exception(f"An error occurred while exporting data: {e}")

    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def save_to_csv(dataframe, file_path):
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing the data to be saved.
        file_path (str): The path to the CSV file.

    Returns:
        bool: True if the data was successfully saved, False otherwise.
    """
    try:
        dataframe.to_csv(file_path, index=False)
        return True
    except IOError as ioe:
        logging.info(
            f"An error occurred while saving the data to CSV file: {file_path}: {ioe}"
        )
        raise IOError


def generate_unique_name(first_name, extension):
    """
    Generate a unique name based on the current date and time.

    Args:
        firstname (str): The base filename.

    Returns:
        str: The unique filename incorporating the base filename, current date, and time.

    Example:
        >>> generate_unique_filename("data", ".txt")
        'data_20220329_134500.txt'
    """
    try:
        logging.info("generate_unique_filename function is called")
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )  # Generate timestamp in the format YYYYMMDD_HHMMSS
        filename = f"{first_name}_{timestamp}{extension}"
        logging.info("!! Successfully generated unique_filename !!")
        return filename

    except Exception as e:
        logging.error(
            f"An error occurred while generating the unique filename: {str(e)}"
        )
        raise NameError


def read_json_file(file_path):
    """
    Reads a JSON file and returns its data in dictionary format.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The data from the JSON file as a dictionary.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data
