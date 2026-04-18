import click
from api_config import API_Runner, get_latest_record
from constants import RuntimeConfig

from common.logger import pipeline_logger

#####


@click.command()
@click.option(
    "--destination_schema",
    envvar="DESTINATION_SCHEMA",
    help="The destination schema in the datawarehouse where the data will be loaded.",
)
@click.option(
    "--full-refresh",
    is_flag=True,
    help="If set, the data will be fully refreshed in the destination.",
)
@click.option(
    "--target-endpoint", help="If set, only the specified endpoint will be loaded."
)
def cli(
    destination_schema: str,
    full_refresh: bool = False,
    target_endpoint: str | None = None,
) -> None:
    """
    CLI entrypoint for running the DLT pipeline to fetch NBA player analytics data from a REST API.
    It accepts command-line options for the destination schema and whether to perform a full refresh of the data.

    Run `uv run src/pipeline/run.py --help` for more information on the available options.

    Args:
        destination_schema (str): The schema in the destination where the data will be stored.
            Can also be set via the DESTINATION_SCHEMA environment variable.

        full_refresh (bool): A flag to indicate whether to perform a full refresh of the data. If set, existing data in the destination will be replaced.
            Otherwise, new data will be merged with existing data.

        target_endpoint (str | None): If set, only the specified endpoint will be loaded.
    """

    if not full_refresh:
        pipeline_logger.info("Running pipeline in incremental mode (merge)")
        start_date = get_latest_record(destination_schema=destination_schema)

    config = RuntimeConfig()
    pipeline = API_Runner(
        destination_schema=destination_schema,
        full_refresh=full_refresh,
        runtime_config=config,
        start_date=start_date if not full_refresh else None,
    )
    pipeline.load(target_endpoint=target_endpoint)


#####

if __name__ == "__main__":
    cli()
