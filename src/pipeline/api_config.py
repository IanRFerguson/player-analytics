import dlt
from pydantic import BaseModel

#####


class API_Runner(BaseModel):
    pipeline_name: str = "nba_player_analytics"
    destination_schema: str
    full_refresh: bool = False

    def sources(self) -> list[dlt.sources.Source]:
        # WRITE_DISPOSITION = "replace" if self.full_refresh else "merge"

        # Here you would define your sources, for example:
        # return [rest_api_source(config=self)]
        return []

    def load(self):
        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination="bigquery",
            dataset=self.destination_schema,
        )
        pipeline.run(self.sources())
