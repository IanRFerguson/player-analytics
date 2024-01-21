from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from typing import Optional
from pandas import DataFrame
from utilities.logger import logger
import os

#####

LOAD_BEHAVIOR = {
    "append": "WRITE_APPEND",
    "truncate": "WRITE_TRUNCATE",
    "drop": "WRITE_TRUNCATE",
}


class BigQuery:
    def __init__(
        self,
        service_credentials: str,
        project: Optional[str] = None,
        location: Optional[str] = None,
    ):
        """
        Lightweight wrapper to handle API calls to Google BigQuery
        """

        self.__setup_creds(service_credentials)
        self.__project = project
        self.__location = location
        self.__client = None

    def __setup_creds(self, service_credentials: str):
        """
        Ensures that environment is correctly populated before running
        any API calls
        """

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_credentials

    @property
    def client(self):
        """
        TODO: fill this in
        """

        if not self.__client:
            self.__client = bigquery.Client(
                project=self.__project, location=self.__location
            )

        return self.__client

    def get_table_id(self, table_name: str):
        """
        Retrieves table ID for a given BigQuery table
        """

        if self.__project and self.__project not in table_name:
            table_name = f"{self.__project}.{table_name}"

        table_ref = self.client.get_table(table=table_name)
        logger.debug(f"Returning table reference {table_ref}")

        return table_ref

    def drop_table(self, table_name: str):
        """
        Drops a given BigQuery table
        """

        if self.__project and self.__project not in table_name:
            table_name = f"{self.__project}.{table_name}"

        logger.debug(f"Attempting to drop table {table_name}...")
        self.client.delete_table(table=table_name)
        logger.info(f"Table {table_name} has been dropped")

    def table_exists(self, table_name: str):
        """
        Determines if a BigQuery table exists
        """

        try:
            _ = self.get_table_id(table_name=table_name)
        except NotFound:
            logger.debug(f"{table_name} does not exist in BigQuery project")
            return False

        return True

    def copy_dataframe_to_bigquery(
        self,
        dataframe: DataFrame,
        table_name: str,
        if_exists: str,
        force_data_types_to_strings: bool = True,
    ):
        """
        Writes a Pandas DataFrame to Google BigQuery
        """

        logger.debug(f"Attempting to copy dataframe to {table_name}")

        if if_exists == "drop" and self.table_exists(table_name=table_name):
            self.drop_table(table_name=table_name)

        job_config = bigquery.LoadJobConfig(write_disposition=LOAD_BEHAVIOR[if_exists])

        try:
            table_reference = self.get_table_id(table_name=table_name)
        except NotFound:
            table_reference = table_name

        # Instantiate load job
        job = self.client.load_table_from_dataframe(
            dataframe=dataframe, destination=table_reference, job_config=job_config
        )
        # Kick off load job
        job.result()

        logger.info(f"Wrote {len(dataframe)} rows to {table_name}")

    def _get_schema_definition_from_dataframe(
        self, dataframe: DataFrame, force_data_types_to_strings: bool = True
    ):
        """
        Creates a LoadJobConfig schema out of column names
        """

        schema_ = []

        if force_data_types_to_strings:
            for var in dataframe.columns:
                schema_.append({"name": var, "type": "STRING"})

        else:
            pass

        return schema_
