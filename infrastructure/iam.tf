locals {
  json_data = jsondecode(file("${path.module}/local.json"))
}


data "google_iam_policy" "owner" {
  binding {
    role = "roles/bigquery.dataOwner"

    members = [
      "serviceAccount:${local.json_data.SERVICE_ACCOUNT}",
      "user:${local.json_data.USER_EMAIL}"
    ]
  }
}

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
