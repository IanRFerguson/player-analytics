import click
from constants import RuntimeConfig

from common.logger import pipeline_logger

#####


@click.command()
@click.option(
    "--destination_schema",
    env_var="DESTINATION_SCHEMA",
    default="basketball",
    help="The destination schema in the datawarehouse where the data will be loaded.",
)
@click.option(
    "--full-refresh",
    is_flag=True,
    help="If set, the data will be fully refreshed in the destination.",
)
def cli(destination_schema: str, full_refresh: bool = False):
    # config = RuntimeConfig(destination_schema=destination_schema)
    pass


#####

if __name__ == "__main__":
    cli()
