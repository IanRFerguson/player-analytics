# nba_dbt

Lightweight `dbt` workflow to pull raw data through a few transformations and aggregations.

## Model Hierarchy

* `base/` - These are views that pull the raw data from the API into `dbt`
* `staging/` - The bulk of our transformations occur here; renaming fields, updating data types, etc.
* `clean/` - We get a little fancy here, e.g., opponent splits, back to back splits
* `player_summaries/` - These are views of each player's performance, and end up being written to the `_clean` schema