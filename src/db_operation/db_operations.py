import shutil
import sqlite3
from sqlite3.dbapi2 import Connection
from datetime import datetime
import os
import csv
import logging
from configs.config import ARTIFACTS
from src.utils.common import create_directories


class DbOperations:
    """
    This class shall be used for handling all the SQL operations.

    Written By: Siddhartha Shandilya
    Version: 1.0
    Revisions: None

    """

    def __init__(self):
        self.database: str = "mydb"
        self.path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"], ARTIFACTS["DATABASE_DIR"]["SQL_DATABASE_DIR"]
        )
        self.bad_file_path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"],
            ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
            ARTIFACTS["LOCAL_DATA_DIR"]["BAD_DATA_DIR"],
        )

    def database_connection(self, database: str = None) -> Connection:
        """

        Creates a connection to a SQLite database with the given name. If the database already exists, the connection to it is opened.

         Args:
         - databaseName (str): The name of the database to connect to.

         Returns:
         - conn (sqlite3.Connection): A connection to the database.

         Raises:
         - ConnectionError: If there's an error connecting to the database.

         Written By: Siddhartha Shandilya
         Version: 1.0
         Revisions: None
        """
        conn = None
        logging.info(" database_connection function is called")
        try:
            if database is None:
                database = self.database
            logging.info(
                f"function called for creating connection to database : {database}"
            )
            create_directories([self.path])
            database_path = os.path.join(self.path, database)
            conn = sqlite3.connect(database_path + ".db")
            logging.info(f"Opened : {database} database successfully ")
            return conn
        except ConnectionError:
            logging.info(f"Error while connecting to database: {ConnectionError}")
            raise ConnectionError

    def create_table_db(
        self, database_name, column_names_with_data_type: dict, table_name: str
    ):
        """
        Method to create a table in the given database which will be used to insert the Good data after raw data validation.

        Args:
            DatabaseName (str): Name of the database
            column_names_with_data_type (dict): Dictionary containing column names and their data types

        Returns:
            None

        Raises:
            Exception: If there is an error while creating a table

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        """
        try:
            conn = self.database_connection(database=database_name)
            c = conn.cursor()
            c.execute(
                f"SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = '{table_name}'"
            )

            if c.fetchone()[0] == 1:
                conn.close()
                logging.info("Tables created successfully!!")
                logging.info(f"Closed {database_name} database successfully")
            else:
                for key in column_names_with_data_type.keys():
                    type_ = column_names_with_data_type[key]
                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try:
                        conn.execute(
                            'ALTER TABLE {table_name} ADD COLUMN "{column_name}" {dataType}'.format(
                                table_name=table_name,
                                column_name=key,
                                dataType=type_,
                            )
                        )
                    except Exception as e:
                        logging.info(e)
                        conn.execute(
                            "CREATE TABLE  {table_name} ({column_name} {dataType})".format(
                                table_name=table_name,
                                column_name=key,
                                dataType=type_,
                            )
                        )

                conn.close()
                logging.info(f"{table_name} table created successfully!!")
                logging.info(f"Closed {database_name} database successfully")

        except Exception as e:
            logging.info(f"Error while creating table: {e}")
            conn.close()
            logging.info("Closed {database_name} database successfully")
            raise e

    def insert_into_table(self, database_name, table_name, data_directory_path):
        """
        Inserts the data from the GoodData directory into the Good_Raw_Data table of the given database.

        Args:
            database (str): Name of the database to connect to.-
            data_directory_path (str) : Path to the directory where validated data is stored

        Returns:
            None

        Raises:
            Exception: If there is any issue while inserting data into the table.

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None

        """
        logging.info("insert_into_table function is called")
        conn = self.database_connection(database=database_name)
        bad_file_path = self.bad_file_path
        onlyfiles = [f for f in os.listdir(data_directory_path)]

        for file in onlyfiles:
            try:
                with open(data_directory_path + "/" + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in line[1]:
                            try:
                                conn.execute(
                                    "INSERT INTO {good_raw_data} values ({values})".format(
                                        good_raw_data=table_name,
                                        values=(list_),
                                    )
                                )
                                conn.commit()
                            except Exception as e:
                                logging.error(e)
                                raise e
                    logging.info(f"{file}: value loaded successfully!!")

            except Exception as e:
                conn.rollback()
                logging.info(f"Error while creating table: {e}")
                shutil.move(os.path.join(data_directory_path, file), bad_file_path)
                logging.info(f"File Moved Successfully{file}")
                conn.close()

        conn.close()

    def selecting_data_from_table_into_csv(
        self, database: str, table_name: str, data_file_dir_name, file_name
    ) -> None:
        """
         This method exports the data from the table to a CSV file to a given location.

        Args:
         database (str) : Name of the database from where data needs to be exported
         data_file_dir_name (str) : Path of the directory where the file is to be stored
         file_name (str) : name of the file where the data is to be stored

         Returns:
             None

         Raises:
             Exception: If there is an error in exporting data

         Written By: Siddhartha Shandilya
         Version: 1.0
         Revisions: None
        """

        self.file_from_db = data_file_dir_name
        self.file_name = file_name
        self.file_from_db_path = os.path.join(self.file_from_db, self.file_name)

        try:
            conn = self.database_connection(database=database)
            sql_select = f"SELECT *  FROM {table_name}"
            cursor = conn.cursor()

            cursor.execute(sql_select)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            # Make the CSV ouput directory
            if not os.path.isdir(self.file_from_db):
                os.makedirs(self.file_from_db)

            # Open CSV file for writing.
            csv_file = csv.writer(
                open(self.file_from_db_path, "w", newline=""),
                delimiter=",",
                lineterminator="\r\n",
                quoting=csv.QUOTE_ALL,
                escapechar="\\",
            )

            # Add the headers and data to the CSV file.
            csv_file.writerow(headers)
            csv_file.writerows(results)
            conn.close()
            logging.info("File exported successfully!!!")

        except Exception as e:
            logging.info(f"File exporting failed. Error : {e}")
            conn.close()
