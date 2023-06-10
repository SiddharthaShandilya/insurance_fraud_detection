import os
import yaml
import logging
import time
import pandas as pd
import json
import shutil


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
        print(f"Directory at path {path} has been deleted.")
    except OSError as e:
        print(f"Error: {path} : {e.strerror}")
