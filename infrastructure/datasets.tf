# These datasets need to be created in your project prior to 
# running the ELT pipeline

locals {
  json_data = jsondecode(file("${path.module}/local.json"))
}

#####

data "google_iam_policy" "owner" {
  binding {
    role = "roles/bigquery.dataOwner"

    members = [
      "serviceAccount:${local.json_data.SERVICE_ACCOUNT}",
      "user:${local.json_data.USER_EMAIL}"
    ]
  }
}

#####

# Production dataset
resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id                  = "raw__nyk_data"
  friendly_name               = "[PROD] Raw NYK Data"
  description                 = "Output dataset for production ELT runs"
  location                    = "US"
  default_table_expiration_ms = null
}

# Testing dataset
resource "google_bigquery_dataset" "dev_dataset" {
  dataset_id                  = "raw__nyk_data__test"
  friendly_name               = "[DEV] Raw NYK Data"
  description                 = "Output dataset for development ELT runs"
  location                    = "US"
  default_table_expiration_ms = null
}

# Config dataset
resource "google_bigquery_dataset" "config_dataset" {
  dataset_id                  = "config"
  friendly_name               = "Configuration"
  description                 = "Stores load configs"
  location                    = "US"
  default_table_expiration_ms = null
}

#####

resource "google_bigquery_dataset_iam_policy" "prod_dataset" {
  dataset_id  = google_bigquery_dataset.prod_dataset.dataset_id
  policy_data = data.google_iam_policy.owner.policy_data
}

resource "google_bigquery_dataset_iam_policy" "dev_dataset" {
  dataset_id  = google_bigquery_dataset.dev_dataset.dataset_id
  policy_data = data.google_iam_policy.owner.policy_data
}

resource "google_bigquery_dataset_iam_policy" "config_dataset" {
  dataset_id  = google_bigquery_dataset.dev_dataset.dataset_id
  policy_data = data.google_iam_policy.owner.policy_data
}
